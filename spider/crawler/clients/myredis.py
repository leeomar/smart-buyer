"""
base on redis-py
"""
import redis
class MyRedisClient(redis.Redis):
    
    def __init__(self, host, port, expire_time, db=0):
        super(MyRedisClient, self).__init__(host, port, db)
        self.db = int(db)
        self.host = host
        self.port = int(port)
        self.default_expire = int(expire_time) 

    @classmethod
    def from_settings(cls, settings):
        host = settings.get('host')
        port = settings.get('port')
        db = settings.get('db', 0)
        default_expire= settings.get('default_expire')
        return cls(host, port, default_expire, db)
        
    def __str__(self):
        return "MyRedisClient connect to [%s:%s], db:%s, default expire:%s"%\
            (self.host, self.port, self.db, self.default_expire)
    
    def close(self):
        try:
            self.flushdb()
            self.connection_pool.disconnect()
        except:
            pass
        finally:
            self.client = None

    def expire(self, key, time=None):
        super(MyRedisClient, self).expire(key, time if time else
            self.default_expire)
