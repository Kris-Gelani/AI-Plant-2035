import pandas as pd

df = pd.read_csv("plant_data.csv")

carbon = df["Carbon_Intensity"][0]

baseline = 0.50
reduction = baseline - carbon

credit_price = 50      # $ per carbon credit

credits = max(0, reduction * 100)
revenue = credits * credit_price

print("===== CARBON CREDIT AI =====")

print("Carbon Intensity =", carbon)
print("Carbon Reduction =", round(reduction, 2))
print("Carbon Credits =", round(credits, 2))
print("Carbon Revenue = $", round(revenue, 2), "/h")

if revenue > 1000:
    print("Carbon Strategy: EXCELLENT")
else:
    print("Carbon Strategy: IMPROVING")