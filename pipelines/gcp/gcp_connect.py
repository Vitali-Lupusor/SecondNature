'''
Date: 2020-11-14
Author: Vitali Lupusor

Description: TODO
'''

from . import get_credentials

@get_credentials
def get_client(service):
    '''TODO:

    Arguments:
        service (str): TODO

    return (): TODO
    '''
    # Import external modules
    _cloud = __import__('google.cloud', fromlist=[service])
    service = getattr(_cloud, service)

    return service
