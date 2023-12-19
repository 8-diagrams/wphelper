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
    if msg.get('data') :
        procCallback( bot, msg )
    return 
@Utils.wpTry
def procCallback(bot : telepot.Bot, msg :dict ):
    from_id = msg['from']['id']
    data = str( msg.get('data') )
    if data.startswith('push_'):
        sitename =  data[len('push_') : ]
        sitesItem = DataAO.getWpSetting(from_id, sitename) 
        myname = sitename 
        if sitesItem:
            myname = sitesItem[0].get('wpname')
        DataAO.setUserStatus( from_id, DataAO.TGUSts.WAIT_ACTICLE, sitename )
        bot.sendMessage(from_id, f"请回复消息，发文给 {myname} ")
    elif data.startswith('oper_pub_'):
        myid =  data[len('oper_pub_') : ]
        resp = DataAO.findArticle(from_id, myid )
        if not resp:
            logger.info(f"[oper_pub_] not found article {myid}")
            bot.sendMessage(from_id, '文章不存在啊')
            return 
        if resp.get('status') != 'INIT':
            logger.info(f"[oper_pub_] not found article {myid}")
            bot.sendMessage(from_id, '文章已发布')
            return 
        import WpUtils
        sett = DataAO.getWpSetting( from_id, resp.get('sitename') )
        logger.info(f"[oper_pub_]  acticle status {resp.get('status') } {  resp.get('title') } ")
        if resp.get('status') != 'INIT':
            logger.info(f"[oper_pub_] not found valid article {myid}")
            bot.sendMessage(from_id, '文章已经发布/取消。')
            return 
        wpOp = WpUtils.WPHelper( sett[0].get('website'), sett[0].get('username'), sett[0].get('pwd') )
        post_tag = []
        category = []
        if resp.get('category'):
            category = resp.get('category').split(",")
        logger.info(f"[oper_pub_] {from_id} begin post {sett[0].get('website')} => {resp.get('title')}")
        wpid = wpOp.post( resp.get('title'), resp.get('content') , category=category, post_tag=post_tag  )
        DataAO.updateArticle(from_id, myid, { 'id': myid, "tg_id":from_id, "wp_post_id": wpid, "status":"OK" })
        DataAO.setUserStatus(from_id, DataAO.TGUSts.INIT)
        bot.sendMessage(from_id, "文章发布成功")

    elif data.startswith('oper_cat_'):
        myid =  data[len('oper_cat_') : ]
        resp = DataAO.findArticle(from_id, myid )
        if not resp:
            logger.info(f"[oper_cat_] {from_id} not found article {myid}")
            bot.sendMessage(from_id, '文章不存在啊')
            return 
        if resp.get('status') != 'INIT':
            logger.info(f"[oper_cat_] {from_id}  not found article {myid}")
            bot.sendMessage(from_id, '文章已发布/取消。')
            return 
         
        logger.info(f"[oper_cat_] {from_id}   acticle status {resp.get('status') } {  resp.get('title') } ")
        DataAO.setUserStatus(from_id, DataAO.TGUSts.DRAFT_ACTICLE_EDIT_CAT, myid)
        bot.sendMessage(from_id,"请回复文章类型 用 ，隔开")

    elif data.startswith('oper_cancel_'):
        myid =  data[len('oper_cancel_') : ]
        resp = DataAO.findArticle(from_id, myid )
        if not resp:
            logger.info(f"[oper_cancel_] {from_id} not found article {myid}")
            bot.sendMessage(from_id, '文章不存在啊')
            return 
        if resp.get('status') != 'INIT':
            logger.info(f"[oper_cancel_] {from_id}  not found article {myid}")
            bot.sendMessage(from_id, '文章已发布/取消。')
            return 
         
        logger.info(f"[oper_cancel_] {from_id}   acticle status {resp.get('status') } {  resp.get('title') } ")
        DataAO.updateArticle(from_id, myid, {'status':'CANCEL'} )
        DataAO.setUserStatus(from_id, DataAO.TGUSts.INIT )
        bot.sendMessage(from_id, '文章已设置取消')
        


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
    
    elif text == '/pub':
        return showPublish(bot, from_id )
    else :
        user_status = DataAO.getUserStatus( from_id ).get('status')
        logger.info(f"[on_chat_message_private]  to default handler userstatus : [{user_status}]")
        #
        if DataAO.getUserStatus( from_id ).get('status') == DataAO.TGUSts.WAIT_SET :
            return handleSetting(bot, from_id, text,  msg )
        elif DataAO.getUserStatus( from_id ).get('status') == DataAO.TGUSts.WAIT_ACTICLE :
            logger.info(f"[on_chat_message_private] content size:{len(text)} ")
            saveContent(bot, from_id, text )
            return 
        elif DataAO.getUserStatus( from_id ).get('status') == DataAO.TGUSts.DRAFT_ACTICLE_EDIT_CAT  :
            logger.info(f"[on_chat_message_private] cat size:{len(text)} ")
            saveContent_cat(bot, from_id, text )
            return 
        else:
            logger.info(f"[on_chat_message_private]  to default handler no proc")

        

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
            DataAO.setUserStatus(from_id, DataAO.TGUSts.INIT)
    except Exception as e:
        import traceback
        logger.info(f"[handleSetting] exception {traceback.format_exc()}")
        bot.sendMessage( from_id, "添加网址失败")
        bot.sendMessage(from_id, text = '需要：  网址 用户名 密码 备注(可选)')
        return False 

