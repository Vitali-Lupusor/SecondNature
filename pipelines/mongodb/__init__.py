"""MongoDB Operations.

The extraction logic for the "users" collection.

Date: 2020-11-14
Author: Vitali Lupusor
"""

# Import standard modules
from datetime import datetime
from typing import Optional, Union

# Import internal modules
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
    cut_off_date: Optional[Union[str, datetime]] = None,
    start_date: Optional[Union[str, datetime]] = None,
    *args,
    **kwargs
) -> str:
    """Extract the "users" collection.

    If no attributes are provided, only the partition of the table that
    represesnt subset of invoices for the day before execution date will be
    extracted, i.e. if run on 2020-11-14, the extract will contain data for the
    period between 2020-11-13 00:00:00 and 2020-11-13 23:59:59.

    The time boundaries can be twicked.

    Arguments:
        cut_off_date (Optional[Union[str, datetime]]):
            The upper limit of the invoice date value for the extracted
            partition.

        start_date (Optional[Union[str, datetime]]):
            The lower limit of the invoice date value for the extracted
            partition.

        *args (tuple):
            Tuple containing an array of optional possitional attributes.

        **kwargs (dict):
            A dictionary of key-value sets of optional attributes.

    return (str):
        The logic that will be applied on the pymongo collection object.
    """
    # MongoDB syntax for the extraction logic
    logic = f"""aggregate([
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
    ])"""

    return logic
