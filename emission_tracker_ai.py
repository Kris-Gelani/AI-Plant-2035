# ==========================================
# AI PLANT 2035
# Phase 22.2 - Emission Tracker AI
# ==========================================

print("=" * 50)
print("AI EMISSION TRACKER")
print("=" * 50)

# ------------------------------------------
# Daily Emission Data (ton/day)
# ------------------------------------------

daily_emissions = [
    420,
    415,
    430,
    405,
    400,
    395,
    390
]

# ------------------------------------------
# Calculations
# ------------------------------------------

avg_emission = (
    sum(daily_emissions)
    / len(daily_emissions)
)

annual_emission = (
    avg_emission * 365
)

target_reduction = (
    annual_emission * 0.10
)

net_zero_gap = (
    annual_emission
    - target_reduction
)

# ------------------------------------------
# Trend Analysis
# ------------------------------------------

if daily_emissions[-1] < daily_emissions[0]:
    trend = "IMPROVING"

elif daily_emissions[-1] > daily_emissions[0]:
    trend = "WORSENING"

else:
    trend = "STABLE"

# ------------------------------------------
# AI Recommendations
# ------------------------------------------

recommendations = []

if avg_emission > 400:
    recommendations.append(
        "Reduce Fuel Consumption"
    )

if trend == "WORSENING":
    recommendations.append(
        "Audit Energy Systems"
    )

if annual_emission > 150000:
    recommendations.append(
        "Carbon Reduction Program"
    )

if annual_emission > 100000:
    recommendations.append(
        "Carbon Credit Strategy"
    )

# ------------------------------------------
# Results
# ------------------------------------------

print()

print(
    "Average Daily Emission :",
    round(avg_emission, 2),
    "ton/day"
)

print()

print(
    "Annual Emission :",
    format(round(annual_emission, 0), ","),
    "ton/year"
)

print()

print(
    "Reduction Target :",
    format(round(target_reduction, 0), ","),
    "ton/year"
)

print()

print(
    "Net Zero Gap :",
    format(round(net_zero_gap, 0), ","),
    "ton/year"
)

print()

print(
    "Emission Trend :",
    trend
)

print()
print("AI Recommendations")

for rec in recommendations:
    print("->", rec)

print()
print("=" * 50)