import tkinter as tk
import pandas as pd
import joblib
import traceback
import sys
from tkinter import Frame, messagebox

# =====================================
# LOAD MODEL
# =====================================

try:
    model = joblib.load("profit_model.pkl")
except Exception as e:
    print("Failed to load model profit_model.pkl:")
    traceback.print_exc()
    raise

current_index = 0

# =====================================
# WINDOW
# =====================================

root = tk.Tk()
root.title("AI Plant 2035 Enterprise Digital Twin")
root.geometry("1200x800")
root.configure(bg="#f1f3f6")

# =====================================
# TITLE
# =====================================

title = tk.Label(
    root,
    text="🏭 AI Plant 2035 Enterprise Digital Twin",
    font=("Arial", 24, "bold"),
    bg="#f1f3f6"
)
title.pack(pady=10)

# =====================================
# KPI FRAME
# =====================================

kpi_frame = Frame(root, bg="#f1f3f6")
kpi_frame.pack()

profit_card = tk.Label(
    kpi_frame,
    width=18,
    height=5,
    bg="green",
    fg="white",
    font=("Arial", 16, "bold")
)
profit_card.grid(row=0, column=0, padx=10)

conversion_card = tk.Label(
    kpi_frame,
    width=18,
    height=5,
    bg="blue",
    fg="white",
    font=("Arial", 16, "bold")
)
conversion_card.grid(row=0, column=1, padx=10)

carbon_card = tk.Label(
    kpi_frame,
    width=18,
    height=5,
    bg="orange",
    fg="black",
    font=("Arial", 16, "bold")
)
carbon_card.grid(row=0, column=2, padx=10)

health_card = tk.Label(
    kpi_frame,
    width=18,
    height=5,
    bg="red",
    fg="white",
    font=("Arial", 16, "bold")
)
health_card.grid(row=0, column=3, padx=10)

# =====================================
# STATUS LABELS
# =====================================

state_label = tk.Label(
    root,
    font=("Arial", 18, "bold"),
    bg="#f1f3f6"
)
state_label.pack(pady=10)

health_score_label = tk.Label(
    root,
    font=("Arial", 16),
    bg="#f1f3f6"
)
health_score_label.pack()

risk_label = tk.Label(
    root,
    font=("Arial", 16, "bold"),
    bg="#f1f3f6"
)
risk_label.pack()

grade_label = tk.Label(
    root,
    font=("Arial", 16, "bold"),
    bg="#f1f3f6"
)
grade_label.pack()

decision_label = tk.Label(
    root,
    font=("Arial", 16),
    bg="#f1f3f6",
    justify="left"
)
decision_label.pack(pady=10)

prediction_label = tk.Label(
    root,
    font=("Arial", 16, "bold"),
    bg="#f1f3f6"
)
prediction_label.pack()

carbon_forecast_label = tk.Label(
    root,
    font=("Arial", 16),
    bg="#f1f3f6"
)
carbon_forecast_label.pack(pady=10)

# =====================================
# UPDATE FUNCTION
# =====================================

def update_dashboard():

    global current_index

    df = pd.read_csv("plant_data.csv")

    row = df.iloc[current_index]

    try:
        # KPI Cards

        profit_card.config(
            text=f"Profit\n\n{row['Profit']} $/h"
        )

        conversion_card.config(
            text=f"Conversion\n\n{row['Conversion']} %"
        )

        carbon_card.config(
            text=f"Carbon\n\n{row['Carbon_Intensity']}"
        )

        health_card.config(
            text=f"Health\n\n{row['Equipment_Health']}"
        )

        # Health Score

        health_score = (
            row["Equipment_Health"] +
            row["Reactor_Health"]
        ) / 2

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

        # Plant Grade

        if health_score >= 90:
            grade = "A"

        elif health_score >= 80:
            grade = "B"

        elif health_score >= 70:
            grade = "C"

        else:
            grade = "D"

        # AI Recommendations

        recommendations = []

        if row["Carbon_Intensity"] > 0.35:
            recommendations.append("Reduce CO2 Feed")

        if row["Profit"] < 700:
            recommendations.append("Increase Production Rate")

        if row["Equipment_Health"] < 80:
            recommendations.append("Schedule Maintenance")

        if len(recommendations) == 0:
            recommendations.append("Plant Operating Optimally")

        # ML Prediction (WARNING FIXED)

        input_data = pd.DataFrame({
            "Conversion": [row["Conversion"]],
            "Carbon_Intensity": [row["Carbon_Intensity"]],
            "Equipment_Health": [row["Equipment_Health"]]
        })

        prediction = model.predict(input_data)

        # Carbon Forecast

        next_week = row["Carbon_Intensity"] * 0.95
        next_month = row["Carbon_Intensity"] * 0.90

        # Update Labels

        state_label.config(
            text=f"Plant State : {current_index + 1}"
        )

        health_score_label.config(
            text=f"Health Score : {round(health_score,2)}"
        )

        risk_label.config(
            text=f"Failure Risk : {risk}",
            fg=risk_color
        )

        grade_label.config(
            text=f"Plant Grade : {grade}"
        )

        decision_label.config(
            text="AI Decisions:\n\n" +
            "\n".join([f"• {x}" for x in recommendations])
        )

        prediction_label.config(
            text=f"Predicted Profit : {round(prediction[0],2)} $/h"
        )

        carbon_forecast_label.config(
            text=
            f"Current Carbon : {row['Carbon_Intensity']}\n"
            f"Next Week : {round(next_week,3)}\n"
            f"Next Month : {round(next_month,3)}"
        )

        # Next State

        current_index += 1

        if current_index >= len(df):
            current_index = 0

        root.after(
            5000,
            update_dashboard
        )
    except KeyboardInterrupt:
        print("Dashboard interrupted by user")
        try:
            root.quit()
        except Exception:
            pass
        sys.exit(0)
    except Exception:
        print("Error updating dashboard for index", current_index)
        traceback.print_exc()
        try:
            messagebox.showerror("Dashboard Error", f"Error updating dashboard: see console for details")
        except Exception:
            pass
        return

    

# =====================================
# START
# =====================================

update_dashboard()
print("Dashboard Starting...")
root.mainloop()