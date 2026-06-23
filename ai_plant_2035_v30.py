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

class AIPlant2035EnterpriseFinal:
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("AI PLANT 2035 - AUTONOMOUS AI ENERGY ENTERPRISE | Reliance • ExxonMobil • Shell • Saudi Aramco")
        self.root.geometry("1920x1080")
        self.root.configure(bg="#061126")
        self.root.state('zoomed')

        self.conn = sqlite3.connect('ai_plant_historian.db')
        self.create_db()

        self.current_site = "Jamnagar"
        self.sites = ["Jamnagar", "Baytown", "Pernis", "Abqaiq", "Rotterdam", "Antwerp", "Panipat"]

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
            'Overall_Efficiency': 89.7, 'Energy_Eff': 91.3, 'ESG_Score': 88.4
        }

        self.history = {k: [] for k in ['time', 'profit', 'temp', 'carbon', 'efficiency', 'maintenance']}
        self.alarms = []

        self.ai_recommendations = [
            "Increase FCC feed rate by 4.2% → Expected +1.8% Profit",
            "Reduce Furnace duty by 3% → Energy saving of 2.4%",
            "Optimize Hydrogen recycle → +1.8% recovery gain"
        ]

        self.setup_ui()
        self.load_initial_data()
        self.start_auto_refresh()

    def create_db(self):
        cursor = self.conn.cursor()
        cursor.execute('''CREATE TABLE IF NOT EXISTS historian (
            ts TEXT, site TEXT, profit REAL, carbon REAL, efficiency REAL, pump_health REAL)''')
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
        # Top Header
        header = tk.Frame(self.root, bg="#111827", height=95)
        header.pack(fill="x")
        header.pack_propagate(False)

        tk.Label(header, text="AI PLANT 2035", font=("Arial", 34, "bold"), bg="#111827", fg="#00ff99").pack(side="left", padx=40, pady=22)
        tk.Label(header, text="AUTONOMOUS AI ENERGY ENTERPRISE", font=("Arial", 16, "bold"), bg="#111827", fg="#00ff99").pack(side="left", padx=20, pady=22)

        self.clock_label = tk.Label(header, text="", font=("Arial", 15), bg="#111827", fg="#a1a1aa")
        self.clock_label.pack(side="right", padx=30)
        self.update_clock()

        tk.Label(header, text="AI Confidence: 99.8%", font=("Arial", 14), bg="#111827", fg="#00ff99").pack(side="right", padx=30)

        # Main Content
        main_frame = tk.Frame(self.root, bg="#061126")
        main_frame.pack(fill="both", expand=True, padx=12, pady=12)

        # Left Panel - CEO War Room + Multi-Site
        left_panel = tk.Frame(main_frame, bg="#111827", width=360)
        left_panel.pack(side="left", fill="y", padx=(0, 12))
        left_panel.pack_propagate(False)

        tk.Label(left_panel, text="CEO WAR ROOM", font=("Arial", 18, "bold"), bg="#111827", fg="white").pack(pady=15)

        self.exec_labels = {}
        exec_items = ["Profit Today", "Profit YTD", "ESG Score", "Reliability", "AI Maturity", "Overall Score"]
        for item in exec_items:
            f = tk.Frame(left_panel, bg="#1f2937", height=68)
            f.pack(fill="x", padx=15, pady=6)
            f.pack_propagate(False)
            tk.Label(f, text=item, font=("Arial", 11), bg="#1f2937", fg="#9ca3af").pack(anchor="w", padx=15, pady=(8,0))
            self.exec_labels[item] = tk.Label(f, text="A+", font=("Arial", 19, "bold"), bg="#1f2937", fg="#00ff99")
            self.exec_labels[item].pack(anchor="w", padx=15, pady=2)

        # Multi-Site
        tk.Label(left_panel, text="MULTI-REFINERY COMMAND", font=("Arial", 16, "bold"), bg="#111827", fg="#c084fc").pack(pady=(25,8))
        self.site_combo = ttk.Combobox(left_panel, values=self.sites, state="readonly")
        self.site_combo.set(self.current_site)
        self.site_combo.pack(fill="x", padx=15, pady=5)
        self.site_combo.bind("<<ComboboxSelected>>", self.switch_site)

        # Center Panel - Digital Twin
        center_panel = tk.Frame(main_frame, bg="#111827")
        center_panel.pack(side="left", fill="both", expand=True, padx=10)

        tk.Label(center_panel, text="REAL-TIME DIGITAL TWIN", font=("Arial", 18, "bold"), bg="#111827", fg="white").pack(pady=10)

        self.canvas = tk.Canvas(center_panel, bg="#0a1428", height=520, highlightthickness=0)
        self.canvas.pack(fill="both", expand=True, padx=15, pady=8)
        self.draw_process_flow()

        # Simulator
        sim_frame = tk.Frame(center_panel, bg="#1f2937")
        sim_frame.pack(fill="x", padx=15, pady=10)
        tk.Label(sim_frame, text="REAL DIGITAL TWIN SIMULATOR", font=("Arial", 14, "bold"), bg="#1f2937", fg="#eab308").pack(pady=6)
        btn_frame = tk.Frame(sim_frame, bg="#1f2937")
        btn_frame.pack()
        buttons = [
            ("+10% Feed", self.sim_feed_plus, "#00ff99"),
            ("-10% Feed", self.sim_feed_minus, "#ffcc00"),
            ("Crude Change", self.sim_crude_switch, "#60a5fa"),
            ("Emergency Shutdown", self.sim_shutdown, "#ff4d4d")
        ]
        for text, cmd, color in buttons:
            tk.Button(btn_frame, text=text, command=cmd, bg=color, fg="black" if color != "#ff4d4d" else "white", font=("Arial", 10, "bold")).pack(side="left", padx=8, pady=8)

        # Right Panel
        right_panel = tk.Frame(main_frame, bg="#111827", width=380)
        right_panel.pack(side="right", fill="y")
        right_panel.pack_propagate(False)

        # Predictive Maintenance
        tk.Label(right_panel, text="PREDICTIVE MAINTENANCE AI", font=("Arial", 16, "bold"), bg="#111827", fg="#f87171").pack(pady=12)
        self.maint_labels = {}
        for eq in ["Pump", "Compressor", "Heat Exchanger", "Furnace", "Valve"]:
            f = tk.Frame(right_panel, bg="#1f2937")
            f.pack(fill="x", padx=12, pady=5)
            tk.Label(f, text=eq, bg="#1f2937", fg="#93c5fd", font=("Arial", 11, "bold")).pack(anchor="w", padx=15)
            hf = tk.Frame(f, bg="#1f2937")
            hf.pack(fill="x", padx=15)
            self.maint_labels[eq] = tk.Label(hf, text="92.4%", font=("Arial", 16, "bold"), bg="#1f2937", fg="#00ff99")
            self.maint_labels[eq].pack(side="left", padx=5)

        # AI Copilot
        tk.Label(right_panel, text="AI COPILOT PRO", font=("Arial", 16, "bold"), bg="#111827", fg="#c084fc").pack(pady=(25,8))
        self.chat_entry = tk.Entry(right_panel, bg="#1f2937", fg="white", font=("Arial", 11))
        self.chat_entry.pack(fill="x", padx=12, pady=6)
        self.chat_entry.bind("<Return>", self.copilot_response)
        self.chat_log = tk.Text(right_panel, bg="#1f2937", fg="#bae6fd", height=10, font=("Arial", 10))
        self.chat_log.pack(fill="both", expand=True, padx=12, pady=6)

        # Alarms
        tk.Label(right_panel, text="ALARM MANAGEMENT", font=("Arial", 15, "bold"), bg="#111827", fg="#ff4d4d").pack(pady=(20,8))
        self.alarm_list = tk.Listbox(right_panel, bg="#1f2937", fg="#fda4af", height=7)
        self.alarm_list.pack(fill="x", padx=12, pady=5)

        # Bottom Analytics
        bottom_panel = tk.Frame(self.root, bg="#111827", height=380)
        bottom_panel.pack(fill="x", side="bottom", padx=12, pady=12)
        graph_frame = tk.Frame(bottom_panel, bg="#111827")
        graph_frame.pack(fill="both", expand=True)

        self.figures = []
        self.axes = []
        self.canvases = []
        titles = ["Profit Trend", "Carbon Trend", "Efficiency", "Maintenance"]
        colors = ["#00ff99", "#ff4d4d", "#67e8f9", "#ffcc00"]
        for i in range(4):
            fig, ax = plt.subplots(figsize=(5.5, 3.1), facecolor="#111827")
            ax.set_facecolor("#1f2937")
            ax.set_title(titles[i], color="white", fontsize=12)
            canvas = FigureCanvasTkAgg(fig, graph_frame)
            canvas.get_tk_widget().pack(side="left", fill="both", expand=True, padx=8)
            self.figures.append(fig)
            self.axes.append(ax)
            self.canvases.append(canvas)

        self.update_graphs()

        # Footer
        footer = tk.Frame(self.root, bg="#061126", height=38)
        footer.pack(fill="x", side="bottom")
        tk.Label(footer, text="© 2035 xAI Industrial • AI PLANT 2035 Enterprise V30 • 4286 Live Sensors • System Nominal", bg="#061126", fg="#64748b", font=("Arial", 10)).pack(pady=9)

    def draw_process_flow(self):
        self.canvas.delete("all")
        for i in range(0, 1450, 40):
            self.canvas.create_line(i, 0, i, 520, fill="#1e2937")
        for i in range(0, 520, 40):
            self.canvas.create_line(0, i, 1450, i, fill="#1e2937")

        # Units
        self.canvas.create_rectangle(90, 110, 280, 280, fill="#1e40af", outline="#60a5fa", width=5)
        self.canvas.create_text(185, 195, text="CDU", fill="white", font=("Arial", 15, "bold"))

        self.canvas.create_rectangle(420, 80, 610, 250, fill="#7e22ce", outline="#c084fc", width=5)
        self.canvas.create_text(515, 165, text="FCC", fill="white", font=("Arial", 15, "bold"))

        self.canvas.create_rectangle(760, 160, 950, 330, fill="#166534", outline="#4ade80", width=5)
        self.canvas.create_text(855, 245, text="HYDROTREATER", fill="white", font=("Arial", 13, "bold"))

        # Flow lines
        self.canvas.create_line(280, 195, 420, 165, fill="#67e8f9", width=10, arrow=tk.LAST)
        self.canvas.create_line(610, 165, 760, 245, fill="#67e8f9", width=10, arrow=tk.LAST)

    def update_clock(self):
        self.clock_label.config(text=datetime.now().strftime("%H:%M:%S | %d %b %Y"))
        self.root.after(1000, self.update_clock)

    def switch_site(self, event=None):
        self.current_site = self.site_combo.get()
        messagebox.showinfo("Site Switch", f"Switched to {self.current_site}")

    def simulate_data(self):
        self.sensor_data['Profit'] += random.uniform(-22000, 42000)
        self.sensor_data['Carbon_Index'] += random.uniform(-0.9, 0.9)
        self.sensor_data['Plant_Health'] = max(87, min(99.9, self.sensor_data['Plant_Health'] + random.uniform(-0.5, 0.4)))

        for k in self.maintenance_data:
            if "Health" in k:
                self.maintenance_data[k] = max(68, min(99, self.maintenance_data[k] + random.uniform(-1.3, 1.1)))

        self.optimization_data['Overall_Efficiency'] = max(83, min(96.5, self.optimization_data['Overall_Efficiency'] + random.uniform(-0.7, 0.8)))

        cursor = self.conn.cursor()
        cursor.execute("INSERT INTO historian VALUES (?,?,?,?,?,?)", 
            (datetime.now().isoformat(), self.current_site, self.sensor_data['Profit'], 
             self.sensor_data['Carbon_Index'], self.optimization_data['Overall_Efficiency'], 
             self.maintenance_data['Pump_Health']))
        self.conn.commit()

        now = datetime.now().strftime("%H:%M")
        self.history['time'].append(now)
        self.history['profit'].append(self.sensor_data['Profit']/1000000)
        self.history['temp'].append(self.sensor_data['CDU_Temp'])
        self.history['carbon'].append(self.sensor_data['Carbon_Index'])
        self.history['efficiency'].append(self.optimization_data['Overall_Efficiency'])
        self.history['maintenance'].append(sum(self.maintenance_data.values()) / len(self.maintenance_data))

        if len(self.history['time']) > 40:
            for k in self.history:
                self.history[k] = self.history[k][-40:]

        if random.random() < 0.22:
            alarm = f"{random.choice(['HIGH', 'CRITICAL'])} TEMP {random.choice(['CDU','FCC'])}"
            self.alarms.append(alarm)
            self.alarm_list.insert(0, alarm)
            if self.alarm_list.size() > 12:
                self.alarm_list.delete(12)

    def update_ui(self):
        for eq in self.maint_labels:
            h = self.maintenance_data.get(eq + "_Health", 88)
            col = "#00ff99" if h > 90 else "#ffcc00" if h > 80 else "#ff4d4d"
            self.maint_labels[eq].config(text=f"{h:.1f}%", fg=col)

        self.exec_labels["Overall Score"].config(text=f"{int(self.optimization_data['Overall_Efficiency'])}")
        self.exec_labels["Profit Today"].config(text=f"${self.sensor_data['Profit']/1000000:.2f}M")

    def update_graphs(self):
        titles = ["Profit Trend", "Carbon Trend", "Efficiency Trend", "Maintenance Trend"]
        keys = ['profit', 'carbon', 'efficiency', 'maintenance']
        colors = ["#00ff99", "#ff4d4d", "#67e8f9", "#ffcc00"]
        for i, ax in enumerate(self.axes):
            ax.clear()
            ax.plot(self.history['time'], self.history[keys[i]], color=colors[i], linewidth=3.5, marker='o', markersize=4)
            ax.set_title(titles[i], color="white", fontsize=12)
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
        messagebox.showinfo("Simulation", "Feed rate increased +10%")

    def sim_feed_minus(self):
        self.sensor_data['FCC_Flow'] -= 110
        messagebox.showinfo("Simulation", "Feed rate decreased -10%")

    def sim_crude_switch(self):
        self.sensor_data['Carbon_Index'] -= 4.5
        messagebox.showinfo("Simulation", "Crude blend switched successfully")

    def sim_shutdown(self):
        messagebox.showwarning("Emergency", "Emergency Shutdown Activated. All units safe.")

    def copilot_response(self, event=None):
        query = self.chat_entry.get().strip().lower()
        self.chat_entry.delete(0, tk.END)
        responses = {
            "profit": "Profit dropped due to lower FCC conversion. Recommendation: Increase feed rate by 5%.",
            "carbon": "Reduce carbon intensity by optimizing furnace duty and heat integration.",
            "maintenance": "Compressor health is declining. Schedule predictive maintenance within 48 hours.",
            "fcc": "FCC optimization: Increase severity for higher gasoline yield and better margins.",
        }
        resp = responses.get(next((k for k in responses if k in query), "default"), "System optimized. All parameters within optimal range.")
        self.chat_log.insert(tk.END, f"AI Copilot: {resp}\n\n")
        self.chat_log.see(tk.END)

    def run(self):
        self.root.mainloop()


if __name__ == "__main__":
    app = AIPlant2035EnterpriseFinal()
    app.run()