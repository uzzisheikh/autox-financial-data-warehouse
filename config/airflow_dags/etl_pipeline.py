from airflow import DAG
from airflow.operators.python import PythonOperator
from datetime import datetime
from spark_jobs.redshift_loader import load_to_redshift
from glue_jobs.glue_etl import run_glue_etl

def start_pipeline():
    print("Starting AUTOX ETL Pipeline")

default_args = {
    'owner': 'data_team',
    'start_date': datetime(2026, 3, 10),
    'retries': 1,
}

dag = DAG('autox_financial_etl', default_args=default_args, schedule_interval='@daily')

start = PythonOperator(
    task_id='start_pipeline',
    python_callable=start_pipeline,
    dag=dag
)

spark_task = PythonOperator(
    task_id='load_redshift',
    python_callable=load_to_redshift,
    dag=dag
)

glue_task = PythonOperator(
    task_id='run_glue_etl',
    python_callable=run_glue_etl,
    dag=dag
)

start >> spark_task >> glue_task
