import pandas as pd
import time

df = pd.read_csv("plant_data.csv")

while True:

    for i, row in df.iterrows():

        print("\n" + "=" * 50)
        print("AI PLANT 2035 DIGITAL TWIN")
        print("=" * 50)

        print("Plant State :", i + 1)
        print()

        # Process Data
        print("Methanol Production :", row["Methanol"])
        print("CO2 Feed            :", row["CO2_Feed"])
        print("Heater Duty         :", row["Heater_Duty"])

        print()

        print("Conversion          :", row["Conversion"], "%")
        print("Carbon Intensity    :", row["Carbon_Intensity"])
        print("Equipment Health    :", row["Equipment_Health"])
        print("Profit              : $", row["Profit"], "/h")

        print()

        # Health Score
        health_score = (
            row["Equipment_Health"] +
            row["Conversion"]
        ) / 2

        print("Health Score        :", round(health_score, 2))

        # Failure Prediction
        if row["Equipment_Health"] >= 90:
            risk = "LOW"
        elif row["Equipment_Health"] >= 75:
            risk = "MEDIUM"
        else:
            risk = "HIGH"

        print("Failure Risk        :", risk)

        # AI Decision Engine
        recommendations = []

        if row["Carbon_Intensity"] > 0.35:
            recommendations.append("Reduce CO2 Feed")

        if row["Profit"] < 700:
            recommendations.append("Increase Production Rate")

        if row["Equipment_Health"] < 80:
            recommendations.append("Schedule Maintenance")

        if len(recommendations) == 0:
            recommendations.append("Plant Operating Optimally")

        print()
        print("AI Decisions:")

        for rec in recommendations:
            print(" -", rec)

        print("\nNext Update in 5 Seconds...")
        time.sleep(5)