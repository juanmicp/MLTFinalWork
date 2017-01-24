#!/usr/bin/env python
# -*- coding: utf-8 -*-

import sqlite3
import codecs
import os

def readAsc (name):
	f = codecs.open("data_berka/" + name + ".asc", "r", "utf-8")
	data = []
	header = True
	for line in f:
		if (not header):
			row = tuple(line.replace ('"', '').split(";"))
			if row != []:
				data.append(row)
		header = False
	return data


dbfile = 'data_berka.db'
if os.path.exists(dbfile):
	os.remove(dbfile)
con = sqlite3.connect(dbfile)
cur = con.cursor()
cur.execute("""	CREATE TABLE district 	(A1 INT PRIMARY KEY,
					A2 TEXT,
					A3 TEXT,
					A4 INT,
					A5 INT,
					A6 INT,
					A7 INT,
					A8 INT,
					A9 INT,
					A10 INT,
					A11 INT,
					A12 INT,
					A13 INT,
					A14 INT,
					A15 INT,
					A16 INT)""")

cur.execute("""CREATE TABLE account 	(account_id INT PRIMARY KEY,
				 	district_id INT,
				 	frecuency TEXT,
				 	date TEXT,
					FOREIGN KEY(district_id) REFERENCES district(A1))""")

cur.execute("""CREATE TABLE client 	(client_id INT PRIMARY KEY,
				 	birth_number TEXT,
				 	district_id INT,
				 	FOREIGN KEY(district_id) REFERENCES district(A1))""")

cur.execute("""CREATE TABLE disp 	(disp_id INT PRIMARY KEY,
				 	client_id INT,
				 	account_id INT,
				 	type TEXT,
					FOREIGN KEY(client_id) REFERENCES client(client_id),
					FOREIGN KEY(account_id) REFERENCES account(account_id))""")

cur.execute("""CREATE TABLE card 	(card_id INT PRIMARY KEY,
				 	disp_id INT,
				 	type TEXT,
				 	issued TEXT,
					FOREIGN KEY(disp_id) REFERENCES disp(disp_id))""")

cur.execute("""CREATE TABLE loan 	(loan_id INT PRIMARY KEY,
				 	account_id INT,
				 	date TEXT,
				 	amount INT,
					duration INT,
					payments REAL,
					status TEXT,
					FOREIGN KEY(account_id) REFERENCES account(account_id))""")

cur.execute("""CREATE TABLE trans 	(trans_id INT PRIMARY KEY,
				 	account_id INT,
				 	date TEXT,
				 	type TEXT,
					operation TEXT,
					amount REAL,
					balance REAL,
					k_symbol TEXT,
					bank TEXT,
					account TEXT,
					FOREIGN KEY(account_id) REFERENCES account(account_id))""")

cur.execute("""CREATE TABLE ord 	(order_id INT PRIMARY KEY,
				 	account_id INT,
				 	bank_to TEXT,
				 	account_to TEXT,
					amount REAL,
					k_symbol TEXT,
					FOREIGN KEY(account_id) REFERENCES account(account_id))""")

cur.executemany("INSERT INTO district VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)", readAsc("district"))
con.commit()

#Same with others tables:

cur.executemany("INSERT INTO account VALUES (?, ?, ?, ?)", readAsc("account"))
con.commit()

cur.executemany("INSERT INTO client VALUES (?, ?, ?)", readAsc("client"))
con.commit()

cur.executemany("INSERT INTO disp VALUES (?, ?, ?, ?)", readAsc("disp"))
con.commit()

cur.executemany("INSERT INTO card VALUES (?, ?, ?, ?)", readAsc("card"))
con.commit()

cur.executemany("INSERT INTO loan VALUES (?, ?, ?, ?, ?, ?, ?)", readAsc("loan"))
con.commit()

cur.executemany("INSERT INTO ord VALUES (?, ?, ?, ?, ?, ?)", readAsc("order"))
con.commit()

cur.executemany("INSERT INTO trans VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)", readAsc("trans"))
con.commit()

con.close()
