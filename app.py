"""Trigger the application - executable file.

The application is orchstrated by Apache Airflow. This allows for a visual
interpretation of the success/failure for each step of the pipeline.

IMPORTANT!
Make sure that once Apache Airflow is installed the "dags_folder" key is set up
to the top level of this application.

Date: 2020-11-14
Author: Vitali Lupusor
"""

# Import external modules
from airflow import DAG
from airflow.operators.python_operator import PythonOperator
from datetime import datetime
from datetime import timedelta

# Import internal modules
from config import Config
from pipelines import users_extract_logic
from pipelines import users_pyspark_ETL
from pipelines import upload
from pipelines import from_file_to_bq
from pipelines import users_destination_schema

# Instantiate import modules
config = Config()

# Collection configuration information
users_meta = config.COLLECTIONS['users']['bq_location']

default_args = {
    'owner': 'secondNature',
    'start_date': datetime(2020, 6, 1, 15, 00, 00),         # This is based on COMPANY_START_DATE value provided in the README.md file
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
    schedule_interval=timedelta(days=1)                     # Scheduled to be triggered daily
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
        'destination': users_meta['gcs_location'],
        'encryption_key': None,
        'keep': False
    }
)

task_etl_users_feed = PythonOperator(
    task_id='users_ETL',
    dag=dag,
    depends_on_past=False,
    provide_context=False,
    python_callable=users_pyspark_ETL,
    op_kwargs={
        'source': '{{ task_instance.xcom_pull(task_ids="extract_table_users") }}'
    }
)

task_upload_to_datawarehouse = PythonOperator(
    task_id='upload_to_datawarehouse',
    dag=dag,
    depends_on_past=False,
    provide_context=False,
    python_callable=from_file_to_bq,
    op_kwargs={
        'source': '{{ task_instance.xcom_pull(task_ids="users_ETL") }}',
        'destination': (
            f'{config.PROJECT_NAME}.'
            f"{users_meta['datasets']['destination']['name']}."
            f"{users_meta['datasets']['destination']['table']['name']}"
        ),
        'schema': users_destination_schema,
        'mode': users_meta['datasets']['destination']['table']['mode'],
        'header_rows': users_meta['datasets']['destination']['table']['header_rows'],
        'partitioning_field': users_meta['datasets']['destination']['table']['partitioning_field'],
        'partitioning_type': users_meta['datasets']['destination']['table']['partitioning_type'],
        'partitioning_freq': users_meta['datasets']['destination']['table']['partitioning_freq'],
        'clustering_fields': users_meta['datasets']['destination']['table']['clustering_fields']
    }
)

task_extract_table_users >> task_etl_users_feed >> [
    task_upload_to_datalake, task_upload_to_datawarehouse
]
