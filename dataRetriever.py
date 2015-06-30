import cx_Oracle
import sqlite3
import time

def connectOracle():
	con = cx_Oracle.connect('defaultdatabase')
	cur = con.cursor()
	cur.execute("SELECT * FROM defaultDB")

	myList = list(cur)

	cur.close()
	con.close()

	return myList
