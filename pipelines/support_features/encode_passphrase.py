'''
Date: 2020-11-14
Author: Vitali Lupusor

Description: Encode the passphrase.
'''

def encode_passphrase(passphrase):
    '''Make sure the passphrase is of "bytes" data type.

    Arguments:
        passphrase (str, butes): Passphrase used to decrypt files.

    return (bytes): UTF-8 encoded string.
    '''
    if isinstance(passphrase, str):
        passphrase = passphrase.encode('utf-8')
    elif not isinstance(passphrase, bytes):
        message = 'The passphrase should be of str or bytes type'
        raise TypeError(message)

    return passphrase
