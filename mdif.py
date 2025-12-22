import pandas as pd
import numpy as np

# Charger le fichier avec l'encodage correct
df = pd.read_csv("data_3hrs.csv", encoding="ISO-8859-1")

# Générer humidité réaliste Tunisie décembre (5575%)
df["Humidity (%)"] = np.random.uniform(55, 75, len(df)).round(2)

# Générer température °C réaliste Tunisie décembre (1520°C)
df["Temperature (°C)"] = np.random.uniform(15, 20, len(df)).round(2)

# Convertir °C ? °F
df["Temperature (°F)"] = (df["Temperature (°C)"] * 9/5 + 32).round(2)

# Sauvegarder un nouveau fichier
df.to_csv("data_decembre_tunisie.csv", index=False)

print("Dataset modifié avec succès !")

