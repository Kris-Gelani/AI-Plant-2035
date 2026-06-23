import pandas as pd

df = pd.read_csv("plant_data.csv")

for i in range(len(df)):

    row = df.iloc[i]

    print("\n========================")
    print(f"Plant State {i+1}")
    print("========================")

    if row["Carbon_Intensity"] > 0.40:
        print("⚠ ALERT: High Carbon Emission")

    if row["Equipment_Health"] < 80:
        print("🔧 ALERT: Maintenance Required")

    if row["Profit"] < 700:
        print("💰 ALERT: Low Profit")

    if (
        row["Carbon_Intensity"] <= 0.40
        and row["Equipment_Health"] >= 80
        and row["Profit"] >= 700
    ):
        print("✅ Plant Operating Normally")