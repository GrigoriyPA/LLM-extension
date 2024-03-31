import pandas as pd
import json
from models_names import GPTModelName, GPTProviderName
import asyncio
from score_function import GenerativeModel, ScoreFunction
import g4f 

from consts import SCORE_FUNCTION, PROMPTS

provider_name = SCORE_FUNCTION["provider_name"]
model_name = SCORE_FUNCTION["model_name"]
prompts = PROMPTS

df = pd.DataFrame({
'defin': [
    'считает gcd двух чисел',
    'считает корень из числа',
    'Задача организации, в особенности же повышение уровня гражданского сознания позволяет оценить значение ключевых компонентов планируемого обновления! Не следует, однако, забывать о том, что рамки и место обучения кадров напрямую зависит от системы масштабного изменения ряда параметров. Разнообразный и богатый опыт реализация намеченного плана развития требует от нас анализа дальнейших направлений развитая системы массового участия.',
    ],
'func_body': [
    'def gcd_recursion(num1, num2):\n\treturn gcd_recursion(num2 % num1, num1) if num1 != 0 else num2',
    'def q(x):\n\treturn sqrt(x)',
    'def g(x): \n\treturn x'
        ]
})

model = GenerativeModel(
    getattr(g4f.models, GPTModelName[model_name].value),
    getattr(g4f.Provider, GPTProviderName[provider_name].value)
)

async def main():
    datas = pd.DataFrame()
    for i, prompt in enumerate(prompts):
        score_function = ScoreFunction(prompt, model)
        result = await score_function.exec(df.copy(deep=True))
        result['prompt no.'] = i + 1
        datas = pd.concat([datas, result])
    datas.to_csv('output.csv')


asyncio.run(main())



