import json
import torch
import os
from pathlib import Path
from torch.utils.data import Dataset, DataLoader
from transformers import AutoTokenizer, AutoModelForCausalLM
from peft import LoraConfig, get_peft_model, TaskType
from tqdm import tqdm
import argparse
from configs.settings import MODEL_PATH

from finetune.dataset import CodeQADataset

# ======================
# Config
# ======================

parser = argparse.ArgumentParser(description="LoRA fine-tuning for code QA")

parser.add_argument("--base_model", type=str, default="Qwen/Qwen2-1.5B-Instruct")
parser.add_argument("--train_file", type=str, default="data/train.jsonl")
parser.add_argument("--output_dir", type=str, default="output/qwen_lora")

parser.add_argument("--epochs", type=int, default=2)
parser.add_argument("--batch_size", type=int, default=2)
parser.add_argument("--lr", type=float, default=2e-4)
parser.add_argument("--max_length", type=int, default=768)
parser.add_argument("--grad_accum", type=int, default=4)

args = parser.parse_args()

DEVICE = "cuda" if torch.cuda.is_available() else "cpu"


# ======================
# Train Loop
# ======================
def main():
    os.makedirs(args.output_dir, exist_ok=True)

    tokenizer = AutoTokenizer.from_pretrained(
        MODEL_PATH,
        local_files_only=True,
        trust_remote_code=True
    )

    model = AutoModelForCausalLM.from_pretrained(
            MODEL_PATH,
            local_files_only=True,
            trust_remote_code=True
        )

    lora_cfg = LoraConfig(
        task_type=TaskType.CAUSAL_LM,
        r=8,
        lora_alpha=32,
        lora_dropout=0.1,
        target_modules=["q_proj", "v_proj"],
    )

    model = get_peft_model(model, lora_cfg)
    model.train()

    optimizer = torch.optim.AdamW(model.parameters(), lr=args.lr)

    dataset = CodeQADataset(args.train_file, tokenizer, args.grad_accum)
    loader = DataLoader(dataset, batch_size=args.batch_size, shuffle=True)

    for epoch in range(args.epochs):
        print(f"\n===== Epoch {epoch + 1}/{args.epochs} =====")
        total_loss = 0.0

        bar = tqdm(loader)

        optimizer.zero_grad()

        for step, batch in enumerate(bar):
            batch = {k: v.to(model.device) for k, v in batch.items()}

            out = model(**batch)
            loss = out.loss / args.grad_accum
            loss.backward()

            if (step + 1) % args.grad_accum == 0:
                optimizer.step()
                optimizer.zero_grad()

            total_loss += loss.item() * args.grad_accum
            bar.set_postfix(loss=total_loss / (step + 1))

        print(f"Epoch avg loss: {total_loss / len(loader):.4f}")

    model.save_pretrained(args.output_dir)
    tokenizer.save_pretrained(args.output_dir)

    print(f"LoRA adapter saved to {args.output_dir.resolve()}")


if __name__ == "__main__":
    main()