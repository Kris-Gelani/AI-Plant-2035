import tkinter as tk
from tkinter import ttk
import random
from datetime import datetime

# =====================================
# WINDOW
# =====================================

root = tk.Tk()
root.title("AI Plant 2035 Enterprise Digital Twin")
root.geometry("1600x900")
root.configure(bg="#081229")

# =====================================
# VARIABLES
# =====================================

temperature = tk.StringVar()
pressure = tk.StringVar()
flowrate = tk.StringVar()
profit = tk.StringVar()
plant_grade = tk.StringVar()
ai_alert = tk.StringVar()
clock_var = tk.StringVar()

# =====================================
# TITLE
# =====================================

title_frame = tk.Frame(root, bg="#081229")
title_frame.pack(fill="x", pady=10)

title = tk.Label(
    title_frame,
    text="🏭 AI PLANT 2035 ENTERPRISE DIGITAL TWIN",
    font=("Segoe UI", 28, "bold"),
    fg="white",
    bg="#081229"
)
title.pack(side="left", padx=25)

clock_label = tk.Label(
    title_frame,
    textvariable=clock_var,
    font=("Segoe UI", 16, "bold"),
    fg="#22c55e",
    bg="#081229"
)
clock_label.pack(side="right", padx=30)

# =====================================
# KPI CARDS
# =====================================

top_frame = tk.Frame(root, bg="#081229")
top_frame.pack(pady=10)

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
# MAIN AREA
# =====================================

main_frame = tk.Frame(root, bg="#081229")
main_frame.pack(fill="both", expand=True)

# =====================================
# DIGITAL TWIN PANEL
# =====================================

plant_panel = tk.Frame(
    main_frame,
    bg="#111827",
    width=900,
    height=500,
    bd=3,
    relief="ridge"
)

plant_panel.pack(side="left", padx=15)
plant_panel.pack_propagate(False)

tk.Label(
    plant_panel,
    text="DIGITAL REFINERY FLOW",
    font=("Segoe UI",20,"bold"),
    fg="white",
    bg="#111827"
).pack(pady=10)

canvas = tk.Canvas(
    plant_panel,
    width=820,
    height=360,
    bg="#111827",
    highlightthickness=0
)

canvas.pack()

# Units

canvas.create_rectangle(40,140,150,240,fill="#2563eb")
canvas.create_text(95,190,text="CDU",fill="white",font=("Arial",18,"bold"))

canvas.create_rectangle(250,140,360,240,fill="#16a34a")
canvas.create_text(305,190,text="FCC",fill="white",font=("Arial",18,"bold"))

canvas.create_rectangle(460,140,570,240,fill="#ea580c")
canvas.create_text(515,190,text="HDT",fill="white",font=("Arial",18,"bold"))

canvas.create_rectangle(670,140,790,240,fill="#7c3aed")
canvas.create_text(730,190,text="PRODUCTS",fill="white",font=("Arial",14,"bold"))

canvas.create_line(150,190,250,190,fill="white",width=4,arrow=tk.LAST)
canvas.create_line(360,190,460,190,fill="white",width=4,arrow=tk.LAST)
canvas.create_line(570,190,670,190,fill="white",width=4,arrow=tk.LAST)

# =====================================
# RIGHT PANEL
# =====================================

right_panel = tk.Frame(main_frame, bg="#081229")
right_panel.pack(side="left", fill="y")

# =====================================
# AI ALERT PANEL
# =====================================

alert_frame = tk.Frame(
    right_panel,
    bg="#111827",
    width=500,
    height=200,
    bd=3,
    relief="ridge"
)

alert_frame.pack(pady=10)
alert_frame.pack_propagate(False)

tk.Label(
    alert_frame,
    text="AI DECISION ENGINE",
    font=("Segoe UI",18,"bold"),
    fg="white",
    bg="#111827"
).pack(pady=10)

alert_label = tk.Label(
    alert_frame,
    textvariable=ai_alert,
    font=("Segoe UI",14,"bold"),
    fg="#22c55e",
    bg="#111827",
    wraplength=420
)

alert_label.pack(pady=15)

# =====================================
# SENSOR PANEL
# =====================================

sensor_frame = tk.Frame(
    right_panel,
    bg="#111827",
    width=500,
    height=300,
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

tk.Label(sensor_frame,textvariable=temperature,font=("Segoe UI",13),fg="white",bg="#111827").pack(anchor="w",padx=20,pady=5)
tk.Label(sensor_frame,textvariable=pressure,font=("Segoe UI",13),fg="white",bg="#111827").pack(anchor="w",padx=20,pady=5)
tk.Label(sensor_frame,textvariable=flowrate,font=("Segoe UI",13),fg="white",bg="#111827").pack(anchor="w",padx=20,pady=5)
tk.Label(sensor_frame,textvariable=profit,font=("Segoe UI",13),fg="#22c55e",bg="#111827").pack(anchor="w",padx=20,pady=5)
tk.Label(sensor_frame,textvariable=plant_grade,font=("Segoe UI",13,"bold"),fg="#facc15",bg="#111827").pack(anchor="w",padx=20,pady=5)

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

# =====================================
# LIVE UPDATE ENGINE
# =====================================

def update_dashboard():

    temp = random.randint(320,380)
    press = round(random.uniform(10,16),2)
    flow = random.randint(120000,130000)
    prof = random.randint(2800000,3600000)

    temperature.set(f"Temperature : {temp} °C")
    pressure.set(f"Pressure : {press} bar")
    flowrate.set(f"Flow Rate : {flow:,} BPD")
    profit.set(f"Profit : ${prof:,}/month")

    if temp > 365:
        ai_alert.set("⚠ High Furnace Temperature Detected")
        plant_grade.set("Plant Grade : B")
    elif press > 14.5:
        ai_alert.set("⚠ High Pressure Warning")
        plant_grade.set("Plant Grade : B+")
    else:
        ai_alert.set("✅ Plant Operating Optimally")
        plant_grade.set("Plant Grade : A+")

    root.after(2000, update_dashboard)

# =====================================
# CLOCK
# =====================================

def update_clock():

    now = datetime.now()

    clock_var.set(
        now.strftime("%d-%b-%Y  %H:%M:%S")
    )

    root.after(1000, update_clock)

# =====================================
# START
# =====================================

update_dashboard()
update_clock()

root.mainloop()