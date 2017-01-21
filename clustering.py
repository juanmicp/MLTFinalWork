#!/usr/bin/env python
# -*- coding: utf-8 -*-

# http://lisp.vse.cz/pkdd99/berka.htm
# Preveer impagos usando las tablas loan, disposition y client
# Contar el numero de impagos de un cliente y hacer una grafica cliente/#impagos
#
#Hacer un dbscan o un kmeans y hacer un par de clusters uno para clientes
# sin riesgo de impago y otro para los que tengan riesgo

import sqlite3

connection = sqlite3.connect('data_berka.db')
cursor = connection.cursor()

cursor.execute("SELECT account_id FROM loan WHERE status='D\r\n'") #sin lo de \r\n no va

array_cuentas_impago = [row[0] for row in cursor.fetchall()]

dict_cuentas_impago = dict()

for cuenta in array_cuentas_impago:
    if cuenta in dict_cuentas_impago:
        dict_cuentas_impago[cuenta] += 1
    else:
        dict_cuentas_impago[cuenta] = 1

print dict_cuentas_impago
