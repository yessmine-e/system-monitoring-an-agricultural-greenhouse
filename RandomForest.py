# -*- coding: utf-8 -*-

import pandas as pd
import numpy as np
from sklearn.ensemble import RandomForestRegressor
from sklearn.metrics import r2_score, mean_absolute_error, mean_squared_error
import pickle

df = pd.read_csv("data_decembre_tunisie.csv", encoding="ISO-8859-1")
df.columns = ["Timestamp", "Humidity", "Temperature_F", "Temperature_C"]

n_steps = 3

def create_features_multi(df, n_steps=3):
    X, y = [], []
    for i in range(n_steps, len(df)):
        temp_feat = df["Temperature_C"].iloc[i-n_steps:i].values
        hum_feat = df["Humidity"].iloc[i-n_steps:i].values
        X.append(np.concatenate([temp_feat, hum_feat]))
        y.append([df["Temperature_C"].iloc[i], df["Humidity"].iloc[i]])
    return np.array(X), np.array(y)

X, y = create_features_multi(df, n_steps)

split_idx = int(len(X) * 0.8)
X_train, X_test = X[:split_idx], X[split_idx:]
y_train, y_test = y[:split_idx], y[split_idx:]

model = RandomForestRegressor(
    n_estimators=300,
    max_depth=15,
    min_samples_split=5,
    min_samples_leaf=2,
    max_features="sqrt",
    bootstrap=True,
    random_state=42,
    n_jobs=-1,
)

model.fit(X_train, y_train)

y_pred = model.predict(X_test)

r2 = r2_score(y_test, y_pred)
mae = mean_absolute_error(y_test, y_pred)
rmse = mean_squared_error(y_test, y_pred, squared=False)

print("R carre global :", r2)
print("MAE global :", mae)
print("RMSE global :", rmse)

r2_temp = r2_score(y_test[:, 0], y_pred[:, 0])
r2_hum = r2_score(y_test[:, 1], y_pred[:, 1])
print("R carre Temperature :", r2_temp)
print("R carre Humidite :", r2_hum)

with open("model_temp_hum.pkl", "wb") as f:
    pickle.dump(model, f)

print("Modele sauvegarde dans model_temp_hum.pkl")