def sendOperPanel(bot, from_id,  title, myid ):
    myid = str(myid)
    inline_keyboard = []
    button = InlineKeyboardButton(text='发布', callback_data=f'oper_pub_{myid}')
    inline_keyboard.append( button )
    button = InlineKeyboardButton(text='设置封面', callback_data=f'oper_face_{myid}')
    inline_keyboard.append( button )
    button = InlineKeyboardButton(text='设置分类', callback_data=f'oper_cat_{myid}')
    inline_keyboard.append( button )
    button = InlineKeyboardButton(text='放弃', callback_data=f'oper_cancel_{myid}')
    inline_keyboard.append( button )
    markup = InlineKeyboardMarkup( inline_keyboard=[inline_keyboard] )
    bot.sendMessage( from_id, f"编辑文章： {title}", reply_markup=markup)
    

def saveContent(bot: telepot.Bot , from_id, text:str):
    statusSet = DataAO.getUserStatus(from_id)
    sitename = statusSet.get('params')
    lines = text.split("\n")
    line_push = []
    for line in lines:
        line=line.strip()
        if line:
            line_push.append(line )
    title = line_push[0]
    content = "\n".join( line_push[1:])
    myid = DataAO.saveArticle(from_id, sitename, title, content, '' , [] , [] )
    DataAO.setUserStatus( from_id, DataAO.TGUSts.DRAFT_ACTICLE, str(myid) ) 
    sendOperPanel(bot, from_id, title, myid )
    return True 

@Utils.wpTry
def saveContent_cat(bot: telepot.Bot , from_id, text:str):
    statusSet = DataAO.getUserStatus(from_id)
    artcleId = statusSet.get('params')
    text = text.replace("，", ',')
    cats = text.split(",")
    if len(cats) == 1:
        cats = text.split("，")
    cats_str = ','.join(cats)
    DataAO.updateArticle(from_id, artcleId, {'category': cats_str })
    DataAO.setUserStatus( from_id, DataAO.TGUSts.DRAFT_ACTICLE, str(artcleId) ) 
    bot.sendMessage(from_id, "文章类型更新成功")
    return True 


def showPublish(bot: telepot.Bot, from_id ):
    
    li = DataAO.getWpSetting( from_id )
    if not li :
        bot.sendMessage( from_id, "请先添加wordpress站点")
        DataAO.setUserStatus(from_id,  DataAO.TGUSts.INIT)
        return
    inline_keyboard = [] 
    for site in li:
        website = site.get('website')
        button = InlineKeyboardButton(text=site.get('wpname'), callback_data=f'push_{website}')
        inline_keyboard.append( button )
    markup = InlineKeyboardMarkup( inline_keyboard=[inline_keyboard] )
    bot.sendMessage( from_id, "请选择需要发送的网站", reply_markup=markup)
    return 
