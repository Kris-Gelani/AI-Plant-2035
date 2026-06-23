# ============================================
# AI PLANT 2035
# Phase 23.1
# CRUDE OPTIMIZER AI
# ============================================

print("=" * 55)
print("AI CRUDE OPTIMIZER")
print("=" * 55)
print()

# --------------------------------------------
# CRUDE DATA
# --------------------------------------------

crude_name = "Arab Light"

api_gravity = 34.5

sulfur = 1.8

crude_cost = 78.0      # $/bbl

refined_product_value = 105.0   # $/bbl

throughput = 100000    # bbl/day

# --------------------------------------------
# MARGIN CALCULATION
# --------------------------------------------

gross_margin = (
    refined_product_value
    - crude_cost
)

daily_profit = (
    gross_margin
    * throughput
)

annual_profit = (
    daily_profit
    * 365
)

# --------------------------------------------
# CRUDE QUALITY
# --------------------------------------------

if api_gravity > 38:
    crude_type = "LIGHT"

elif api_gravity > 30:
    crude_type = "MEDIUM"

else:
    crude_type = "HEAVY"

# --------------------------------------------
# SULFUR CLASSIFICATION
# --------------------------------------------

if sulfur < 0.5:
    sulfur_class = "SWEET"

else:
    sulfur_class = "SOUR"

# --------------------------------------------
# OPTIMIZATION SCORE
# --------------------------------------------

score = 100

if sulfur > 1.5:
    score -= 15

if crude_cost > 80:
    score -= 10

if api_gravity < 30:
    score -= 10

# --------------------------------------------
# STATUS
# --------------------------------------------

if score >= 90:
    status = "EXCELLENT"

elif score >= 75:
    status = "GOOD"

elif score >= 60:
    status = "MODERATE"

else:
    status = "POOR"

# --------------------------------------------
# AI RECOMMENDATIONS
# --------------------------------------------

recommendations = []

if sulfur > 1.5:
    recommendations.append(
        "Blend With Sweet Crude"
    )

if crude_cost > 80:
    recommendations.append(
        "Negotiate Lower Crude Price"
    )

if api_gravity < 30:
    recommendations.append(
        "Increase Light Crude Ratio"
    )

recommendations.append(
    "Optimize CDU Operation"
)

recommendations.append(
    "Maximize High Value Products"
)

# --------------------------------------------
# DASHBOARD
# --------------------------------------------

print("CRUDE INFORMATION")
print("-" * 30)

print("Crude Name :", crude_name)
print("API Gravity :", api_gravity)
print("Sulfur :", sulfur, "%")
print("Crude Type :", crude_type)
print("Sulfur Class :", sulfur_class)

print()

print("ECONOMICS")
print("-" * 30)

print("Crude Cost : $", crude_cost, "/bbl")
print("Product Value : $", refined_product_value, "/bbl")

print(
    "Gross Margin : $",
    round(gross_margin, 2),
    "/bbl"
)

print()

print(
    "Daily Profit : $",
    format(round(daily_profit, 0), ",")
)

print(
    "Annual Profit : $",
    format(round(annual_profit, 0), ",")
)

print()

print("OPTIMIZATION RESULT")
print("-" * 30)

print("Optimization Score :", score)
print("Status :", status)

print()

print("AI Recommendations")

for rec in recommendations:
    print("->", rec)

print()
print("=" * 55)