print("=" * 60)
print("AI WIND POWER OPTIMIZER")
print("=" * 60)

wind_capacity = 75
capacity_factor = 35

daily_generation = (
    wind_capacity *
    24 *
    capacity_factor / 100
)

annual_generation = (
    daily_generation * 365
)

print()
print("Wind Capacity :", wind_capacity, "MW")
print("Capacity Factor :", capacity_factor, "%")

print()
print("Daily Generation :",
      round(daily_generation,2),
      "MWh/day")

print("Annual Generation :",
      format(round(annual_generation,0),","),
      "MWh/year")

print()
print("AI Recommendations")
print("-> Optimize Turbine Dispatch")
print("-> Improve Blade Performance")
print("-> Reduce Downtime")

print()
print("=" * 60)