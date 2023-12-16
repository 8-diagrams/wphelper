from pickle import GLOBAL
import pymysql
from pyparsing import originalTextFor
import redis
from configparser import ConfigParser

redisHostName = None
gConfig = None 

import mylog

GLogger = mylog.logger

def getdbconn():
    global gConfig
    if not gConfig:
       gConfig = ConfigParser()
       gConfig.read("./env.conf", encoding='UTF-8')
    #config = ConfigParser("./env.conf")
    connect = pymysql.Connect(
    host= gConfig.get('mysql','host'),
    port= int( gConfig.get('mysql','port') ),
    user= gConfig.get('mysql','user') ,
    passwd= gConfig.get('mysql','passwd') ,
    db='tgbotweb',
    charset='utf8mb4'
    )
    #GLogger.info("Connect to DB " + gConfig.get('mysql','host') + ' - ' + str(connect) )
    return connect

def getredis():
    global gConfig
    if not gConfig:
       gConfig = ConfigParser()
       gConfig.read("./env.conf", encoding='UTF-8')
    global redisHostName
    if not redisHostName:
        redisHostName = gConfig.get("redis","hostname")
    hostname = redisHostName #'redis_server'
    return redis.Redis(hostname, port=6379)



from datetime import datetime, timezone, timedelta
def _getDateTimeNow():
    return  datetime.strftime( datetime.now( timezone(timedelta(hours=8)) ) , '%Y-%m-%d %H:%M:%S' )

def _getDateTime( dtObj = None):
    if dtObj:
        return  datetime.strftime( dtObj , '%Y-%m-%d %H:%M:%S' )
    else:
        return _getDateTimeNow()

#time format as "2022-07-15T08:43:05.355+0000"
def fullTime2UTC8_v1(pd, with_ms = False):
    
    date_pd = datetime.strptime( pd, '%Y-%m-%dT%H:%M:%S.%f%z')
    date_pd_utc8 = date_pd.astimezone( timezone(timedelta(hours=8)) )
    if with_ms:
        return date_pd_utc8.strftime(  '%Y-%m-%d %H:%M:%S.%f')
    else:
        return date_pd_utc8.strftime(  '%Y-%m-%d %H:%M:%S')

#'2022-07-15T08:43:05+0000'
def fullTime2UTC8_v2(pd, with_ms = False):
    
    date_pd = datetime.strptime( pd, '%Y-%m-%dT%H:%M:%S%z')
    date_pd_utc8 = date_pd.astimezone( timezone(timedelta(hours=8)) )
    if with_ms:
        return date_pd_utc8.strftime(  '%Y-%m-%d %H:%M:%S.%f')
    else:
        return date_pd_utc8.strftime(  '%Y-%m-%d %H:%M:%S')



def fullTime2UTC8( pd, with_ms = False):
    try:
        return fullTime2UTC8_v1(pd, with_ms )
    except:
        try:
            return  fullTime2UTC8_v2(pd, with_ms )
        except:
            return pd 

def _getUtc():
    return datetime.datetime.strftime( datetime.datetime.utcnow() , '%Y-%m-%dT%H:%M:%S.%f+00.00' )

if __name__ == '__main__':
   
    import json

    conn = getdbconn()
