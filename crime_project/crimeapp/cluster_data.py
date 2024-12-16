import pandas as panda
from sklearn.cluster import KMeans
import json

cleaned_data = panda.read_csv("data/cleaned_crime_data.csv")

min_lat = 52.4
max_lat = 52.6
min_lon = -1.9
max_lon = -1.7

brum_data = cleaned_data[(cleaned_data['Latitude'] >= min_lat) & 
                               (cleaned_data['Latitude'] <= max_lat) &
                               (cleaned_data['Longitude'] >= min_lon) &
                               (cleaned_data['Longitude'] <= max_lon)]

B = brum_data[['Longitude', 'Latitude']]

kmeans = KMeans(n_clusters=3)
kmeans.fit(B)

brum_data['Cluster'] = kmeans.labels_

brum_data_json = brum_data[['Longitude', 'Latitude', 'Cluster']].to_dict(orient='records')


with open("data/crime_with_clusters_brum.json", "w") as json_file:
    json.dump(brum_data_json, json_file)
