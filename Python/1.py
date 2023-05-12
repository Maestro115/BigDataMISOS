import pandas as pd
from sqlalchemy import create_engine
import json
import os

def get_db_connection():
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
    return connection, engine




def read_data(connection):
    # формируем SQL-запрос для выборки данных
    query = "SELECT price, id_region FROM data WHERE id_region IN (77, 78) AND price IS NOT NULL"
    data = pd.read_sql(query, connection)
    return data

def save_data(connection, data):
    # создание новой таблицы в БД
    data.to_sql('table1_query', connection, if_exists='append', index=False)
    # сохранение изменений в БД
    connection.commit()

def get_mean_prices(engine):
    # формируем SQL-запрос для выборки данных
    query = "SELECT price, id_region FROM data WHERE id_region IN (77, 78) AND price IS NOT NULL"
    # считываем данные из базы данных в DataFrame
    df = pd.read_sql_query(query, engine)
    # группируем данные по id_region и вычисляем среднее значение цены на жилье
    mean_prices = df.groupby('id_region').mean()
    return mean_prices

def print_mean_prices(mean_prices):
    # выводим результаты с форматированием чисел
    print(mean_prices.to_string(float_format='{:,.2f}'.format))

def close_db_connection(connection):
    # Закрываем коннект с базой
    connection.close()

def main():
    connection, engine = get_db_connection()
    data = read_data(connection)
    save_data(connection, data)
    mean_prices = get_mean_prices(engine)
    print_mean_prices(mean_prices)
    close_db_connection(connection)

if __name__ == '__main__':
    main()