import json
from torch.utils.data import Dataset

class CodeQADataset(Dataset):
    def __init__(self, path, tokenizer, max_length):
        self.samples = []
        self.tokenizer = tokenizer
        self.max_length = max_length

        with open(path, "r", encoding="utf-8") as f:
            for line in f:
                self.samples.append(json.loads(line))

    def __len__(self):
        return len(self.samples)

    def build_prompt(self, s):
        return (
            "### Instruction:\n"
            "Answer the question based on the given code.\n\n"
            "### Question:\n"
            f"{s['question']}\n\n"
            "### Code:\n"
            f"{s['context']['code']}\n\n"
            "### Answer:\n"
            f"{s['answer']}"
        )

    def __getitem__(self, idx):
        text = self.build_prompt(self.samples[idx])

        tokens = self.tokenizer(
            text,
            max_length=self.max_length,
            truncation=True,
            padding="max_length",
            return_tensors="pt",
        )

        input_ids = tokens.input_ids.squeeze(0)
        attention_mask = tokens.attention_mask.squeeze(0)

        return {
            "input_ids": input_ids,
            "attention_mask": attention_mask,
            "labels": input_ids.clone(),
        }
