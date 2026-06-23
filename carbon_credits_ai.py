# ==========================================
# AI PLANT 2035
# Phase 22.3 - Carbon Credit AI
# ==========================================

print("=" * 50)
print("AI CARBON CREDIT OPTIMIZER")
print("=" * 50)

# ------------------------------------------
# Plant Data
# ------------------------------------------

annual_emission = 148868      # ton/year
reduction_target = 14887      # ton/year

carbon_credit_price = 25      # $/ton CO2

# ------------------------------------------
# Carbon Credit Calculations
# ------------------------------------------

carbon_credits = reduction_target

credit_value = (
    carbon_credits
    * carbon_credit_price
)

# ------------------------------------------
# ESG Rating
# ------------------------------------------

if annual_emission < 100000:
    esg_rating = "A"

elif annual_emission < 200000:
    esg_rating = "B"

elif annual_emission < 300000:
    esg_rating = "C"

else:
    esg_rating = "D"

# ------------------------------------------
# AI Recommendations
# ------------------------------------------

recommendations = []

if carbon_credits > 10000:
    recommendations.append(
        "Sell Carbon Credits"
    )

if annual_emission > 120000:
    recommendations.append(
        "Increase Renewable Energy"
    )

if esg_rating in ["C", "D"]:
    recommendations.append(
        "Launch ESG Improvement Program"
    )

recommendations.append(
    "Develop Net Zero Roadmap"
)

# ------------------------------------------
# Results
# ------------------------------------------

print()

print(
    "Annual Emission :",
    format(annual_emission, ","),
    "ton/year"
)

print(
    "Reduction Target :",
    format(reduction_target, ","),
    "ton/year"
)

print()

print(
    "Carbon Credits :",
    format(carbon_credits, ","),
    "credits"
)

print(
    "Credit Value : $",
    format(credit_value, ",")
)

print()

print(
    "ESG Rating :",
    esg_rating
)

print()

print("AI Recommendations")

for rec in recommendations:
    print("->", rec)

print()
print("=" * 50)