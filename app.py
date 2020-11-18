'''
Date: 2020-11-14
Author: Vitali Lupusor

Description: TODO
'''

# Import external modules
from airflow import DAG
from airflow.operators.bash_operator import BashOperator
from airflow.operators.python_operator import PythonOperator
from datetime import timedelta

# Import internal modules
from config import Config
from pipelines import extract_table

# Instantiate import modules
config = Config()

default_args = config.AIRFLOW_DEFAULT_CONFIG

dag = DAG(
    dag_id='data_migration',
    description=(
        'Extract a subset of a MongoDB database collection and '
        'store it locally.\n'
        'Each extract contains 1-day-worth of data.' # TODO: Carry on with the description.
    ),
    default_args=default_args,
    schedule_interval=timedelta(minutes=5)                       # Scheduled to be triggered daily
)

for collection, partition_field in config.COLLECTION_PARTITIONING.items():
    task_extract_table = PythonOperator(
        task_id='extract_table',
        dag=dag,
        python_callable=extract_table,
        op_kwargs={
            'database': config.DATABASE,
            'collection': collection,
            'partition_field': partition_field,
            'start_date': None,
            'cut_off_date': None,
            'provide_context':True
        }
    )
