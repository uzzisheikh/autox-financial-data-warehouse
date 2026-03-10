import pandas as pd
import psycopg2
from utils.helpers import load_config

config = load_config()

def load_to_redshift():
    df = pd.read_csv("data/financial_data.csv")
    conn = psycopg2.connect(
        host=config['redshift']['host'],
        dbname=config['redshift']['dbname'],
        user=config['redshift']['user'],
        password=config['redshift']['password'],
        port=config['redshift']['port']
    )
    cur = conn.cursor()
    for index, row in df.iterrows():
        cur.execute(
            "INSERT INTO financial_transactions (txn_id, amount, txn_date) VALUES (%s,%s,%s)",
            (row['txn_id'], row['amount'], row['txn_date'])
        )
    conn.commit()
    conn.close()
    print("Loaded data into Redshift")
