from datetime import timedelta
from airflow import DAG
from airflow.utils.dates import days_ago
from airflow.decorators import task, dag
from pipeline import ml_pipeline

default_args = {
    'owner': 'airflow',
    'retries': 1,
    'retry_delay': timedelta(minutes=5),
}

@dag(
    default_args=default_args,
    schedule_interval='@daily',  
    start_date=days_ago(1),
    catchup=False,
    dag_id='dag_pipeline',
    tags=['ml_pipeline'],
)
def main():
    ml_pipeline()

main()
