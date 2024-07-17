from datetime import datetime, timedelta
from airflow import DAG
from airflow.operators.python_operator import PythonOperator
from src.extract_heroes import heroes_pipeline


default_args = {
    'owner': 'linkedin.com/in/diegosts',
    'depends_on_past': False,
    'email_on_failure': False,
    'email_on_retry': False,
    'retries': 1,
    'retry_delay': timedelta(minutes=5),
}

dag = DAG(
    'marvel_heroes_ingestion',
    default_args=default_args,
    description='DAG responsável pela ingestão dos heróis da Marvel',
    schedule_interval=timedelta(days=1),
    start_date=datetime(2024, 7, 16),
    catchup=False,
)

python_task = PythonOperator(
    task_id='ingest_marvel_heroes',
    python_callable=heroes_pipeline,
    dag=dag,
)

python_task
