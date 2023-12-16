import mylog 
logger = mylog.logger
import db as mydb 

import SimpleLock

glock = SimpleLock.Lock('/tmp/simple_lock_ff')

class Connector:
    def __init__(self, pool) -> None:
        
        self.myid = pool.pick_id()
        self.conn = pool.get( self.myid )
        self.pool = pool 

    def __del__(self):
        self.pool.collect_id(self.myid)
    
    def get_conn(self):
        return self.conn 

class DBPool:
    def __init__(self, size) -> None:
        self.mysql_pool_size = size
        #item 0 conn, item 1 ~~ 0 not use / 1 used 
        self.list_conn = [] 
        self.init_mysql_pool()

    def init_mysql_pool (self):
        logger.info("[DBPool] size {self.mysql_pool_size}")
        for i in range(self.mysql_pool_size):
            conn_ins = mydb.getdbconn()
            self.list_conn.append(  [conn_ins, 0 ])
            logger.info(f"[init DBPool] {self.mysql_pool_size} {i} add {conn_ins}")
        logger.info(f"[init DBPool] {self.mysql_pool_size}")
    
    def pick_id(self):
        pick_id = -1
        try:
            lk = glock.try_lock(3)
            if lk == False :
                logger.info("[system-error] pick_id lock fail")
                pick_id = -1
            for i in range(self.mysql_pool_size):
                item = self.list_conn[i]
                if item[1] == 0:
                    item[1] = 1
                    pick_id = i 
                    logger.info(f"pick db idx {pick_id}")
                    break  
        except Exception as e:
            logger.info(f"pick db exception {e}")
            return False 
        finally:
            glock.unlock()

        
        return pick_id 
    
    def collect_id(self, myid):
        try:
            lk = glock.try_lock(3)
            if lk == False :
                logger.info("[system-error] collect lock fail")
                return False 
            item = self.list_conn[myid]
            item[1] = 0 
            logger.info(f"collect db idx {myid}")
            return True 
        except Exception as e:
            logger.info(f"pick db exception {e}")
            return False 
        finally:
            glock.unlock()

    def get(self, myid): 
         
        try:
            self.list_conn[myid][0].ping(reconnect=True)
            return self.list_conn[myid][0] 
        except:
            import traceback
            logger.info(f"mysql reconnet for exception {traceback.format_exc()}")
            self.list_conn[myid][0] =  mydb.getdbconn()
            return self.list_conn[myid][0] 


