# -*- coding: utf-8 -*-

import pandas as pd
import numpy as np
from sklearn.ensemble import RandomForestRegressor
from sklearn.model_selection import train_test_split
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


X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)


model = RandomForestRegressor(n_estimators=100, random_state=42)
model.fit(X_train, y_train)

# Tester le score
score = model.score(X_test, y_test)
print("Rcarre du modele RandomForest:", score)

# Sauvegarder dans un seul fichier .pkl
with open("model_temp_hum.pkl", "wb") as f:
    pickle.dump(model, f)

print("Modele multi-sortie sauvegarde dans model_temp_hum.pkl ")

