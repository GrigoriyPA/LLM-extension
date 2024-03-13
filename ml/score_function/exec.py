import pandas as pd
import json
from models_names import GPTModelName, GPTProviderName

with open('config.json') as f:
    config = json.load(f)

provider_name = config["score_function"]["provider_name"]
model_name = config["score_function"]["model_name"]

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

prompts = [
"""
Подходит ли функции описание? 
функция: 
{func_body}. 
описание: {defin}. 

Выведи ответ в формате: 
рассуждения: **рассуждения** 
ответ:**ТОЛЬКО одно дробное число от 0 до 1 которое характеризует похожесть описания на правду**
""",
"""
Пример 1:
Функция: 
def add(a, b):
    return a + b
Описание:
Функция складывает два числа и возвращает результат.
Степень соответствия: 1

Пример 2:
Функция: 
def sum_list(l):
    return sum(l)
Описание:
Функция возвращает длину списка.
Степень соответствия: 0

Теперь оцени степень соответствия следующей пары.
Функция: {func_body}. 
Описание: {defin}.
Рассуждения: **ваши рассуждения**
Степень соответствия: **дробное число от 0 до 1**
""", 

"""
Примеры:
1) Функция: 
def multiply(x, y):
    return x * y
Описание:
Функция multiply принимает два числа x и y и возвращает их произведение.
Степень соответствия: 1

2) Функция: 
def divide(x, y):
    return x / y
Описание:
divide это функция, которая вычитает y из x.
Степень соответствия: 0

3) Функция: 
def square(x):
    return x * x
Описание:
Функция square возводит число в куб.
Степень соответствия: 0.3

4) Функция: 
def say_hello(name):
    return 'Hello, ' + name
Описание:
Функция say_hello добавляет приветствие к заданному имени.
Степень соответствия: 0.7

Оценка соответствия происходит на основании следующих критериев:
1) Должно быть подробное и развернутое описание того, что делает функция.
2) Нужно описание каждого аргумента функции.
3) Должно быть описание возвращаемого значения.
4) Информация должна быть достоверной.

Анализируя приведенные образцы, оцени подходящесть описания для функции: 
{func_body}. 
Описание функции: {defin}.
Рассуждения: **ваши рассуждения**
Степень соответствия: **дробное число от 0 до 1**
"""
]

from score_function import GenerativeModel, ScoreFunction
import g4f 

datas = pd.DataFrame()

model = GenerativeModel(
    getattr(g4f.models, GPTModelName[model_name].value),
    getattr(g4f.Provider, GPTProviderName[provider_name].value)
)

for i, prompt in enumerate(prompts):
    score_function = ScoreFunction(prompt, model)
    result = score_function.exec(df.copy(deep=True))
    result['prompt no.'] = i + 1
    datas = pd.concat([datas, result])

datas.to_csv('output.csv')




