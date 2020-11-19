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
    # Import internal modules
    from pipelines import users_extract_logic

    result = users_extract_logic(
        cut_off_date='2020-06-03',              # This date can be changed or omitted altogether
        start_date='2020-06-02'                 # This date can be changed or omitted altogether
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
