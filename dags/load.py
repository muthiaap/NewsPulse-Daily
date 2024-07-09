import pandas as pd
import psycopg2
from psycopg2 import sql
from datetime import timedelta
from airflow.decorators import task
from datetime import date

@task(task_id='Load')
def load_to_postgresql(df, table_name = 'news_sentiments'):
    df['date'] = date.today() - timedelta(days=1)

    print("DataFrame content:\n", df)
    
    conn_string = "dbname='postgres' host='host.docker.internal' user='postgres' password='26111999Map' port=5432"
    conn = None
    cursor = None
    
    try:
        conn = psycopg2.connect(conn_string)
        cursor = conn.cursor()
        
        for index, row in df.iterrows():
            insert_query = sql.SQL("""
                INSERT INTO {table} (news, sentiment, date)
                VALUES (%s, %s, %s)
            """).format(table=sql.Identifier(table_name))
            cursor.execute(insert_query, (row['news'], row['sentiment'], row['date']))
        
        conn.commit()
        print(f"Data successfully loaded into {table_name} table.")
        
    except Exception as e:
        print(f"An error occurred: {e}")
        
    finally:
        if cursor:
            cursor.close()
        if conn:
            conn.close()
