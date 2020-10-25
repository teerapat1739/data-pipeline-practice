from airflow import DAG
from airflow.operators.python_operator import PythonOperator
from datetime import datetime, timedelta
from airflow.models import Variable
from bs4 import BeautifulSoup
import requests
import http.client
import mimetypes


def method_one():
    conn = http.client.HTTPSConnection("www.prachachat.net")
    payload = ''
    headers = {}
    all_path = ["/feed", "/finance/feed", "/marketing/feed", "/economy/feed", "/politics/feed", "/world-news/feed"]
    dict_item = {"title":"","date":"","url":"","source":""} 
    for i in range(len(all_path)):
        conn.request("GET", all_path[i], payload, headers)
        res = conn.getresponse()
        data = res.read()
        soup = BeautifulSoup(data.decode("utf-8"), 'lxml')
        items = soup.find_all('item')
        for item in items:
            dict_item["title"] = item.title.text
            dict_item["date"] = " ".join(item.pubdate.text.split(' ')[1:4])
            dict_item["source"] = "prachachat"
            dict_item["url"] = item.select_one('comments').text.split('#')[0]
            # send_api.send(dict_item,routing_key)
    print('dict_item_1',dict_item)


default_args = {
    "owner": 'Airflow',
    "start_date": datetime(2020,9,30),
}

dag = DAG("variable", default_args=default_args, schedule_interval=timedelta(1))

# t1 = BashOperator(task_id="print_path", bash_command="echo /usr/local/airflow", dag=dag)
t1 =  push_task = PythonOperator(task_id='push_task', python_callable=method_one, provide_context=True)
