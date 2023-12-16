import fcntl


class Lock(object):
    def __init__(self, file_name):
        self.file_name = file_name
        self.handle = open(file_name, 'w+')

    def lock(self):
        
        fcntl.flock(self.handle, fcntl.LOCK_EX | fcntl.LOCK_NB)

    def try_lock(self, sec):
        times = int(sec / 0.01)
        if times == 0:
            times = 1
        import time
        for i in range(times):
            #print( f"{i}, {times}")
            try: 
                self.lock()
                return True
            except Exception as e:
                #print(e)
                time.sleep(0.01)
                #return False
        return False

    def unlock(self):
        fcntl.flock(self.handle, fcntl.LOCK_UN)

    def __del__(self):
        try:
            self.handle.close()
        except:
            pass

def getLock(path):
    lock = Lock(path)
    return lock 
    

if __name__ == "__main__":

    a  = Lock('/tmp/12nn')
    b  = Lock('/tmp/12nn')

    a.lock()

    print ("a lock")
    #res = b.try_lock( 30 )
    res = False
    print (f"b lock {res}")
    
    a.unlock()
