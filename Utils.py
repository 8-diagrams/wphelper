def getBotKey(  ):
    try:
        from configparser import ConfigParser
        config = ConfigParser()
        config.read("./env.conf", encoding='UTF-8')
        key_data = config.get("general","bot_key")
        return key_data
    except Exception as e:
        return ''
    
import RedisLock
import mylog 
logger = mylog.logger

def WLocker(lockkey):

    def decorater(func):
        def wrapper(*args, **kargs):
            lockname = lockkey
            lock_args = lockname
            redis_conn = RedisLock.connect_redis()
            lock_id = RedisLock.acquire_lock(redis_conn, lockname, lock_args)
            if not lock_id:
                logger.info(f"[Locker] lock {lockkey} fail.")
                return False
            try:
                logger.info(f"[Locker] lock {lockkey} get OK.")
                return func(*args, **kargs) 
            except Exception as e:
                import traceback
                logger.info(f"[Locker] lock {lockkey} exception {traceback.format_exc()}")
                return False
            finally:
                logger.info(f"[Locker] lock {lockkey} release OK.")
                RedisLock.release_lock(redis_conn, lockname, lock_id)
                redis_conn.close()
        return wrapper
    
    return decorater


def wpTry(func):
    def warpper(*args, **kwargs):
        print(f"[warpper] try log {args}")
        try:
            return func(*args, **kwargs)
        except Exception as e :
            import traceback
            logger.info(f'xpTry {traceback.format_exc()} ')
            raise e 
    return warpper

