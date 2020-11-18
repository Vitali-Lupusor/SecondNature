'''
Date: 2020-11-14
Author: Vitali Lupusor

Description: TODO
'''

def mongo_client(host=None, port=27017, **kwargs):
    '''TODO

    Arguments:
        host (): TODO
        port (): TODO
        **kwargs (dict): TODO

    return (): TODO
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
