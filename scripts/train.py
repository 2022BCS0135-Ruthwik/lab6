import pandas as pd
from sklearn.ensemble import RandomForestRegressor
from sklearn.metrics import mean_squared_error, r2_score
import joblib
import json
import os

# Create directories if they do not exist
os.makedirs('app/artifacts', exist_ok=True)

# 1. Load dataset
url = "https://archive.ics.uci.edu/ml/machine-learning-databases/wine-quality/winequality-red.csv"
df = pd.read_csv(url, sep=';')

# 2. Select the specified 5 features
features = ['alcohol', 'sulphates', 'citric acid', 'volatile acidity', 'density']
target = 'quality'

X = df[features]
y = df[target]

# 3. Train RandomForestRegressor
model = RandomForestRegressor(n_estimators=100, max_depth=15, random_state=42)
model.fit(X, y)

# 4. Compute metrics
predictions = model.predict(X)
mse = mean_squared_error(y, predictions)
r2 = r2_score(y, predictions)

print(f"Mean Squared Error: {mse}")
print(f"R2 Score: {r2}")

# 5. Save outputs
joblib.dump(model, 'app/artifacts/model.pkl')

metrics = {
    "accuracy": r2
}

with open('app/artifacts/metrics.json', 'w') as f:
    json.dump(metrics, f, indent=4)
