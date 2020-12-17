"""Initiate the code related to PySpark ETL process of the "users" files.

Date: 2020-11-14
Author: Vitali Lupusor
"""

# Import external modules
from pyspark.sql import types

# Import the modules
from .source_schema import users_source_schema

users_source_schema = users_source_schema(types=types)

# Import the ETL modules
from .users import users_ETL
