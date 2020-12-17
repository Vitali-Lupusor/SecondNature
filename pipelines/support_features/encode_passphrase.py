"""Encode the passphrase.

Date: 2020-11-14
Author: Vitali Lupusor
"""

# Import standard modules
from typing import Union


def encode_passphrase(passphrase: Union[str, bytes]) -> bytes:
    """Make sure the passphrase is of "bytes" data type.

    Arguments:
        passphrase Union[str, bytes]:
            Passphrase used to decrypt files.

    return (bytes):
        UTF-8 encoded string.
    """
    if isinstance(passphrase, str):
        passphrase = passphrase.encode('utf-8')
    elif not isinstance(passphrase, bytes):
        message = 'The passphrase should be of str or bytes type'
        raise TypeError(message)

    return passphrase
