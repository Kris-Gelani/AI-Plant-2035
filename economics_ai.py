import pandas as pd

df = pd.read_csv("plant_data.csv")

profit = df["Profit"][0]
carbon = df["Carbon_Intensity"][0]

carbon_tax = carbon * 100
net_profit = profit - carbon_tax

print("===== ECONOMICS AI =====")

print("Gross Profit = $", profit, "/h")
print("Carbon Tax = $", round(carbon_tax, 2), "/h")
print("Net Profit = $", round(net_profit, 2), "/h")

if net_profit > 400:
    print("Economic Status: STRONG")
elif net_profit > 300:
    print("Economic Status: STABLE")
else:
    print("Economic Status: WEAK")