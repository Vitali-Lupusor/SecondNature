'''
Date: 2020-11-14
Author: Vitali Lupusor

Description: Pipeline configuration file.
'''

class Config:
    '''Configuration class - the centralised configuration object.

    All pipeline configurations should be defined here.
    '''
    # Import external modules
    _os = __import__('os', fromlist=['getenv'])
    getenv = _os.getenv
    _datetime = __import__('datetime', fromlist=['datetime', 'timedelta'])
    datetime = _datetime.datetime
    timedelta = _datetime.timedelta

    # Database Credentials
    DATABASE = 'secondNature'
    COLLECTION_GROUPS = 'groups'
    COLLECTION_MESSAGES = 'messages'
    COLLECTION_USERS = 'users'
    USERNAME = getenv('MONGO_ACCOUNT') or 'root'        # The credentials should be stored in a vault
    PASSWORD = getenv('MONGO_PASSWORD') or 'example'    # Left here for now, but would most likely move to Google Secret Manager
    PORT = int(getenv('MONGO_PORT') or 21017)

    # Airflow Configuration Variables
    AIRFLOW_DEFAULT_CONFIG = {
        'owner': 'secondNature',
        'start_date': datetime(2020, 5, 31),        # This is based on COMPANY_START_DATE value provided in the README.md file
        'email': [],
        'email_on_failure': False,                  # TODO: set up an emil SMTP and change to True
        'email_on_retry': False,
        'retries': 1,
        'retry_delay': timedelta(minutes=5)
    }

    # Google Configuration Variables
    PROJECT_NAME = 'id-business-intelligence'
    BUCKET_NAME = 'playground-pipelines'
    CREDENTIALS = 'credentials/encypted_service_account.txt'
    PASSPHRASE = '87yq7EaftReN4nBaIdoZGtf5BBZzQCAmv-DgxXxqTlg='                                # This is going to be provided separatelly in an email
    ENCRYPTION_KEY = getenv('GCS_ENRYPTION_KEY')                    # This will use "customer-supplied" encryption for files in GCS.
                                                                    # It means that even people with access to the bucket won't be able take 
                                                                    # copies, if they don't have this key.

    # Operation Variables
    COLLECTIONS = {
        # 'groups': {
        #     'partition_field': 'startDate',
        #     'gcs_location': 'groups'
        # },
        # 'messages': {
        #     'partition_field': '',
        #     'gcs_location': 'messages'
        # },
        'users': {
            'partition_field': 'subscriptions.invoices.info.date',
            'gcs_location': 'users'
        }
    }
