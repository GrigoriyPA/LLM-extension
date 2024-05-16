import json

from src.constants import database
from src.database import database_entities
from src.database import database_utils

finetune_dataset_table = database_utils.Table(database.MAIN_DATABASE,
                                              "finetune_docstring_dataset_clear",
                                              database_entities.Function)

arr = []
for row in finetune_dataset_table.read():
    if row.docstring is None:
        continue
    prompt = f"Function:\n{row.code}\nDocstring:\n{row.docstring}"
    arr.append({"text": prompt})

with open("train.jsonl", 'w') as f:
    for item in arr:
        f.write(json.dumps(item) + "\n")

"""
autotrain llm --train --model microsoft/Phi-3-mini-128k-instruct --data-path . --lr 2e-4 --batch-size 3 --epochs 1 --trainer sft --peft --project-name finetune-phi3-docstring
"""
