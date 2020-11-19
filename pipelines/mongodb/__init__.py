'''
Date: 2020-11-14
Author: Vitali Lupusor

Description: TODO
'''

# Import internal modules
from .mongo_connect import mongo_client
from .get_collection import get_collection
from config import Config

# Instantiate the imported modules
config = Config()

database_name = config.DATABASE
collection_users = config.COLLECTION_USERS

@get_collection(
    database_name=database_name, collection_name=collection_users
)
def users_extract_logic(
    cut_off_date=None, start_date=None, *args, **kwargs
):
    '''TODO

    Arguments:
        cut_off_date (): TODO
        start_date (): TODO
        *args (tuple): TODO
        **kwargs (dict): TODO

    return (): TODO
    '''
    # MongoDB syntax for the extraction logic
    logic = f'''aggregate([
        {{
            '$unwind': {{
                'path': '$subscriptions'
            }}
        }},
        {{
            '$unwind': {{
                'path': '$subscriptions.invoices'
            }}
        }},
        {{
            '$unwind': {{
                'path': '$subscriptions.invoices.info'
            }}
        }},
        {{
            '$unwind': {{
                'path': '$subscriptions.invoices.info.date'
            }}
        }},
        {{
            '$match': {{
                'subscriptions.invoices.info.date': {{
                    '$gte': datetime.strptime('{start_date}', '%Y-%m-%d %H:%M:%S'),
                    '$lt': datetime.strptime('{cut_off_date}', '%Y-%m-%d %H:%M:%S')
                }}
            }},
        }}
    ])'''

    return logic
