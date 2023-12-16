import redis
import uuid
import time
import os
from configparser import ConfigParser

def connect_redis2():
    RDfile = "./redis-name.conf"
    if os.path.exists(RDfile):
        with open(RDfile) as f:
            hostname = f.read()
            hostname = hostname.strip()
            return redis.Redis(hostname, port=6379)
    return redis.Redis(host='127.0.0.1', port=6379)

redisHostName = '127.0.0.1'

def connect_redis():
    gConfig = ConfigParser()
    gConfig.read("./env.conf", encoding='UTF-8')
    global redisHostName
    redisHostName = gConfig.get("redis","hostname")
    hostname = redisHostName #'redis_server'
    return redis.Redis(hostname, port=6379)

def acquire_lock(conn: redis.Redis, lockname, args, acquite_timeout=30):
    identifier = str(uuid.uuid4())
    end = time.time() + acquite_timeout
    while time.time() < end:
        # try to get lock
        if conn.setnx('lock:' + lockname, identifier): 
            # output the proc args
            #print('Get Lock for: '+ str(args))
            conn.expire( 'lock:' + lockname , 60 )
            return identifier
    return False

def release_lock(conn, lockname, identifier):
    pipe = conn.pipeline(True)
    lockname = 'lock:' + lockname
    while True:
        try:
            pipe.watch(lockname)
            identifier_real = pipe.get(lockname).decode()
            if identifier_real == identifier:
                pipe.multi()
                pipe.delete(lockname)
                pipe.execute()
                return True;
            pipe.unwatch()
            break
        except redis.exceptions.WatchError:
            pass
    return False
