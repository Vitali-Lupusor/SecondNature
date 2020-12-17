"""Connected to a Google Cloud Platform project.

Date: 2020-11-14
Author: Vitali Lupusor
"""

# Import third-party modules
from google import cloud

# Import internal modules
from . import get_credentials


@get_credentials
def get_client(service: str) -> cloud:
    """Authenticate with GCP.

    Requests authentication for the specified GCP service, i.e. storage,
    bigquery, logging, etc.

    Arguments:
        service (str):
            GCP service.

    return (google.cloud.${service}):
        GCP service.
    """
    # Import external modules
    _cloud = __import__('google.cloud', fromlist=[service])
    service = getattr(_cloud, service)

    return service
