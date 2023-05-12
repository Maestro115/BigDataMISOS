import os
import pandas as pd
from sqlalchemy import create_engine
import json


def get_credentials():
    creds_dir = os.path.join(os.path.dirname(__file__), '..', 'Creds')
    creds_path = os.path.join(creds_dir, 'credentials.json')
    with open(creds_path) as f:
        return json.load(f)


def connect_to_db():
    config = get_credentials()

    db_host = config['db_host']
    db_port = config['db_port']
    db_name = config['db_name']
    db_user = config['db_user']
    db_pass = config['db_pass']

    # установка соединения с БД
    engine = create_engine(f'postgresql+psycopg2://{db_user}:{db_pass}@{db_host}:{db_port}/{db_name}')
    connection = engine.connect()
    return connection


def main():
    file_path = os.path.join(os.path.dirname(__file__), '..', 'Data', 'input_data.csv')
    connection = connect_to_db()

    # определяем чанки (например, по 10000 строк) и последовательно записываем в базу данных
    chunksize = 10000
    for chunk in pd.read_csv(file_path, sep=';', chunksize=chunksize):
        chunk.to_sql('data', connection, if_exists='append', index=False)


if __name__ == '__main__':
    main()
