"""Decrypt encrypted files.

To spare the installation of additional software as well as
dealing with private and public keys I have used the Fernet encryption.
For an elevated security this would be replaced with GnuPG or any alike
encryption tool.

Date: 2020-11-14
Author: Vitali Lupusor
"""


def decrypt(file_path: str, passphrase: bytes) -> str:
    """Decrypt a Fornet encrypted file.

    Arguments:
        file_path (str):
            The pass to the encrypted file.

        passphrase (bytes, str):
            The passphrase necessary to decrypt the file.

    return (str):
        The decrypted content of an encrypted file.
    """
    # Import external modules
    _fernet = __import__('cryptography.fernet', fromlist=['Fernet'])
    Fernet = _fernet.Fernet

    # Import internal modules
    from . import encode_passphrase

    # Make sure the passphrase is of bytes type
    passphrase = encode_passphrase(passphrase)

    key = Fernet(passphrase)

    with open(file_path, 'rb') as file_object:
        decrypted_data = key.decrypt(
            file_object.read()
        )

    return decrypted_data.decode('utf-8')
