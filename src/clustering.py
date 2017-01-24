#!/usr/bin/env python
# -*- coding: utf-8 -*-

import sqlite3
import numpy

ddbb_name = 'ddbb/data_berka.db'
connection = sqlite3.connect(ddbb_name)
cursor = connection.cursor()


""" Calculating number of unpaid loans per region
"""
cursor.execute("""SELECT A3, COUNT(A3) FROM district WHERE A1 IN (
                    SELECT district_id FROM account WHERE account_id IN (
                        SELECT account_id FROM loan WHERE status='D\r\n'
                    )
                  )
                  GROUP BY A3""")

# Regions with any unpaid loan
regiones_con_impagos = [(str(row[0]), int(row[1])) for row in cursor.fetchall()]

# Reading all regions on the database
cursor.execute("""SELECT DISTINCT(A3) FROM district""")
regiones_BBDD = [str(x[0]) for x in cursor.fetchall()]

# Creating a list with the regions with unpaid loans and the ones with 0 unpaid loans
todas_regiones = list(regiones_con_impagos)
todas_regiones.extend((region, 0) for region in regiones_BBDD if region not in (reg_imp[0] for reg_imp in regiones_con_impagos))

print todas_regiones

""" Plotting the result
"""
from matplotlib import pyplot

# Making up an ID for each region to be able to plot a graph with them
region_id = []
id = -1
for dupla in todas_regiones:
    id += 1
    region_id.append((id, dupla[0]))

miX = [id[0] for id in region_id] # REGION ID
miY = [region[1] for region in todas_regiones] # NUM OF UNPAID LOANS ON THE REGION

pyplot.scatter(miX, miY)
pyplot.show()

#The clustering would be affected by the random IDs
X = zip(numpy.zeros(len(miY)), miY)

""" Two clusters are needed; for regions with risk of unpaid loans and for those without risk
"""
number_clusters = 2

from sklearn.preprocessing import StandardScaler
from sklearn import cluster, metrics

X = StandardScaler().fit_transform(X)
spectral = cluster.SpectralClustering(n_clusters=number_clusters, eigen_solver='arpack', affinity='rbf')
spectral.fit(X)

if hasattr(spectral, 'labels_'):
    labels = spectral.labels_.astype(numpy.int)
else:
    labels = spectral.predict(X)
# Plot
colors = numpy.array(['r', 'b']) #red or blue

pyplot.scatter(miX[:], X[:, 1], color=colors[labels].tolist(), s=15)

R = [x[0] for x in todas_regiones]

pyplot.xticks(miX, R, size='small', rotation=45)
pyplot.yticks(())

print("Spectral algorithm, number of clusters "+ str(number_clusters) + \
        "\nSilhouette Coefficient: %0.3f" % metrics.silhouette_score(numpy.asarray(X), labels))

pyplot.ylabel('Unpaid loans')
pyplot.xlabel('Regions')

pyplot.show()
