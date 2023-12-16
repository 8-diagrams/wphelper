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
    ins_sql = 'insert into admin (tg_id, role) values (%s, %s) on update key update access_time =  access_time+1  '
    cur.execute(ins_sql , [ tg_id  ,level] )
    conn.commit()
    cur.close()


    