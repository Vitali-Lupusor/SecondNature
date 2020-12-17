"""Connect to a MongoDB host.

Date: 2020-11-14
Author: Vitali Lupusor
"""

# Import standard modules
from typing import Optional

# Import third-party modules
from pymongo import MongoClient


def mongo_client(
    host: Optional[str] = None,
    port: int = 27017,
    **kwargs
) -> MongoClient:
    """Connect to a MongoDG host.

    Return an authenticate client, if authentication required.

    Arguments:
        host (str):
            MongoDB host IP.

        port (int):
            Connection port.

        **kwargs (dict):
            Optional key-value attributes.

    return (pymongo.MongoClient):
        Authenticated client.
    """
    # Configure the defaul attributes
    host = host or 'localhost'

    # Connected to Database host machine
    client = MongoClient(
        host=host,
        port=port,
        **kwargs
    )
    return client
