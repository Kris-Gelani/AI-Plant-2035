import tkinter as tk
import pandas as pd

index = 0

root = tk.Tk()
root.title("AI Plant 2035 Dashboard")
root.geometry("500x500")

title = tk.Label(
    root,
    text="AI Plant 2035 Dashboard",
    font=("Arial", 16, "bold")
)
title.pack(pady=10)

profit_label = tk.Label(root, font=("Arial", 12))
profit_label.pack(pady=5)

conversion_label = tk.Label(root, font=("Arial", 12))
conversion_label.pack(pady=5)

carbon_label = tk.Label(root, font=("Arial", 12))
carbon_label.pack(pady=5)

equipment_label = tk.Label(root, font=("Arial", 12))
equipment_label.pack(pady=5)


def refresh_data():

    global index

    df = pd.read_csv("plant_data.csv")

    row = df.iloc[index]

    profit_label.config(
        text=f"Profit: {row['Profit']} $/h"
    )

    conversion_label.config(
        text=f"Conversion: {row['Conversion']} %"
    )

    carbon_label.config(
        text=f"Carbon Intensity: {row['Carbon_Intensity']}"
    )

    equipment_label.config(
        text=f"Equipment Health: {row['Equipment_Health']}"
    )

    print(f"Showing Row {index+1}")

    # Next row
    index += 1

    # છેલ્લી row પછી ફરી Row 1
    if index == len(df):
        index = 0

    root.after(5000, refresh_data)


refresh_data()

root.mainloop()