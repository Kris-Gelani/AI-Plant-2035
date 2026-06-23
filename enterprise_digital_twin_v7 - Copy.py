import tkinter as tk
from tkinter import ttk, messagebox
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import numpy as np
import pandas as pd
import random
from datetime import datetime
import threading
import time
import sqlite3

try:
    from sklearn.ensemble import RandomForestRegressor
    from sklearn.linear_model import LinearRegression
    SKLEARN_AVAILABLE = True
except ImportError:
    SKLEARN_AVAILABLE = False

class AIPlant2035DigitalTwinV7:
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("AI PLANT 2035 - AUTONOMOUS AI REFINERY v7.0 | ExxonMobil • Shell • Reliance • Saudi Aramco")
        self.root.geometry("1920x1080")
        self.root.configure(bg="#081229")
        self.root.state('zoomed')

        self.conn = sqlite3.connect('plant_historian_v7.db')
        self.create_db()

        self.current_plant = "Reliance Jamnagar"
        self.plant_data = {
            "Reliance Jamnagar": {'Profit': 1245000, 'Carbon_Index': 42.3, 'Overall_Efficiency': 89.7},
            "ExxonMobil": {'Profit': 980000, 'Carbon_Index': 45.1, 'Overall_Efficiency': 87.2},
            "Shell": {'Profit': 1150000, 'Carbon_Index': 39.8, 'Overall_Efficiency': 91.4},
            "Saudi Aramco": {'Profit': 1420000, 'Carbon_Index': 37.5, 'Overall_Efficiency': 93.1}
        }

        self.sensor_data = {
            'CDU_Temp': 385.2, 'CDU_Press': 2.8, 'CDU_Flow': 1450,
            'FCC_Temp': 520.5, 'FCC_Press': 1.9, 'FCC_Flow': 920,
            'Hydro_Temp': 340.8, 'Hydro_Press': 85.4
        }

        self.maintenance_data = {
            'Pump_Health': 94.2, 'Compressor_Health': 87.8, 'Furnace_Health': 89.7
        }

        self.history = {k: [] for k in ['time', 'profit', 'temp', 'carbon', 'efficiency', 'maintenance']}
        self.alarms = []
        self.ai_decisions = []

        self.ai_recommendations = [
            "Increase FCC feed rate by 4.2% → Expected +1.8% Profit",
            "Reduce Furnace duty by 3% → Energy saving + Carbon reduction",
            "Optimize Hydrogen recycle rate"
        ]

        self.setup_ui()
        self.load_initial_data()
        self.start_auto_refresh()

    def create_db(self):
        cursor = self.conn.cursor()
        cursor.execute('''CREATE TABLE IF NOT EXISTS historian (
            timestamp TEXT, plant TEXT, profit REAL, cdu_temp REAL, 
            carbon REAL, efficiency REAL, pump_health REAL)''')
        self.conn.commit()

    def load_initial_data(self):
        now = datetime.now().strftime("%H:%M")
        for _ in range(15):
            self.history['time'].append(now)
            self.history['profit'].append(1.245)
            self.history['temp'].append(385)
            self.history['carbon'].append(42.3)
            self.history['efficiency'].append(89.7)
            self.history['maintenance'].append(92)

    def setup_ui(self):
        # Header
        header = tk.Frame(self.root, bg="#111827", height=90)
        header.pack(fill="x")
        header.pack_propagate(False)
        tk.Label(header, text="AI PLANT 2035", font=("Arial", 32, "bold"), bg="#111827", fg="#22ff88").pack(side="left", padx=30, pady=20)
        tk.Label(header, text="AUTONOMOUS AI REFINERY v7.0 • LIVE", font=("Arial", 16, "bold"), bg="#111827", fg="#22ff88").pack(side="left", padx=20)

        self.plant_var = tk.StringVar(value=self.current_plant)
        plant_combo = ttk.Combobox(header, textvariable=self.plant_var, values=list(self.plant_data.keys()), state="readonly", width=25)
        plant_combo.pack(side="left", padx=20)
        plant_combo.bind("<<ComboboxSelected>>", self.switch_plant)

        self.clock_label = tk.Label(header, text="", font=("Arial", 16), bg="#111827", fg="#a1a1aa")
        self.clock_label.pack(side="right", padx=30)
        self.update_clock()

        # Notebook for Multi-Plant
        self.notebook = ttk.Notebook(self.root)
        self.notebook.pack(fill="both", expand=True, padx=10, pady=10)

        # Main Dashboard Tab
        main_tab = tk.Frame(self.notebook, bg="#081229")
        self.notebook.add(main_tab, text="Main Control Room")

        main_frame = tk.Frame(main_tab, bg="#081229")
        main_frame.pack(fill="both", expand=True)

        # Left - Executive War Room
        left_panel = tk.Frame(main_frame, bg="#111827", width=340)
        left_panel.pack(side="left", fill="y", padx=(0, 10))
        left_panel.pack_propagate(False)

        tk.Label(left_panel, text="EXECUTIVE WAR ROOM", font=("Arial", 16, "bold"), bg="#111827", fg="white").pack(pady=12)
        self.exec_labels = {}
        items = ["Plant Grade", "Profit Grade", "Reliability", "ESG", "AI Grade", "Overall Score"]
        for item in items:
            f = tk.Frame(left_panel, bg="#1f2937")
            f.pack(fill="x", padx=15, pady=6)
            tk.Label(f, text=item, font=("Arial", 11), bg="#1f2937", fg="#9ca3af").pack(anchor="w", padx=12)
            self.exec_labels[item] = tk.Label(f, text="A+", font=("Arial", 18, "bold"), bg="#1f2937", fg="#22ff88")
            self.exec_labels[item].pack(anchor="e", padx=12)

        # Center - Digital Twin
        center_panel = tk.Frame(main_frame, bg="#111827")
        center_panel.pack(side="left", fill="both", expand=True, padx=10)

        tk.Label(center_panel, text="3D PID & PFD DIGITAL TWIN", font=("Arial", 16, "bold"), bg="#111827", fg="white").pack(pady=8)
        self.canvas = tk.Canvas(center_panel, bg="#0a1428", height=480, highlightthickness=0)
        self.canvas.pack(fill="both", expand=True, padx=15, pady=5)
        self.draw_process_flow()

        # Simulator Controls
        sim_frame = tk.Frame(center_panel, bg="#1f2937")
        sim_frame.pack(fill="x", padx=15, pady=8)
        tk.Label(sim_frame, text="AUTONOMOUS AI SIMULATOR", font=("Arial", 14, "bold"), bg="#1f2937", fg="#eab308").pack(pady=5)
        btn_frame = tk.Frame(sim_frame, bg="#1f2937")
        btn_frame.pack()
        for text, cmd in [("+10% Feed", self.sim_feed_plus), ("-10% Feed", self.sim_feed_minus), 
                         ("Crude Change", self.sim_crude_switch), ("Emergency Shutdown", self.sim_shutdown)]:
            tk.Button(btn_frame, text=text, command=cmd, bg="#22ff88" if "Feed" in text else "#ef4444" if "Shutdown" in text else "#60a5fa", fg="black" if "Feed" in text else "white").pack(side="left", padx=5)

        # Right Panel
        right_panel = tk.Frame(main_frame, bg="#111827", width=380)
        right_panel.pack(side="right", fill="y")
        right_panel.pack_propagate(False)

        # Autonomous AI Decisions
        tk.Label(right_panel, text="AUTONOMOUS AI CORE", font=("Arial", 15, "bold"), bg="#111827", fg="#22ff88").pack(pady=10)
        self.decision_text = tk.Text(right_panel, bg="#1f2937", fg="#67e8f9", height=10, font=("Arial", 11))
        self.decision_text.pack(fill="both", expand=True, padx=12, pady=5)

        # AI Copilot
        tk.Label(right_panel, text="INDUSTRIAL AI COPILOT", font=("Arial", 14, "bold"), bg="#111827", fg="#c084fc").pack(pady=(15,5))
        self.chat_entry = tk.Entry(right_panel, bg="#1f2937", fg="white", font=("Arial", 11))
        self.chat_entry.pack(fill="x", padx=12, pady=5)
        self.chat_entry.bind("<Return>", self.copilot_response)
        self.chat_log = tk.Text(right_panel, bg="#1f2937", fg="#a5f3fc", height=8, font=("Arial", 10))
        self.chat_log.pack(fill="both", expand=True, padx=12, pady=5)

        # Alarm Management
        tk.Label(right_panel, text="ALARM MANAGEMENT", font=("Arial", 14, "bold"), bg="#111827", fg="#ef4444").pack(pady=(15,5))
        self.alarm_list = tk.Listbox(right_panel, bg="#1f2937", fg="#fda4af", height=8)
        self.alarm_list.pack(fill="both", expand=True, padx=12, pady=5)
        tk.Button(right_panel, text="Acknowledge All", command=self.acknowledge_alarms, bg="#eab308").pack(pady=5)

        # Bottom Graphs
        bottom = tk.Frame(self.root, bg="#111827", height=340)
        bottom.pack(fill="x", side="bottom", padx=12, pady=8)
        graph_frame = tk.Frame(bottom, bg="#111827")
        graph_frame.pack(fill="both", expand=True)

        self.figures = []
        self.axes = []
        self.canvases = []
        titles = ["Profit", "Carbon", "Efficiency", "Maintenance"]
        for i in range(4):
            fig, ax = plt.subplots(figsize=(5, 2.6), facecolor="#111827")
            ax.set_facecolor("#1f2937")
            ax.set_title(titles[i], color="white", fontsize=11)
            canvas = FigureCanvasTkAgg(fig, graph_frame)
            canvas.get_tk_widget().pack(side="left", fill="both", expand=True, padx=6)
            self.figures.append(fig)
            self.axes.append(ax)
            self.canvases.append(canvas)

        self.update_graphs()

        # Footer
        footer = tk.Frame(self.root, bg="#081229", height=35)
        footer.pack(fill="x", side="bottom")
        tk.Label(footer, text="© 2035 xAI Industrial • Autonomous AI Refinery v7.0 • 3482 Sensors • AI Confidence 99.9%", bg="#081229", fg="#64748b", font=("Arial", 10)).pack(pady=8)

    def draw_process_flow(self):
        self.canvas.delete("all")
        for i in range(0, 1400, 40):
            self.canvas.create_line(i, 0, i, 480, fill="#1e2937")
        for i in range(0, 480, 40):
            self.canvas.create_line(0, i, 1400, i, fill="#1e2937")

        units = [("CDU", 80, 90), ("FCC", 380, 60), ("Hydrotreater", 720, 150)]
        for name, x, y in units:
            self.canvas.create_rectangle(x, y, x+190, y+160, fill="#1e40af", outline="#60a5fa", width=5)
            self.canvas.create_text(x+95, y+80, text=name, fill="white", font=("Arial", 14, "bold"))

        self.canvas.create_line(270, 170, 380, 135, fill="#67e8f9", width=10, arrow=tk.LAST)
        self.canvas.create_line(570, 135, 720, 220, fill="#67e8f9", width=10, arrow=tk.LAST)

    def switch_plant(self, event=None):
        self.current_plant = self.plant_var.get()
        self.refresh_all()

    def update_clock(self):
        self.clock_label.config(text=datetime.now().strftime("%H:%M:%S | %d %b %Y"))
        self.root.after(1000, self.update_clock)

    def simulate_data(self):
        self.sensor_data['Profit'] += random.uniform(-18000, 35000)
        self.sensor_data['Carbon_Index'] += random.uniform(-0.8, 0.8)

        for k in self.maintenance_data:
            self.maintenance_data[k] = max(70, min(99, self.maintenance_data[k] + random.uniform(-1.2, 1.0)))

        # Autonomous Decision
        decision = random.choice(["Increase Feed Rate", "Reduce Furnace Duty", "Optimize H2 Recycle", "Maintain Current"])
        reason = "Based on real-time profit and carbon optimization"
        self.ai_decisions = [f"DECISION: {decision}\nReason: {reason}\nConfidence: {random.randint(92,99)}%"]

        # Historian
        cursor = self.conn.cursor()
        cursor.execute("INSERT INTO historian VALUES (?,?,?,?,?,?,?,?)", 
            (datetime.now().isoformat(), self.current_plant, self.sensor_data['Profit'], 
             self.sensor_data['CDU_Temp'], self.sensor_data['Carbon_Index'], 89.5, 92.0))
        self.conn.commit()

        now = datetime.now().strftime("%H:%M")
        self.history['time'].append(now)
        self.history['profit'].append(self.sensor_data['Profit']/1000000)
        self.history['temp'].append(self.sensor_data['CDU_Temp'])
        self.history['carbon'].append(self.sensor_data['Carbon_Index'])
        self.history['efficiency'].append(89.7)
        self.history['maintenance'].append(91)

        if len(self.history['time']) > 30:
            for k in self.history:
                self.history[k] = self.history[k][-30:]

        # Random Alarm
        if random.random() < 0.18:
            self.alarms.append(f"[{datetime.now().strftime('%H:%M')}] HIGH TEMP FCC")
            self.alarm_list.insert(0, self.alarms[-1])

    def update_ui(self):
        self.decision_text.delete(1.0, tk.END)
        for d in self.ai_decisions:
            self.decision_text.insert(tk.END, d + "\n\n")

        self.exec_labels["Overall Score"].config(text=f"{int(random.uniform(88,95))}")

    def update_graphs(self):
        titles = ["Profit Trend", "Carbon Trend", "Efficiency", "Maintenance"]
        keys = ['profit', 'carbon', 'efficiency', 'maintenance']
        colors = ["#22ff88", "#f87171", "#67e8f9", "#fbbf24"]
        for i, ax in enumerate(self.axes):
            ax.clear()
            ax.plot(self.history['time'], self.history[keys[i]], color=colors[i], linewidth=3, marker='o')
            ax.set_title(titles[i], color="white", fontsize=11)
            ax.tick_params(colors="#9ca3af")
            ax.grid(True, alpha=0.2)
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
                    time.sleep(2.5)
                except:
                    break
        threading.Thread(target=loop, daemon=True).start()

    def sim_feed_plus(self):
        self.sensor_data['FCC_Flow'] += 95
        messagebox.showinfo("Autonomous Action", "Feed increased +10%")

    def sim_feed_minus(self):
        self.sensor_data['FCC_Flow'] -= 95
        messagebox.showinfo("Autonomous Action", "Feed decreased -10%")

    def sim_crude_switch(self):
        self.sensor_data['Carbon_Index'] -= 4
        messagebox.showinfo("Autonomous Action", "Crude blend optimized")

    def sim_shutdown(self):
        messagebox.showwarning("Safety System", "Safe Shutdown Sequence Initiated")

    def copilot_response(self, event=None):
        query = self.chat_entry.get().strip().lower()
        self.chat_entry.delete(0, tk.END)
        resp = "AI Copilot: "
        if "profit" in query:
            resp += "Profit dropped due to FCC conversion. Increasing feed rate recommended."
        elif "carbon" in query:
            resp += "Carbon increased. Reducing furnace duty and optimizing heat recovery."
        elif "maintenance" in query or "failure" in query:
            resp += "Compressor health declining. Schedule predictive maintenance."
        else:
            resp += "System optimized. Current parameters are within optimal range."
        self.chat_log.insert(tk.END, resp + "\n\n")
        self.chat_log.see(tk.END)

    def acknowledge_alarms(self):
        self.alarm_list.delete(0, tk.END)
        self.alarms.clear()
        messagebox.showinfo("Alarms", "All alarms acknowledged")

    def run(self):
        self.root.mainloop()


if __name__ == "__main__":
    app = AIPlant2035DigitalTwinV7()
    app.run()