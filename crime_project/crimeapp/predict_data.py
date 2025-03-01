import pandas as pd
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split
from sklearn.metrics import classification_report
from sklearn.preprocessing import LabelEncoder
import json
import numpy as np

with open("static/crime_with_clusters_brum.json", "r") as f:
    data = json.load(f)

df = pd.DataFrame(data)

df["Year"] = pd.to_datetime(df["Month"]).dt.year
df["Month"] = pd.to_datetime(df["Month"]).dt.month
df["DayOfWeek"] = pd.to_datetime(df["Month"]).dt.dayofweek
df["Season"] = df["Month"] % 12 // 3 + 1

label_encoders = {}
categorical_features = [
    "Crime type",
    "Last outcome category",
    "LSOA name",
    "Cluster",
]
for feature in categorical_features:
    le = LabelEncoder()
    df[feature] = le.fit_transform(df[feature])
    label_encoders[feature] = le

features = [
    "Longitude",
    "Latitude",
    "Cluster",
    "Year",
    "Month",
    "DayOfWeek",
    "Season",
    "Last outcome category",
    "LSOA name",
]
target = "Crime type"

X = df[features]
y = df[target]

X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.2, random_state=42
)

model = RandomForestClassifier(n_estimators=100, random_state=42)
model.fit(X_train, y_train)

y_pred = model.predict(X_test)
print(
    classification_report(
        y_test, y_pred, target_names=label_encoders["Crime type"].classes_
    )
)

future_months = pd.date_range(start="2024-10", end="2025-03", freq="MS")
predictions = []

for month in future_months:
    X_future = df[features].copy()
    X_future["Year"] = month.year
    X_future["Month"] = month.month

    y_future = model.predict(X_future)

    for i in range(len(X_future)):
        predictions.append(
            {
                "Latitude": X_future.iloc[i]["Latitude"],
                "Longitude": X_future.iloc[i]["Longitude"],
                "Crime type": label_encoders["Crime type"].inverse_transform(
                    [y_future[i]]
                )[0],
                "Month": month.strftime("%Y-%m"),
            }
        )

with open("static/predictions.json", "w") as f:
    json.dump(predictions, f, indent=4)

print("Predictions saved to static/predictions.json")

# ---
# currently using a Random Forest model to predict crime types based on location, time, and other features -> currently from oct 2024 to march 2025
# Next to do:
# 1. Adding more features (e.g., weather data, population density) - try get a different set of data covering the same months
# 2. Testing other models like XGBoost -
# 3. Tuning hyperparameters (e.g., n_estimators, max_depth)
