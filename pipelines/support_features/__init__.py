'''
Date: 2020-11-14
Author: Vitali Lupusor

Description: TODO
'''

# Import internal modules
from .mongo_connect import mongo_client
from .spark_build_application import build_spark
from .validate_date_intput import validate_date
from .decryption_function import decrypt
from .encode_passphrase import encode_passphrase

def extract_table(
    database, collection, partition_field=None,
    cut_off_date=None, start_date=None, **kwargs
):
    '''TODO

    Arguments:
        database (): TODO
        collection (): TODO
        cut_off_date (): TODO
        start_date (): TODO

    return (str): TODO
    '''
    # Import external modules
    _datetime = __import__('datetime', fromlist=['datetime', 'timedelta'])
    datetime = _datetime.datetime
    timedelta = _datetime.timedelta
    os = __import__('os')
    _json_util = __import__('bson.json_util', fromlist=['dumps'])
    dumps = _json_util.dumps
    _errors = __import__('pymongo.errors', fromlist=['PyMongoError'])
    PyMongoError = _errors.PyMongoError

    # Import internal modules
    from config import Config

    # Instantiate the imported objects
    config = Config()

    # Configure the default attributes
    execution_date = kwargs.get('execution_date')
    if partition_field:
        cut_off_date = validate_date(cut_off_date or execution_date)
        start_date = validate_date(start_date) \
            if start_date \
                else validate_date(cut_off_date) - timedelta(days=1)

    # Connect to database
    client = mongo_client(
        username=config.USERNAME,
        password=config.PASSWORD
    )
    if database in client.list_database_names():                # Validate the provided database name
        db = eval(f'client.{database}')
    else:
        message = f'{database} is not an existing database'
        raise PyMongoError(message)
    if collection in db.list_collection_names():                # Validate the provided collection name
        collection = db.get_collection(collection)
    else:
        message = (
            f'{collection} is not an existing collection of '
            f'{database} database'
        )
        raise PyMongoError(message)

    # Extract data from table
    tmp_dir = os.getenv('TEMP') or os.getenv('TMP') \
        or os.getenv('TMPDIR')
    output_name = '_'.join([
        collection.name,
        datetime.today().strftime('%Y-%m-%d'),
        'D',
        start_date.strftime('%Y-%m-%d'),
        cut_off_date.strftime('%Y-%m-%d')
    ]) + '.json'
    tmp_path = os.path.join(
        tmp_dir, output_name
    )

    with open(tmp_path, 'w') as file_object:
        table = list(
            collection.find(
                {
                    partition_field: {
                        '$gte': start_date,
                        '$lt': cut_off_date
                    }
                },
                sort=[(partition_field, 1)]
            )
        ) if partition_field \
            else list(collection.find())
        file_object.write('[')
        for index, document in enumerate(table):
            if index != len(table)-1:
                file_object.write(
                    f'{dumps(document)},'
                )
            else:
                file_object.write(
                    dumps(document)
                )
        file_object.write(']')

    return tmp_path
