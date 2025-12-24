import os
import subprocess

def clone_repo(repo_url: str, target_dir: str):
    """
    Clone a GitHub repository to local disk if it does not already exist.
    """
    if os.path.exists(target_dir):
        print(f"[INFO] Repository already exists at {target_dir}, skipping clone.")
        return

    print(f"[INFO] Cloning repository from {repo_url} ...")
    subprocess.run(
        ["git", "clone", repo_url, target_dir],
        check=True
    )
    print("[INFO] Repository cloned successfully.")