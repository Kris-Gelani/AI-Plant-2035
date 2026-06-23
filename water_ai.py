import pandas as pd

df = pd.read_csv("plant_data.csv")

heater = df["Heater_Duty"][0]
conversion = df["Conversion"][0]

water_usage = heater * 0.02

print("===== WATER AI =====")

print("Water Usage =", round(water_usage, 2), "m3/h")

water_efficiency = conversion / water_usage

print("Water Efficiency =", round(water_efficiency, 2))

if water_efficiency > 0.8:
    print("Water Status: EXCELLENT")

elif water_efficiency > 0.5:
    print("Water Status: GOOD")

else:
    print("Water Status: IMPROVEMENT REQUIRED")