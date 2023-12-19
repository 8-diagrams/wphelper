import mylog 
import dbmgr
logger = mylog.logger

dbpool = dbmgr.DBPool(12)
import Utils

@Utils.WLocker("admin")
@Utils.wpTry
def access(tg_id):
    conn = dbmgr.Connector( dbpool ).get_conn()
    cur = conn.cursor()
    cur.execute('select count(*) from admins ')
    row = cur.fetchone() 
    users_cnt = row[0]
    level = 0 if users_cnt > 0 else 99 
    ins_sql = 'insert into admins (tg_id, role) values (%s, %s) on duplicate key update access_time =  access_time+1  '
    cur.execute(ins_sql , [ tg_id  ,level] )
    conn.commit()
    cur.close()


    
class TGUSts:
    INIT ='INIT'
    WAIT_SET ='WAIT_SET'
    WAIT_ACTICLE = 'WAIT_ACTICLE'
    DRAFT_ACTICLE = 'DRAFT_ACTICLE'
    DRAFT_ACTICLE_EDIT_CAT = 'DRAFT_ACTICLE_EDIT_CAT'
    DRAFT_ACTICLE_EDIT_FACE = 'DRAFT_ACTICLE_EDIT_FACE'

@Utils.WLocker("status")
@Utils.wpTry
def setUserStatus(tg_id, status, params = '' ):
    logger.info(f'[setUserStatus] BG {tg_id, status, params}')
    sql = 'insert into userstatus ( tg_id, status, params ) values (%s, %s, %s) on duplicate key update status =%s, params = %s   '
    conn = dbmgr.Connector( dbpool ).get_conn()
    cur = conn.cursor()
    cur.execute( sql, [tg_id,  status, params, status, params])
    conn.commit()
    cur.close()


@Utils.wpTry
def getUserStatus(tg_id  ):
    logger.info(f'[getUserStatus] BG {tg_id, }')
    fields_str = 'status, params'
    fields = fields_str2list(fields_str)
    sql = f'select {fields_str} from userstatus where tg_id = %s   '
    conn = dbmgr.Connector( dbpool ).get_conn()
    cur = conn.cursor()
    cur.execute( sql, [tg_id, ])
    row = cur.fetchone( )
    resp = getVdict(row, fields)
    conn.commit()
    cur.close()
    return resp 


@Utils.wpTry
def setWpPwd(tg_id, website,username, pwd, wpname):
    logger.info( f'[setWpPwd] BG {tg_id, }')
    sql = 'insert into wpsetting ( tg_id, website, username, pwd, wpname ) values (%s, %s, %s, %s, %s ) on duplicate key update username =%s, pwd = %s , wpname = %s  '
    conn = dbmgr.Connector( dbpool ).get_conn()
    cur = conn.cursor()
    cur.execute( sql, [tg_id,  website, username, pwd, wpname, username, pwd, wpname ])
    conn.commit()
    cur.close()
    return True 

@Utils.wpTry
def getWpSetting(tg_id , sitename = None ):
    logger.info( f'[getWpSetting] BG {tg_id, }')
    fields_str = 'tg_id, website, username, pwd, wpname'
    fields = fields_str2list(fields_str)
    conn = dbmgr.Connector( dbpool ).get_conn()
    cur = conn.cursor()
    if not sitename :
        sql = f'select {fields_str} from wpsetting where  tg_id = %s   '
        cur.execute( sql, [tg_id, ])
    else:
        sql = f'select {fields_str} from wpsetting where  tg_id = %s and website = %s '
        cur.execute( sql, [tg_id, sitename ])
    rows = cur.fetchall()
    conn.commit()
    cur.close()
    li =[]
    for row in rows:
        resp = getVdict(row, fields )
        li.append(resp )
    return li  

def fields_str2list(s):
    li = []
    for item in s.split(','):
        item = item.strip()
        if not item:
            continue 
        li.append( item )
    return li 
        
def getVdict(row, fields):
    res_map = {}
    if not row:
        return res_map
    for idx , fieldname in enumerate(fields):
        res_map[ fieldname ] = row[idx]
    return res_map 

