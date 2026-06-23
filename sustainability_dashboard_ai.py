# ============================================
# AI PLANT 2035
# Phase 22.5
# SUSTAINABILITY DASHBOARD AI
# ============================================

print("=" * 55)
print("AI SUSTAINABILITY DASHBOARD")
print("=" * 55)
print()

# --------------------------------------------
# ENERGY SYSTEM DATA
# --------------------------------------------

energy_efficiency = 95.0

steam_usage = 120
steam_cost = 18000

boiler_efficiency = 89.75

heat_recovery_savings = 3011250

utility_cost = 45500

# --------------------------------------------
# CARBON DATA
# --------------------------------------------

annual_emission = 148868

carbon_credits = 14887

credit_value = 372175

esg_rating = "B"

net_zero_score = 50

# --------------------------------------------
# SUSTAINABILITY SCORE
# --------------------------------------------

sustainability_score = (
    energy_efficiency
    + boiler_efficiency
    + net_zero_score
) / 3

# --------------------------------------------
# GRADE
# --------------------------------------------

if sustainability_score >= 90:
    grade = "A+"

elif sustainability_score >= 80:
    grade = "A"

elif sustainability_score >= 70:
    grade = "B"

elif sustainability_score >= 60:
    grade = "C"

else:
    grade = "D"

# --------------------------------------------
# STATUS
# --------------------------------------------

if grade == "A+":
    status = "WORLD CLASS"

elif grade == "A":
    status = "EXCELLENT"

elif grade == "B":
    status = "GOOD"

elif grade == "C":
    status = "AVERAGE"

else:
    status = "NEEDS IMPROVEMENT"

# --------------------------------------------
# AI RECOMMENDATIONS
# --------------------------------------------

recommendations = []

if energy_efficiency < 98:
    recommendations.append(
        "Improve Energy Efficiency"
    )

if boiler_efficiency < 92:
    recommendations.append(
        "Optimize Boiler Combustion"
    )

if net_zero_score < 70:
    recommendations.append(
        "Accelerate Net Zero Program"
    )

if esg_rating != "A":
    recommendations.append(
        "Improve ESG Rating"
    )

recommendations.append(
    "Increase Renewable Energy Usage"
)

recommendations.append(
    "Expand Heat Recovery Network"
)

# --------------------------------------------
# DASHBOARD
# --------------------------------------------

print("ENERGY PERFORMANCE")
print("-" * 30)

print(
    "Energy Efficiency :",
    energy_efficiency,
    "%"
)

print(
    "Steam Usage :",
    steam_usage,
    "TPH"
)

print(
    "Steam Cost : $",
    format(steam_cost, ",")
)

print(
    "Boiler Efficiency :",
    boiler_efficiency,
    "%"
)

print(
    "Utility Cost : $",
    format(utility_cost, ",")
)

print()

print("SUSTAINABILITY PERFORMANCE")
print("-" * 30)

print(
    "Annual Emission :",
    format(annual_emission, ","),
    "ton/year"
)

print(
    "Carbon Credits :",
    format(carbon_credits, ",")
)

print(
    "Credit Value : $",
    format(credit_value, ",")
)

print(
    "ESG Rating :",
    esg_rating
)

print(
    "Net Zero Score :",
    net_zero_score,
    "%"
)

print()

print(
    "Heat Recovery Savings : $",
    format(heat_recovery_savings, ",")
)

print()

print("OVERALL RESULT")
print("-" * 30)

print(
    "Sustainability Score :",
    round(sustainability_score, 2)
)

print(
    "Sustainability Grade :",
    grade
)

print(
    "Status :",
    status
)

print()

print("AI Recommendations")

for rec in recommendations:
    print("->", rec)

print()
print("=" * 55)