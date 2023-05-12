@echo off

rem Создание виртуального окружения
python -m venv myenv
call myenv\Scripts\activate.bat

rem Установка зависимостей
pip install -r requirements.txt

rem Выполнение python-файлов
python import.py
python 1.py
python 2.py
python 3.py

rem Деактивация виртуального окружения
deactivate
