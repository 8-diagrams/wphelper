import telepot
import fastapi
from fastapi import Response, Request
from fastapi import  Cookie , Form
from pydantic import BaseModel
import decimal

from typing import Optional
import time
from telepot.loop import MessageLoop
from telepot.namedtuple import ReplyKeyboardMarkup
import RedisLock
import db as mydb 
import Utils
import mylog 
logger = mylog.logger


#key for bot
gKey="5379225836:xxxxx"
gBot = None
gKey = Utils.getBotKey()



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

def checkKey(sx):
    try:
        redis_conn = RedisLock.connect_redis()
        udata = redis_conn.get("Admin_Limit")
        if udata:
            udata = udata.decode('utf8')
        else:
            logger.info("checkKey: Not key")
            return False 
        if udata != sx:
            return False 
        return True 
        
    except Exception as e:
        logger.info(f"checkKey error {e}")
        return False
        pass 
    finally:
        if redis_conn:
            redis_conn.close()


def setKey(sx):
    try:
        redis_conn = RedisLock.connect_redis()
        redis_conn.set("Admin_Limit", sx )
        redis_conn.expire("Admin_Limit", 120 * 60)
        return True 
    except Exception as e:
        return False
        pass 
    finally:
        if redis_conn:
            redis_conn.close()

def on_chat_message(msg):
    logger.info ( str(msg) )
    content_type, chat_type, chat_id = telepot.glance(msg)
    gBot.sendMessage(chat_id, text="我收到了:" + str( msg['text']) )
    str_chat_id = str(chat_id)
    if msg['text'] == '1243' :
        import uuid 
        sx = uuid.uuid4().hex
        url = '联系管理员'
        gBot.sendMessage(chat_id, text= url )
        return url 


from pydantic import BaseModel
class CookiesRequestItem(BaseModel):
    url: str
    data: str 
    cmd : str 

import telepot
app = fastapi.FastAPI()


async def catch_exceptions_middleware(request: Request, call_next):
    try:
        return await call_next(request)
    except Exception:
        # you probably want some kind of logging here
        import traceback
        logger.info ( f"CAO! {traceback.format_exc()}" )
        return Response("Internal server error SMSM", status_code=500)

app.middleware('http')(catch_exceptions_middleware)


@app.get("/")
def index():
    logger.info("Some one call.")
    return {"msg":"OK"}

    

### start bot 
def on_handle_message(msg:dict):
    import BotProc
    return BotProc.on_chat_message( gBot, msg )

def on_callback_query(msg:dict):
    import BotProc
    return BotProc.on_callback_query( gBot, msg )



gBot = telepot.Bot( gKey )
MessageLoop(gBot, {'chat': on_handle_message,
                  'callback_query': on_callback_query} ).run_as_thread()
