"""Validate date values.

Date: 2020-11-14
Author: Vitali Lupusor
"""

# Import standard modules
from typing import Optional, Union
from datetime import datetime


def validate_date(
    date: Optional[Union[str, datetime]] = None
) -> datetime:
    """Validate the provided values as a date value.

    Arguments:
        date (datetime.datetime, NoneType, str):
                The value that should be validated. If none provided,
                will return today's date with time set to midnight.

    return (datetime.datetime):
        datetime object from the provided value.
    """
    # Import standard modules
    _re = __import__('re', fromlist=['search'])
    search = _re.search

    if not date:
        _date = datetime.today()
    elif isinstance(date, datetime):
        _date = date
    elif isinstance(date, str):
        separator_0, separator_1 = search(
            r'^\d+(.?)\d{2}(.?)\d+', date
        ).groups()
        if separator_0 != separator_1:
            message = f'Invalid date format for value {date}'
            raise ValueError(message)
        else:
            try:
                _date = datetime.strptime(
                    date,
                    f'%Y{separator_0}%m{separator_0}%d'
                )
            except ValueError:
                _date = datetime.strptime(
                    date,
                    f'%d{separator_0}%m{separator_0}%Y'
                )

    return datetime.combine(_date.date(), _date.time().min)
