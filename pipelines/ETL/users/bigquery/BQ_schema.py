'''
Date: 2020-11-21
Author: Vitali Lupusor

Description: TODO
'''

def user_bq_schema(SchemaField):
    '''TODO

    Arguments:
        arg (): TODO

    return (): TODO
    '''
    schema = [
        SchemaField(
            '_id', 'RECORD', 'NULLABLE', None, (
                SchemaField('oid', 'STRING', 'NULLABLE', None, ()),
            )
        ),
        SchemaField('age', 'INTEGER', 'NULLABLE', None, ()),
        SchemaField('country', 'STRING', 'NULLABLE', None, ()),
        SchemaField(
            'fakeDataHelpers', 'RECORD', 'NULLABLE', None, (
                SchemaField('messagesPerDay', 'INTEGER', 'NULLABLE', None, ()),
            )
        ),
        SchemaField('firstname', 'STRING', 'NULLABLE', None, ()),
        SchemaField('gender', 'STRING', 'NULLABLE', None, ()),
        SchemaField(
            'groupId', 'RECORD', 'NULLABLE', None, (
                SchemaField('oid', 'STRING', 'NULLABLE', None, ()),
            )
        ),
        SchemaField('lastname', 'STRING', 'NULLABLE', None, ()),
        SchemaField('postCode', 'STRING', 'NULLABLE', None, ()),
        SchemaField(
            'signUpDate', 'RECORD', 'NULLABLE', None, (
                SchemaField('date', 'INTEGER', 'NULLABLE', None, ()),
            )
        ),
        SchemaField(
            'subscriptions', 'RECORD', 'NULLABLE', None, (
                SchemaField(
                    '_id', 'RECORD', 'NULLABLE', None, (
                        SchemaField('oid', 'STRING', 'NULLABLE', None, ()),
                    )
                ),
                SchemaField(
                    'invoices', 'RECORD', 'NULLABLE', None, (
                        SchemaField(
                            '_id', 'RECORD', 'NULLABLE', None, (
                                SchemaField('oid', 'STRING', 'NULLABLE', None, ()),
                            )
                        ),
                        SchemaField('amount', 'FLOAT', 'NULLABLE', None, ()),
                        SchemaField('currency', 'STRING', 'NULLABLE', None, ()),
                        SchemaField(
                            'info', 'RECORD', 'NULLABLE', None, (
                                SchemaField(
                                    'date', 'RECORD', 'NULLABLE', None, (
                                        SchemaField('date', 'INTEGER', 'NULLABLE', None, ()),
                                    )
                                ),
                                SchemaField('status', 'STRING', 'NULLABLE', None, ())
                            )
                        ),
                    )
                ),
                SchemaField(
                    'planType', 'RECORD', 'NULLABLE', None, (
                        SchemaField(
                            '_id', 'RECORD', 'NULLABLE', None, (
                                SchemaField('oid', 'STRING', 'NULLABLE', None, ()),
                            )
                        ),
                        SchemaField('currency', 'STRING', 'NULLABLE', None, ()),
                        SchemaField('paymentType', 'STRING', 'NULLABLE', None, ()),
                        SchemaField('planCost', 'FLOAT', 'NULLABLE', None, ()),
                        SchemaField('planDescription', 'STRING', 'NULLABLE', None, ()),
                        SchemaField('planID', 'INTEGER', 'NULLABLE', None, ()),
                        SchemaField('planLengthUnits', 'STRING', 'NULLABLE', None, ()),
                        SchemaField('planLength', 'INTEGER', 'NULLABLE', None, ())
                    )
                ),
                SchemaField(
                    'startDate', 'RECORD', 'NULLABLE', None, (
                        SchemaField('date', 'INTEGER', 'NULLABLE', None, ()),
                    )
                ),
                SchemaField(
                    'subscriptionID', 'RECORD', 'NULLABLE', None, (
                        SchemaField('oid', 'STRING', 'NULLABLE', None, ()),
                    )
                )
            )
        )
    ]

    return schema
