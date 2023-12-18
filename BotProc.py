import telepot
from telepot.loop import MessageLoop

from telepot.namedtuple import ReplyKeyboardMarkup,InlineKeyboardButton,InlineKeyboardMarkup
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
    text = msg.get('text')
    if not text :
        logger.info(f'[on_chat_message_private] no hanble msg {msg}') 
        return 
    text = text.strip()
    logger.info(f"[on_chat_message_private] got text [{text}]")
    if text == '/start':
        try:
            saveSt =  DataAO.setUserStatus( from_id, DataAO.TGUSts.INIT)
        except Exception as e:
            import traceback
            logger.info(f"[on_chat_message_private] exception {traceback.format_exc()}")
        return 
    
    elif text == '/set':
        DataAO.setUserStatus( from_id, DataAO.TGUSts.WAIT_SET )
        return 
    elif text == '/getstatus':
        st = DataAO.getUserStatus( from_id  )
        bot.sendMessage(from_id, text = f'{st}')
        return 
    elif text.startswith('push_'):
        raw = text[len('push_')]
        bot.sendMessage(from_id, f'选择了网站[{raw}]')
    else :
        if DataAO.getUserStatus( from_id ).get('status') == DataAO.TGUSts.WAIT_SET :
            return handleSetting(bot, from_id, text,  msg )
        

    return 

def handleSetting(bot: telepot.Bot, from_id, text,  msg :dict  ):
    logger.info(f'[handleSetting] {from_id} => {text} ')
    bot.sendMessage(from_id, '收到设置信息')
    items = text.split()
    if len(items) < 3:
        bot.sendMessage(from_id, text = '需要：  网址 用户名 密码 备注(可选)')
        return 
    web = items[0]
    username = items[1]
    pwd = items[2]
    if len(items) > 3 :
        memo = items[3]
    else:
        memo = web
    try:
        ret = DataAO.setWpPwd(from_id, web, username, pwd, memo )
        if ret :
            bot.sendMessage( from_id, "添加网址成功")
            DataAO.setUserStatus( DataAO.TGUSts.INIT)
    except Exception as e:
        import traceback
        logger.info(f"[handleSetting] exception {traceback.format_exc()}")
        bot.sendMessage( from_id, "添加网址失败")
        bot.sendMessage(from_id, text = '需要：  网址 用户名 密码 备注(可选)')
        return False 



def showPublish(bot: telepot.Bot, from_id ):
    
    li = DataAO.getWpSetting( from_id )
    if not li :
        bot.sendMessage( from_id, "请先添加wordpress站点")
        DataAO.setUserStatus( DataAO.TGUSts.INIT)
        return
    inline_keyboard = [] 
    for site in li:
        website = site.get('website')
        button = InlineKeyboardButton(text=site.get('wpname'), callback_data=f'push_{website}')
        inline_keyboard.append( button )
    markup = InlineKeyboardMarkup( inline_keyboard=[inline_keyboard] )
    bot.sendMessage( from_id, "请选择需要发送的网站", reply_markup=markup)
    return 
