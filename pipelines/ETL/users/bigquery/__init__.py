"""Collect all BigQuery features in one place.

Date: 2020-11-21
Author: Vitali Lupusor
"""

# Import extenal modules
from google.cloud.bigquery import SchemaField

# Import internal modules
from .destination_schema import _users_destination_schema

users_destination_schema = _users_destination_schema(SchemaField)
