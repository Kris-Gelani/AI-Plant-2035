import pandas as pd

df = pd.read_csv("plant_data.csv")

heater = df["Heater_Duty"][0]
profit = df["Profit"][0]

energy_efficiency = profit / heater

print("===== ENERGY AI =====")

print("Heater Duty =", heater, "kW")
print("Profit =", profit, "$/h")
print("Energy Efficiency =", round(energy_efficiency, 4))

if energy_efficiency > 0.10:
    print("Energy Status: EXCELLENT")
elif energy_efficiency > 0.08:
    print("Energy Status: GOOD")
else:
    print("Energy Status: IMPROVEMENT REQUIRED")