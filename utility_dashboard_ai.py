import pandas as pd

# ==========================
# LOAD DATA
# ==========================

df = pd.read_csv("plant_data.csv")

latest = df.iloc[-1]

# ==========================
# STEAM SYSTEM
# ==========================

steam_usage = 120      # TPH
steam_cost = 18000     # $/day

# ==========================
# POWER SYSTEM
# ==========================

power_usage = 18       # MW
power_cost = 24000     # $/day

# ==========================
# COOLING WATER
# ==========================

cw_usage = 25000       # m3/day
cw_cost = 3500         # $/day

# ==========================
# BOILER
# ==========================

boiler_efficiency = 89.75

# ==========================
# ENERGY KPI
# ==========================

total_utility_cost = (
    steam_cost
    + power_cost
    + cw_cost
)

energy_efficiency = 95

# ==========================
# UTILITY GRADE
# ==========================

if energy_efficiency >= 90:
    grade = "A"

elif energy_efficiency >= 80:
    grade = "B"

elif energy_efficiency >= 70:
    grade = "C"

else:
    grade = "D"

# ==========================
# REPORT
# ==========================

print("="*50)
print("AI UTILITY DASHBOARD")
print("="*50)

print()

print("STEAM SYSTEM")
print("Steam Usage :", steam_usage, "TPH")
print("Steam Cost  : $", format(steam_cost, ","))

print()

print("POWER SYSTEM")
print("Power Usage :", power_usage, "MW")
print("Power Cost  : $", format(power_cost, ","))

print()

print("COOLING WATER")
print("CW Usage :", cw_usage, "m3/day")
print("CW Cost  : $", format(cw_cost, ","))

print()

print("BOILER")
print(
    "Boiler Efficiency :",
    boiler_efficiency,
    "%"
)

print()

print(
    "Energy Efficiency :",
    energy_efficiency,
    "%"
)

print(
    "Total Utility Cost : $",
    format(total_utility_cost,",")
)

print()

print(
    "Utility Grade :",
    grade
)

print()

print("AI Recommendations")
print("-> Optimize Steam Usage")
print("-> Improve Boiler Efficiency")
print("-> Reduce Power Consumption")
print("-> Increase Heat Recovery")