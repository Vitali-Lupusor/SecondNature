'''
Date: 2020-11-14
Author: Vitali Lupusor

Description: TODO
'''

def test_connection():
    '''TODO

    Arguments:
        arg (): TODO

    return (): TODO
    '''
    # Import internal modules
    from pipelines.support_features import mongo_client
    from config import Config

    config = Config()

    client = mongo_client(
        username=config.USERNAME,
        password=config.PASSWORD
    )

    return client

if __name__ == '__main__':
    try:
        client = test_connection()
    except Exception as exception:
        print(
            'Connection test failed!',
            exception,
            sep='\n'
        )
    else:
        print('Connection test passed!')

