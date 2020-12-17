"""Connect to a MongoDB database and get the collection.

This is a decorator function that will connect to the database, get the
collection object and apply the appropriate logic (specified in a separate
function) in order to extract data.

Date: 2020-11-14
Author: Vitali Lupusor
"""


def get_collection(database_name: str, collection_name: str):
    """Extract a MongoDB collection.

    Take in the file extraction logic and apply it on the collection object of
    the specified database.

    Arguments:
        database_name (str):
            The name of the database to which to connect.

        collection_name (str):
            The name of the collection that will be queried.

    return (function):
        The decorator function.
    """

    def decorator_get_collection(funct):
        """Pass the decorated function to globals.

        Arguments:
            funct (function): The function that will be decorated.

        return (function): A wrapper function.
        """
        # Import external modules
        _functools = __import__('functools', fromlist=['wraps'])
        wraps = _functools.wraps

        @wraps(funct)
        def wrapper_get_collection(*args, **kwargs):
            """Wrap the target function.

            Wraps some logic around the decorated function.

            Arguments:
                *args (tuple): Possitional attributes of the decorated function.
                **kwargs (dict): Key-value attributes of the decorated function.

            return (str): The full path to the extracted file.
            """
            # Import external modules
            _datetime = __import__('datetime', fromlist=['datetime', 'timedelta'])
            datetime = _datetime.datetime
            timedelta = _datetime.timedelta
            os = __import__('os')
            _json_util = __import__('bson.json_util', fromlist=['dumps'])
            dumps = _json_util.dumps
            _errors = __import__('pymongo.errors', fromlist=['PyMongoError'])
            PyMongoError = _errors.PyMongoError

            # # Import internal modules
            from config import Config
            from pipelines.support_features import validate_date
            from .mongo_connect import mongo_client

            # Instantiate the imported objects
            config = Config()

            # Configure the default attributes
            execution_date = kwargs.get('execution_date')
            cut_off_date = kwargs.get('cut_off_date')
            start_date = kwargs.get('start_date')

            # Validate the provided date values
            cut_off_date = validate_date(cut_off_date or execution_date)
            start_date = validate_date(start_date) \
                if start_date \
                else validate_date(cut_off_date) - timedelta(days=1)

            # Connect to database
            client = mongo_client(
                username=config.USERNAME,
                password=config.PASSWORD
            )
            if database_name in client.list_database_names():                # Validate the provided database name
                db = eval(f'client.{database_name}')
            else:
                message = f'{database_name} is not an existing database'
                raise PyMongoError(message)
            if collection_name in db.list_collection_names():                # Validate the provided collection name
                collection = db.get_collection(collection_name)
            else:
                message = (
                    f'{collection_name} is not an existing collection of '
                    f'{database_name} database'
                )
                raise PyMongoError(message)

            # Prepare the name and the path of the to-be-extracted file
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

            # Execute the decorated function
            extraction_logic = funct(
                start_date=start_date,
                cut_off_date=cut_off_date
            )

            # Extract data from table
            with open(tmp_path, 'w') as file_object:
                table = list(
                    eval(f'collection.{extraction_logic}')
                )
                for document in table:
                    file_object.write(
                        f'{dumps(document)}\n'
                    )

            return tmp_path

        return wrapper_get_collection

    return decorator_get_collection
