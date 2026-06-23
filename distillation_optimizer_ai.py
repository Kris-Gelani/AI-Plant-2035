# ============================================
# AI PLANT 2035
# Phase 23.2
# DISTILLATION OPTIMIZER AI
# ============================================

print("=" * 55)
print("AI DISTILLATION OPTIMIZER")
print("=" * 55)
print()

# --------------------------------------------
# CDU FEED DATA
# --------------------------------------------

feed_rate = 100000      # bbl/day

# --------------------------------------------
# PRODUCT YIELDS
# --------------------------------------------

lpg_pct = 5
naphtha_pct = 20
kerosene_pct = 12
diesel_pct = 28
ago_pct = 15
residue_pct = 20

# --------------------------------------------
# VOLUMES
# --------------------------------------------

lpg_vol = feed_rate * lpg_pct / 100
naphtha_vol = feed_rate * naphtha_pct / 100
kerosene_vol = feed_rate * kerosene_pct / 100
diesel_vol = feed_rate * diesel_pct / 100
ago_vol = feed_rate * ago_pct / 100
residue_vol = feed_rate * residue_pct / 100

# --------------------------------------------
# PRODUCT VALUES ($/bbl)
# --------------------------------------------

lpg_price = 80
naphtha_price = 95
kerosene_price = 110
diesel_price = 125
ago_price = 105
residue_price = 60

# --------------------------------------------
# REVENUE
# --------------------------------------------

daily_revenue = (
    lpg_vol * lpg_price
    + naphtha_vol * naphtha_price
    + kerosene_vol * kerosene_price
    + diesel_vol * diesel_price
    + ago_vol * ago_price
    + residue_vol * residue_price
)

annual_revenue = daily_revenue * 365

# --------------------------------------------
# OPTIMIZATION SCORE
# --------------------------------------------

score = 100

if diesel_pct < 25:
    score -= 15

if residue_pct > 25:
    score -= 15

if naphtha_pct < 18:
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

if diesel_pct < 30:
    recommendations.append(
        "Increase Diesel Recovery"
    )

if residue_pct > 20:
    recommendations.append(
        "Reduce Residue Production"
    )

if naphtha_pct < 22:
    recommendations.append(
        "Optimize Naphtha Cut Point"
    )

recommendations.append(
    "Optimize CDU Furnace Duty"
)

recommendations.append(
    "Improve Fractionation Efficiency"
)

# --------------------------------------------
# DASHBOARD
# --------------------------------------------

print("FEED INFORMATION")
print("-" * 30)

print("Feed Rate :", format(feed_rate, ","), "bbl/day")

print()

print("PRODUCT YIELDS")
print("-" * 30)

print("LPG       :", lpg_pct, "%")
print("Naphtha   :", naphtha_pct, "%")
print("Kerosene  :", kerosene_pct, "%")
print("Diesel    :", diesel_pct, "%")
print("AGO       :", ago_pct, "%")
print("Residue   :", residue_pct, "%")

print()

print("PRODUCT VOLUMES")
print("-" * 30)

print("LPG       :", format(round(lpg_vol,0), ","), "bbl/day")
print("Naphtha   :", format(round(naphtha_vol,0), ","), "bbl/day")
print("Kerosene  :", format(round(kerosene_vol,0), ","), "bbl/day")
print("Diesel    :", format(round(diesel_vol,0), ","), "bbl/day")
print("AGO       :", format(round(ago_vol,0), ","), "bbl/day")
print("Residue   :", format(round(residue_vol,0), ","), "bbl/day")

print()

print("ECONOMICS")
print("-" * 30)

print(
    "Daily Revenue : $",
    format(round(daily_revenue,0), ",")
)

print(
    "Annual Revenue : $",
    format(round(annual_revenue,0), ",")
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