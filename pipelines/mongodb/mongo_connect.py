'''
Date: 2020-11-14
Author: Vitali Lupusor

Description: Connect to a MongoDB host.
'''

def mongo_client(host=None, port=27017, **kwargs):
    '''Connection to a MongoDG host and return an authenticate 
    client (if authentication required).

    Arguments:
        host (str): MongoDB host IP.
        port (int): Connection port.
        **kwargs (dict): Optional key-value attributes.

    return (pymongo.MongoClient): Authenticated client.
    '''
    # Import external modules
    _pymongo = __import__('pymongo', fromlist=['MongoClient'])
    MongoClient = _pymongo.MongoClient

    # Configure the defaul attributes
    host = host or 'localhost'

    # Connected to Database host machine
    client = MongoClient(
        host=host,
        port=port,
        **kwargs
    )
    return client
