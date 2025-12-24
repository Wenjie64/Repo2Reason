from utils.repo_downloader import clone_repo
from parser.repo_scanner import scan_python_files
from generator.ast_parser import parse_file
from generator.code_qa_generator import generate_code_qa
from utils.jsonl_writer import write_jsonl
from configs.settings import *

def main():
    clone_repo(REPO_URL, REPO_PATH)

    samples = []
    for f in scan_python_files(REPO_PATH):
        parsed = parse_file(f)
        samples.extend(generate_code_qa(parsed))

    write_jsonl(samples, CODE_QA_OUTPUT)
    print(f"[DONE] Generated {len(samples)} reasoning QA samples")

if __name__ == "__main__":
    main()
