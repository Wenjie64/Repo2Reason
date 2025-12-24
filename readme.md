# Repo2Reason

Repo2Reason 是一个本地代码仓（repository-agnostic）的代码理解与训练数据生成及验证工程，目标是从任意本地代码仓库中自动构建 **“代码 + 推理”** 数据，并通过 **LoRA 微调**对数据集效果进行快速验证。

本项目以 `django-realworld` 作为示例仓库，但整体实现**不依赖任何特定框架或业务代码**，可直接迁移到其他 Python 项目或代码仓库中使用。

---

## 一、项目能力总览

本工程覆盖三个核心能力模块，既可独立运行，也可串联为完整流水线：

1. 场景一：代码 QA 数据生成（Code + Reasoning）  
2. 场景二：Design Generator  
3. LoRA 微调与验证（Train / Eval）

---

## 二、目录结构说明

Repo2Reason/
├── configs/  
│   └── settings.py              # 全局配置  
│  
├── data/  
│   ├── code_qa.jsonl             # 场景一：完整 QA 数据集  
│   ├── train.jsonl               # 训练集  
│   ├── eval.jsonl                # 验证集  
│   └── split_dataset.py          # 数据集划分脚本  
│  
├── generator/  
│   ├── ast_parser.py             # AST 解析器  
│   ├── code_qa_generator.py      # 代码 QA + 推理链生成逻辑  
│   ├── design_prompt_builder.py  # Design Prompt 构建  
│   ├── run_code_qa.py             # 场景一入口  
│   └── run_design.py              # 场景二入口  
│  
├── finetune/  
│   ├── dataset.py                # LoRA 数据集封装  
│   ├── train_lora.py              # LoRA 微调  
│   ├── eval_lora.py               # 模型验证  
│   └── output/                    # LoRA 权重输出目录  
│  
├── llm/  
│   └── qwen_client.py             # LLM 统一调用接口 
│   └── models                     # 预训练模型
│       ├── qwen2.5-3b             # qwen 2.5 模型
├── repos/  
│   └── django-realworld/          # 示例仓库（不存在会自动下载）  
│  
├── utils/  
│   ├── repo_downloader.py         # 仓库自动下载  
│   └── jsonl_writer.py            # JSONL 写入工具  
│  
├── requirements.txt  
├── bash.sh  
└── README.md  

---

## 三、场景一：代码 QA 数据生成（Code + Reasoning）

### 目标

场景一的目标是：

基于任意本地代码仓库，自动生成**高质量的代码理解 QA 数据集**，并且**每一条样本必须包含可解释的推理链（Reasoning）**。

每条 QA 数据严格包含以下四个字段：

1. Question  
   - 针对类、函数或模块职责  
   - 关注设计意图或行为逻辑  

2. Answer  
   - 基于代码事实的简洁回答  

3. Context（代码上下文）  
   - 原始代码段（code snippet）  
   - 在仓库中的相对路径（location）  

4. Reasoning（推理链）  
   - 解释为什么能从该代码段得出答案  
   - 体现结构、继承或方法行为分析  

该场景用于构建 **“代码 + 推理链”联合监督数据集**，可直接用于大模型微调或评估。

---

### 运行方式

python generator/run_code_qa.py

---

### 输出

输出文件路径：

data/code_qa.jsonl

单条样本示例：

{
  "question": "What is the responsibility of class `ConduitJSONRenderer`?",
  "answer": "The class customizes how API responses are rendered into JSON.",
  "context": {
    "code": "class ConduitJSONRenderer(JSONRenderer): ...",
    "location": "../repos/django-realworld/conduit/apps/core/renderers.py"
  },
  "reasoning": "The class inherits from JSONRenderer and overrides the render method, indicating it controls serialization behavior."
}

---

## 四、场景二：Design Generator

### 目标

场景二的目标是：

结合**本地代码仓库结构**与**用户输入的需求描述**，自动生成系统级设计方案（Design Proposal）。

设计结果具备以下特征：

- 设计基于真实代码仓库结构
- 可直接用于自动化系统或下游推理

---

### 运行方式

python generator/run_design.py --requirement "Design a scalable backend service with authentication"

说明：  
--requirement 为必填参数，支持用户自定义任意需求描述。

---

### 输出示例（JSON）

{
  "overview": "This repository implements a RESTful backend service.",
  "modules": [
    {
      "name": "Authentication",
      "description": "Handles user login and permission validation",
      "key_files": ["apps/users/views.py", "apps/users/serializers.py"]
    }
  ],
  "data_flow": [
    "Client sends request",
    "ViewSet processes request",
    "Serializer validates input",
    "Response is rendered"
  ],
  "key_files": [
    "apps/core/renderers.py",
    "apps/users/views.py"
  ]
}

---

## 五、LoRA 微调与验证

### 1. 数据集划分

python data/split_dataset.py

生成：

data/train.jsonl  
data/eval.jsonl  

---

### 2. LoRA 微调（CPU / MPS）

python finetune/train_lora.py \
  --epochs 2 \
  --batch_size 2 \
  --lr 2e-4 \
  --max_length 768 \
  --grad_accum 4
 

LoRA 权重输出至：

finetune/output/

---

### 3. 验证（eval.jsonl）

python finetune/eval_lora.py

验证数据来源：

data/eval.jsonl

---

## 六、环境依赖

- Python ≥ 3.9  
- PyTorch ≥ 2.1（macOS CPU / MPS）  
- transformers ≥ 4.39  

安装依赖：

pip install -r requirements.txt

---
