print("=" * 65)
print("AI ENTERPRISE RISK ANALYZER")
print("=" * 65)

process_risk = 12
market_risk = 18
energy_risk = 15
supply_risk = 10

risk_score = (
    process_risk +
    market_risk +
    energy_risk +
    supply_risk
)

if risk_score < 40:
    status = "LOW"

elif risk_score < 70:
    status = "MEDIUM"

else:
    status = "HIGH"

print()
print("Total Risk Score :", risk_score)
print("Risk Status :", status)

print()
print("AI Recommendations")
print("-> Diversify Supply Chain")
print("-> Improve Process Safety")
print("-> Reduce Energy Dependence")

print()
print("=" * 65)