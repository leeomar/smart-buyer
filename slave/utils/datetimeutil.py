#/bin/python
# coding: utf8
import datetime
import time

DEFAULT_DATETIME_FORMAT = "%Y-%m-%d %H:%M:%S"
def get_struct_time(mytime):
    if isinstance(mytime, time.struct_time):
        return mytime
    elif isinstance(mytime, str):
        return time.strptime(mytime, DEFAULT_DATETIME_FORMAT)
    elif isinstance(mytime, datetime.datetime):
        return mytime.timetuple()
    elif isinstance(mytime, (int, long, float)):
        return time.localtime(mytime)
    else:
        raise Exception("unkown time, type:%s, %s" % (type(mytime), mytime))

#time.struct_time(tm_year=2012, tm_mon=5, tm_mday=7, tm_hour=8, tm_min=9,
#tm_sec=38, tm_wday=0, tm_yday=128, tm_isdst=0)
#TODO:
def same_datetime(time1, time2, cmp_year=True, cmp_month=True, cmp_day=True,
    cmp_hour=True, cmp_min=True, cmp_second=True):
    st1 = get_struct_time(time1)
    st2 = get_struct_time(time2)
    
    same_year = st1.tm_year == st2.tm_year if cmp_year else True
    same_month = st1.tm_mon == st2.tm_mo if cmp_month else True
    same_day = st1.tm_mday == st2.tm_mday if cmp_day else True
    pass

def is_same_day(time1, time2):
    st1 = get_struct_time(time1)
    st2 = get_struct_time(time2)
    
    return st1.tm_year == st2.tm_year and \
        st1.tm_mon == st2.tm_mon and \
        st1.tm_mday == st2.tm_mday

if __name__ == '__main__':
    print get_struct_time(time.time())
    print get_struct_time(int(time.time()))
    print get_struct_time(datetime.datetime.now())
    print get_struct_time("2012-05-07 08:00:00")

    t1 = time.time()
    t2 = datetime.datetime.now()
    print is_same_day(t1, t2)

    t3 = "2012-05-06 08:00:00"
    print is_same_day(t1, t3)
