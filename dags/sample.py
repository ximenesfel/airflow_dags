from datetime import timedelta
from airflow import DAG
from airflow.contrib.operators.kubernetes_pod_operator import KubernetesPodOperator
from airflow.utils.dates import days_ago

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


training = KubernetesPodOperator(task_id="inference",
                                 name="inference",
                                 namespace="test",
                                 cmds=["echo"],
                                 image="python:3.11.1",
                                 in_cluster=True,
                                 dag=dag
)


training