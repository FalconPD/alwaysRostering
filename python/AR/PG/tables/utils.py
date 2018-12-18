import xlrd
import datetime

def to_datetime(cell, datemode):
    """
    Returns a python datetime given an xlrd cell. Needs datemode from the sheet
    for conversion
    """
    if cell.value == '':
        return None
    return datetime.datetime(*xlrd.xldate_as_tuple(cell.value, datemode))
