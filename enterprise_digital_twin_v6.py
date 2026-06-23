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

class AIPlant2035DigitalTwinV6:
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("AI PLANT 2035 - Enterprise Digital Twin v6.0 | ExxonMobil • Shell • Reliance • Saudi Aramco")
        self.root.geometry("1920x1080")
        self.root.configure(bg="#081229")
        self.root.state('zoomed')

        self.conn = sqlite3.connect('plant_historian_v6.db')
        self.create_db()

        self.sensor_data = {
            'CDU_Temp': 385.2, 'CDU_Press': 2.8, 'CDU_Flow': 1450,
            'FCC_Temp': 520.5, 'FCC_Press': 1.9, 'FCC_Flow': 920,
            'Hydro_Temp': 340.8, 'Hydro_Press': 85.4, 'Hydro_Flow': 680,
            'Profit': 1245000, 'Carbon_Index': 42.3, 'Plant_Health': 96.5
        }

        self.maintenance_data = {
            'Pump_Health': 94.2, 'Compressor_Health': 87.8, 'HeatEx_Health': 91.5,
            'Furnace_Health': 89.7, 'Valve_Health': 95.1
        }

        self.optimization_data = {
            'Dist_Efficiency': 96.4, 'FCC_Conversion': 78.9, 'Hydro_Efficiency': 94.2,
            'Overall_Efficiency': 89.7, 'Energy_Eff': 91.3
        }

        self.history = {k: [] for k in ['time', 'profit', 'temp', 'carbon', 'efficiency', 'energy', 'maintenance']}
        self.alarms = []

        self.ai_recommendations = [
            "Increase FCC feed rate by 4.2% → +1.8% Profit",
            "Reduce Furnace duty by 3% → Energy saving",
            "Optimize Hydrogen recycle → +1.8% recovery"
        ]

        self.setup_ui()
        self.load_initial_data()
        self.start_auto_refresh()

    def create_db(self):
        cursor = self.conn.cursor()
        cursor.execute('''CREATE TABLE IF NOT EXISTS historian (
            timestamp TEXT, profit REAL, cdu_temp REAL, cdu_press REAL, 
            fcc_flow REAL, carbon REAL, efficiency REAL, pump_health REAL)''')
        self.conn.commit()

    def load_initial_data(self):
        now = datetime.now().strftime("%H:%M")
        for _ in range(12):
            self.history['time'].append(now)
            self.history['profit'].append(1.245)
            self.history['temp'].append(385)
            self.history['carbon'].append(42.3)
            self.history['efficiency'].append(89.7)
            self.history['energy'].append(91.3)
            self.history['maintenance'].append(92)

    def setup_ui(self):
        # Header
        header = tk.Frame(self.root, bg="#111827", height=90)
        header.pack(fill="x")
        header.pack_propagate(False)
        tk.Label(header, text="AI PLANT 2035", font=("Arial", 32, "bold"), bg="#111827", fg="#22ff88").pack(side="left", padx=30, pady=20)
        tk.Label(header, text="ENTERPRISE DIGITAL TWIN v6.0 • LIVE", font=("Arial", 16, "bold"), bg="#111827", fg="#22ff88").pack(side="left", padx=20)
        self.clock_label = tk.Label(header, text="", font=("Arial", 16), bg="#111827", fg="#a1a1aa")
        self.clock_label.pack(side="right", padx=30)
        self.update_clock()

        main_frame = tk.Frame(self.root, bg="#081229")
        main_frame.pack(fill="both", expand=True, padx=10, pady=10)

        # Left Panel - Executive + ROS
        left_panel = tk.Frame(main_frame, bg="#111827", width=340)
        left_panel.pack(side="left", fill="y", padx=(0, 10))
        left_panel.pack_propagate(False)

        tk.Label(left_panel, text="EXECUTIVE DASHBOARD", font=("Arial", 16, "bold"), bg="#111827", fg="white").pack(pady=12)
        self.exec_labels = {}
        exec_items = ["Plant Grade", "Profit Score", "Reliability", "ESG Score", "AI Maturity", "Overall Score"]
        for item in exec_items:
            f = tk.Frame(left_panel, bg="#1f2937")
            f.pack(fill="x", padx=15, pady=5)
            tk.Label(f, text=item, font=("Arial", 11), bg="#1f2937", fg="#9ca3af").pack(anchor="w", padx=12)
            self.exec_labels[item] = tk.Label(f, text="A+", font=("Arial", 17, "bold"), bg="#1f2937", fg="#22ff88")
            self.exec_labels[item].pack(anchor="e", padx=12)

        # ROS Status
        tk.Label(left_panel, text="REFINERY OPERATING SYSTEM", font=("Arial", 15, "bold"), bg="#111827", fg="#eab308").pack(pady=(20,8))
        status_items = ["Plant Status", "Operations", "Utility", "Reliability", "Production"]
        for item in status_items:
            f = tk.Frame(left_panel, bg="#1f2937")
            f.pack(fill="x", padx=15, pady=4)
            tk.Label(f, text=item, bg="#1f2937", fg="#9ca3af").pack(side="left", padx=12)
            tk.Label(f, text="NORMAL", fg="#22ff88", font=("Arial", 11, "bold"), bg="#1f2937").pack(side="right", padx=12)

        # Center - Digital Twin
        center_panel = tk.Frame(main_frame, bg="#111827")
        center_panel.pack(side="left", fill="both", expand=True, padx=10)

        tk.Label(center_panel, text="PID & PFD DIGITAL TWIN", font=("Arial", 16, "bold"), bg="#111827", fg="white").pack(pady=8)
        self.canvas = tk.Canvas(center_panel, bg="#0a1428", height=460, highlightthickness=0)
        self.canvas.pack(fill="both", expand=True, padx=15, pady=5)
        self.draw_process_flow()

        # Simulator
        sim_frame = tk.Frame(center_panel, bg="#1f2937")
        sim_frame.pack(fill="x", padx=15, pady=8)
        tk.Label(sim_frame, text="AI DIGITAL TWIN SIMULATOR", font=("Arial", 14, "bold"), bg="#1f2937", fg="#eab308").pack(pady=5)
        btns = tk.Frame(sim_frame, bg="#1f2937")
        btns.pack()
        tk.Button(btns, text="+10% Feed", command=self.sim_feed_plus, bg="#22ff88", fg="black").pack(side="left", padx=4)
        tk.Button(btns, text="-10% Feed", command=self.sim_feed_minus, bg="#fbbf24", fg="black").pack(side="left", padx=4)
        tk.Button(btns, text="Crude Change", command=self.sim_crude_switch, bg="#60a5fa", fg="black").pack(side="left", padx=4)
        tk.Button(btns, text="Emergency Shutdown", command=self.sim_shutdown, bg="#ef4444", fg="white").pack(side="left", padx=4)

        # Right Panel
        right_panel = tk.Frame(main_frame, bg="#111827", width=380)
        right_panel.pack(side="right", fill="y")
        right_panel.pack_propagate(False)

        # Predictive Maintenance
        tk.Label(right_panel, text="PREDICTIVE MAINTENANCE AI", font=("Arial", 15, "bold"), bg="#111827", fg="#f87171").pack(pady=10)
        self.maint_labels = {}
        for eq in ["Pump", "Compressor", "Heat Exchanger", "Furnace", "Valve"]:
            f = tk.Frame(right_panel, bg="#1f2937")
            f.pack(fill="x", padx=12, pady=5)
            tk.Label(f, text=eq, bg="#1f2937", fg="#93c5fd", font=("Arial", 11, "bold")).pack(anchor="w", padx=12)
            hf = tk.Frame(f, bg="#1f2937")
            hf.pack(fill="x", padx=12)
            self.maint_labels[eq] = tk.Label(hf, text="92%", font=("Arial", 16, "bold"), bg="#1f2937", fg="#22ff88")
            self.maint_labels[eq].pack(side="left")

        # Advanced AI Prediction
        tk.Label(right_panel, text="AI PREDICTION CENTER", font=("Arial", 15, "bold"), bg="#111827", fg="#c084fc").pack(pady=(20,8))
        pred_frame = tk.Frame(right_panel, bg="#1f2937")
        pred_frame.pack(fill="x", padx=12, pady=6)
        preds = ["Profit Tomorrow", "Carbon Next Week", "Failure Risk"]
        for p in preds:
            f = tk.Frame(pred_frame, bg="#1f2937")
            f.pack(fill="x", padx=12, pady=3)
            tk.Label(f, text=p, bg="#1f2937", fg="#9ca3af").pack(anchor="w")
            tk.Label(f, text="+$28k / 41.2 / LOW", bg="#1f2937", fg="#67e8f9", font=("Arial", 11, "bold")).pack(anchor="e")

        # AI Copilot
        tk.Label(right_panel, text="AI COPILOT COMMAND", font=("Arial", 14, "bold"), bg="#111827", fg="#eab308").pack(pady=(20,5))
        self.chat_entry = tk.Entry(right_panel, bg="#1f2937", fg="white", font=("Arial", 11))
        self.chat_entry.pack(fill="x", padx=12, pady=5)
        self.chat_entry.bind("<Return>", self.copilot_response)
        self.chat_log = tk.Text(right_panel, bg="#1f2937", fg="#a5f3fc", height=7, font=("Arial", 10))
        self.chat_log.pack(fill="both", expand=True, padx=12, pady=5)

        # Alarms
        tk.Label(right_panel, text="ALARM MANAGEMENT", font=("Arial", 14, "bold"), bg="#111827", fg="#ef4444").pack(pady=(15,5))
        self.alarm_list = tk.Listbox(right_panel, bg="#1f2937", fg="#fda4af", height=6)
        self.alarm_list.pack(fill="x", padx=12, pady=5)

        # Bottom Graphs
        bottom = tk.Frame(self.root, bg="#111827", height=360)
        bottom.pack(fill="x", side="bottom", padx=12, pady=8)
        graph_frame = tk.Frame(bottom, bg="#111827")
        graph_frame.pack(fill="both", expand=True)

        self.figures = []
        self.axes = []
        self.canvases = []
        titles = ["Profit", "Carbon", "Efficiency", "Maintenance"]
        colors = ["#22ff88", "#f87171", "#67e8f9", "#fbbf24"]
        for i in range(4):
            fig, ax = plt.subplots(figsize=(5, 2.8), facecolor="#111827")
            ax.set_facecolor("#1f2937")
            ax.set_title(titles[i], color="white", fontsize=11)
            canvas = FigureCanvasTkAgg(fig, graph_frame)
            canvas.get_tk_widget().pack(side="left", fill="both", expand=True, padx=5)
            self.figures.append(fig)
            self.axes.append(ax)
            self.canvases.append(canvas)

        self.update_graphs()

        # Footer
        footer = tk.Frame(self.root, bg="#081229", height=35)
        footer.pack(fill="x", side="bottom")
        tk.Label(footer, text="© 2035 xAI Industrial • Digital Twin v6.0 • 3124 Sensors • AI Confidence 99.8%", bg="#081229", fg="#64748b", font=("Arial", 10)).pack(pady=8)

    def draw_process_flow(self):
        self.canvas.delete("all")
        for i in range(0, 1350, 40):
            self.canvas.create_line(i, 0, i, 460, fill="#1e2937")
        for i in range(0, 460, 40):
            self.canvas.create_line(0, i, 1350, i, fill="#1e2937")

        # Major Units
        units = [("CDU", 80, 90, "#1e40af"), ("FCC", 380, 60, "#7e22ce"), ("Hydrotreater", 720, 140, "#166534")]
        for name, x, y, color in units:
            self.canvas.create_rectangle(x, y, x+190, y+150, fill=color, outline="#60a5fa", width=4)
            self.canvas.create_text(x+95, y+75, text=name, fill="white", font=("Arial", 14, "bold"))

        # Flow lines with animation capability
        self.flow_lines = []
        self.flow_lines.append(self.canvas.create_line(270, 165, 380, 135, fill="#67e8f9", width=8, arrow=tk.LAST))
        self.flow_lines.append(self.canvas.create_line(570, 135, 720, 210, fill="#67e8f9", width=8, arrow=tk.LAST))

    def update_clock(self):
        self.clock_label.config(text=datetime.now().strftime("%H:%M:%S | %d %b %Y"))
        self.root.after(1000, self.update_clock)

    def simulate_data(self):
        self.sensor_data['Profit'] += random.uniform(-15000, 32000)
        self.sensor_data['Carbon_Index'] += random.uniform(-0.7, 0.7)
        self.sensor_data['Plant_Health'] = max(89, min(99.8, self.sensor_data['Plant_Health'] + random.uniform(-0.4, 0.35)))

        for k in self.maintenance_data:
            self.maintenance_data[k] = max(72, min(99, self.maintenance_data[k] + random.uniform(-1.1, 0.9)))

        self.optimization_data['Overall_Efficiency'] = max(85, min(95, self.optimization_data['Overall_Efficiency'] + random.uniform(-0.5, 0.6)))

        # Historian
        cursor = self.conn.cursor()
        cursor.execute("INSERT INTO historian VALUES (?,?,?,?,?,?,?,?)", 
            (datetime.now().isoformat(), self.sensor_data['Profit'], self.sensor_data['CDU_Temp'],
             self.sensor_data['CDU_Press'], self.sensor_data['FCC_Flow'], self.sensor_data['Carbon_Index'],
             self.optimization_data['Overall_Efficiency'], self.maintenance_data['Pump_Health']))
        self.conn.commit()

        now = datetime.now().strftime("%H:%M")
        self.history['time'].append(now)
        self.history['profit'].append(self.sensor_data['Profit']/1000000)
        self.history['temp'].append(self.sensor_data['CDU_Temp'])
        self.history['carbon'].append(self.sensor_data['Carbon_Index'])
        self.history['efficiency'].append(self.optimization_data['Overall_Efficiency'])
        self.history['energy'].append(self.optimization_data.get('Energy_Eff', 91))
        self.history['maintenance'].append(sum(self.maintenance_data.values())/len(self.maintenance_data))

        if len(self.history['time']) > 30:
            for k in self.history:
                self.history[k] = self.history[k][-30:]

        # Random alarm
        if random.random() < 0.15:
            self.alarms.append(f"HIGH TEMP {random.choice(['CDU','FCC'])}")
            self.alarm_list.insert(0, self.alarms[-1])
            if self.alarm_list.size() > 8:
                self.alarm_list.delete(8)

    def update_ui(self):
        # Maintenance
        for eq in self.maint_labels:
            h = self.maintenance_data.get(eq + "_Health", 88)
            col = "#22ff88" if h > 90 else "#fbbf24" if h > 80 else "#ef4444"
            self.maint_labels[eq].config(text=f"{h:.1f}%", fg=col)

        # Executive
        self.exec_labels["Overall Score"].config(text=f"{int(self.optimization_data['Overall_Efficiency'])}")
        self.exec_labels["Profit Score"].config(text="A")

    def update_graphs(self):
        titles = ["Profit Trend", "Carbon Trend", "Efficiency", "Maintenance"]
        keys = ['profit', 'carbon', 'efficiency', 'maintenance']
        colors = ["#22ff88", "#f87171", "#67e8f9", "#fbbf24"]
        for i, ax in enumerate(self.axes):
            ax.clear()
            ax.plot(self.history['time'], self.history[keys[i]], color=colors[i], linewidth=3, marker='o', markersize=3)
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
                    time.sleep(2.8)
                except:
                    break
        threading.Thread(target=loop, daemon=True).start()

    def sim_feed_plus(self):
        self.sensor_data['FCC_Flow'] += 92
        messagebox.showinfo("Simulator", "Feed increased +10%")

    def sim_feed_minus(self):
        self.sensor_data['FCC_Flow'] -= 92
        messagebox.showinfo("Simulator", "Feed decreased -10%")

    def sim_crude_switch(self):
        self.sensor_data['Carbon_Index'] -= 3.2
        messagebox.showinfo("Simulator", "Crude blend switched")

    def sim_shutdown(self):
        messagebox.showwarning("ALERT", "Emergency Shutdown Activated - All units safe")

    def copilot_response(self, event=None):
        query = self.chat_entry.get().strip().lower()
        self.chat_entry.delete(0, tk.END)
        if "profit" in query:
            resp = "Profit drop due to FCC conversion. Recommend increasing feed rate."
        elif "carbon" in query:
            resp = "Reduce carbon by lowering furnace duty and optimizing heat integration."
        elif "maintenance" in query or "failure" in query:
            resp = "Compressor RUL low. Schedule inspection within 48 hours."
        else:
            resp = "Optimizing parameters for maximum profitability and lowest emissions."
        self.chat_log.insert(tk.END, f"AI: {resp}\n\n")
        self.chat_log.see(tk.END)

    def run(self):
        self.root.mainloop()


if __name__ == "__main__":
    app = AIPlant2035DigitalTwinV6()
    app.run()