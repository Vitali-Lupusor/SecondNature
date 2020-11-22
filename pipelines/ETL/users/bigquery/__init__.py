'''
Date: 2020-11-21
Author: Vitali Lupusor

Description: Initiate the code related to BigQuery ETL of the 
        "users" files.
'''

# Import extenal modules
from google.cloud.bigquery import SchemaField

# Import internal modules
from .destination_schema import users_destination_schema

users_destination_schema = users_destination_schema(SchemaField)
