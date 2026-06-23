import pandas as pd

df = pd.read_csv("plant_data.csv")

carbon = df["Carbon_Intensity"][0]
conversion = df["Conversion"][0]

# Sustainability Score
sustainability = round(
    (100 - carbon*100 + conversion) / 2,
    2
)

# Carbon Rating
if carbon < 0.30:
    rating = "A+"

elif carbon < 0.50:
    rating = "A"

elif carbon < 0.70:
    rating = "B"

else:
    rating = "C"

# ESG Score
esg = round(
    sustainability * 0.9,
    2
)

print("\n===== SUSTAINABILITY AI =====")
print("Carbon Intensity =", carbon)
print("Carbon Rating =", rating)
print("Sustainability Score =", sustainability)
print("ESG Score =", esg)