from datetime import timedelta
from airflow import DAG
from airflow.contrib.operators.kubernetes_pod_operator import KubernetesPodOperator
from airflow.operators.python_operator import PythonOperator
from airflow.operators.bash_operator import BashOperator
from airflow.models import DagRun
from airflow.utils.state import State
from airflow.utils.dates import days_ago
from kubernetes.client import models as k8s

default_args = {
    'owner': 'Airflow',
    'depends_on_past': False,
    'start_date': days_ago(0),
    'catchup': False,
    'email': ['airflow@example.com'],
    'email_on_failure': False,
    'email_on_retry': False,
    'retries': 0,
    'retry_delay': timedelta(minutes=5),
}

dag = DAG(
    'kuberntes_yaml',
    default_args=default_args,
    schedule_interval=None,
    max_active_runs=1,
    concurrency=10,
)

start = BashOperator(
    task_id='start',
    bash_command='echo 1',
    dag=dag
)

training = KubernetesPodOperator(task_id="inference",
                                 name="inference",
                                 namespace="airflow",
                                 cmds=["echo"],
                                 image="rest_python:latest",
                                 in_cluster=True,
                                 dag=dag
)

finish = BashOperator(
    task_id='finish',
    bash_command='echo 1',
    dag=dag
)

start >> training >> finish