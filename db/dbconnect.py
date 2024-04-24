import mysql.connector

def connect():
    mydb = mysql.connector.connect( host = 'comp4442-gp.crqk44cigx2u.us-east-1.rds.amazonaws.com',
	user = 'admin',
	port = '3306',
	database = 'comp4442-gp',
	passwd = '12345678'
    )
    return mydb
