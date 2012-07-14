import time
import datetime

def datatime2seconds(dtime):
    if isinstance(dtime, datetime.datetime):
        return int(time.mktime(dtime.timetuple()))
    else:
        raise Exception('expect datetime, got %s' % type(dtime))
