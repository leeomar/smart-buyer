"""
wrapper base on redis-py client code
"""
import redis
class RedisClient(object):
    
    def __init__(self, host, port, default_expire_time, db=0):
        self.db = db
        self.host = host
        self.port = port
        self.default_expire_time = default_expire_time 
        self.client = None
        
    def __str__(self):
        return 'redis client, connect to [%s:%s], db:%s, expire:%s' %\
            (self.host, self.port, self.db, self.default_expire_time)
    
    def close(self):
        if self.client:
            self.client.flushdb()
            self.client.connection_pool.disconnect()
        self.client = None

    def open(self):
        self.close()    
        self.client = redis.Redis(host=self.host, 
            port=self.port, db=self.db)
        #log.msg("redis connect to %s:%s, db:%s" \
        #        % (self.host, self.port, db), level=log.DEBUG) 
    
    def ttl(self, key):
        return self.client.ttl(key)
        
    def dbsize(self):
        self.client.dbsize()
        
    def flushdb(self):
        self.client.flushdb()

    def expire(self, key, expire_time=None):
        #-1: never expire
        if expire_time is None:
            expire_time = self.default_expire_time

        if expire_time > 0:
            self.client.expire(key, expire_time)

    def put(self, key, value, expire_time=None, update_expire_time=True):
        if isinstance(value, dict):
            self.client.hmset(key, value)
        else:
            self.client.set(key, value)

        if update_expire_time: 
            self.expire(key, expire_time)

    def get(self, key, expire_time=None, update_expire_time=False):
        if update_expire_time:
            self.expire(key, expire_time)
        return self.client.get(key)
    
    def exists(self, key):
        return self.client.exists(key)

    #following is dictionary data manipulate interface
    def hgetall(self, key, expire_time=None, update_expire_time=False):
        if update_expire_time:
            self.expire(key, expire_time)
        return self.client.hgetall(key)
    
    def hget(self, key, field, expire_time=None, update_expire_time=False):
        if update_expire_time:
            self.expire(key, expire_time)
        return self.client.hget(key, field)
    
    def hset(self, key, field, value, expire_time=None, update_expire_time=True):
        self.client.hset(key, field, value)
        if update_expire_time:
            self.expire(key, expire_time)

    def hdel(self, key, **fields):
        pipeline = self.client.pipeline()
        for i in range(0, len(fields)):
            pipeline.hdel(key, fields[i])
        return pipeline.execute()

    def delete(self, *keys):
        if not keys:
            return

        for i in range(0, len(keys)):
            self.client.delete(keys[i])
