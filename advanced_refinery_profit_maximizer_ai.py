# ==========================================================
# AI ADVANCED REFINERY PROFIT MAXIMIZER
# AI Plant 2035
# Phase 24.1
# ==========================================================

print("=" * 60)
print("AI ADVANCED REFINERY PROFIT MAXIMIZER")
print("=" * 60)

# ----------------------------------------------------------
# REFINERY FEED DATA
# ----------------------------------------------------------

crude_rate = 100000          # bbl/day
crude_cost = 78             # $/bbl

# ----------------------------------------------------------
# PRODUCT YIELDS
# ----------------------------------------------------------

lpg_yield = 5
naphtha_yield = 20
kerosene_yield = 12
diesel_yield = 28
gasoil_yield = 15
residue_yield = 20

# ----------------------------------------------------------
# PRODUCT PRICES
# ----------------------------------------------------------

lpg_price = 95
naphtha_price = 105
kerosene_price = 115
diesel_price = 125
gasoil_price = 110
residue_price = 70

# ----------------------------------------------------------
# PRODUCTION CALCULATION
# ----------------------------------------------------------

lpg_prod = crude_rate * lpg_yield / 100
naphtha_prod = crude_rate * naphtha_yield / 100
kerosene_prod = crude_rate * kerosene_yield / 100
diesel_prod = crude_rate * diesel_yield / 100
gasoil_prod = crude_rate * gasoil_yield / 100
residue_prod = crude_rate * residue_yield / 100

# ----------------------------------------------------------
# REVENUE CALCULATION
# ----------------------------------------------------------

lpg_revenue = lpg_prod * lpg_price
naphtha_revenue = naphtha_prod * naphtha_price
kerosene_revenue = kerosene_prod * kerosene_price
diesel_revenue = diesel_prod * diesel_price
gasoil_revenue = gasoil_prod * gasoil_price
residue_revenue = residue_prod * residue_price

total_revenue = (
    lpg_revenue +
    naphtha_revenue +
    kerosene_revenue +
    diesel_revenue +
    gasoil_revenue +
    residue_revenue
)

# ----------------------------------------------------------
# COSTS
# ----------------------------------------------------------

crude_feed_cost = crude_rate * crude_cost

utility_cost = 57500
maintenance_cost = 12000
labor_cost = 8000

total_operating_cost = (
    crude_feed_cost +
    utility_cost +
    maintenance_cost +
    labor_cost
)

# ----------------------------------------------------------
# PROFIT
# ----------------------------------------------------------

daily_profit = (
    total_revenue -
    total_operating_cost
)

annual_profit = (
    daily_profit * 365
)

# ----------------------------------------------------------
# PROFIT MARGIN
# ----------------------------------------------------------

profit_margin = (
    daily_profit /
    total_revenue
) * 100

# ----------------------------------------------------------
# PROFIT STATUS
# ----------------------------------------------------------

if profit_margin >= 25:
    status = "EXCELLENT"

elif profit_margin >= 15:
    status = "GOOD"

elif profit_margin >= 5:
    status = "FAIR"

else:
    status = "POOR"

# ----------------------------------------------------------
# PROFIT SCORE
# ----------------------------------------------------------

profit_score = round(
    min(profit_margin * 4, 100),
    2
)

# ----------------------------------------------------------
# AI RECOMMENDATIONS
# ----------------------------------------------------------

recommendations = []

if diesel_yield < 30:
    recommendations.append(
        "Increase Diesel Yield"
    )

if utility_cost > 50000:
    recommendations.append(
        "Reduce Utility Cost"
    )

if residue_yield > 15:
    recommendations.append(
        "Upgrade Residue Conversion"
    )

recommendations.append(
    "Optimize Crude Selection"
)

recommendations.append(
    "Improve Energy Integration"
)

# ----------------------------------------------------------
# DASHBOARD
# ----------------------------------------------------------

print()
print("REFINERY FEED")
print("-" * 35)

print(
    "Crude Rate :",
    format(crude_rate, ","),
    "bbl/day"
)

print(
    "Crude Cost : $",
    crude_cost,
    "/bbl"
)

# ----------------------------------------------------------

print()
print("PRODUCT YIELDS")
print("-" * 35)

print("LPG      :", lpg_yield, "%")
print("Naphtha  :", naphtha_yield, "%")
print("Kerosene :", kerosene_yield, "%")
print("Diesel   :", diesel_yield, "%")
print("Gasoil   :", gasoil_yield, "%")
print("Residue  :", residue_yield, "%")

# ----------------------------------------------------------

print()
print("REVENUE")
print("-" * 35)

print(
    "Total Revenue : $",
    format(round(total_revenue, 0), ",")
)

# ----------------------------------------------------------

print()
print("OPERATING COST")
print("-" * 35)

print(
    "Crude Feed Cost : $",
    format(round(crude_feed_cost, 0), ",")
)

print(
    "Utility Cost : $",
    format(utility_cost, ",")
)

print(
    "Maintenance Cost : $",
    format(maintenance_cost, ",")
)

print(
    "Labor Cost : $",
    format(labor_cost, ",")
)

print(
    "Total Operating Cost : $",
    format(round(total_operating_cost, 0), ",")
)

# ----------------------------------------------------------

print()
print("PROFITABILITY")
print("-" * 35)

print(
    "Daily Profit : $",
    format(round(daily_profit, 0), ",")
)

print(
    "Annual Profit : $",
    format(round(annual_profit, 0), ",")
)

print(
    "Profit Margin :",
    round(profit_margin, 2),
    "%"
)

# ----------------------------------------------------------

print()
print(
    "Profit Score :",
    profit_score
)

print(
    "Status :",
    status
)

# ----------------------------------------------------------

print()
print("AI RECOMMENDATIONS")
print("-" * 35)

for rec in recommendations:
    print("->", rec)

print()
print("=" * 60)
print("ADVANCED REFINERY PROFIT MAXIMIZER COMPLETE")
print("=" * 60)