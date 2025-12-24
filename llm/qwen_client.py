from transformers import AutoTokenizer, AutoModelForCausalLM
from configs.settings import MODEL_PATH

class QwenClient:
    def __init__(self, model_name):
        # self.tokenizer = AutoTokenizer.from_pretrained(model_name)
        # self.model = AutoModelForCausalLM.from_pretrained(
        #     model_name,
        #     device_map="auto",
        #     dtype=torch.float16 if torch.backends.mps.is_available() else torch.float32
        # )
        self.model = AutoModelForCausalLM.from_pretrained(
            MODEL_PATH,
            local_files_only=True,
            trust_remote_code=True
        )

        self.tokenizer = AutoTokenizer.from_pretrained(
            MODEL_PATH,
            local_files_only=True,
            trust_remote_code=True
        )

    def generate(self, prompt):
        inputs = self.tokenizer(prompt, return_tensors="pt").to(self.model.device)
        outputs = self.model.generate(**inputs, max_new_tokens=600)
        return self.tokenizer.decode(outputs[0], skip_special_tokens=True)