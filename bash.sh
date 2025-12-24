#!/bin/bash
set -e

echo "=== Repo2Reason Pipeline Start ==="

# 1. 创建虚拟环境（如不存在）
if [ ! -d "venv" ]; then
  python3 -m venv venv
fi

source venv/bin/activate

echo "[1/6] Installing dependencies..."
python -m pip install --upgrade pip
pip install -r requirements.txt

echo "[2/6] Generate Code QA dataset..."
python generator/run_code_qa.py

echo "[3/6] Split dataset..."
python data/split_dataset.py

echo "[4/6] Run Design Generator..."
python generator/run_design.py \
  --requirement "Design a scalable backend system based on this repository"

echo "[5/6] Train LoRA model..."
python finetune/train_lora.py \
  --epochs 2 \
  --batch_size 2 \
  --lr 2e-4 \
  --max_length 768 \
  --grad_accum 4

echo "[6/6] Evaluate LoRA model..."
python finetune/eval_lora.py

echo "=== Repo2Reason Pipeline Finished Successfully ==="
