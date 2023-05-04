from datetime import datetime
import pytz
import numpy as np
import random

def get_hour():
    """
    Returns the current hour in the timezone 'America/New_York' as an integer value.

    Returns:
        hour (int): The current hour in 'America/New_York'.
    """
    timezone = pytz.timezone('America/New_York')
    now  = datetime.now(timezone)
    hour = now.hour
    return int(hour)

def get_state():
    """
    Determines the current time of day (in the America/New_York timezone)
    and returns a state identifier based on which time "bucket" the current
    hour falls into. The state identifier is a string ranging from '0' to '7',
    where '0' represents the hours between midnight and 3am, '1' represents
    the hours between 3am and 6am, and so on. 

    Returns:
    - state (str): A string representing the current time bucket.
    """
    hour = get_hour()
    if hour < 3:
        return '0'
    elif hour < 6:
        return '1'
    elif hour < 9:
        return '2'
    elif hour < 12:
        return '3'
    elif hour < 15:
        return '4'
    elif hour < 18:
        return '5'
    elif hour < 21:
        return '6'
    else:
        return '7'
