'''
Date: 2020-11-14
Author: Vitali Lupusor

Description: TODO
'''

# Import internal modules
from config import Config
from pipelines.support_features import decrypt
from pipelines.support_features import encode_passphrase

# Instantiate the imported modules
config = Config()

# Set up working variables
project = config.PROJECT_NAME
credentials_path = config.CREDENTIALS
passphrase = encode_passphrase(config.PASSPHRASE)

def get_credentials(
    _funct=None, *,
    projtect=project,
    credentials_path=credentials_path,
    passphrase=passphrase
):
    '''TODO

    Arguments:
        credentials_path (str): TODO

    return () : TODO
    '''
    # Import external modules
    _functools = __import__('functools', fromlist=['wraps'])
    wraps = _functools.wraps

    def decorator_get_credentials(function):
        '''TODO

        Arguments:
            function (function): TODO

        return (function): TODO
        '''
        @wraps(function)
        def wrapper_get_credentials(*args, **kwargs):
            '''TODO

            Arguments:
                *args (list): TODO
                **kwargs (dict): TODO

            return (function): TODO
            '''
            # Import external modules
            _os = __import__('os', fromlist=['environ', 'remove'])
            environ = _os.environ
            remove = _os.remove

            if credentials_path:
                if not passphrase:
                    message = (
                        'Please provide the passphrase to decrypt the file'
                    )
                    raise AttributeError(message)
                else:
                    cred_json = 'credentials/tmp.json'

                    # Decrypt credentials file
                    with open(cred_json, 'wb') as cred_object:
                        cred_object.write(
                            decrypt(
                                file_path=credentials_path,
                                passphrase=passphrase
                            ).encode('utf-8')
                        )

            else:
                cred_json = environ.get('GOOGLE_APPLICATION_CREDENTIALS')

            service = function(*args, **kwargs)
            client = service.Client.from_service_account_json(cred_json)

            # Clean up
            if credentials_path:
                remove(cred_json)

            return client

        return wrapper_get_credentials

    if _funct:
        return decorator_get_credentials(_funct)
    else:
        return decorator_get_credentials
