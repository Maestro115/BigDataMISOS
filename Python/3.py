import psycopg2
import pandas as pd
import matplotlib.pyplot as plt
from sqlalchemy import create_engine
import json
import os


def connect_to_db():
    creds_dir = os.path.join(os.path.dirname(__file__), '..', 'Creds')
    creds_path = os.path.join(creds_dir, 'credentials.json')
    with open(creds_path) as f:
        config = json.load(f)

    db_host = config['db_host']
    db_port = config['db_port']
    db_name = config['db_name']
    db_user = config['db_user']
    db_pass = config['db_pass']

    # установка соединения с БД
    engine = create_engine(f'postgresql+psycopg2://{db_user}:{db_pass}@{db_host}:{db_port}/{db_name}')
    connection = engine.connect()
    return connection



def fetch_data(connection):
    # формируем SQL-запрос для выборки данных
    query = "SELECT * FROM data WHERE id_region = 77 AND rooms IS NOT NULL AND area IS NOT NULL AND price IS NOT NULL AND price <= 150000000 AND area <=300;"
    data = pd.read_sql(query, connection)

    # создание новой таблицы в БД
    data.to_sql('table3_query', connection, if_exists='replace', index=False)

    # сохранение изменений в БД
    connection.commit()
    return data


def analyze_data(data):
    # Выполняем анализ зависимостей
    corr_matrix = data[["price", "level", "levels", "building_type", "object_type"]].corr()
    print("Матрица корреляций:")
    print(corr_matrix)

    # Строим диаграмму рассеяния для уровня этажа и цены на жилье
    plt.scatter(data["level"], data["price"])
    plt.xlabel("Этаж квартиры")
    plt.ylabel("Цена, млн. руб.")
    plt.show()


def main():
    connection = connect_to_db()
    data = fetch_data(connection)
    analyze_data(data)
    connection.close()


if __name__ == '__main__':
    main()
