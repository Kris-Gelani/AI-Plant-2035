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

class AIPlant2035DigitalTwinV16:
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("AI PLANT 2035 - AUTONOMOUS AI ENERGY ENTERPRISE V16 | ExxonMobil • Shell • Reliance • Saudi Aramco")
        self.root.geometry("1920x1080")
        self.root.configure(bg="#061126")
        self.root.state('zoomed')

        self.conn = sqlite3.connect('ai_plant_v16.db')
        self.create_db()

        self.plants = ["Reliance Jamnagar", "ExxonMobil Baytown", "Shell Pernis", "Saudi Aramco Abqaiq", "BP Rotterdam", "Total Antwerp", "IOC Panipat", "Chevron Pascagoula"]
        self.current_plant = self.plants[0]

        self.sensor_data = {
            'CDU_Temp': 385.2, 'CDU_Press': 2.8, 'CDU_Flow': 1450,
            'FCC_Temp': 520.5, 'FCC_Press': 1.9, 'FCC_Flow': 920,
            'Hydro_Temp': 340.8, 'Hydro_Press': 85.4, 'Hydro_Flow': 680,
            'Profit': 1245000, 'Carbon_Index': 42.3, 'Plant_Health': 96.5
        }

        self.maintenance_data = {
            'Pump': {'health': 94.2, 'rul': 245, 'risk': 'Low'},
            'Compressor': {'health': 87.8, 'rul': 118, 'risk': 'Medium'},
            'Furnace': {'health': 89.7, 'rul': 142, 'risk': 'Medium'},
            'Valve': {'health': 95.1, 'rul': 289, 'risk': 'Low'}
        }

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
        header = tk.Frame(self.root, bg="#111827", height=100)
        header.pack(fill="x")
        header.pack_propagate(False)

        tk.Label(header, text="AI PLANT 2035", font=("Arial", 36, "bold"), bg="#111827", fg="#00ff99").pack(side="left", padx=40, pady=25)
        tk.Label(header, text="AUTONOMOUS AI ENERGY ENTERPRISE V16", font=("Arial", 18, "bold"), bg="#111827", fg="#00ff99").pack(side="left", padx=20)

        self.plant_combo = ttk.Combobox(header, values=self.plants, state="readonly", width=30, font=("Arial", 12))
        self.plant_combo.set(self.current_plant)
        self.plant_combo.pack(side="left", padx=30)
        self.plant_combo.bind("<<ComboboxSelected>>", self.switch_plant)

        self.clock_label = tk.Label(header, text="", font=("Arial", 16), bg="#111827", fg="#a1a1aa")
        self.clock_label.pack(side="right", padx=40)
        self.update_clock()

        tk.Label(header, text="AI CONFIDENCE: 99.8%", font=("Arial", 14, "bold"), bg="#111827", fg="#00ff99").pack(side="right", padx=30)

        # Main Frame
        main_frame = tk.Frame(self.root, bg="#061126")
        main_frame.pack(fill="both", expand=True, padx=12, pady=12)

        # Left Panel - Executive & Maintenance
        left_panel = tk.Frame(main_frame, bg="#111827", width=360)
        left_panel.pack(side="left", fill="y", padx=(0, 10))
        left_panel.pack_propagate(False)

        tk.Label(left_panel, text="CEO EXECUTIVE DASHBOARD", font=("Arial", 16, "bold"), bg="#111827", fg="white").pack(pady=15)

        self.exec_labels = {}
        exec_items = ["Profit Today", "Carbon Intensity", "ESG Score", "Reliability", "AI Maturity", "Overall Score"]
        for item in exec_items:
            f = tk.Frame(left_panel, bg="#1f2937", height=70)
            f.pack(fill="x", padx=15, pady=8)
            f.pack_propagate(False)
            tk.Label(f, text=item, font=("Arial", 11), bg="#1f2937", fg="#9ca3af").pack(anchor="w", padx=15, pady=8)
            self.exec_labels[item] = tk.Label(f, text="A+", font=("Arial", 20, "bold"), bg="#1f2937", fg="#00ff99")
            self.exec_labels[item].pack(anchor="e", padx=15)

        # Predictive Maintenance
        tk.Label(left_panel, text="PREDICTIVE MAINTENANCE AI", font=("Arial", 15, "bold"), bg="#111827", fg="#ffcc00").pack(pady=(25,10))
        self.maint_labels = {}
        for eq in ["Pump", "Compressor", "Furnace", "Valve"]:
            f = tk.Frame(left_panel, bg="#1f2937")
            f.pack(fill="x", padx=15, pady=6)
            tk.Label(f, text=eq, font=("Arial", 12, "bold"), bg="#1f2937", fg="#60a5fa").pack(anchor="w", padx=15)
            hf = tk.Frame(f, bg="#1f2937")
            hf.pack(fill="x", padx=15, pady=4)
            self.maint_labels[eq] = tk.Label(hf, text="94.2% | 245d", font=("Arial", 13, "bold"), bg="#1f2937", fg="#00ff99")
            self.maint_labels[eq].pack(anchor="w")

        # Center - Digital Twin
        center_panel = tk.Frame(main_frame, bg="#111827")
        center_panel.pack(side="left", fill="both", expand=True, padx=10)

        tk.Label(center_panel, text="INDUSTRIAL METAVERSE 3D DIGITAL TWIN", font=("Arial", 17, "bold"), bg="#111827", fg="white").pack(pady=10)

        self.canvas = tk.Canvas(center_panel, bg="#0a1428", height=520, highlightthickness=0)
        self.canvas.pack(fill="both", expand=True, padx=15, pady=8)
        self.draw_process_flow()

        # Simulator Controls
        sim_frame = tk.Frame(center_panel, bg="#1f2937")
        sim_frame.pack(fill="x", padx=15, pady=10)
        tk.Label(sim_frame, text="AUTONOMOUS AI CONTROL", font=("Arial", 14, "bold"), bg="#1f2937", fg="#00ff99").pack()
        btn_frame = tk.Frame(sim_frame, bg="#1f2937")
        btn_frame.pack(pady=8)
        for text, cmd in [("+10% Feed", self.sim_feed_plus), ("-10% Feed", self.sim_feed_minus), ("Crude Switch", self.sim_crude_switch), ("Emergency SD", self.sim_shutdown)]:
            tk.Button(btn_frame, text=text, command=cmd, font=("Arial", 10, "bold"), bg="#00ff99" if "Feed" in text else "#ff4d4d", fg="black" if "Feed" in text else "white").pack(side="left", padx=8)

        # Right Panel
        right_panel = tk.Frame(main_frame, bg="#111827", width=390)
        right_panel.pack(side="right", fill="y")
        right_panel.pack_propagate(False)

        # AI Decisions
        tk.Label(right_panel, text="AUTONOMOUS AI DECISIONS", font=("Arial", 15, "bold"), bg="#111827", fg="#00ff99").pack(pady=12)
        self.decision_text = tk.Text(right_panel, bg="#1f2937", fg="#67e8f9", height=8, font=("Arial", 11))
        self.decision_text.pack(fill="x", padx=12, pady=6)

        # AI Copilot
        tk.Label(right_panel, text="ENTERPRISE AI COPILOT", font=("Arial", 15, "bold"), bg="#111827", fg="#c084fc").pack(pady=(20,6))
        self.chat_entry = tk.Entry(right_panel, bg="#1f2937", fg="white", font=("Arial", 11))
        self.chat_entry.pack(fill="x", padx=12, pady=5)
        self.chat_entry.bind("<Return>", self.copilot_response)
        self.chat_log = tk.Text(right_panel, bg="#1f2937", fg="#bae6fd", height=9, font=("Arial", 10))
        self.chat_log.pack(fill="both", expand=True, padx=12, pady=5)

        # Alarms
        tk.Label(right_panel, text="ALARM MANAGEMENT CENTER", font=("Arial", 14, "bold"), bg="#111827", fg="#ff4d4d").pack(pady=(15,5))
        self.alarm_list = tk.Listbox(right_panel, bg="#1f2937", fg="#fda4af", height=7)
        self.alarm_list.pack(fill="x", padx=12, pady=5)
        tk.Button(right_panel, text="Acknowledge All", command=self.ack_all_alarms, bg="#ffcc00", fg="black").pack(pady=6)

        # Bottom Graphs
        bottom = tk.Frame(self.root, bg="#111827", height=340)
        bottom.pack(fill="x", side="bottom", padx=12, pady=10)
        gframe = tk.Frame(bottom, bg="#111827")
        gframe.pack(fill="both", expand=True)

        self.figures = []
        self.axes = []
        self.canvases = []
        titles = ["Profit Trend", "Carbon Trend", "Efficiency", "Maintenance", "Temperature", "Energy"]
        colors = ["#00ff99", "#ff4d4d", "#67e8f9", "#ffcc00", "#c084fc", "#eab308"]
        for i in range(6):
            fig, ax = plt.subplots(figsize=(4.1, 2.5), facecolor="#111827")
            ax.set_facecolor("#1f2937")
            ax.set_title(titles[i], color="white", fontsize=11)
            canvas = FigureCanvasTkAgg(fig, gframe)
            canvas.get_tk_widget().pack(side="left", fill="both", expand=True, padx=5)
            self.figures.append(fig)
            self.axes.append(ax)
            self.canvases.append(canvas)

        self.update_graphs()

        # Footer
        footer = tk.Frame(self.root, bg="#061126", height=40)
        footer.pack(fill="x", side="bottom")
        tk.Label(footer, text="© 2035 xAI Industrial • Autonomous AI Energy Enterprise V16 • 5124 Sensors • Production Mode", bg="#061126", fg="#64748b", font=("Arial", 10)).pack(pady=10)

    def draw_process_flow(self):
        self.canvas.delete("all")
        for i in range(0, 1500, 40):
            self.canvas.create_line(i, 0, i, 520, fill="#1e2937")
        for i in range(0, 520, 40):
            self.canvas.create_line(0, i, 1500, i, fill="#1e2937")

        units = [("Storage Tanks", 80, 80), ("CDU", 280, 100), ("FCC", 520, 70), ("Hydrotreater", 780, 150), ("Products", 1060, 110)]
        for name, x, y in units:
            color = "#1e40af" if "CDU" in name else "#7e22ce" if "FCC" in name else "#166534"
            self.canvas.create_rectangle(x, y, x+180, y+160, fill=color, outline="#00ff99", width=4)
            self.canvas.create_text(x+90, y+80, text=name, fill="white", font=("Arial", 12, "bold"))

        self.canvas.create_line(260, 170, 280, 140, fill="#67e8f9", width=10, arrow=tk.LAST)
        self.canvas.create_line(460, 140, 520, 170, fill="#67e8f9", width=10, arrow=tk.LAST)
        self.canvas.create_line(700, 170, 780, 210, fill="#67e8f9", width=10, arrow=tk.LAST)

    def switch_plant(self, event=None):
        self.current_plant = self.plant_combo.get()
        self.refresh_all()

    def update_clock(self):
        self.clock_label.config(text=datetime.now().strftime("%H:%M:%S | %d %b %Y"))
        self.root.after(1000, self.update_clock)

    def simulate_data(self):
        self.sensor_data['Profit'] += random.uniform(-25000, 45000)
        self.sensor_data['Carbon_Index'] += random.uniform(-1.0, 1.0)

        for eq in self.maintenance_data:
            self.maintenance_data[eq]['health'] = max(65, min(99.8, self.maintenance_data[eq]['health'] + random.uniform(-1.5, 1.2)))

        decision = random.choice(["Increase FCC Feed Rate", "Reduce Furnace Duty", "Optimize Hydrogen Usage", "Adjust Crude Blend"])
        self.ai_decisions = [f"AUTONOMOUS ACTION: {decision}\nReason: Real-time optimization\nConfidence: {random.randint(94,99)}%"]

        cursor = self.conn.cursor()
        cursor.execute("INSERT INTO historian VALUES (?,?,?,?,?,?,?)", 
            (datetime.now().isoformat(), self.current_plant, self.sensor_data['Profit'], 
             self.sensor_data['CDU_Temp'], self.sensor_data['Carbon_Index'], 90.2, 91.8))
        self.conn.commit()

        now = datetime.now().strftime("%H:%M")
        self.history['time'].append(now)
        self.history['profit'].append(self.sensor_data['Profit']/1000000)
        self.history['temp'].append(self.sensor_data['CDU_Temp'])
        self.history['carbon'].append(self.sensor_data['Carbon_Index'])
        self.history['efficiency'].append(random.uniform(86, 94))
        self.history['maintenance'].append(sum(d['health'] for d in self.maintenance_data.values()) / len(self.maintenance_data))

        if len(self.history['time']) > 40:
            for k in self.history:
                self.history[k] = self.history[k][-40:]

        if random.random() < 0.25:
            self.alarms.append(f"[{datetime.now().strftime('%H:%M')}] HIGH TEMP FCC")
            self.alarm_list.insert(0, self.alarms[-1])
            if self.alarm_list.size() > 12:
                self.alarm_list.delete(12)

    def update_ui(self):
        self.decision_text.delete(1.0, tk.END)
        for d in self.ai_decisions:
            self.decision_text.insert(tk.END, d + "\n\n")

        for item in list(self.exec_labels.keys()):
            self.exec_labels[item].config(text=random.choice(["A+", "A", "B+"]))

        for eq in self.maint_labels:
            data = self.maintenance_data.get(eq, {'health': 90, 'rul': 200})
            self.maint_labels[eq].config(text=f"{data['health']:.1f}% | {data['rul']}d")

    def update_graphs(self):
        titles = ["Profit Trend", "Carbon Trend", "Efficiency", "Maintenance", "Temperature", "Energy"]
        keys = ['profit', 'carbon', 'efficiency', 'maintenance', 'temp', 'maintenance']
        colors = ["#00ff99", "#ff4d4d", "#67e8f9", "#ffcc00", "#c084fc", "#eab308"]
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
                    time.sleep(2.5)
                except:
                    break
        threading.Thread(target=loop, daemon=True).start()

    def sim_feed_plus(self):
        self.sensor_data['FCC_Flow'] += 120
        messagebox.showinfo("Autonomous Action", "FCC Feed Increased +10%")

    def sim_feed_minus(self):
        self.sensor_data['FCC_Flow'] -= 120
        messagebox.showinfo("Autonomous Action", "FCC Feed Reduced -10%")

    def sim_crude_switch(self):
        self.sensor_data['Carbon_Index'] -= 5.2
        messagebox.showinfo("Autonomous Action", "Crude Blend Optimized")

    def sim_shutdown(self):
        messagebox.showwarning("Safety System", "Autonomous Safe Shutdown Activated")

    def copilot_response(self, event=None):
        query = self.chat_entry.get().strip().lower()
        self.chat_entry.delete(0, tk.END)
        if "profit" in query:
            resp = "Profit decreased due to lower FCC conversion. Recommendation: Increase feed rate by 6%."
        elif "carbon" in query:
            resp = "Carbon increased. Reduce furnace duty and improve heat integration immediately."
        elif "failure" in query or "maintenance" in query:
            resp = "Compressor RUL low. Schedule predictive maintenance in next 48 hours."
        elif "fcc" in query:
            resp = "FCC optimization: Increase reactor temperature by 10°C for higher yield."
        else:
            resp = "System operating within optimal parameters. No immediate action required."
        self.chat_log.insert(tk.END, f"AI Copilot: {resp}\n\n")
        self.chat_log.see(tk.END)

    def ack_all_alarms(self):
        self.alarm_list.delete(0, tk.END)
        self.alarms = []
        messagebox.showinfo("Alarms", "All alarms acknowledged")

    def run(self):
        self.root.mainloop()


if __name__ == "__main__":
    app = AIPlant2035DigitalTwinV16()
    app.run()