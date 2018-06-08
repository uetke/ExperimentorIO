from django import template
import datetime
register = template.Library()


def print_timestamp(timestamp):
    try:
        #assume, that timestamp is given in seconds with decimal point
        ts = float(timestamp/1000)
    except ValueError:
        return None
    return datetime.datetime.fromtimestamp(ts)


register.filter('make_date', print_timestamp)