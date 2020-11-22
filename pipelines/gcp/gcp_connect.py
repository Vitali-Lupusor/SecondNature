'''
Date: 2020-11-14
Author: Vitali Lupusor

Description: Connected to a Google Cloud Platform project.
'''

from . import get_credentials

@get_credentials
def get_client(service):
    '''Requests authentication for the specified GCP service, i.e. 
    storage, bigquery, logging, etc.

    Arguments:
        service (str): GCP service.

    return (google.cloud.${service}): GCP service.
    '''
    # Import external modules
    _cloud = __import__('google.cloud', fromlist=[service])
    service = getattr(_cloud, service)

    return service
