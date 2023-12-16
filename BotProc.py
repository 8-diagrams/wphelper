import telepot
from telepot.loop import MessageLoop
from telepot.namedtuple import ReplyKeyboardMarkup
import db as mydb 
import Utils
import mylog 
import dbmgr
import DataAO
 
logger = mylog.logger

dbpool = dbmgr.DBPool(12)

def on_chat_message(bot : telepot.Bot, msg :dict ):
    logger.info(f"[on_chat_message] handle msg {msg}")
    if msg.get('chat').get('type') == 'private':
        return on_chat_message_private( bot, msg )
    return 

def on_callback_query(bot : telepot.Bot, msg :dict ):
    logger.info(f"[on_callback_query] handle msg {msg}")
    return 


def on_chat_message_private(bot : telepot.Bot, msg :dict ):
    logger.info(f"[on_chat_message_private] handle msg {msg}")
    from_id = msg['chat']['id']
    DataAO.access( from_id  )
    text = msg['chat'].get('text')
    if not text :
        logger.info(f'[on_chat_message_private] no hanble msg {msg}') 
        return 
    text = text.strip()

    if text == '/start':
        DataAO.setUserStatus( from_id, DataAO.TGUSts.INIT)
    return 