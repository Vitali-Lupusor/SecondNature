'''
Date: 2020-11-14
Author: Vitali Lupusor

Description: Executable file - triggers the application.
    The application is orchstrated by Apache Airflow. This allows 
    for a visual interpretation of the success/failure for each step 
    of the pipeline.
'''

# Import external modules
from airflow import DAG
from airflow.operators.python_operator import PythonOperator
from datetime import datetime
from datetime import timedelta

# Import internal modules
from config import Config
from pipelines import users_extract_logic
from pipelines import upload

# Instantiate import modules
config = Config()

default_args = {
    'owner': 'secondNature',
    'start_date': datetime(2020, 5, 31, 15, 00, 00),        # This is based on COMPANY_START_DATE value provided in the README.md file
    'email': [],
    'email_on_failure': False,                              # TODO: set up an emil SMTP and change to True
    'email_on_retry': False,
    'retries': 1,
    'retry_delay': timedelta(minutes=5)
}

dag = DAG(
    dag_id='data_migration',
    description=(
        'Extract a subset of a MongoDB database collection and '
        'upload it to Google Cloud Storge.\n'
        'Each extract contains 1-day-worth of data.'
    ),
    default_args=default_args,
    schedule_interval=timedelta(days=1)                       # Scheduled to be triggered daily
)

task_extract_table_users = PythonOperator(
    task_id='extract_table_users',
    dag=dag,
    depends_on_past=False,
    wait_for_downstream=True,
    python_callable=users_extract_logic,
    provide_context=True,
    op_kwargs={
        'start_date': None,
        'cut_off_date': None
    }
)

task_upload_to_datalake = PythonOperator(
    task_id='upload_to_datalake',
    dag=dag,
    depends_on_past=False,
    provide_context=False,
    python_callable=upload,
    op_kwargs={
        'source': '{{ task_instance.xcom_pull(task_ids="extract_table_users") }}',
        'destination': config.COLLECTIONS['users']['gcs_location']
    }
)

############################   TESTING   ############################

task_extract_table_users >> task_upload_to_datalake

############################ END TESTING ############################
