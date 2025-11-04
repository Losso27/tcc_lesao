from datetime import datetime
from dateutil.relativedelta import relativedelta
import re


def convert_string_to_boolean(string):
    if string == "sim" or string == "yes":
        return True
    else:
        return False
    
def convert_string_to_date(string):
    return datetime.strptime(string, "%b %d, %Y %I:%M %p")

def convert_date_to_age(date):
    now = datetime.now()
    return relativedelta(now, date).years

def convert_string_to_float(string):
    if re.match('[a-zA-Z]', string):
        return None
    string = string.replace(".","").replace(",",".")
    return float(string)