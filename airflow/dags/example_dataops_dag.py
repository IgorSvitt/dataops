from datetime import datetime

from airflow import DAG
from airflow.operators.bash import BashOperator

with DAG(
    dag_id="example_dataops_dag",
    start_date=datetime(2025, 1, 1),
    schedule=None,
    catchup=False,
) as dag:
    t1 = BashOperator(task_id="hello", bash_command="echo 'Airflow is running' && date")
    t2 = BashOperator(task_id="done", bash_command="echo 'DAG finished'")

    t1 >> t2
