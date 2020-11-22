'''
Date: 2020-11-14
Author: Vitali Lupusor

Description: ETL process 
'''

def users_ETL(source, **spark_config):
    '''Flatten the feeds from "users" collection and output disk.
    Also, converts the date fields to DateType.

    Arguments:
        source (str): The full or relative path to the file.
        **spark_config (dict): Spark configuration settings key-value 
                attributes.

    return (str): The full path (file name included) where the file 
            is outputed to.
    '''
    # Import external modules
    _os = __import__('os', fromlist=[
        'path', 'getenv', 'listdir', 'makedirs', 'rename'
    ])
    path = _os.path
    getenv = _os.getenv
    listdir = _os.listdir
    makedirs = _os.makedirs
    rename = _os.rename
    _re = __import__('re', fromlist=['search', 'IGNORECASE'])
    search = _re.search
    IGNORECASE =_re.IGNORECASE
    _functions = __import__(
        'pyspark.sql.functions', fromlist=['col', 'from_unixtime']
    )
    col = _functions.col
    from_unixtime = _functions.from_unixtime

    # Import internal modules
    from pipelines.support_features import build_spark
    from . import users_source_schema

    # Configure working variables
    output_dir = path.join(
        getenv('TMP') or getenv('TEMP') or getenv('TMPDIR'),
        'secondNature',
        'output'
    )
    filename = path.basename(source)
    filename, extention = path.splitext(filename)

    # Create the temporary output directory
    if not path.isdir(output_dir):
        makedirs(output_dir)

    # Build the spark application object
    spark = build_spark(tuple(spark_config.items()))

    # Read in the data
    users = spark.read \
        .format(extention[1:]) \
        .option('path', source) \
        .schema(users_source_schema) \
        .load()

    # Unnest (unwind) the field
    users =  users.select([
        col('_id.$oid').alias('id'),
        'age',
        'country',
        col('fakeDataHelpers.messagesPerDay').alias('messagesPerDay'),
        'firstname',
        'lastname',
        'gender',
        col('groupId.$oid').alias('groupId'),
        'postCode',
        col('signUpDate.$date').alias('signUpDate'),
        *[
            col(f'subscriptions.{column}').alias(f'subscription_{column}') \
                for column in users.select('subscriptions.*').columns
        ]
    ])
    users = users.select([
        'id',
        'age',
        'country',
        'messagesPerDay',
        'firstname',
        'lastname',
        'gender',
        'groupId',
        'postCode',
        'signUpDate',
        col('subscription__id.$oid').alias('subscription_id'),
        *[
            col(f'subscription_invoices.{column}').alias(f'invoice_{column}') \
                for column in users.select('subscription_invoices.*').columns
        ],
        *[
            col(f'subscription_planType.{column}').alias(f'planType_{column}') \
                for column in users.select('subscription_planType.*').columns
        ],
        col('subscription_startDate.$date').alias('subscription_startDate'),
        col('subscription_subscriptionID.$oid').alias('subscriptionID')
    ])
    users = users.select([
        'id',
        'age',
        'country',
        'messagesPerDay',
        'firstname',
        'lastname',
        'gender',
        'groupId',
        'postCode',
        'signUpDate',
        'subscription_id',
        col('invoice__id.$oid').alias('invoice_id'),
        'invoice_amount',
        'invoice_currency',
        *[
            col(f'invoice_info.{column}').alias(f'invoice_{column}') \
                for column in users.select('invoice_info.*').columns
        ],
        col('planType__id.$oid').alias('planType_id'),
        'planType_currency',
        'planType_paymentType',
        col('planType_planCost').alias('planCost'),
        col('planType_planDescription').alias('planDescription'),
        col('planType_planID').alias('planID'),
        col('planType_planLength').alias('planLength'),
        col('planType_planLengthUnits').alias('planLengthUnits'),
        'subscription_startDate',
        'subscriptionID'
    ])
    users = users.select([
        'id',
        'age',
        'country',
        'messagesPerDay',
        'firstname',
        'lastname',
        'gender',
        'groupId',
        'postCode',
        'signUpDate',
        'subscription_id',
        'invoice_id',
        'invoice_amount',
        'invoice_currency',
        col('invoice_date.$date').alias('invoice_date'),
        'invoice_status',
        'planType_id',
        'planType_currency',
        'planType_paymentType',
        'planCost',
        'planDescription',
        'planID',
        'planLength',
        'planLengthUnits',
        'subscription_startDate',
        'subscriptionID'
    ])

    # Convert date fields to DateType
    for column in users.columns:
        if 'date' in column.lower():
            users = users.withColumn(
                column,
                (
                    from_unixtime(users[column] / 1000)
                ).cast('timestamp')
            )

    # Output the ETLed file
    users.coalesce(1).write \
        .format('csv') \
        .mode('overwrite') \
        .option('header', True) \
        .option('nullValue', '') \
        .option('emptyValue', '') \
        .option('timestampFormat', 'yyyy-MM-dd HH:mm:ss') \
        .option('path', output_dir) \
        .save()

    # Rename
    tmp_filename = next(
        file for file in listdir(output_dir) \
            if search(r'part.*\.csv$', file, IGNORECASE)
    )
    tmp_file_path = path.join(
        output_dir, tmp_filename
    )
    output_file_path = path.join(
        output_dir, f'{filename}.csv'
    )
    rename(
        tmp_file_path, output_file_path
    )

    return output_file_path
