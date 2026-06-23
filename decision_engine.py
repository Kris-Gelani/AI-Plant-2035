import pandas as pd

df = pd.read_csv("plant_data.csv")

profit = df["Profit"][0]
carbon = df["Carbon_Intensity"][0]
conversion = df["Conversion"][0]
equipment = df["Equipment_Health"][0]

print("===== SMART AI DECISION ENGINE =====")

decisions = []

if profit < 500:
    decisions.append("Increase Production")

if carbon > 0.4:
    decisions.append("Reduce Carbon Emissions")

if conversion < 80:
    decisions.append("Increase Reactor Conversion")

if equipment < 90:
    decisions.append("Schedule Maintenance")

if len(decisions) == 0:
    decisions.append("Plant Operating Optimally")

for i, d in enumerate(decisions, 1):
    print(f"{i}. {d}")