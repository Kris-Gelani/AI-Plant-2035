import pandas as pd

df = pd.read_csv("plant_data.csv")

co2_feed = df["CO2_Feed"][0]
methanol = df["Methanol"][0]

inventory = 5000      # kg
daily_production = methanol * 24

days_left = inventory / daily_production

print("===== SUPPLY CHAIN AI =====")

print("Inventory =", inventory, "kg")
print("Daily Production =", round(daily_production,2), "kg/day")
print("Inventory Days Left =", round(days_left,2))

if days_left < 3:
    print("ACTION: Reorder Raw Material")

elif days_left < 7:
    print("ACTION: Monitor Inventory")

else:
    print("ACTION: Inventory Sufficient")