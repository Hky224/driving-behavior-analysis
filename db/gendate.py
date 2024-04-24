import time
import random
import dbconnect

conn = dbconnect.connect()
cur = conn.cursor()

def genData():
    Time = int(time.time())
    speed = random.randint(0,10) + 20*random.randint(1,10)
    data = {}
    data['time'] = Time
    data['speed'] = speed
    return data

def execute():
    data = genData()
    sql = "insert into RealTimeMonitor(num,ctime) values ({0},{1})".format(data['speed'],data['time'])
    print(sql)
    ret = cur.execute(sql)

while True:   
    execute()
    time.sleep(1)