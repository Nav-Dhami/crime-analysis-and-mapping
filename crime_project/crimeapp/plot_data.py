import pandas as panda
from sklearn.cluster import KMeans
import matplotlib.pyplot as plot

cleaned_data = panda.read_csv("data/cleaned_crime_data.csv")

C = cleaned_data[['Longitude', 'Latitude']]

kmeans = KMeans(n_clusters = 3)
kmeans.fit(C)

plot.scatter(C['Longitude'], C['Latitude'], c = kmeans.labels_, cmap='viridis')
plot.title("West Midlands Crime Clustering")
plot.xlabel("Longitude")
plot.ylabel("Latitude")
plot.show()