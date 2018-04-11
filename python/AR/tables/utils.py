from datetime import datetime, date

def genesis_to_date(genesis_str):
    if genesis_str == '':
        return None
    else:
        return datetime.strptime(genesis_str, '%m/%d/%Y').date()

def genesis_to_datetime(genesis_str):
    """Tries to get a date and time from a Genesis report string.

    If it can't get a date and time it returns just the date, failing
    that it returns None. This is because if an entry occurs at exactly
    midnight, the time portion of the date time is not printed on the report.
    """
    date = None
    for date_format in ['%m/%d/%y %I:%M%p', '%m/%d/%Y']:
        try:
            date = datetime.strptime(genesis_str, date_format)
            break
        except ValueError:
            pass
    return date

def genesis_to_boolean(genesis_str):
    if genesis_str == 'Y':
        return True
    else:
        return False
