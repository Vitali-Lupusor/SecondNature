"""Upload files from local machine to GCS.

Date: 2020-11-14
Author: Vitali Lupusor
"""

# Import standard modules
from typing import Optional


def upload(
    source: str,
    destination: str,
    encryption_key: Optional[bytes] = None,
    keep: bool = False
) -> None:
    """Upload a single file from local machine to a provided GCS destination.

    If "encryption_key" provided, the file will be encypted with a
    "customer-supplied" key. Meaning that even people with access to "rest"
    bucket won't be able to take copies of the file.

    Cleans up after execution, if "keep" is set to False.

    Arguments:
        source (str):
            The path to the target file.

        destination (str):
            Either provide the FULL GCS path, i.e. "gs://bucket/prefix/file",
            or ommit the "gs://bucket/".
            In the case of a partial path, the bucket name will default to the
            one provided in the "./config.py" file.

        encryption_key (bytes):
            32-bit encrytption key.

        keep (bool):
            Flag specifying whether to keep the file after the upload or delete
            it. Defaults to False - delete the file.

    return (NoneType): No return.
    """
    # Import external modules
    _os = __import__('os', fromlist=['path', 'remove'])
    path = _os.path
    remove = _os.remove
    _re = __import__('re', fromlist=['search', 'IGNORECASE'])
    search = _re.search
    IGNORECASE = _re.IGNORECASE

    # Import internal modules
    from config import Config
    from . import get_client

    # Instantiate the imported modules
    config = Config()

    # Get GCS client
    gcs = get_client(service='storage')

    pathname, extention = path.splitext(destination)

    # Analyse the format of the proviede destination attribute
    if search(r'gs://.+/?', destination, IGNORECASE):
        if extention:
            bucket_name, prefix, dest_filename = search(
                r'gs://([\w-]+)/(?:(.+)/)?(.+\.(?:{}))$'.format(extention),
                destination,
                IGNORECASE
            ).groups()
        else:
            bucket_name, prefix = search(
                r'gs://([\w-]+)/(?:(.+))?',
                pathname,
                IGNORECASE
            ).groups()
            dest_filename = path.basename(source)
    else:
        bucket_name = config.BUCKET_NAME

        if extention:
            prefix, dest_filename = path.split(destination)
        else:
            prefix = pathname
            dest_filename = path.basename(source)

    blob_name = '/'.join([prefix, dest_filename]) \
        .strip('/')                   # In case there is no prefix

    bucket = gcs.get_bucket(
        bucket_or_name=bucket_name
    )
    blob = bucket.blob(
        blob_name=blob_name,
        encryption_key=encryption_key   # Currently set to None. For more info read comments in ./config.py -> ENCRYPTION_KEY
    )

    with open(source, 'rb') as file_obj:
        blob.upload_from_file(
            file_obj=file_obj
        )

    # Clean up
    if not keep:
        remove(source)
