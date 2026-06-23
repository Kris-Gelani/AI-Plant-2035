import tkinter as tk

# =====================================
# WINDOW
# =====================================

root = tk.Tk()

root.title("AI Plant 2035 Enterprise Digital Twin")
root.geometry("1600x900")
root.configure(bg="#081229")

# =====================================
# TITLE
# =====================================

title = tk.Label(
    root,
    text="🏭 AI PLANT 2035 ENTERPRISE DIGITAL TWIN",
    font=("Segoe UI", 28, "bold"),
    fg="white",
    bg="#081229"
)

title.pack(pady=15)

# =====================================
# TOP KPI SECTION
# =====================================

top_frame = tk.Frame(root, bg="#081229")
top_frame.pack()

cards = [
    ("Production", "125,000 BPD", "#2563eb"),
    ("Profit", "$3.2 M", "#16a34a"),
    ("Energy", "95%", "#0891b2"),
    ("Carbon", "82", "#ea580c")
]

for i, (name, value, color) in enumerate(cards):

    card = tk.Frame(
        top_frame,
        bg=color,
        width=250,
        height=120,
        bd=3,
        relief="raised"
    )

    card.grid(row=0, column=i, padx=12)
    card.grid_propagate(False)

    tk.Label(
        card,
        text=name,
        font=("Segoe UI",16,"bold"),
        fg="white",
        bg=color
    ).pack(pady=12)

    tk.Label(
        card,
        text=value,
        font=("Segoe UI",24,"bold"),
        fg="white",
        bg=color
    ).pack()

# =====================================
# MIDDLE SECTION
# =====================================

middle = tk.Frame(root, bg="#081229")
middle.pack(fill="both", expand=True, pady=20)

# =====================================
# DIGITAL TWIN PANEL
# =====================================

plant_frame = tk.Frame(
    middle,
    bg="#111827",
    width=850,
    height=500,
    bd=3,
    relief="ridge"
)

plant_frame.pack(side="left", padx=20)
plant_frame.pack_propagate(False)

tk.Label(
    plant_frame,
    text="DIGITAL PLANT FLOW DIAGRAM",
    font=("Segoe UI",18,"bold"),
    fg="white",
    bg="#111827"
).pack(pady=10)

canvas = tk.Canvas(
    plant_frame,
    width=780,
    height=380,
    bg="#111827",
    highlightthickness=0
)

canvas.pack()

# CDU
canvas.create_rectangle(
    40,150,130,240,
    fill="#2563eb"
)

canvas.create_text(
    85,195,
    text="CDU",
    fill="white",
    font=("Arial",16,"bold")
)

# FCC
canvas.create_rectangle(
    220,150,310,240,
    fill="#16a34a"
)

canvas.create_text(
    265,195,
    text="FCC",
    fill="white",
    font=("Arial",16,"bold")
)

# HYDROTREATER
canvas.create_rectangle(
    400,150,520,240,
    fill="#ea580c"
)

canvas.create_text(
    460,195,
    text="HDT",
    fill="white",
    font=("Arial",16,"bold")
)

# PRODUCTS
canvas.create_rectangle(
    620,150,740,240,
    fill="#7c3aed"
)

canvas.create_text(
    680,195,
    text="PRODUCTS",
    fill="white",
    font=("Arial",14,"bold")
)

# ARROWS
canvas.create_line(
    130,195,220,195,
    fill="white",
    width=4,
    arrow=tk.LAST
)

canvas.create_line(
    310,195,400,195,
    fill="white",
    width=4,
    arrow=tk.LAST
)

canvas.create_line(
    520,195,620,195,
    fill="white",
    width=4,
    arrow=tk.LAST
)

# =====================================
# RIGHT PANEL
# =====================================

right_panel = tk.Frame(
    middle,
    bg="#081229"
)

right_panel.pack(side="left")

# =====================================
# AI ALERTS
# =====================================

alert_frame = tk.Frame(
    right_panel,
    bg="#111827",
    width=450,
    height=220,
    bd=3,
    relief="ridge"
)

alert_frame.pack(pady=10)
alert_frame.pack_propagate(False)

tk.Label(
    alert_frame,
    text="AI ALERTS",
    font=("Segoe UI",18,"bold"),
    fg="white",
    bg="#111827"
).pack(pady=10)

alerts = [
    "✅ Plant operating normally",
    "⚡ Energy efficiency above target",
    "♻ Carbon emission reduced",
    "🛠 No maintenance risk detected"
]

for a in alerts:

    tk.Label(
        alert_frame,
        text=a,
        font=("Segoe UI",12),
        fg="#22c55e",
        bg="#111827"
    ).pack(anchor="w", padx=20)

# =====================================
# LIVE SENSORS
# =====================================

sensor_frame = tk.Frame(
    right_panel,
    bg="#111827",
    width=450,
    height=250,
    bd=3,
    relief="ridge"
)

sensor_frame.pack(pady=10)
sensor_frame.pack_propagate(False)

tk.Label(
    sensor_frame,
    text="LIVE SENSOR STATUS",
    font=("Segoe UI",18,"bold"),
    fg="white",
    bg="#111827"
).pack(pady=10)

sensor_data = [
    "Temperature : 342 °C",
    "Pressure : 12.5 bar",
    "Flow Rate : 125,000 BPD",
    "Hydrogen Purity : 98.4 %",
    "Steam Usage : 120 TPH",
    "Power Usage : 18 MW"
]

for s in sensor_data:

    tk.Label(
        sensor_frame,
        text=s,
        font=("Segoe UI",12),
        fg="white",
        bg="#111827"
    ).pack(anchor="w", padx=20)

# =====================================
# FOOTER
# =====================================

footer = tk.Label(
    root,
    text="Overall Plant Score : 92 | Status : WORLD CLASS",
    font=("Segoe UI",20,"bold"),
    fg="#22c55e",
    bg="#081229"
)

footer.pack(pady=10)

root.mainloop()