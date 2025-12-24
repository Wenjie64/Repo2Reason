import json
import random
from configs.settings import *


def main():
    random.seed(SEED)

    with open(INPUT_FILE, "r", encoding="utf-8") as f:
        samples = [json.loads(line) for line in f]

    random.shuffle(samples)

    split_idx = int(len(samples) * TRAIN_RATIO)
    train_samples = samples[:split_idx]
    eval_samples = samples[split_idx:]

    TRAIN_FILE.parent.mkdir(parents=True, exist_ok=True)

    with open(TRAIN_FILE, "w", encoding="utf-8") as f:
        for s in train_samples:
            f.write(json.dumps(s, ensure_ascii=False) + "\n")

    with open(EVAL_FILE, "w", encoding="utf-8") as f:
        for s in eval_samples:
            f.write(json.dumps(s, ensure_ascii=False) + "\n")

    print(f"Split finished:")
    print(f"  Train samples: {len(train_samples)}")
    print(f"  Eval samples : {len(eval_samples)}")


if __name__ == "__main__":
    main()