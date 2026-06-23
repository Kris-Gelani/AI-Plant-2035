print("=" * 60)
print("AI ELECTROLYZER PERFORMANCE")
print("=" * 60)

power_input = 55000
hydrogen_output = 10000

specific_energy = (
    power_input /
    hydrogen_output
)

efficiency = (
    50 /
    specific_energy
) * 100

print()
print("Power Input :", power_input, "kWh/day")
print("Hydrogen Output :", hydrogen_output, "kg/day")

print()
print("Specific Energy :",
      round(specific_energy,2),
      "kWh/kg")

print("Efficiency :",
      round(efficiency,2),
      "%")

print()
print("AI Recommendations")
print("-> Reduce Cell Voltage")
print("-> Improve Stack Health")
print("-> Optimize Water Quality")

print()
print("=" * 60)