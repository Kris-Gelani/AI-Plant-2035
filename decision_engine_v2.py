import pandas as pd

df = pd.read_csv("plant_data.csv")

for i, row in df.iterrows():

    print("="*40)
    print("Plant State", i+1)
    print("="*40)

    recommendations = []

    if row["Profit"] < 700:
        recommendations.append(
            "Increase Production Rate"
        )

    if row["Carbon_Intensity"] > 0.35:
        recommendations.append(
            "Reduce CO2 Feed"
        )

    if row["Equipment_Health"] < 80:
        recommendations.append(
            "Schedule Maintenance"
        )

    if len(recommendations) == 0:
        recommendations.append(
            "Plant Operating Optimally"
        )

    for rec in recommendations:
        print("AI Decision:", rec)

    print()