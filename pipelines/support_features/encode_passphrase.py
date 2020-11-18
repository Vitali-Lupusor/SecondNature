'''
Date: 2020-11-14
Author: Vitali Lupusor

Description: TODO
'''

def encode_passphrase(passphrase):
    '''TODO

    Arguments:
        passphrase (str, butes): TODO

    return (bytes): TODO
    '''
    if isinstance(passphrase, str):
        passphrase = passphrase.encode('utf-8')
    elif not isinstance(passphrase, bytes):
        message = 'The passphrase should be of str or bytes type'
        raise TypeError(message)

    return passphrase
