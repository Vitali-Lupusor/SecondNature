'''
Date: 2020-11-21
Author: Vitali Lupusor

Description: Loads files from Google Cloud Storage directly to a BigQuery table.
        This function is currently not in use, but is 100% functional.
'''

def from_gcs_to_bq(gcs_uri, destination, schema=None, mode=None, header_rows=1):
    '''Load a files from GCS into BigQuery.

    Arguments:
        gcs_uri (str): The URI of the GCS blob in "gs://bucket/prefix/file" format.
        destination (str): The path to the destination table in format 
                "project.dataset.table".
        schema (google.cloud.bigquery.SchemaType): Schema of the dstination table.
        mode (str, NoneType): Table's write disposition. Possible values: 
                ['empty', 'append', 'overwrite']. If not specified, defaults 
                to 'empty'.
        header_rows (int): The number of rows that make up the header. 
                Defaults to 1. This is being ignored, if the source file format is 
                anything other than CSV.

    return (NoneType): No return.
    '''
    # Import externla modules
    _cloud = __import__('google.cloud', fromlist=['bigquery'])
    bigquery = _cloud.bigquery
    _os = __import__('os', fromlist=['path'])
    path = _os.path

    # Import internal modules
    from . import get_client

    # Get BigQuery client object
    bq = get_client(service='bigquery')

    # Configure the working variables
    source_file_extention = path.splitext(gcs_uri)[1]
    source_format = 'NEWLINE_DELIMITED_JSON' \
        if source_file_extention[1:].upper() == 'JSON' \
            else source_file_extention[1:].upper()
    if not mode:
        mode = 'WRITE_EMPTY'
    elif mode.lower().strip() == 'overwrite':
        mode = 'WRITE_TRUNCATE'
    elif mode.lower().strip() == 'append':
        mode = 'WRITE_APPEND'
    elif mode.lower().strip() == 'empty':
        mode = 'WRITE_EMPTY'
    else:
        message = (
            'Table write mode can take the following values: '
            "['empty', 'append', 'overwrite']"
        )
        raise ValueError(message)

    # Configure the Load Job
    job_config = bigquery.LoadJobConfig()

    job_config.source_format = getattr(                     # Declare the format of the source file
        bigquery.SourceFormat, source_format
    )
    if source_file_extention.lower() == '.csv':
        job_config.skip_leading_rows = header_rows          # The number of rows the header spreads across
    if schema:
        job_config.schema = schema                          # Provide table schema
    else:
        job_config.autodetect = True                        # If schema not provided, autodetect it
    job_config.write_disposition = getattr(                 # Table write mode
        bigquery.WriteDisposition, mode
    )
    job_config.null_maker = ''                              # Read empty strings as NULL values

    # Upload the table from GCS
    job_load = bq.load_table_from_uri(
        source_uris=gcs_uri,
        destination=destination,
        job_config=job_config
    )

    job_load.result()
