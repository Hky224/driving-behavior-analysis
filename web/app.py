from flask import Flask, render_template, request
import mysql.connector

app = Flask(__name__)

def connect():
    mydb = mysql.connector.connect(
        host='comp4442-gp.crqk44cigx2u.us-east-1.rds.amazonaws.com',
        user='admin',
        port='3306',
        database='comp4442-gp',
        passwd='12345678'
    )
    return mydb

@app.route('/')
def index():
    return render_template('table.html')

@app.route('/filter', methods=['POST'])
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


@app.route('/monitor')
def monitor_data():
    return render_template('monitor.html')

if __name__ == '__main__':
    app.run()