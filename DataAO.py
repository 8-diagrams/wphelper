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
def setWpPwd(tg_id, website,username, pwd, memo):
    logger.info( f'[setWpPwd] BG {tg_id, }')
    sql = 'insert into wpsetting ( tg_id, website, username, pwd, wpname ) values (%s, %s, %s, %s, %s ) on duplicate key update username =%s, pwd = %s   '
    conn = dbmgr.Connector( dbpool ).get_conn()
    cur = conn.cursor()
    cur.execute( sql, [tg_id,  website, username, pwd, username, pwd, memo ])
    conn.commit()
    cur.close()
    return True 

@Utils.wpTry
def getWpSetting(tg_id ):
    logger.info( f'[getWpSetting] BG {tg_id, }')
    fields_str = 'tg_id, website, username, pwd, wpname'
    fields = fields_str2list(fields_str)
    sql = f'select {fields_str} from wpsetting where  tg_id = %s   '
    conn = dbmgr.Connector( dbpool ).get_conn()
    cur = conn.cursor()
    cur.execute( sql, [tg_id, ])
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
