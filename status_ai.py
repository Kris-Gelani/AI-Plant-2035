import pandas as pd

df = pd.read_csv("plant_data.csv")

profit = df["Profit"][0]
carbon = df["Carbon_Intensity"][0]
equipment = df["Equipment_Health"][0]

print("===== PLANT STATUS AI =====")

status = "GREEN"

if profit < 400:
    status = "YELLOW"

if carbon > 0.5:
    status = "ORANGE"

if equipment < 80:
    status = "RED"

print("Plant Status =", status)

if status == "GREEN":
    print("Plant Operating Normally")

elif status == "YELLOW":
    print("Profit Improvement Required")

elif status == "ORANGE":
    print("Emission Reduction Required")

else:
    print("Urgent Maintenance Required")