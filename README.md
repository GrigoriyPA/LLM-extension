# Курсовой проект "LLM+IDE"

Суть курсовой работы заключается в разработке плагина для IDE [Visual Studio Code](https://code.visualstudio.com/). 
Плагин создается с целью автоматизации написания некоторых частей кода.
В частности, на текущий момент мы собираемся реализовывать следующий функционал:
* Генерация документации для функций
* Генерация тестов для функций
* Анализ семантического смысла переменной по некоторым отрывкам кода

## Планы и детали реализации по отдельным частям курсовой работы
* [ML](#ml)
* [VS Code Extension](#vs-code-extension)
* [Server](#server)

# ML

В качестве бейзлайна были выбраны две модели: [CodeLlama 7B Instruct](https://huggingface.co/codellama/CodeLlama-7b-Instruct-hf) 
и [Stable Code 3B](https://hf.dongsiqie.me/stabilityai/stable-code-3b). Генерация осуществляется при помощи специально 
подобранного промпта, это бейзлайн.
В первую очередь мы решили заняться генерацией документации для функций.

Планы:
1. Написать скрипт для автоматической загрузки моделей, запуска генерации на произвольных бенчмарках, 
сохранение этих результатов (сделано)
1. Подобрать нужный промпт, чтобы получить какой-либо бейзлайн (сделано)
1. Научиться автоматически оценивать качество документации. Один из
способов это делать - скорить ответы при помощи ChatGPT. 
Для более качественного скоринга нужно собрать небольшой набор собственноручно размеченных данных 
и затем использовать few-shot
1. Подготовить датасет функций, на котором можно замерять качество. Один из вариантов сбора датасета - 
спарсить с гитхаба "хорошие" питоновские функции и при помощи ChatGPT написать к ним документацию
1. После того как мы научимся скорить ответы и найдем нужные бенчи можно запускать серии экспериментов
1. Если будет достаточно вычислительных ресурсов, то можно будет зафайнтюнить небольшие модельки
на нашем синтетическом датасете
1. Переходить к реализации других фичей с примерным сохранением вышеописанного пайплайна

# VS Code Extension

# Server

