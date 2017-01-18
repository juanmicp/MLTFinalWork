#!/usr/bin/env python
# -*- coding: utf-8 -*-

import sqlite3
import codecs
import csv
import os

dbfile = 'data_berka.db'
if os.path.exists(dbfile): 
	os.remove(dbfile)
con = sqlite3.connect(dbfile)
cur = con.cursor()
cur.execute("""	CREATE TABLE district 	(A1 INT,
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

cur.execute("""CREATE TABLE account 	(account_id INT,
				 	district_id INT,
				 	frecuency TEXT,
				 	date TEXT,
					FOREIGN KEY(district_id) REFERENCES district(A1))""")

cur.execute("""CREATE TABLE client 	(client_id INT,
				 	birth_number TEXT,
				 	district_id INT,
				 	FOREIGN KEY(district_id) REFERENCES district(A1))""")

cur.execute("""CREATE TABLE disp 	(disp_id INT,
				 	client_id INT,
				 	account_id INT,
				 	type TEXT,
					FOREIGN KEY(client_id) REFERENCES client(client_id),
					FOREIGN KEY(account_id) REFERENCES account(account_id))""")

cur.execute("""CREATE TABLE card 	(card_id INT,
				 	disp_id INT,
				 	type TEXT,
				 	issued TEXT,
					FOREIGN KEY(disp_id) REFERENCES disp(disp_id))""")

cur.execute("""CREATE TABLE loan 	(loan_id INT,
				 	account_id INT,
				 	date TEXT,
				 	amount INT,
					duration INT,
					payments REAL,
					status TEXT,
					FOREIGN KEY(account_id) REFERENCES account(account_id))""")
"""

cur.execute(""CREATE TABLE order 	(order_id INT,
				 	account_id INT,
				 	bank_to TEXT,
				 	account_to TEXT,
					amount REAL,
					k_symbol TEXT,
					FOREIGN KEY(account_id) REFERENCES account(account_id))"")
"""

cur.execute("""CREATE TABLE trans 	(trans_id INT,
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

with open('data_berka/district.asc','rb') as f:
	data = csv.DictReader(f)
	to_db = [(i['A1'], i['A2'], i['A3'], i['A4'], i['A5'], i['A6'], i['A7'], i['A8'], i['A9'], i['A10'], i['A11'], i['A12'], i['A13'], i['A14'], i['A15'], i['A16']) for i in data]

cur.executemany("INSERT INTO district (A1, A2, A3, A4, A5, A6, A7, A8, A9, A10, A11, A12, A13, A14, A15, A16) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?);", to_db)
con.commit()

#Same with others tables...

con.close()
