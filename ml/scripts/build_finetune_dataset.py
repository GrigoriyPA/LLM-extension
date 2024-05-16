import json

from src.constants.database import MAIN_DATABASE
from src.database.database_entities import Function
from src.database.database_utils import Table

t = Table(MAIN_DATABASE, "finetune_docstring_dataset_clear", Function)

arr = []
it = 0
for el in t.read():
    if el.docstring is None:
        continue
    prompt = f"Function:\n{el.code}\nDocstring:\n{el.docstring}"
    arr.append({"text": prompt})


with open("train.jsonl", 'w') as f:
    for item in arr:
        f.write(json.dumps(item) + "\n")


"""
sudo autotrain llm --train --model microsoft/Phi-3-mini-128k-instruct --data-path . --lr 2e-4 --batch-size 3 --epochs 1 --trainer sft --peft --project-name finetune-phi3-docstring
"""