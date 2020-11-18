'''
Date: 2020-11-14
Author: Vitali Lupusor

Description: TODO
'''

def validate_date(date=None):
    '''TODO

    Arguments:
        date (): TODO

    return (): TODO
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
