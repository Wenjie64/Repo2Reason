from pathlib import Path

BASE_DIR = Path(__file__).parent.resolve()

REPO_URL = "https://github.com/gothinkster/django-realworld-example-app.git"
REPO_PATH = "../repos/django-realworld"

CODE_QA_OUTPUT = "../data/code_qa.jsonl"
DESIGN_OUTPUT = "../data/design.md"

MODEL_NAME = "Qwen/Qwen2.5-3B-Instruct"
SMALL_MODEL_NAME = "Qwen/Qwen2.5-0.5B-Instruct"
MODEL_PATH = BASE_DIR / "models" / "qwen2.5-3b"

INPUT_FILE = Path("./code_qa.jsonl")
TRAIN_FILE = Path("./train.jsonl")
EVAL_FILE = Path("./eval.jsonl")

TRAIN_RATIO = 0.9
SEED = 42