import pandas as panda
from sklearn.cluster import KMeans
import json


cleaned_data = panda.read_csv("data/cleaned_crime_data.csv")

# Birmingham boundaries
min_lat = 52.40
max_lat = 52.55
min_lon = -1.967  
max_lon = -1.750  

brum_data = cleaned_data[(cleaned_data['Latitude'] >= min_lat) & 
                         (cleaned_data['Latitude'] <= max_lat) & 
                         (cleaned_data['Longitude'] >= min_lon) & 
                         (cleaned_data['Longitude'] <= max_lon)]

# Downsample the data - take every 10th point for performance
brum_data = brum_data.sample(frac=0.1, random_state=42)  

B = brum_data[['Longitude', 'Latitude']]


n_clusters = 5  # Limit clusters
kmeans = KMeans(n_clusters=n_clusters, random_state=42)
kmeans.fit(B)

brum_data['Cluster'] = kmeans.labels_

brum_data_json = brum_data[['Longitude', 'Latitude', 'Cluster']].to_dict(orient='records')

with open("static/crime_with_clusters_brum.json", "w") as json_file:
    json.dump(brum_data_json, json_file)

print("clustered data for Birmingham saved to 'static/crime_with_clusters_brum.json'")