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
