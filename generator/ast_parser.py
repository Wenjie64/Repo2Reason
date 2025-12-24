import ast
import os
from collections import defaultdict
def parse_file(path):
    with open(path, "r", encoding="utf-8", errors="ignore") as f:
        code = f.read()

    tree = ast.parse(code)
    functions, classes = [], []

    for node in ast.walk(tree):
        if isinstance(node, ast.FunctionDef):
            functions.append({
                "name": node.name,
                "code": ast.get_source_segment(code, node)
            })
        elif isinstance(node, ast.ClassDef):
            classes.append({
                "name": node.name,
                "code": ast.get_source_segment(code, node)
            })

    return {
        "path": path,
        "functions": functions,
        "classes": classes
    }

def extract_key_files(parsed_files, max_files=6):
    keywords = ["views.py", "models.py", "serializers.py", "urls.py"]
    selected = []

    for f in parsed_files:
        for k in keywords:
            if f["path"].endswith(k):
                snippet = []
                if f["functions"]:
                    snippet.append(f["functions"][0])
                if f["classes"]:
                    snippet.append(f["classes"][0])

                selected.append({
                    "path": f["path"],
                    "snippet": snippet
                })

        if len(selected) >= max_files:
            break

    return selected

def build_repo_summary(parsed_files):
    summary = {
        "framework": "Django REST Framework",
        "layers": set(),
        "modules": defaultdict(list)
    }

    for f in parsed_files:
        path = f["path"]

        for layer in ["views", "models", "serializers"]:
            if layer in path:
                summary["layers"].add(layer)

        parts = path.split("/")
        if "apps" in parts:
            i = parts.index("apps")
            if i + 1 < len(parts):
                summary["modules"][parts[i + 1]].append(path)

    summary["layers"] = list(summary["layers"])
    return summary

def scan_python_files(root):
    files = []
    for dp, _, fs in os.walk(root):
        for f in fs:
            if f.endswith(".py"):
                files.append(os.path.join(dp, f))
    return files