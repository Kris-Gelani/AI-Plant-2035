# ==========================================
# AI PLANT 2035
# Phase 22.1 - Carbon Footprint AI
# ==========================================

print("=" * 50)
print("AI CARBON FOOTPRINT ANALYZER")
print("=" * 50)

# ------------------------------------------
# Plant Data
# ------------------------------------------

fuel_consumption = 12      # ton/hr
power_usage = 18           # MW
production = 1000          # ton/day

# ------------------------------------------
# Carbon Emission Factors
# ------------------------------------------

fuel_factor = 0.8          # ton CO2 per ton fuel
power_factor = 0.5         # ton CO2 per MWh

# ------------------------------------------
# Emission Calculations
# ------------------------------------------

fuel_emission = (
    fuel_consumption * 24 * fuel_factor
)

power_emission = (
    power_usage * 24 * power_factor
)

total_emission = (
    fuel_emission + power_emission
)

carbon_intensity = (
    total_emission / production
)

# ------------------------------------------
# Net Zero Score
# ------------------------------------------

if carbon_intensity < 0.30:
    score = 95

elif carbon_intensity < 0.50:
    score = 80

elif carbon_intensity < 0.80:
    score = 65

else:
    score = 40

# ------------------------------------------
# AI Recommendations
# ------------------------------------------

recommendations = []

if fuel_emission > 200:
    recommendations.append(
        "Improve Boiler Efficiency"
    )

if power_emission > 150:
    recommendations.append(
        "Install Solar Power"
    )

if carbon_intensity > 0.40:
    recommendations.append(
        "Increase Heat Recovery"
    )

if total_emission > 400:
    recommendations.append(
        "Carbon Credit Strategy"
    )

# ------------------------------------------
# Results
# ------------------------------------------

print()

print(
    "Fuel Consumption :",
    fuel_consumption,
    "ton/hr"
)

print(
    "Power Usage      :",
    power_usage,
    "MW"
)

print()

print(
    "Fuel CO2         :",
    round(fuel_emission, 2),
    "ton/day"
)

print(
    "Power CO2        :",
    round(power_emission, 2),
    "ton/day"
)

print()

print(
    "Total Emissions  :",
    round(total_emission, 2),
    "ton/day"
)

print(
    "Carbon Intensity :",
    round(carbon_intensity, 3)
)

print()

print(
    "Net Zero Score   :",
    score,
    "%"
)

print()
print("AI Recommendations")

for rec in recommendations:
    print("->", rec)

print()
print("=" * 50)