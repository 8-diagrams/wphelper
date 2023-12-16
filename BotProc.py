import telepot
from telepot.loop import MessageLoop
from telepot.namedtuple import ReplyKeyboardMarkup
import db as mydb 
import Utils
import mylog 
logger = mylog.logger


def on_chat_message(bot : telepot.Bot, msg :dict ):
    logger.info(f"[on_chat_message] handle msg {msg}")
    
    return 

def on_callback_query(bot : telepot.Bot, msg :dict ):
    logger.info(f"[on_callback_query] handle msg {msg}")
    return 