'''
	`tg_id` INT(11) NULL DEFAULT NULL,
	`sitename` VARCHAR(512) NULL DEFAULT NULL COLLATE 'utf8_general_ci',
	`title` VARCHAR(1024) NULL DEFAULT NULL COMMENT '主题' COLLATE 'utf8_general_ci',
	`content` LONGTEXT NULL DEFAULT NULL COLLATE 'utf8_general_ci',
	`face_img_url` VARCHAR(2048) NULL DEFAULT NULL COLLATE 'utf8_general_ci',
	`wp_post_id` CHAR(64) NULL DEFAULT NULL COMMENT 'wp的文章id' COLLATE 'utf8_general_ci',
	`wp_img_id` CHAR(64) NULL DEFAULT NULL COMMENT 'wp 的图片id' COLLATE 'utf8_general_ci',
	`post_tag` VARCHAR(512) NULL DEFAULT NULL COLLATE 'utf8_general_ci',
	`category` VARCHAR(512) NULL DEFAULT NULL COLLATE 'utf8_general_ci',
	`status`
'''

@Utils.wpTry
def saveArticle(tg_id, sitename, title, content,  face_img_url, post_tag = [], category=[] ):
    logger.info( f'[saveArticle] BG {tg_id, }')
    fields_str = 'tg_id, sitename, title, content,  face_img_url, post_tag, category'
    fields = fields_str2list(fields_str) 
    sql = f'insert into articles (  {fields_str}  ) values ( { ",".join( [ "%s" ] * len(fields) ) }  )    '
    conn = dbmgr.Connector( dbpool ).get_conn()
    cur = conn.cursor()
    logger.info(f"[saveArticle] ==> { sql, [tg_id, sitename, title, content,  face_img_url, ','.join(post_tag) , ','.join(category) ] }")
    cur.execute( sql, [tg_id, sitename, title, content,  face_img_url, ','.join(post_tag) , ','.join(category) ])
    myid = conn.insert_id()
    conn.commit()
    cur.close()
    return myid 

@Utils.wpTry
def getArticles(tg_id, sitename):
    logger.info( f'[getArticle] BG {tg_id, }')
    fields_str = 'tg_id, sitename, title, content,  face_img_url, post_tag, category, id, status, tg_msg_id, wp_img_id'
    fields = fields_str2list(fields_str) 
    sql = f'select  {fields_str}  from articles where tg_id = %s and sitename = %s  order by id desc  '
    conn = dbmgr.Connector( dbpool ).get_conn()
    cur = conn.cursor()
    cur.execute( sql, [ tg_id, sitename  ])
    li = []
    rows = cur.fetchall()
    for row in rows:
        resp = getVdict(row, fields)
        li.append( resp )
    conn.commit()
    cur.close()
    return li 

@Utils.wpTry
def findArticle(tg_id, myid):
    logger.info( f'[findArticles] BG {tg_id, }')
    fields_str = 'tg_id, sitename, title, content, face_img_url, post_tag, category, id, status, tg_msg_id, wp_img_id'
    fields = fields_str2list(fields_str) 
    sql = f'select  {fields_str}  from articles where tg_id = %s and id = %s  limit 1  '
    conn = dbmgr.Connector( dbpool ).get_conn()
    cur = conn.cursor()
    cur.execute( sql, [ tg_id, myid  ])
    row = cur.fetchone()
    resp = getVdict(row, fields)
    conn.commit()
    cur.close()
    return resp 


@Utils.wpTry
def updateArticle(tg_id, myid, upDict:dict):
    logger.info( f'[updateArticle] BG {tg_id, }')
    #fields_str = 'tg_id, sitename, title, content, face_img_url, post_tag, category, id, status'
    #fields = fields_str2list(fields_str) 
    fns = [ f'{ key }' + ' = %s ' for key in upDict.keys() ]
    sql = f'update articles set {",".join(fns) } where tg_id = %s and id = %s    '
    conn = dbmgr.Connector( dbpool ).get_conn()
    cur = conn.cursor()
    values = [ str(k) for k in  upDict.values() ]
    pvalues = [ tg_id, myid  ]
    values.extend( pvalues )
    logger.info(f"[updateArticle-sql] { sql, values }")
    cur.execute( sql, values )
    
    conn.commit()
    cur.close()
    return True  
