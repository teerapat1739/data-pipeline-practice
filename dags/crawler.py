from airflow import DAG
from airflow.operators.python_operator import PythonOperator
from airflow.operators.postgres_operator import PostgresOperator
from airflow.hooks.postgres_hook import PostgresHook


from datetime import datetime, timedelta
import requests
import pandas as pd    


import os


# TODO: move to configuration in airflow
SCRAPE_SERVICE_ENDPOINT=os.getenv('SCRAPE_SERVICE_ENDPOINT')




default_args = {
    "owner": "airflow",
    "depends_on_past": False,
    "start_date": datetime(2020, 1, 1),
    "email": ["airflow@airflow.com"],
    "email_on_failure": False,
    "email_on_retry": False,
    "retries": 1,
    "retry_delay": timedelta(minutes=5),
}

def get_news_api():
    response = requests.get(SCRAPE_SERVICE_ENDPOINT + 'news')

    df = pd.read_json(SCRAPE_SERVICE_ENDPOINT + 'news')
    print(df)
    df.to_csv('/usr/local/airflow/dags/news.csv')


def transfer_function(ds, **kwargs):

    destination_hook = PostgresHook(postgres_conn_id='postgres_conn', schema='airflow')
    destination_conn = destination_hook.get_conn()
    destination_cursor = destination_conn.cursor()

    df = pd.read_csv ('/usr/local/airflow/dags/news.csv', encoding='utf8')
    df["date"] = pd.to_datetime(df["date"],errors = 'ignore') 

    for _,row in df.iterrows():
        sql = "INSERT INTO news (date, source, title, url) VALUES (%s, %s, %s, %s)"
        val = (row["date"], row["source"], row["title"], row["url"])
        destination_cursor.execute(sql, val)
        destination_conn.commit()
    
    destination_hook = PostgresHook(postgres_conn_id='postgres_conn', schema='airflow')
    destination_conn = destination_hook.get_conn()

    destination_cursor = destination_conn.cursor()


    destination_cursor.close()
    destination_conn.close()
    print("Data transferred successfully!")


with DAG(dag_id="news-data-pipe-line", schedule_interval="@daily", default_args=default_args, catchup=False) as dag:

    get_news = PythonOperator(
            task_id="get_news",
            python_callable=get_news_api
    )

    create_news_table = PostgresOperator(
           task_id="create_news_table",
           postgres_conn_id="postgres_conn",
           mysql_conn_id="postgres_conn", 
           sql="CREATE TABLE IF NOT EXISTS news(date  timestamp, source varchar(40), title varchar(255), url varchar(255))"
    )

    save_csv_to_db = PythonOperator(
        task_id = 'save_csv_to_db',
        python_callable = transfer_function,
        provide_context=True,
        dag = dag
    )



    # change import csv data string to type date time from db with dataframe

    get_news >> create_news_table >> save_csv_to_db