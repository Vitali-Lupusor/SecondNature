'''
Date: 2020-11-14
Author: Vitali Lupusor

Description: TODO
'''

def test_extract_table():
    '''TODO

    Arguments:
        arg (): TODO

    return (): TODO
    '''
    # Import external modules
    from random import choice

    # Import internal modules
    from config import Config
    from pipelines import extract_table

    # Instantiate imported modules
    config = Config()

    # Select a random collection
    collection = choice(
        list(
            config.COLLECTION_PARTITIONING.keys()
        )
    )
    partition_field = config.COLLECTION_PARTITIONING[collection]

    result = extract_table(
        database=config.DATABASE,
        collection=collection,
        partition_field=partition_field,
        cut_off_date='2020-06-25',              # This date can be changed or omitted altogether
        start_date='2020-06-24'                 # This date can be changed or omitted altogether
    )

    return result

if __name__ == '__main__':
    # Import external modules
    os = __import__('os')

    try:
        result = test_extract_table()
    except Exception as exception:
        print(
            'Table extraction test failed!',
            exception,
            sep='\n'
        )
    else:
        if os.path.isfile(result):
            print('Table extraction test passed!')
            os.remove(result)
        else:
            print(
                'Test failed! The extract has not been generated.'
            )
