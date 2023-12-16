import datetime 
 
def Utc2Gmt8d(t):
    utctime = t
    utctime = utctime.replace  ( tzinfo = datetime.timezone( datetime.timedelta(hours=0) ) )
    d = utctime.astimezone( datetime.timezone( datetime.timedelta(hours=8) ) )
    #return d.strftime("%Y-%m-%d %H:%M:%S") 
    return d 

def Utc2Gmt8(t):
    utctime = datetime.datetime.strptime(t,"%Y-%m-%d %H:%M:%S" )
    utctime = utctime.replace  ( tzinfo = datetime.timezone( datetime.timedelta(hours=0) ) )
    d = utctime.astimezone( datetime.timezone( datetime.timedelta(hours=8) ) )
    #return d.strftime("%Y-%m-%d %H:%M:%S") 
    return d 

def toUtc(t):
    d = t.astimezone( datetime.timezone( datetime.timedelta(hours=0) ) )
    return d     

def Utc2Gmt8_HHMM(t):
    if type(t) == datetime.datetime:
        d = Utc2Gmt8d( t )
    else:
        d = Utc2Gmt8( t )
    return d.strftime("%H:%M")

def getTimeStamp(dt):
    import datetime
    return datetime.datetime.timestamp( dt )


import decimal

def dreg(num):
    if type (num) != decimal.Decimal:
        num = decimal.Decimal(num)
    return num.to_integral() if num == num.to_integral() else num.normalize()


if __name__ == '__main__':

    print ( Utc2Gmt8_HHMM( '2023-10-28 14:49:40' ) )



