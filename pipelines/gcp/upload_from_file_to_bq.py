'''
Date: 2020-11-21
Author: Vitali Lupusor

Description: Upload a file from the local machine into a BigQuery talbe.
        If the table does not exist, it is being created.
'''

def from_file_to_bq(
    source, destination, schema=None, mode=None, header_rows=1,
    partitioning_field=None, partitioning_type=None,
    partitioning_freq=None, clustering_fields=None
):
    '''Load a files from the local machine into BigQuery.
    The job will wait until the upload is completed.

    Arguments:
        source (str): The full path to the source file.

        destination (str): The path to the destination table in format 
                "project.dataset.table".

        schema (google.cloud.bigquery.SchemaType): Schema of the dstination table.

        mode (str, NoneType): Table's write disposition. Possible values: 
                ['empty', 'append', 'overwrite']. If not specified, defaults 
                to 'empty'.

        header_rows (int): The number of rows that make up the header. 
                Defaults to 1. This is being ignored, if the source file format is 
                anything other than CSV.

        partitioning_field (str): The name of the field by with to partition the table.
                Defaults to None.

                IMPORTANT!
                The field should be at the highest level of schema hierarchy; and can 
                be only of 'DATE', 'DATETIME', 'TIMESTAMP' or 'INTEGER' types.

        partitioning_type (str): Specify whether it is a time or range partitioning. 
                Available options are ['time', 'range']. Defaults to None.

        partitioning_freq (any): If it is a time partitioning, then the options are: 
                ['day', 'hour']. Currently only "day" is supported. Defaults to None.

                IMPORTANT!
                If tge partitioning type is range, the value should be a dictionary 
                with the following mandatory fileds: {'start', 'end', 'interval'}!

        clustering_fields (list): The list of field by with to cluster the table. 
                The order in which the field as listed is important. For performance 
                optimisation order the field based on the most "popular" column first.
                Defaults to None.

                IMPORTANT!
                The field can only be of primary data types, i.e. INTEGER, STRING, 
                etc (no STRUCTs!).
                As of 2018-06-29, clustering fields cannot be set on a table
                which does not also have time partioning defined.

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
    source_file_extention = path.splitext(source)[1]
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

    if partitioning_field:
        if not partitioning_freq:
            if partitioning_type.lower() == 'time':
                partitioning_freq =  'day'
            elif partitioning_type.lower() == 'range':
                message = (
                    'Please specify the partitioning frequency!\n'
                    "Example {'start': 0, 'end': 10000000, 'interval': 10000}"
                )
                raise ValueError(message)
            else:
                message = (
                    '"time" and "rnage" are the only acceptable values'
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
    if partitioning_field:                                  # Configure the table partitioning
        if partitioning_type.lower().strip() == 'time':
            job_config.time_partitioning = bigquery.TimePartitioning(
                type_=getattr(
                    bigquery.TimePartitioningType, partitioning_freq.upper()
                ),
                field=partitioning_field
            )
        elif partitioning_type.lower().strip() == 'range':
            job_config.range_partitioning = bigquery.RangePartitioning(
                range_=bigquery.PartitionRange(**partitioning_freq),
                field=partitioning_field
            )
    if clustering_fields:                                   # Configure the table clustering
        if partitioning_type.lower().strip() == 'time':
            job_config.clustering_fields = clustering_fields
        else:
            message = (
                'As of 2018-06-29, clustering fields cannot be set on a '
                'table which does not also have time partioning defined.'
            )
            raise ValueError(message)

    # Upload the table from local machine
    with open(source, 'rb') as file_obj:
        job_load = bq.load_table_from_file(
            file_obj=file_obj,
            destination=destination,
            job_config=job_config
        )

    # Wait for the file to be loaded
    job_load.result()
