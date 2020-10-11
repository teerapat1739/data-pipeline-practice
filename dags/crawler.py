from airflow import DAG
from airflow.operators.bash_operator import BashOperator
from datetime import datetime, timedelta
from airflow.models import Variable


default_args = {
    "owner": 'Airflow',
    "start_date": datetime(2020,9,30),
}

dag = DAG("variable", default_args=default_args, schedule_interval=timedelta(1))

# t1 = BashOperator(task_id="print_path", bash_command="echo /usr/local/airflow", dag=dag)
t1 = BashOperator(task_id="print_path", bash_command="echo {{var.value.source_path}}", dag=dag)