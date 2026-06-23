import pandas as pd

df = pd.read_csv("plant_data.csv")

profit = df["Profit"][0]
carbon = df["Carbon_Intensity"][0]
equipment = df["Equipment_Health"][0]

print("===== ENTERPRISE AI =====")

erp_score = (
    profit * 0.5 +
    equipment * 2 -
    carbon * 100
)

print("ERP Score =", round(erp_score, 2))

if erp_score > 300:
    print("Enterprise Status: EXCELLENT")

elif erp_score > 200:
    print("Enterprise Status: GOOD")

else:
    print("Enterprise Status: IMPROVEMENT REQUIRED")