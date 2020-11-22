'''
Date: 2020-11-22
Author: Vitali Lupusor

Description: The schema of the BigQuery "users" master table.
'''

def users_destination_schema(SchemaField):
    '''Build BigQuery schema for the "users" feeds.

    Arguemnts:
        SchemaField (google.cloud.bigquery.SchemaField): BigQuery 
                schema object.

    return (list): BigQuery schema for the "users" master table.
    '''
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
