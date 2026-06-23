import pandas as pd

# ==========================
# LOAD DATA
# ==========================

df = pd.read_csv("plant_data.csv")

latest = df.iloc[-1]

profit = latest["Profit"]
conversion = latest["Conversion"]

# ==========================
# ENERGY MODEL
# ==========================

steam_usage = 120          # TPH
power_usage = 18           # MW

utility_cost = (
    steam_usage * 200 +
    power_usage * 1000
)

energy_efficiency = (
    (conversion / 100) * 100
)

# ==========================
# AI RECOMMENDATIONS
# ==========================

recommendations = []

if energy_efficiency < 85:
    recommendations.append(
        "Optimize Reactor Conversion"
    )

if steam_usage > 100:
    recommendations.append(
        "Optimize Steam Header"
    )

if power_usage > 15:
    recommendations.append(
        "Reduce Compressor Load"
    )

recommendations.append(
    "Recover Waste Heat"
)

# ==========================
# REPORT
# ==========================

print("="*50)
print("AI ENERGY OPTIMIZER")
print("="*50)

print()

print("Profit :", profit, "$/h")
print("Conversion :", conversion, "%")

print()

print("Steam Usage :", steam_usage, "TPH")
print("Power Usage :", power_usage, "MW")

print()

print(
    "Energy Efficiency :",
    round(energy_efficiency,2),
    "%"
)

print(
    "Utility Cost : $",
    format(utility_cost,","),
    "/day"
)

print()

print("AI Recommendations")

for rec in recommendations:
    print("->", rec)