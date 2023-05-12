#!/bin/bash

# Создание виртуального окружения
python3 -m venv myenv
source myenv/bin/activate

# Установка зависимостей
pip install -r requirements.txt

# Выполнение python-файлов
python import.py
python 1.py
python 2.py
python 3.py

# Деактивация виртуального окружения
deactivate
