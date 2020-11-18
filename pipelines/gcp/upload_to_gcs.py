'''
Date: 2020-11-14
Author: Vitali Lupusor

Description: TODO
'''

def upload(source, destination, encryption_key=None):
    '''TODO

    Arguments:
        source (): TODO
        destination (): TODO
        encryption_key (): TODO

    return (): TODO
    '''
    # Import external modules
    _os = __import__('os', fromlist=['path'])
    path = _os.path

    # Import internal modules
    from . import get_client

    gcs = get_client(service='storage')

    bucket_name = destination[
        len('gs://'):destination[len('gs://'):].index('/')+len('gs://')
    ]
    prefix = destination[
        len(f'gs://{bucket_name}')+1:destination.index(
            path.basename(destination)
        )-1
    ]
    filename = path.basename(source)
    blob_name = '/'.join([prefix, filename])

    bucket = gcs.get_bucket(
        bucket_or_name=bucket_name
    )
    blob = bucket.blob(
        blob_name=blob_name,
        encryption_key=encryption_key # Currently set to None. For more info read comments in config.py -> ENCRYPTION_KEY
    )

    with open(source, 'rb') as file_obj:
        result = blob.upload_from_file(
            file_obj=file_obj
        )

    return result
