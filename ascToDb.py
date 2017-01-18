#!/usr/bin/env python
# -*- coding: utf-8 -*-



import csv, sqlite3

con = sqlite3.connect('data_berka.db')
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
					A16 INT);

		CREATE TABLE account 	(account_id INT,
				 	district_id INT,
				 	frecuency TEXT,
				 	date TEXT,
					FOREIGN KEY(district_id) REFERENCES district(A1));

		CREATE TABLE client 	(client_id INT,
				 	birth_number TEXT,
				 	district_id INT,
				 	FOREIGN KEY(district_id) REFERENCES district(A1));

		CREATE TABLE disp 	(disp_id INT,
				 	client_id INT,
				 	account_id INT,
				 	type TEXT,
					FOREIGN KEY(client_id) REFERENCES client(client_id),
					FOREIGN KEY(account_id) REFERENCES account(account_id));

		CREATE TABLE card 	(card_id INT,
				 	disp_id INT,
				 	type TEXT,
				 	issued TEXT,
					FOREIGN KEY(disp_id) REFERENCES disp(disp_id));

		CREATE TABLE loan 	(loan_id INT,
				 	account_id INT,
				 	date TEXT,
				 	amount INT,
					duration INT,
					payments REAL,
					status TEXT,
					FOREIGN KEY(account_id) REFERENCES account(account_id));

		CREATE TABLE order 	(order_id INT,
				 	account_id INT,
				 	bank_to TEXT,
				 	account_to TEXT,
					amount REAL,
					k_symbol TEXT,
					FOREIGN KEY(account_id) REFERENCES account(account_id));

		CREATE TABLE trans 	(trans_id INT,
				 	account_id INT,
				 	date TEXT,
				 	type TEXT,
					operation TEXT,
					amount REAL,
					balance REAL,
					k_symbol TEXT,
					bank TEXT,
					account TEXT,
					FOREIGN KEY(account_id) REFERENCES account(account_id));

""")

"""
with open('data.csv','rb') as fin: # `with` statement available in 2.5+
    # csv.DictReader uses first line in file for column headings by default
    dr = csv.DictReader(fin) # comma is default delimiter
    to_db = [(i['col1'], i['col2']) for i in dr]

cur.executemany("INSERT INTO t (col1, col2) VALUES (?, ?);", to_db)
con.commit()
con.close()
"""


