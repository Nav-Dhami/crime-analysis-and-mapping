import pandas as pd
from sklearn.cluster import KMeans
import json


file_path = "data/cleaned_crime_data.csv"  
cleaned_data = pd.read_csv(file_path)

# Birmingham boundaries
min_lat, max_lat = 52.40, 52.55
min_lon, max_lon = -1.967, -1.750


brum_data = cleaned_data[
    (cleaned_data['Latitude'].between(min_lat, max_lat)) & 
    (cleaned_data['Longitude'].between(min_lon, max_lon))
].copy()

# Performance downsample - not working? - Check later
brum_data = brum_data.sample(frac=0.1, random_state=42)  

# Ensure all required columns exist
required_columns = ["Longitude", "Latitude", "Crime type", "Month", "Last outcome category", "LSOA name"]
missing_columns = [col for col in required_columns if col not in brum_data.columns]

if missing_columns:
    raise ValueError(f"Missing columns in dataset: {missing_columns}")


coords = brum_data[['Longitude', 'Latitude']]

# K-Means clustering
n_clusters = 5  
kmeans = KMeans(n_clusters=n_clusters, random_state=42, n_init=10)
brum_data.loc[:, 'Cluster'] = kmeans.fit_predict(coords)


columns_to_convert = ["Crime type", "Month", "Last outcome category", "LSOA name"]
brum_data[columns_to_convert] = brum_data[columns_to_convert].fillna("Unknown").astype(str)

# Convert to JSON 
brum_data_json = brum_data[['Longitude', 'Latitude', 'Cluster', 'Crime type', 'Month', 'Last outcome category', 'LSOA name']].to_dict(orient='records')

output_path = "static/crime_with_clusters_brum.json"
with open(output_path, "w") as json_file:
    json.dump(brum_data_json, json_file, indent=4)