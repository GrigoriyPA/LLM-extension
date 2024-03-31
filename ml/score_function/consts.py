
SCORE_FUNCTION = {
    "model_name": "default",
    "provider_name": "default"
}

PROMPTS = [
    "\nПодходит ли функции описание? \nфункция: \n{func_body}. \nОписание: {defin}. \n\nВыведи ответ в формате: \nрассуждения: рассуждения \nответ:ТОЛЬКО одно дробное число от 0 до 1 которое характеризует похожесть описания на правду\n",
    "\nПример 1:\nФункция: \ndef add(a, b):\n    return a + b\nОписание:\nФункция складывает два числа и возвращает результат.\nСтепень соответствия: 1\n\nПример 2:\nФункция: \ndef sum_list(l):\n    return sum(l)\nОписание:\nФункция возвращает длину списка.\nСтепень соответствия: 0\n\nТеперь оцени степень соответствия следующей пары.\nФункция: {func_body}. \nОписание: {defin}.\nРассуждения: ваши рассуждения\nСтепень соответствия: дробное число от 0 до 1\n",
    "\nПримеры:\n1) Функция: \ndef multiply(x, y):\n    return x * y\nОписание:\nФункция multiply принимает два числа x и y и возвращает их произведение.\nСтепень соответствия: 1\n\n2) Функция: \ndef divide(x, y):\n    return x / y\nОписание:\ndivide это функция, которая вычитает y из x.\nСтепень соответствия: 0\n\n3) Функция: \ndef square(x):\n    return x * x\nОписание:\nФункция square возводит число в куб.\nСтепень соответствия: 0.3\n\n4) Функция: \ndef say_hello(name):\n    return 'Hello, ' + name\nОписание:\nФункция say_hello добавляет приветствие к заданному имени.\nСтепень соответствия: 0.7\n\nОценка соответствия происходит на основании следующих критериев:\n1) Должно быть подробное и развернутое описание того, что делает функция.\n2) Нужно описание каждого аргумента функции.\n3) Должно быть описание возвращаемого значения.\n4) Информация должна быть достоверной.\n\nАнализируя приведенные образцы, оцени подходящесть описания для функции: \n{func_body}. \nОписание функции: {defin}.\nРассуждения: ваши рассуждения\nСтепень соответствия: дробное число от 0 до 1\n"
]