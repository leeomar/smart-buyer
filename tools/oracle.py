#/bin/python
# -*- coding: utf-8 -*-
import cx_Oracle
import time
import traceback

class OracleClient:
    
    def __init__(self, user, pwd, host, port, 
        sid=None, sname=None, retrys=3):
        self.user = user
        self.pwd = pwd
        self.host = host 
        self.port = port
        self.sid = sid 
        self.sname=sname
        self.dns = self.makedsn()
        self.retrys = 3
        self.conn = None

    def __str__(self):
        return "oracle client, connect to[%s:%s], sid:%s, sname:%s"\
            %(self.host, self.port, self.sid, self.sname)

    def makedsn(self):
        #dsn_tns = cx_Oracle.makedsn(host, port, SID)
        #(DESCRIPTION=(ADDRESS_LIST=(ADDRESS=(PROTOCOL=TCP)(HOST=%s)(PORT=%s)))(CONNECT_DATA=(SID=odb)))
        base_conn_string = \
            "DESCRIPTION=(ADDRESS_LIST=(ADDRESS=(PROTOCOL=TCP)(HOST=%s)(PORT=%s)))"\
            % (self.host, self.port)

        if self.sid:
            return "(%s(CONNECT_DATA=(SID=%s)))" % (base_conn_string, self.sid)
        elif self.sname:
            return "(%s(CONNECT_DATA=(SERVICE_NAME=%s)))" \
                % (base_conn_string, self.sname)
        else:
            raise Exception("sid and sname cannot be both None")

    def close(self):
        if self.conn:
            self.conn.close()
            self.conn = None

    def open(self):
        self.close()
        self.conn = cx_Oracle.connect(self.user, self.pwd, self.dns)

    def __execute(self, func, *args, **kw):
        for i in range(0, self.retrys):
            try:
                return func(*args, **kw)
            except Exception, e:
                if i == self.retrys - 1:
                    raise e
                else:
                    time.sleep(10*i)
                    continue

    def __execute_sql(self, sql):
        cursor = self.conn.cursor()
        cursor.execute(sql)
        return cursor 

    def select(self, sql):
        return self.__execute(self.__execute_sql, sql)

if __name__=="__main__":
    user = "db40"
    pwd = "db40"
    host = '172.20.23.104'
    port = '1521'
    sid = 'odb'
    db = OracleClient(user, pwd, host, port, sid)
    db.open()

    cursor = db.select("select F157V_STK239,  F042D_STK239  from stk239 where rownum < 10")
    for row in cursor.fetchall():
        print row[0], "%s" % int(time.mktime(row[1].timetuple()) * 1000)

    db.close()
