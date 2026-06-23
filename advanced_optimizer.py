import pandas as pd

df = pd.read_csv("plant_data.csv")

profit = df["Profit"][0]
carbon = df["Carbon_Intensity"][0]
equipment = df["Equipment_Health"][0]

# Multi-objective score
score = (
    profit * 0.5
    + equipment * 2
    + (1 - carbon) * 100
)

print("===== ADVANCED AI OPTIMIZER =====")
print("Profit =", profit)
print("Carbon =", carbon)
print("Equipment =", equipment)
print("Optimization Score =", round(score,2))

if score > 450:
    print("AI Status: EXCELLENT")
elif score > 350:
    print("AI Status: GOOD")
else:
    print("AI Status: NEED OPTIMIZATION")