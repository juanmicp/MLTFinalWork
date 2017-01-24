#!/usr/bin/env python
# -*- coding: utf-8 -*-

# http://lisp.vse.cz/pkdd99/berka.htm

import sqlite3
import numpy

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

""" Plotting the result
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

# pyplot.scatter(miX, miY)
# pyplot.show()

""" Ahora creamos una lista con tuplas del ID de la region y el num. de impagos
"""
X = zip(numpy.zeros(len(miY)), miY) #No debemos meter "miX" porque el clusteing se vería afectado por la propia colocación aleatoria de los id y no es significativo.

""" Queremos crear 2 clusters, uno para riesgo de impago y otro para no riesgo
"""
number_clusters = 2

from sklearn.preprocessing import StandardScaler
from sklearn import cluster, metrics


X = StandardScaler().fit_transform(X)
spectral = cluster.SpectralClustering(n_clusters=number_clusters, eigen_solver='arpack')
spectral.fit(X)

if hasattr(spectral, 'labels_'):
    labels = spectral.labels_.astype(numpy.int)
else:
    labels = spectral.predict(X)
# Plot
colors = numpy.array(['r', 'b']) #rojo o azul

pyplot.scatter(miX[:], X[:, 1], color=colors[labels].tolist(), s=15)

R=[]
for region, n in todas_regiones:
	R.append(region)

pyplot.xticks(miX, R, size='small', rotation=45)
pyplot.yticks(())

print("Spectral algorithm, number of clusters "+ str(number_clusters) + \
        "\nSilhouette Coefficient: %0.3f" % metrics.silhouette_score(numpy.asarray(X), labels))

pyplot.ylabel('Unpaid loans')
pyplot.xlabel('Regions')

pyplot.show()
