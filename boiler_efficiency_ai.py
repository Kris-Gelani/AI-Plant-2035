import pandas as pd

# ==========================
# LOAD DATA
# ==========================

df = pd.read_csv("plant_data.csv")

latest = df.iloc[-1]

# ==========================
# BOILER DATA
# ==========================

fuel_rate = 12          # ton/hr
steam_generation = 150  # TPH

stack_temp = 240        # °C
ambient_temp = 35       # °C

excess_air = 25         # %

# ==========================
# EFFICIENCY MODEL
# ==========================

boiler_efficiency = (
    100
    - ((stack_temp - ambient_temp) * 0.05)
)

boiler_efficiency = round(
    boiler_efficiency,
    2
)

# ==========================
# FUEL COST
# ==========================

fuel_cost_day = (
    fuel_rate
    * 24
    * 500
)

# ==========================
# STACK LOSS
# ==========================

stack_loss = round(
    (stack_temp - ambient_temp)
    * 0.05,
    2
)

# ==========================
# AI RECOMMENDATIONS
# ==========================

recommendations = []

if boiler_efficiency < 90:
    recommendations.append(
        "Optimize Burner Settings"
    )

if excess_air > 20:
    recommendations.append(
        "Reduce Excess Air"
    )

if stack_temp > 220:
    recommendations.append(
        "Install Economizer"
    )

recommendations.append(
    "Improve Heat Recovery"
)

# ==========================
# REPORT
# ==========================

print("="*50)
print("AI BOILER EFFICIENCY ANALYZER")
print("="*50)

print()

print(
    "Fuel Consumption :",
    fuel_rate,
    "ton/hr"
)

print(
    "Steam Generation :",
    steam_generation,
    "TPH"
)

print()

print(
    "Stack Temperature :",
    stack_temp,
    "°C"
)

print(
    "Excess Air :",
    excess_air,
    "%"
)

print()

print(
    "Boiler Efficiency :",
    boiler_efficiency,
    "%"
)

print(
    "Stack Loss :",
    stack_loss,
    "%"
)

print()

print(
    "Fuel Cost : $",
    format(fuel_cost_day,","),
    "/day"
)

print()

print("AI Recommendations")

for rec in recommendations:
    print("->", rec)