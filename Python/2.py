import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from sklearn.linear_model import LinearRegression
from sklearn.ensemble import RandomForestRegressor
from sklearn.metrics import r2_score, mean_squared_error, mean_absolute_error
from sqlalchemy import create_engine
import json
import os


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
    engine = create_engine(f'postgresql+psycopg2://{db_user}:{db_pass}@{db_host}:{db_port}/{db_name}')
    return engine.connect()

def get_data():
    connection = connect_to_db()
    query = "SELECT price, rooms, area FROM data WHERE id_region = 77 AND rooms IS NOT NULL AND area IS NOT NULL AND price IS NOT NULL AND price <= 150000000 AND area <=300;"
    data = pd.read_sql(query, connection)
    connection.close()
    return data

def create_table_in_db(data):
    connection = connect_to_db()
    data.to_sql('table2_query', connection, if_exists='replace', index=False)
    connection.commit()
    connection.close()

def visualize_data(data):
    fig, axs = plt.subplots(1, 2, figsize=(12, 4))
    axs[0].scatter(data['rooms'], data['price'])
    axs[0].set_xlabel('Number of rooms')
    axs[0].set_ylabel('Price')
    axs[0].set_title('Price vs Number of rooms')
    axs[1].scatter(data['area'], data['price'])
    axs[1].set_xlabel('Area')
    axs[1].set_ylabel('Price')
    axs[1].set_title('Price vs Area')
    plt.show()

def calculate_correlation(data):
    corr_rooms_price = np.corrcoef(data['rooms'], data['price'])[0, 1]
    corr_area_price = np.corrcoef(data['area'], data['price'])[0, 1]
    print(f'Correlation between number of rooms and price: {corr_rooms_price:.2f}')
    print(f'Correlation between area and price: {corr_area_price:.2f}')

def build_regression_model(data):
    X = data[['rooms', 'area']]
    y = data['price']
    reg = LinearRegression()
    reg.fit(X, y)
    y_pred = reg.predict(X)
    print ('R2_score:', round (r2_score(y, y_pred),3))        
    print ('MAE:', round (mean_absolute_error(y, y_pred),3))
    print ('√MSE:', round (mean_squared_error(y, y_pred)**(1/2),3))

if __name__ == '__main__':
    data = get_data()
    create_table_in_db(data)
    visualize_data(data)
    calculate_correlation(data)
    build_regression_model(data)
