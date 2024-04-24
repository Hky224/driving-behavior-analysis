from flask import Blueprint, render_template, request
from threading import Thread
import mysql.connector
import time
import random

app_blueprint = Blueprint('app_blueprint',__name__)

def connect():
    mydb = mysql.connector.connect(
        host='comp4442-gp.crqk44cigx2u.us-east-1.rds.amazonaws.com',
        user='admin',
        port='3306',
        database='comp4442-gp',
        passwd='12345678'
    )
    return mydb

@app_blueprint.route('/')
def index():
    return render_template('index.html')

@app_blueprint.route('/filter', methods=['POST'])
def filter_data():
    start_date = request.form['start-date']
    end_date = request.form['end-date']

    conn = connect()
    cursor = conn.cursor()

    chunk_size = 1000  # Define the chunk size for each query
    offset = 0
    result = []

    while True:
        query = """
            SELECT DriverID, CarPlateNumber,
            SUM(isRapidlySpeedup) AS SumRapidlySpeedup,
            SUM(isRapidlySlowdown) AS SumRapidlySlowdown,
            SUM(isNeutralSlide) AS SumNeutralSlide,
            SUM(isNeutralSlideFinished) AS SumNeutralSlideFinished,
            SUM(neutralSlideTime) AS SumNeutralSlideTime,
            SUM(isOverspeed) AS SumOverspeed,
            SUM(isOverspeedFinished) AS SumOverspeedFinished,
            SUM(overspeedTime) AS SumOverspeedTime,
            SUM(isFatigueDriving) AS SumFatigueDriving,
            SUM(isHthrottleStop) AS SumHthrottleStop,
            SUM(isOilLeak) AS SumOilLeak
        FROM Records
        WHERE DrivingDate BETWEEN %s AND %s
        GROUP BY DriverID, CarPlateNumber
        LIMIT %s OFFSET %s;"""

        cursor.execute(query, (start_date, end_date, chunk_size, offset))
        rows = cursor.fetchall()
        if not rows:  # No more data to fetch
            break
        result.extend(rows)
        offset += chunk_size

    cursor.close()
    conn.close()

    return render_template('table.html', result=result)

@app_blueprint.route('/monitor', methods=['POST'])
def monitor_data():
    global data_generation_running
    driverid = request.form['driverid']
    if not data_generation_running:
        Thread(target=execute, args=(driverid,)).start()
    return render_template('monitor.html')

def execute(driverid):
    data_generation_running = True
    db = connect()
    cursor = db.cursor()
    while data_generation_running:
        data = genData(driverid)
        sql = "insert into RealTimeMonitor(DriverID, Speed,Time) values ({0},{1},{2})".format(data['driverid'], data['speed'],data['time'])
        print(sql)
        cursor.execute(sql)
        db.commit()
        time.sleep(1)  # sleep for 1 second
    cursor.close()
    db.close()

def genData(driverid):
    Time = int(time.time())
    speed = random.randint(0,10) + 20*random.randint(1,10)
    data = {}
    data['time'] = Time
    data['speed'] = speed
    data['driverid'] = driverid
    return data