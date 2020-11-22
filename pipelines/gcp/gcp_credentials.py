'''
Date: 2020-11-14
Author: Vitali Lupusor

Description: Operations on getting the credentials to a Google Cloud 
        Platform project.
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
    '''Get the credentials to a Google Cloud Project (GCP).
    You can explicitly provide the path an Fernet encrypted credentials file or 
    you can use your own GCP instance. In case of the former, you will need to 
    also provide the name of your project.

    Arguments:
        _funct (function, NoneType): If the decorator is called without any arguments, 
                pass the decorate function down the process. Alternatively, pass down 
                the line its arguments.

        projtect (str): The name of the GCP project. Defaults to the value given in 
                the `.config.py` file.

        credentials_path (str): The path to Fernet encrypted credentials. Defaults 
                to the value given in the `.config.py` file.

    return (function): The decoration function.
    '''
    # Import external modules
    _functools = __import__('functools', fromlist=['wraps'])
    wraps = _functools.wraps

    def decorator_get_credentials(function):
        '''The decorator function.
        Passes the decorated function down the line.

        Arguments:
            function (function): The function is being decorated.

        return (function): The wrapper function.
        '''
        @wraps(function)
        def wrapper_get_credentials(*args, **kwargs):
            '''Wrapper function.
            Here the main activity takes place.

            Arguments:
                *args (list): Positional arguments for the decorated function.
                **kwargs (dict): Key-value arguments for the decorated function.

            return (google.cloud.${service}.Client): Returns an authenticated 
                    client for the requested service.
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
