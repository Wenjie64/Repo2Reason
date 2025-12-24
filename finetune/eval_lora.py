import argparse
import torch
import math
from torch.utils.data import Dataset, DataLoader
from transformers import AutoTokenizer, AutoModelForCausalLM
from peft import PeftModel
from tqdm import tqdm

from finetune.dataset import CodeQADataset
from configs.settings import MODEL_PATH

parser = argparse.ArgumentParser("LoRA eval on eval.jsonl")

parser.add_argument("--base_model", type=str, default="Qwen/Qwen2-1.5B-Instruct")
parser.add_argument("--lora_path", type=str, default="output/qwen_lora")
parser.add_argument("--eval_file", type=str, default="data/eval.jsonl")

parser.add_argument("--batch_size", type=int, default=2)
parser.add_argument("--max_length", type=int, default=768)

args = parser.parse_args()

device = "cuda" if torch.cuda.is_available() else "cpu"

# ======================
# Eval
# ======================
def main():
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

    model = PeftModel.from_pretrained(base_model, args.lora_path)
    model.eval()

    dataset = CodeQADataset(
        args.eval_file,
        tokenizer,
        args.max_length
    )

    loader = DataLoader(
        dataset,
        batch_size=args.batch_size,
        shuffle=False
    )

    total_loss = 0.0
    total_steps = 0

    with torch.no_grad():
        for batch in tqdm(loader, desc="Evaluating"):
            batch = {k: v.to(model.device) for k, v in batch.items()}

            outputs = model(**batch)
            loss = outputs.loss

            total_loss += loss.item()
            total_steps += 1

    avg_loss = total_loss / total_steps
    ppl = math.exp(avg_loss)

    print("\n===== Eval Result =====")
    print(f"Eval loss: {avg_loss:.4f}")
    print(f"Perplexity: {ppl:.2f}")


if __name__ == "__main__":
    main()