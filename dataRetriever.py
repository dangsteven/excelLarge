import cx_Oracle
import sqlite3
import time

def connectOracle():
	con = cx_Oracle.connect('CER_PMO_RO/cerpmoro@CERINP')
	cur = con.cursor()
	cur.execute("SELECT * FROM defaultDB")

	myList = list(cur)

	cur.close()
	con.close()

	return myList
