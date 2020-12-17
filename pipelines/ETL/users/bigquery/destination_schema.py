"""Build the schema of the BigQuery "users" master table.

Date: 2020-11-22
Author: Vitali Lupusor
"""

# Import standard modules
from typing import List

# Import third-party modules
from google.cloud.bigquery import SchemaField


def _users_destination_schema(SchemaField: SchemaField) -> List[SchemaField]:
    """Build BigQuery schema for the "users" feeds.

    The below Nones can be replaced with field descriptions.
    This helps with a better understanding of the field for the person looking
    at the table and acts as a sort of data dictionary.

    Arguemnts:
        SchemaField (google.cloud.bigquery.SchemaField):
            BigQuery schema object.

    return (List[google.cloud.bigquery.SchemaField]):
        BigQuery schema for the "users" master table.
    """
    schema = [
        SchemaField('id', 'STRING', 'NULLABLE', None, ()),
        SchemaField('age', 'INTEGER', 'NULLABLE', None, ()),
        SchemaField('country', 'STRING', 'NULLABLE', None, ()),
        SchemaField('messagesPerDay', 'INTEGER', 'NULLABLE', None, ()),
        SchemaField('firstname', 'STRING', 'NULLABLE', None, ()),
        SchemaField('lastname', 'STRING', 'NULLABLE', None, ()),
        SchemaField('gender', 'STRING', 'NULLABLE', None, ()),
        SchemaField('groupId', 'STRING', 'NULLABLE', None, ()),
        SchemaField('postCode', 'STRING', 'NULLABLE', None, ()),
        SchemaField('signUpDate', 'TIMESTAMP', 'NULLABLE', None, ()),
        SchemaField('subscription_id', 'STRING', 'NULLABLE', None, ()),
        SchemaField('invoice_id', 'STRING', 'NULLABLE', None, ()),
        SchemaField('invoice_amount', 'FLOAT', 'NULLABLE', None, ()),
        SchemaField('invoice_currency', 'STRING', 'NULLABLE', None, ()),
        SchemaField('invoice_date', 'TIMESTAMP', 'NULLABLE', None, ()),
        SchemaField('invoice_status', 'STRING', 'NULLABLE', None, ()),
        SchemaField('planType_id', 'STRING', 'NULLABLE', None, ()),
        SchemaField('planType_currency', 'STRING', 'NULLABLE', None, ()),
        SchemaField('planType_paymentType', 'STRING', 'NULLABLE', None, ()),
        SchemaField('planCost', 'INTEGER', 'NULLABLE', None, ()),
        SchemaField('planDescription', 'STRING', 'NULLABLE', None, ()),
        SchemaField('planID', 'INTEGER', 'NULLABLE', None, ()),
        SchemaField('planLength', 'INTEGER', 'NULLABLE', None, ()),
        SchemaField('planLengthUnits', 'STRING', 'NULLABLE', None, ()),
        SchemaField('subscription_startDate', 'TIMESTAMP', 'NULLABLE', None, ()),
        SchemaField('subscriptionID', 'STRING', 'NULLABLE', None, ())
    ]

    return schema
