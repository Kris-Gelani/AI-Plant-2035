import tkinter as tk
import pandas as pd

# -----------------------------
# Window Setup
# -----------------------------
root = tk.Tk()
root.title("AI Plant 2035 Digital Twin")
root.geometry("900x600")
root.configure(bg="#f0f2f5")

# -----------------------------
# Read Dataset
# -----------------------------
df = pd.read_csv("plant_data.csv")

current_index = 0

# -----------------------------
# Title
# -----------------------------
title = tk.Label(
    root,
    text="🏭 AI Plant 2035 Digital Twin",
    font=("Arial", 24, "bold"),
    bg="#f0f2f5"
)

title.pack(pady=20)

# -----------------------------
# KPI Frame
# -----------------------------
frame = tk.Frame(root, bg="#f0f2f5")
frame.pack()

profit_label = tk.Label(
    frame,
    text="Profit",
    width=18,
    height=5,
    bg="green",
    fg="white",
    font=("Arial", 16, "bold")
)
profit_label.grid(row=0, column=0, padx=10)

conversion_label = tk.Label(
    frame,
    text="Conversion",
    width=18,
    height=5,
    bg="blue",
    fg="white",
    font=("Arial", 16, "bold")
)
conversion_label.grid(row=0, column=1, padx=10)

carbon_label = tk.Label(
    frame,
    text="Carbon",
    width=18,
    height=5,
    bg="orange",
    fg="black",
    font=("Arial", 16, "bold")
)
carbon_label.grid(row=0, column=2, padx=10)

health_label = tk.Label(
    frame,
    text="Health",
    width=18,
    height=5,
    bg="red",
    fg="white",
    font=("Arial", 16, "bold")
)
health_label.grid(row=0, column=3, padx=10)

# -----------------------------
# Additional Information
# -----------------------------
state_label = tk.Label(
    root,
    font=("Arial", 16, "bold"),
    bg="#f0f2f5"
)
state_label.pack(pady=10)

health_score_label = tk.Label(
    root,
    font=("Arial", 14),
    bg="#f0f2f5"
)
health_score_label.pack()

risk_label = tk.Label(
    root,
    font=("Arial", 14, "bold"),
    bg="#f0f2f5"
)
risk_label.pack()

decision_label = tk.Label(
    root,
    font=("Arial", 14),
    bg="#f0f2f5"
)
decision_label.pack(pady=10)

# -----------------------------
# Live Update Function
# -----------------------------
def update_dashboard():

    global current_index

    row = df.iloc[current_index]

    profit_label.config(
        text=f"Profit\n\n{row['Profit']} $/h"
    )

    conversion_label.config(
        text=f"Conversion\n\n{row['Conversion']} %"
    )

    carbon_label.config(
        text=f"Carbon\n\n{row['Carbon_Intensity']}"
    )

    health_label.config(
        text=f"Health\n\n{row['Equipment_Health']}"
    )

    # Health Score
    health_score = (
        row["Equipment_Health"] +
        row["Conversion"]
    ) / 2

    state_label.config(
        text=f"Plant State : {current_index + 1}"
    )

    health_score_label.config(
        text=f"Health Score : {round(health_score,2)}"
    )

    # Failure Risk
    if row["Equipment_Health"] >= 90:
        risk = "LOW"
        risk_color = "green"

    elif row["Equipment_Health"] >= 75:
        risk = "MEDIUM"
        risk_color = "orange"

    else:
        risk = "HIGH"
        risk_color = "red"

    risk_label.config(
        text=f"Failure Risk : {risk}",
        fg=risk_color
    )

    # AI Decision
    recommendations = []

    if row["Carbon_Intensity"] > 0.35:
        recommendations.append("Reduce CO2 Feed")

    if row["Profit"] < 700:
        recommendations.append("Increase Production Rate")

    if row["Equipment_Health"] < 80:
        recommendations.append("Schedule Maintenance")

    if len(recommendations) == 0:
        recommendations.append("Plant Operating Optimally")

    decision_label.config(
        text="AI Decision : " + ", ".join(recommendations)
    )

    # Fixed Sequence Loop
    current_index += 1

    if current_index >= len(df):
        current_index = 0

    root.after(5000, update_dashboard)

# -----------------------------
# Start
# -----------------------------
update_dashboard()

root.mainloop()