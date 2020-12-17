"""Build PySpark Schema object for the extracted "users" collection.

Date: 2020-11-14
Author: Vitali Lupusor
"""


def users_source_schema(types):
    """Build the PySpark schema for the "users" collection feeds.

    Arguemnts:
        types (pyspark.sql.types):
            PySpark object containing all available data types.

    return (pyspark.sql.types.StructType):
        PySpark schema object for the "users" collection feeds.
    """
    schema = types.StructType(
        (
            types.StructField(
                '_id', types.StructType(
                    [
                        types.StructField('$oid', types.StringType())
                    ]
                )
            ),
            types.StructField('age', types.IntegerType()),
            types.StructField('country', types.StringType()),
            types.StructField(
                'fakeDataHelpers', types.StructType(
                    [
                        types.StructField('messagesPerDay', types.IntegerType())
                    ]
                )
            ),
            types.StructField('firstname', types.StringType()),
            types.StructField('gender', types.StringType()),
            types.StructField(
                'groupId', types.StructType(
                    [
                        types.StructField('$oid', types.StringType())
                    ]
                )
            ),
            types.StructField('lastname', types.StringType()),
            types.StructField('postCode', types.StringType()),
            types.StructField(
                'signUpDate', types.StructType(
                    [
                        types.StructField('$date', types.LongType())
                    ]
                )
            ),
            types.StructField(
                'subscriptions', types.StructType(
                    [
                        types.StructField(
                            '_id', types.StructType(
                                [
                                    types.StructField('$oid', types.StringType())
                                ]
                            )
                        ),
                        types.StructField(
                            'invoices', types.StructType(
                                [
                                    types.StructField(
                                        '_id', types.StructType(
                                            [
                                                types.StructField('$oid', types.StringType())
                                            ]
                                        )
                                    ),
                                    types.StructField('amount', types.DecimalType()),
                                    types.StructField('currency', types.StringType()),
                                    types.StructField(
                                        'info', types.StructType(
                                            [
                                                types.StructField(
                                                    'date', types.StructType(
                                                        [
                                                            types.StructField('$date', types.LongType())
                                                        ]
                                                    )
                                                ),
                                                types.StructField('status', types.StringType())
                                            ]
                                        )
                                    )
                                ]
                            )
                        ),
                        types.StructField(
                            'planType', types.StructType(
                                [
                                    types.StructField(
                                        '_id', types.StructType(
                                            [
                                                types.StructField('$oid', types.StringType())
                                            ]
                                        )
                                    ),
                                    types.StructField('currency', types.StringType()),
                                    types.StructField('paymentType', types.StringType()),
                                    types.StructField('planCost', types.DecimalType()),
                                    types.StructField('planDescription', types.StringType()),
                                    types.StructField('planID', types.StringType()),
                                    types.StructField('planLength', types.IntegerType()),
                                    types.StructField('planLengthUnits', types.StringType())
                                ]
                            )
                        ),
                        types.StructField(
                            'startDate', types.StructType(
                                [
                                    types.StructField('$date', types.LongType())
                                ]
                            )
                        ),
                        types.StructField(
                            'subscriptionID', types.StructType(
                                [
                                    types.StructField('$oid', types.StringType())
                                ]
                            )
                        )
                    ]
                )
            )
        )
    )

    return schema
