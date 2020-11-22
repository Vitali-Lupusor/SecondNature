'''
Date: 2020-11-14
Author: Vitali Lupusor

Description: Date values validation.
'''

def validate_date(date=None):
    '''Validates the provided values as a date value.

    Arguments:
        date (datetime.date, datetime.dateime, NoneType, str): 
                The value that should be validated. If none provided,
                will return today's date with time set to midnight.

    return (datetime.datetime): datetime object from the provided value.
    '''
    # Import external modules
    _datetime = __import__('datetime', fromlist=['datetime'])
    datetime = _datetime.datetime
    _re = __import__('re', fromlist=['search'])
    search = _re.search

    if not date:
        date = datetime.today()
    elif isinstance(date, datetime):
        pass
    elif isinstance(date, str):
        separator_0, separator_1 = search(
            r'^\d+(.?)\d{2}(.?)\d+', date
        ).groups()
        if separator_0 != separator_1:
            message = f'Invalid date format for value {date}'
            raise ValueError(message)
        else:
            try:
                date = datetime.strptime(
                    date,
                    f'%Y{separator_0}%m{separator_0}%d'
                )
            except ValueError:
                date = datetime.strptime(
                    date,
                    f'%d{separator_0}%m{separator_0}%Y'
                )

    return datetime.combine(date.date(), date.time().min)
