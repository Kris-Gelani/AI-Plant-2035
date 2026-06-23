print("=" * 70)
print("AI PLANT 2035 COMMAND CENTER")
print("=" * 70)

production_score = 90
profit_score = 92
energy_score = 95
safety_score = 98
carbon_score = 82

command_score = (
    production_score*0.2 +
    profit_score*0.2 +
    energy_score*0.2 +
    safety_score*0.2 +
    carbon_score*0.2
)

if command_score >= 90:
    status = "WORLD CLASS"

elif command_score >= 80:
    status = "EXCELLENT"

else:
    status = "GOOD"

print()
print("Production Score :", production_score)
print("Profit Score :", profit_score)
print("Energy Score :", energy_score)
print("Safety Score :", safety_score)
print("Carbon Score :", carbon_score)

print()
print("Command Center Score :",
      round(command_score,2))

print("Plant Status :", status)

print()
print("AI COMMANDS")
print("-> Maximize Production")
print("-> Minimize Cost")
print("-> Improve Sustainability")
print("-> Maintain Safety Excellence")
print("-> Increase Profitability")

print()
print("=" * 70)
print("AI PLANT COMMAND CENTER COMPLETE")
print("=" * 70)