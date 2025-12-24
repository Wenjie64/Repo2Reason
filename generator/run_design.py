import argparse
from utils.repo_downloader import clone_repo
from generator.ast_parser import scan_python_files,parse_file,build_repo_summary,extract_key_files
from generator.design_prompt_builder import build_design_prompt
from llm.qwen_client import QwenClient
from configs.settings import *

parser = argparse.ArgumentParser("Design generator")

parser.add_argument("--requirement", type=str, default="Design a scalable backend for article publishing and user management.")

args = parser.parse_args()
def main():
    clone_repo(REPO_URL, REPO_PATH)

    parsed = [parse_file(f) for f in scan_python_files(REPO_PATH)]
    summary = build_repo_summary(parsed)
    key_files = extract_key_files(parsed)

    prompt = build_design_prompt(summary, key_files, args.requirement)

    llm = QwenClient(MODEL_NAME)
    design = llm.generate(prompt)

    with open(DESIGN_OUTPUT, "w", encoding="utf-8") as f:
        f.write(design)

    print("[DONE] Grounded architecture design generated")

if __name__ == "__main__":
    main()
