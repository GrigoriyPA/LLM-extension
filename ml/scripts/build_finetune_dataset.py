import json

from src.constants import database as database_constants
from src.database import database_entities
from src.database import database_utils

finetune_dataset_table = database_utils.Table(database_constants.MAIN_DATABASE,
                                              "finetune_unit_test_dataset_clear",
                                              database_entities.Function)

arr = []
for row in finetune_dataset_table.read():
    if row.unit_test is None:
        continue
    prompt = f"Function:\n{row.code}\nTests:\n{row.unit_test}"
    arr.append({"text": prompt})

with open("train.jsonl", 'w') as f:
    for item in arr:
        f.write(json.dumps(item) + "\n")

"""
autotrain llm --train --model microsoft/Phi-3-mini-128k-instruct --data-path . --lr 2e-4 --batch-size 3 --epochs 1 --trainer sft --peft --project-name finetune-phi3-docstring
"""
