import pandas as pd

df = pd.read_csv("plant_data.csv")

current_carbon = df["Carbon_Intensity"].mean()

next_week = current_carbon * 0.95
next_month = current_carbon * 0.90

print("="*40)
print("CARBON FORECAST AI")
print("="*40)

print("Current Carbon =", round(current_carbon,3))
print("Next Week =", round(next_week,3))
print("Next Month =", round(next_month,3))