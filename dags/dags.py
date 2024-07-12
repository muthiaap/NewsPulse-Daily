from datetime import timedelta
from airflow import DAG
from airflow.utils.dates import days_ago
from airflow.decorators import task, dag
from pipeline import extract, sentiment_analysis, generate_wordclouds, load_to_postgresql

default_args = {
    'owner': 'airflow',
    'retries': 1,
    'retry_delay': timedelta(minutes=5),
}

@dag(
    default_args=default_args,
    schedule_interval='@daily',  # Adjust as necessary
    start_date=days_ago(1),
    catchup=False,
    dag_id='dag_pipeline',
    tags=['ml_pipeline'],
)
def main():
    data = extract()
    analyzed_data = sentiment_analysis(data)
    wordcloud_path = generate_wordclouds(analyzed_data)
    load_to_postgresql(analyzed_data)

main()
