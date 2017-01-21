#!/usr/bin/env python
# -*- coding: utf-8 -*-

# http://lisp.vse.cz/pkdd99/berka.htm

import sqlite3

connection = sqlite3.connect('data_berka.db')
cursor = connection.cursor()


""" Calculating number of unpaid loans per region
"""
cursor.execute("""SELECT A3, COUNT(A3) FROM district WHERE A1 IN (
                    SELECT district_id FROM account WHERE account_id IN (
                        SELECT account_id FROM loan WHERE status='D\r\n'
                    )
                  )
                  GROUP BY A3""")

# Regiones que tienen algun impago
regiones_con_impagos = [(str(row[0]), int(row[1])) for row in cursor.fetchall()]

# Leemos todas las regiones que hay en la BBDD
cursor.execute("""SELECT DISTINCT(A3) FROM district""")
regiones_BBDD = [str(x[0]) for x in cursor.fetchall()]

# Ahora creamos una lista con las regiones que no estan en el vector de regiones con impagos y con las que sí
todas_regiones = list(regiones_con_impagos)
todas_regiones.extend((region, 0) for region in regiones_BBDD if region not in (reg_imp[0] for reg_imp in regiones_con_impagos))

print todas_regiones

""" Applying DBSCAN algorithm
"""
from matplotlib import pyplot

# Nos inventamos un ID numerico para cada region y poder hacer una grafica
region_id = []
id = -1
for dupla in todas_regiones:
    id += 1
    region_id.append((id, dupla[0]))

miX = [id[0] for id in region_id] # ID DE LA REGION
miY = [region[1] for region in todas_regiones] # NUM DE IMPAGOS DE LA REGION

pyplot.scatter(miX, miY)
pyplot.show()
