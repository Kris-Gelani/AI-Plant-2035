import pandas as pd
import matplotlib.pyplot as plt

# Load Data
df = pd.read_csv("plant_data.csv")

# X Axis
x = range(1, len(df) + 1)

# Health Score
health_score = (
    df["Equipment_Health"] +
    df["Reactor_Health"]
) / 2

# Dashboard
plt.figure(figsize=(12,10))

# -----------------------
# Profit Trend
# -----------------------

plt.subplot(3,1,1)

plt.plot(
    x,
    df["Profit"],
    marker="o",
    linewidth=3
)

plt.title("Profit Trend")
plt.grid(True)

# -----------------------
# Health Trend
# -----------------------

plt.subplot(3,1,2)

plt.plot(
    x,
    health_score,
    marker="o",
    linewidth=3
)

plt.title("Health Trend")
plt.grid(True)

# -----------------------
# Carbon Trend
# -----------------------

plt.subplot(3,1,3)

plt.plot(
    x,
    df["Carbon_Intensity"],
    marker="o",
    linewidth=3
)

plt.title("Carbon Trend")
plt.grid(True)

plt.tight_layout()

plt.show()