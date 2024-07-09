from airflow import DAG
from airflow.decorators import task, dag
from airflow.utils.dates import days_ago
import logging
from pipeline import ml_pipeline

@dag(
    schedule_interval='@daily', 
    start_date=days_ago(1),
    catchup=False,
    dag_id = 'dag_pipeline',
    tags=['ml_pipeline']
)
def main():
    ml_pipeline()

main()
