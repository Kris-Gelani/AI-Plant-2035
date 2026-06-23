import tkinter as tk
from tkinter import ttk, messagebox, scrolledtext
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import numpy as np
import pandas as pd
import random
from datetime import datetime
import threading
import time
import sqlite3
import json

class AIPlant2035DigitalTwinV10:
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("AI PLANT 2035 - AUTONOMOUS AI ENERGY ENTERPRISE v10.0 | ExxonMobil • Shell • Reliance • Saudi Aramco")
        self.root.geometry("1920x1080")
        self.root.configure(bg="#081229")
        self.root.state('zoomed')

        self.conn = sqlite3.connect('enterprise_historian_v10.db')
        self.create_db()

        self.plants = ["Reliance Jamnagar", "ExxonMobil Baytown", "Shell Pernis", "Saudi Aramco Abqaiq", "IOC Panipat", "BP Rotterdam", "Chevron Pascagoula", "TotalEnergies Antwerp"]
        self.current_plant = self.plants[0]

        self.sensor_data = {
            'CDU_Temp': 385.2, 'CDU_Press': 2.8, 'CDU_Flow': 1450,
            'FCC_Temp': 520.5, 'FCC_Press': 1.9, 'FCC_Flow': 920,
            'Hydro_Temp': 340.8, 'Hydro_Press': 85.4, 'Hydro_Flow': 680,
            'Profit': 1245000, 'Carbon_Index': 42.3, 'Plant_Health': 96.5
        }

        self.maintenance_data = {'Pump': 94.2, 'Compressor': 87.8, 'Furnace': 89.7, 'Valve': 95.1}
        self.history = {k: [] for k in ['time', 'profit', 'temp', 'carbon', 'efficiency', 'maintenance']}
        self.alarms = []
        self.ai_decisions = []

        self.setup_ui()
        self.load_initial_data()
        self.start_auto_refresh()

    def create_db(self):
        cursor = self.conn.cursor()
        cursor.execute('''CREATE TABLE IF NOT EXISTS historian (
            timestamp TEXT, plant TEXT, profit REAL, cdu_temp REAL, carbon REAL, 
            efficiency REAL, maintenance REAL)''')
        self.conn.commit()

    def load_initial_data(self):
        now = datetime.now().strftime("%H:%M")
        for _ in range(20):
            self.history['time'].append(now)
            self.history['profit'].append(1.245)
            self.history['temp'].append(385)
            self.history['carbon'].append(42.3)
            self.history['efficiency'].append(89.7)
            self.history['maintenance'].append(92)

    def setup_ui(self):
        # Header
        header = tk.Frame(self.root, bg="#111827", height=95)
        header.pack(fill="x")
        header.pack_propagate(False)
        tk.Label(header, text="AI PLANT 2035", font=("Arial", 34, "bold"), bg="#111827", fg="#22ff88").pack(side="left", padx=30, pady=22)
        tk.Label(header, text="AUTONOMOUS AI ENERGY ENTERPRISE v10.0", font=("Arial", 16, "bold"), bg="#111827", fg="#22ff88").pack(side="left", padx=20)

        self.plant_combo = ttk.Combobox(header, values=self.plants, state="readonly", width=28)
        self.plant_combo.set(self.current_plant)
        self.plant_combo.pack(side="left", padx=30)
        self.plant_combo.bind("<<ComboboxSelected>>", self.switch_plant)

        self.clock_label = tk.Label(header, text="", font=("Arial", 16), bg="#111827", fg="#a1a1aa")
        self.clock_label.pack(side="right", padx=40)
        self.update_clock()

        # Main Notebook
        self.notebook = ttk.Notebook(self.root)
        self.notebook.pack(fill="both", expand=True, padx=12, pady=12)

        # Tab 1: Main Control Room
        main_tab = tk.Frame(self.notebook, bg="#081229")
        self.notebook.add(main_tab, text="Main Control Room")

        main_frame = tk.Frame(main_tab, bg="#081229")
        main_frame.pack(fill="both", expand=True, padx=8, pady=8)

        # Left - Executive War Room
        left = tk.Frame(main_frame, bg="#111827", width=340)
        left.pack(side="left", fill="y", padx=(0,8))
        left.pack_propagate(False)

        tk.Label(left, text="EXECUTIVE WAR ROOM", font=("Arial", 17, "bold"), bg="#111827", fg="white").pack(pady=15)
        self.exec_labels = {}
        for item in ["Plant Grade", "Profit Grade", "Carbon Grade", "Safety Grade", "Reliability", "ESG", "AI Grade", "Overall"]:
            f = tk.Frame(left, bg="#1f2937")
            f.pack(fill="x", padx=15, pady=6)
            tk.Label(f, text=item, bg="#1f2937", fg="#9ca3af", font=("Arial", 11)).pack(anchor="w", padx=15)
            self.exec_labels[item] = tk.Label(f, text="A+", bg="#1f2937", fg="#22ff88", font=("Arial", 18, "bold"))
            self.exec_labels[item].pack(anchor="e", padx=15)

        # Center - Digital Twin
        center = tk.Frame(main_frame, bg="#111827")
        center.pack(side="left", fill="both", expand=True, padx=8)

        tk.Label(center, text="INDUSTRIAL METAVERSE DIGITAL TWIN", font=("Arial", 17, "bold"), bg="#111827", fg="white").pack(pady=10)
        self.canvas = tk.Canvas(center, bg="#0a1428", height=520, highlightthickness=0)
        self.canvas.pack(fill="both", expand=True, padx=15, pady=8)
        self.draw_process_flow()

        # Simulator
        simf = tk.Frame(center, bg="#1f2937")
        simf.pack(fill="x", padx=15, pady=8)
        tk.Label(simf, text="AUTONOMOUS AI SIMULATOR", font=("Arial", 14, "bold"), bg="#1f2937", fg="#eab308").pack()
        bf = tk.Frame(simf, bg="#1f2937")
        bf.pack(pady=8)
        for txt, cmd in [("+10% Feed", self.sim_feed_plus), ("-10% Feed", self.sim_feed_minus), ("Crude Switch", self.sim_crude_switch), ("Emergency SD", self.sim_shutdown)]:
            tk.Button(bf, text=txt, command=cmd, width=14, bg="#22ff88" if "+" in txt else "#ef4444").pack(side="left", padx=6)

        # Right Panel
        right = tk.Frame(main_frame, bg="#111827", width=390)
        right.pack(side="right", fill="y")
        right.pack_propagate(False)

        # Autonomous AI Core
        tk.Label(right, text="AUTONOMOUS AI CORE", font=("Arial", 15, "bold"), bg="#111827", fg="#22ff88").pack(pady=12)
        self.decision_text = tk.Text(right, bg="#1f2937", fg="#67e8f9", height=9, font=("Arial", 11))
        self.decision_text.pack(fill="x", padx=12, pady=6)

        # AI Copilot
        tk.Label(right, text="ENTERPRISE AI COPILOT", font=("Arial", 15, "bold"), bg="#111827", fg="#c084fc").pack(pady=(20,6))
        self.chat_entry = tk.Entry(right, bg="#1f2937", fg="white", font=("Arial", 11))
        self.chat_entry.pack(fill="x", padx=12, pady=4)
        self.chat_entry.bind("<Return>", self.copilot_response)
        self.chat_log = tk.Text(right, bg="#1f2937", fg="#bae6fd", height=9, font=("Arial", 10))
        self.chat_log.pack(fill="both", expand=True, padx=12, pady=6)

        # Alarms
        tk.Label(right, text="ALARM MANAGEMENT", font=("Arial", 14, "bold"), bg="#111827", fg="#ef4444").pack(pady=(15,5))
        self.alarm_list = tk.Listbox(right, bg="#1f2937", fg="#fda4af", height=7)
        self.alarm_list.pack(fill="x", padx=12, pady=5)
        tk.Button(right, text="Acknowledge All", command=self.ack_all_alarms, bg="#eab308", fg="black").pack(pady=5)

        # Bottom Graphs
        bottom = tk.Frame(self.root, bg="#111827", height=360)
        bottom.pack(fill="x", side="bottom", padx=12, pady=10)
        gframe = tk.Frame(bottom, bg="#111827")
        gframe.pack(fill="both", expand=True)

        self.figures, self.axes, self.canvases = [], [], []
        titles = ["Profit", "Carbon", "Efficiency", "Maintenance", "Reliability", "Energy"]
        for i in range(6):
            fig, ax = plt.subplots(figsize=(4.2, 2.4), facecolor="#111827")
            ax.set_facecolor("#1f2937")
            ax.set_title(titles[i], color="white", fontsize=10)
            c = FigureCanvasTkAgg(fig, gframe)
            c.get_tk_widget().pack(side="left", fill="both", expand=True, padx=5)
            self.figures.append(fig)
            self.axes.append(ax)
            self.canvases.append(c)

        self.update_graphs()

        # Footer
        footer = tk.Frame(self.root, bg="#081229", height=38)
        footer.pack(fill="x", side="bottom")
        tk.Label(footer, text="© 2035 xAI Industrial • Autonomous AI Energy Enterprise v10.0 • 4286 Sensors Online • AI Confidence 99.9%", bg="#081229", fg="#64748b", font=("Arial", 10)).pack(pady=9)

    def draw_process_flow(self):
        self.canvas.delete("all")
        for i in range(0, 1450, 35):
            self.canvas.create_line(i, 0, i, 520, fill="#1e2937", width=1)
        for i in range(0, 520, 35):
            self.canvas.create_line(0, i, 1450, i, fill="#1e2937", width=1)

        # Units
        units = [("Storage", 60, 80), ("CDU", 280, 90), ("FCC", 520, 70), ("Hydrotreater", 780, 160), ("Products", 1050, 110)]
        for name, x, y in units:
            color = "#1e40af" if "CDU" in name else "#7e22ce" if "FCC" in name else "#166534"
            self.canvas.create_rectangle(x, y, x+170, y+150, fill=color, outline="#60a5fa", width=4)
            self.canvas.create_text(x+85, y+75, text=name, fill="white", font=("Arial", 13, "bold"))

        # Flow lines
        self.canvas.create_line(230, 155, 280, 135, fill="#67e8f9", width=9, arrow=tk.LAST)
        self.canvas.create_line(450, 135, 520, 165, fill="#67e8f9", width=9, arrow=tk.LAST)
        self.canvas.create_line(690, 165, 780, 210, fill="#67e8f9", width=9, arrow=tk.LAST)

    def switch_plant(self, e=None):
        self.current_plant = self.plant_combo.get()
        self.refresh_all()

    def update_clock(self):
        self.clock_label.config(text=datetime.now().strftime("%H:%M:%S | %d %b %Y"))
        self.root.after(1000, self.update_clock)

    def simulate_data(self):
        self.sensor_data['Profit'] += random.uniform(-22000, 42000)
        self.sensor_data['Carbon_Index'] += random.uniform(-0.9, 0.9)
        for k in self.maintenance_data:
            self.maintenance_data[k] = max(68, min(99.5, self.maintenance_data[k] + random.uniform(-1.4, 1.1)))

        # Autonomous AI Decision
        decisions = ["Increase FCC Feed", "Reduce Furnace Duty", "Optimize Hydrogen", "Maintain Steady State", "Crude Blend Adjustment"]
        d = random.choice(decisions)
        self.ai_decisions = [f"ACTION: {d}\nReason: Real-time optimization for profit & emissions\nConfidence: {random.randint(93,99)}%\nImpact: +{random.randint(1,4)}% Profit / -{random.randint(1,6)}% Carbon"]

        # Historian
        cursor = self.conn.cursor()
        cursor.execute("INSERT INTO historian VALUES (?,?,?,?,?,?,?)", 
            (datetime.now().isoformat(), self.current_plant, self.sensor_data['Profit'], 
             self.sensor_data['CDU_Temp'], self.sensor_data['Carbon_Index'], 89.8, 91.5))
        self.conn.commit()

        now = datetime.now().strftime("%H:%M")
        self.history['time'].append(now)
        self.history['profit'].append(self.sensor_data['Profit']/1000000)
        self.history['temp'].append(self.sensor_data['CDU_Temp'])
        self.history['carbon'].append(self.sensor_data['Carbon_Index'])
        self.history['efficiency'].append(random.uniform(87, 94))
        self.history['maintenance'].append(sum(self.maintenance_data.values())/len(self.maintenance_data))

        if len(self.history['time']) > 35:
            for k in self.history:
                self.history[k] = self.history[k][-35:]

        if random.random() < 0.22:
            self.alarms.append(f"[{datetime.now().strftime('%H:%M')}] HIGH TEMP - FCC")
            self.alarm_list.insert(0, self.alarms[-1])
            if self.alarm_list.size() > 10:
                self.alarm_list.delete(10)

    def update_ui(self):
        self.decision_text.delete(1.0, tk.END)
        for d in self.ai_decisions:
            self.decision_text.insert(tk.END, d + "\n\n")

        for item in self.exec_labels:
            self.exec_labels[item].config(text=random.choice(["A+", "A", "A-"]))

    def update_graphs(self):
        titles = ["Profit", "Carbon", "Efficiency", "Maintenance", "Reliability", "Energy"]
        keys = ['profit', 'carbon', 'efficiency', 'maintenance', 'maintenance', 'maintenance']
        colors = ["#22ff88", "#f87171", "#67e8f9", "#fbbf24", "#c084fc", "#eab308"]
        for i, ax in enumerate(self.axes):
            ax.clear()
            ax.plot(self.history['time'], self.history[keys[i]], color=colors[i], linewidth=3, marker='o', markersize=4)
            ax.set_title(titles[i], color="white", fontsize=11)
            ax.tick_params(colors="#9ca3af")
            ax.grid(True, alpha=0.25)
            self.figures[i].tight_layout()
            self.canvases[i].draw()

    def refresh_all(self):
        self.simulate_data()
        self.update_ui()
        self.update_graphs()

    def start_auto_refresh(self):
        def loop():
            while True:
                try:
                    self.root.after(0, self.refresh_all)
                    time.sleep(2.4)
                except:
                    break
        threading.Thread(target=loop, daemon=True).start()

    def sim_feed_plus(self):
        self.sensor_data['FCC_Flow'] += 110
        messagebox.showinfo("Autonomous Action", "FCC Feed +10% - Profit impact positive")

    def sim_feed_minus(self):
        self.sensor_data['FCC_Flow'] -= 110
        messagebox.showinfo("Autonomous Action", "FCC Feed -10%")

    def sim_crude_switch(self):
        self.sensor_data['Carbon_Index'] -= 4.5
        messagebox.showinfo("Autonomous Action", "Crude blend optimized for lower carbon")

    def sim_shutdown(self):
        messagebox.showwarning("Safety", "Autonomous Safe Shutdown Sequence Initiated")

    def copilot_response(self, event=None):
        q = self.chat_entry.get().strip().lower()
        self.chat_entry.delete(0, tk.END)
        if "profit" in q:
            r = "Profit decreased due to FCC conversion drop. Recommendation: Increase feed rate by 6%."
        elif "carbon" in q:
            r = "Carbon increased. Reduce furnace duty by 4% and improve heat integration."
        elif "failure" in q or "maintenance" in q:
            r = "Compressor health declining. Predictive maintenance recommended within 36 hours."
        elif "fcc" in q:
            r = "FCC optimization: Increase reactor temperature by 8°C for higher gasoline yield."
        else:
            r = "System operating optimally. Current parameters within target range."
        self.chat_log.insert(tk.END, f"AI Copilot: {r}\n\n")
        self.chat_log.see(tk.END)

    def ack_all_alarms(self):
        self.alarm_list.delete(0, tk.END)
        self.alarms.clear()

    def run(self):
        self.root.mainloop()


if __name__ == "__main__":
    app = AIPlant2035DigitalTwinV10()
    app.run()