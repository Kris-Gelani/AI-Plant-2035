import pandas as pd

df = pd.read_csv("plant_data.csv")

methanol = df.loc[0, "Methanol"]
co2 = df.loc[0, "CO2_Feed"]
heater = df.loc[0, "Heater_Duty"]
conversion = df.loc[0, "Conversion"]
carbon = df.loc[0, "Carbon_Intensity"]
equipment = df.loc[0, "Equipment_Health"]
reactor = df.loc[0, "Reactor_Health"]
profit = df.loc[0, "Profit"]

plant_health = (equipment + reactor) / 2

if plant_health >= 80:
    status = "HEALTHY"
else:
    status = "WARNING"

if reactor < 60:
    risk = "HIGH"
elif reactor < 80:
    risk = "MEDIUM"
else:
    risk = "LOW"

sustainability = conversion - carbon * 10

digital_twin_index = (
    equipment +
    reactor +
    conversion +
    (100 - carbon * 100)
) / 4

print("===== AI PLANT DIGITAL TWIN =====")
print("Plant Health =", round(plant_health,2), "%")
print("Plant Status =", status)
print("Failure Risk =", risk)
print("Sustainability Score =", round(sustainability,2))
print("Digital Twin Index =", round(digital_twin_index,2))
import matplotlib.pyplot as plt

parameters = [
    "Plant Health",
    "Reactor Health",
    "Conversion",
    "Equipment"
]

values = [
    plant_health,
    reactor,
    conversion,
    equipment
]

plt.figure(figsize=(8,5))
plt.bar(parameters, values)

plt.title("AI Plant 2035 Digital Twin Dashboard")
plt.ylabel("Score (%)")

plt.show()