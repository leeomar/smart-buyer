#/bin/python
# coding: utf8
import datetime
import time as pytime

def today(_format='%Y%m%d'):
    dt = datetime.date.today()
    return dt.strftime(_format)

def yesterday(_format='%Y%m%d'):
    dt = datetime.date.today() + datetime.timedelta(-1)
    return dt.strftime(_format)

def now(_format='%Y%m%d %H:%M:%S'):
    return datetime.datetime.now().strftime(_format)

DEFAULT_DATETIME_FORMAT = "%Y-%m-%d %H:%M:%S"
def get_struct_time(mytime):
    if isinstance(mytime, pytime.struct_time):
        return mytime
    elif isinstance(mytime, str):
        return pytime.strptime(mytime, DEFAULT_DATETIME_FORMAT)
    elif isinstance(mytime, datetime.datetime):
        return mytime.timetuple()
    elif isinstance(mytime, (int, long, float)):
        return pytime.localtime(mytime)
    else:
        raise Exception("unkown time, type:%s, %s" % (type(mytime), mytime))

def is_same_day(time1, time2):
    st1 = get_struct_time(time1)
    st2 = get_struct_time(time2)
    
    return st1.tm_year == st2.tm_year and \
        st1.tm_mon == st2.tm_mon and \
        st1.tm_mday == st2.tm_mday

if __name__ == '__main__':
    print get_struct_time(pytime.time())
    print get_struct_time(int(pytime.time()))
    print get_struct_time(datetime.datetime.now())
    print get_struct_time("2012-05-07 08:00:00")

    t1 = pytime.time()
    t2 = datetime.datetime.now()
    print is_same_day(t1, t2)

    t3 = "2012-05-06 08:00:00"
    print is_same_day(t1, t3)
