import pandas as pd
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split
from sklearn.metrics import classification_report
from sklearn.preprocessing import LabelEncoder
import json
import numpy as np

with open("static/crime_with_clusters_brum.json", "r") as f:
    data = json.load(f)

dF = pd.DataFrame(data)
dF["Year"] = pd.to_datetime(dF["Month"]).dt.year
dF["Month"] = pd.to_datetime(dF["Month"]).dt.month
dF["Season"] = dF["Month"] % 12 // 3 + 1

label_encoders = {}
categorical_features = [
    "Crime type",
    "Last outcome category",
    "LSOA name",
    "Cluster",
]
for feature in categorical_features:
    lE = LabelEncoder()
    dF[feature] = lE.fit_transform(dF[feature])
    label_encoders[feature] = lE

features = [
    "Longitude",
    "Latitude",
    "Cluster",
    "Year",
    "Month",
    "Season",
    "Last outcome category",
    "LSOA name",
]
target = "Crime type"

x = dF[features]
y = dF[target]

x_train, x_test, y_train, y_test = train_test_split(
    x, y, test_size=0.2, random_state=42
)

model = RandomForestClassifier(n_estimators=100, random_state=42)
model.fit(x_train, y_train)

y_predict = model.predict(x_test)
print(
    classification_report(
        y_test, y_predict, target_names=label_encoders["Crime type"].classes_
    )
)




forecasted_months = pd.date_range(start="2024-10", end="2025-03", freq="MS")
predictions = []

monthly_counts = dF.groupby(["Year", "Month"]).size()
avg_crimes_monthly = int(monthly_counts.mean())

seasonal_adjustment = {1: 0.95, 2: 1.05, 3: 1.1, 4: 0.9} #Winter, Spring, Summer, Autumn

for month in forecasted_months:
    season = (month.month % 12) // 3 + 1
    adjustment = seasonal_adjustment.get(season, 1.0)
    sampleSize = int(avg_crimes_monthly * adjustment)
    
    x_forecast = dF[features].sample(sampleSize, replace=True).copy()
    x_forecast["Year"] = month.year
    x_forecast["Month"] = month.month

    y_forecast = model.predict(x_forecast)

    for i in range(len(x_forecast)):
        predictions.append({
            "Latitude": x_forecast.iloc[i]["Latitude"],
            "Longitude": x_forecast.iloc[i]["Longitude"],
            "Crime type": label_encoders["Crime type"].inverse_transform([y_forecast[i]])[0],
            "Month": month.strftime("%Y-%m")
        })

with open("static/predictions.json", "w") as f:
    json.dump(predictions, f, indent=4)

print("Predictions saved to static/predictions.json")

