import pandas as pd

df = pd.read_csv("plant_data.csv")

co2 = df["CO2_Feed"][0]
carbon = df["Carbon_Intensity"][0]

emission_score = co2 * carbon

print("===== EMISSION AI =====")

print("CO2 Feed =", co2, "kmol/h")
print("Carbon Intensity =", carbon)
print("Emission Score =", round(emission_score, 2))

if emission_score < 10:
    print("Emission Level: LOW")

elif emission_score < 20:
    print("Emission Level: MODERATE")

else:
    print("Emission Level: HIGH")