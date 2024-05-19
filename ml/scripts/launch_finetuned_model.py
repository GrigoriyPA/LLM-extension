from transformers import AutoModelForCausalLM, AutoTokenizer
from peft import PeftModel

import torch

finetuned_model_path = "finetuned_models/finetune-phi3-docstring"
init_model_path = "microsoft/Phi-3-mini-128k-instruct"

tokenizer = AutoTokenizer.from_pretrained(init_model_path, device_map="cuda")
model = AutoModelForCausalLM.from_pretrained(
    init_model_path,
    trust_remote_code=True,
    device_map="cuda",
)

model.config.vocab_size = 32011

tmp = model.model.embed_tokens.weight
model.model.embed_tokens = torch.nn.Embedding(32011, 3072)
model.model.embed_tokens.weight.data = tmp[:32011, :]

tmp = model.lm_head.weight
model.lm_head = torch.nn.Linear(3072, 32011)
model.lm_head.weight.data = tmp[:32011, :]

model = PeftModel.from_pretrained(
    model,
    finetuned_model_path,
    ignore_mismatched_sizes=True,
)

model = model.to("cuda")

f = """
def chinchopa(z: list, o, v):
    o = max(z)
    print("I am bob")
    if v == 228:
        return 0
    return 1
"""

input_text = f"Function:\n{f}\nDocstring:\n"
input_ids = tokenizer.encode(input_text, return_tensors="pt")
input_ids = input_ids.to("cuda")

output = model.generate(input_ids, max_length=200)
predicted_text = tokenizer.decode(output[0], skip_special_tokens=True)

print(predicted_text)
