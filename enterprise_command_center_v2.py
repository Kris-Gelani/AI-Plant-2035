import tkinter as tk

# ==========================================
# WINDOW
# ==========================================

root = tk.Tk()

root.title("AI Plant 2035 Enterprise Digital Twin")
root.geometry("1600x900")
root.configure(bg="#0f172a")

# ==========================================
# TITLE
# ==========================================

title = tk.Label(
    root,
    text="🏭 AI PLANT 2035 ENTERPRISE DIGITAL TWIN",
    font=("Segoe UI", 30, "bold"),
    fg="white",
    bg="#0f172a"
)

title.pack(pady=20)

# ==========================================
# KPI SECTION
# ==========================================

kpi_frame = tk.Frame(
    root,
    bg="#0f172a"
)

kpi_frame.pack(pady=10)

cards = [
    ("Production", "125,000", "#2563eb"),
    ("Profit", "$3.2M", "#16a34a"),
    ("Energy", "95%", "#0891b2"),
    ("Carbon", "82", "#ea580c"),
    ("Safety", "98", "#dc2626"),
    ("Maintenance", "91", "#7c3aed"),
    ("Refinery", "89", "#2563eb"),
    ("Hydrogen", "88", "#06b6d4"),
    ("Renewable", "90", "#16a34a"),
    ("ESG", "A", "#ca8a04")
]

row = 0
col = 0

for title_text, value, color in cards:

    card = tk.Frame(
        kpi_frame,
        bg=color,
        width=250,
        height=120,
        bd=3,
        relief="raised"
    )

    card.grid(
        row=row,
        column=col,
        padx=10,
        pady=10
    )

    card.grid_propagate(False)

    tk.Label(
        card,
        text=title_text,
        font=("Segoe UI", 14, "bold"),
        fg="white",
        bg=color
    ).pack(pady=(20, 5))

    tk.Label(
        card,
        text=value,
        font=("Segoe UI", 22, "bold"),
        fg="white",
        bg=color
    ).pack()

    col += 1

    if col > 1:
        row += 1
        col = 0

# ==========================================
# MAIN PANELS
# ==========================================

main_frame = tk.Frame(
    root,
    bg="#0f172a"
)

main_frame.pack(
    fill="both",
    expand=True,
    padx=20,
    pady=20
)

# ==========================================
# LEFT PANEL
# ==========================================

left_panel = tk.Frame(
    main_frame,
    bg="white",
    bd=3,
    relief="raised"
)

left_panel.pack(
    side="left",
    fill="both",
    expand=True,
    padx=10
)

tk.Label(
    left_panel,
    text="AI STATUS CENTER",
    font=("Segoe UI", 18, "bold"),
    bg="white"
).pack(pady=15)

status_data = [
    "Plant State : STABLE",
    "Health Score : 98",
    "Failure Risk : LOW",
    "Plant Grade : A+",
    "",
    "AI Decisions",
    "• Plant Operating Optimally",
    "• Energy Consumption Reduced",
    "• Carbon Emissions Controlled",
    "• Maintenance Schedule Updated",
    "• Production Target Achieved"
]

for item in status_data:

    tk.Label(
        left_panel,
        text=item,
        font=("Segoe UI", 13),
        bg="white",
        anchor="w"
    ).pack(
        anchor="w",
        padx=20,
        pady=4
    )

# ==========================================
# RIGHT PANEL
# ==========================================

right_panel = tk.Frame(
    main_frame,
    bg="white",
    bd=3,
    relief="raised"
)

right_panel.pack(
    side="right",
    fill="both",
    expand=True,
    padx=10
)

tk.Label(
    right_panel,
    text="FORECAST & ANALYTICS",
    font=("Segoe UI", 18, "bold"),
    bg="white"
).pack(pady=15)

forecast_data = [
    "Predicted Profit : $3.45 Million",
    "",
    "Current Carbon : 82",
    "Next Week Carbon : 79",
    "Next Month Carbon : 75",
    "",
    "Production Forecast : 128,500 BPD",
    "Energy Forecast : 96%",
    "Hydrogen Forecast : 91%",
    "ESG Forecast : A+"
]

for item in forecast_data:

    tk.Label(
        right_panel,
        text=item,
        font=("Segoe UI", 13),
        bg="white",
        anchor="w"
    ).pack(
        anchor="w",
        padx=20,
        pady=4
    )

# ==========================================
# SCORE
# ==========================================

score_label = tk.Label(
    root,
    text="Overall Plant Score : 92",
    font=("Segoe UI", 24, "bold"),
    fg="#22c55e",
    bg="#0f172a"
)

score_label.pack(pady=10)

status_label = tk.Label(
    root,
    text="🟢 Plant Status : WORLD CLASS",
    font=("Segoe UI", 18, "bold"),
    fg="#22c55e",
    bg="#0f172a"
)

status_label.pack(pady=10)

# ==========================================
# RUN
# ==========================================

root.mainloop()