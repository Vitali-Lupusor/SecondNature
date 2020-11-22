'''
Date: 2020-11-22
Author: Vitali Lupusor

Description: This is provided in order prove that the pipelines 
        are populating real BigQuery tables.
'''

def query(project, dataset, table, limit=50):
    '''Query a BigQuery table.

    Arguments:
        project (str): The name of the project where the desired table is.

        dataset (str): The name of the BigQuery dataset where the table is.

        table (str): The name of the table to query.

        limit (int): How many rows to return.

    return (str): The output of the query
    '''
    # Import internal modules
    from pipelines.GCP import get_client

    bq = get_client(service='bigquery')

    query_job = bq.query(
        f'''
        SELECT
            *
        FROM
            `{project}.{dataset}.{table}`
        LIMIT
            {limit}
        '''
    )
    result = query_job.result()
    dataframe = result.to_dataframe()
    dataframe.to_csv('./query_result.txt', index=False)

    return 'Check file `./query_result.txt`'

if __name__ == '__main__':
    # Import external modules
    _argparse = __import__('argparse', fromlist=['ArgumentParser'])
    ArgumentParser = _argparse.ArgumentParser

    # Import internal modules
    from config import Config

    config = Config()

    project = config.PROJECT_NAME
    dataset = config.COLLECTIONS['users']['bq_location'] \
        ['datasets']['destination']['name']
    table = config.COLLECTIONS['users']['bq_location'] \
        ['datasets']['destination']['table']['name']

    parser = ArgumentParser(description='Query a BigQuery table')
    parser.add_argument(
        'limit',
        type=int,
        nargs='?',
        default=50,
        help='The number of rows to be returned'
    )

    kwargs = vars(parser.parse_args())

    result = query(
        project=project,
        dataset=dataset,
        table=table,
        **kwargs
    )

    print(result)
