import tkinter as tk
from tkinter import ttk
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import numpy as np
import pandas as pd
import random
from datetime import datetime
import threading
import time

class AIPlant2035DigitalTwinV42:
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("AI Plant 2035 Enterprise Digital Twin v4.2 | Reliance • ExxonMobil • Saudi Aramco")
        self.root.geometry("1920x1080")
        self.root.configure(bg="#081229")
        self.root.state('zoomed')

        # Core Sensor Data
        self.sensor_data = {
            'CDU_Temp': 385.2, 'CDU_Press': 2.8, 'CDU_Flow': 1450,
            'FCC_Temp': 520.5, 'FCC_Press': 1.9, 'FCC_Flow': 920,
            'Hydro_Temp': 340.8, 'Hydro_Press': 85.4, 'Hydro_Flow': 680,
            'Profit': 1245000, 'Carbon_Index': 42.3, 'Plant_Health': 96.5
        }

        # Maintenance Data
        self.maintenance_data = {
            'Pump_Health': 94.2,
            'Compressor_Health': 87.8,
            'Furnace_Health': 91.5,
            'Pump_RUL': 245,
            'Compressor_RUL': 118,
            'Furnace_RUL': 167,
            'Avg_Asset_Health': 91.2,
            'Reliability_Score': 93.7,
            'Maintenance_Readiness': 89.4
        }

        self.history = {
            'time': [],
            'profit': [],
            'temp_cdu': [],
            'carbon': []
        }

        self.ai_recommendations = [
            "Schedule Pump inspection within 72 hours",
            "Reduce Furnace thermal load by 4% to extend RUL",
            "Perform Compressor efficiency diagnostic",
            "Continue normal operation on CDU - optimal conditions"
        ]

        self.alerts = []

        self.setup_ui()
        self.start_auto_refresh()

    def setup_ui(self):
        # Header
        header = tk.Frame(self.root, bg="#111827", height=85)
        header.pack(fill="x")
        header.pack_propagate(False)

        tk.Label(header, text="AI PLANT 2035", font=("Arial", 28, "bold"), 
                bg="#111827", fg="#22ff88").pack(side="left", padx=30, pady=18)
        
        tk.Label(header, text="ENTERPRISE DIGITAL TWIN v4.2 • LIVE OPERATIONS", 
                font=("Arial", 14, "bold"), bg="#111827", fg="#22ff88").pack(side="left", padx=20)

        self.clock_label = tk.Label(header, text="", font=("Arial", 16), bg="#111827", fg="#a1a1aa")
        self.clock_label.pack(side="right", padx=30)
        self.update_clock()

        status_frame = tk.Frame(header, bg="#111827")
        status_frame.pack(side="right", padx=20)
        self.plant_status = tk.Label(status_frame, text="● ALL SYSTEMS NOMINAL", 
                                    font=("Arial", 14, "bold"), bg="#111827", fg="#22ff88")
        self.plant_status.pack()

        # Main Frame
        main_frame = tk.Frame(self.root, bg="#081229")
        main_frame.pack(fill="both", expand=True, padx=12, pady=12)

        # Left KPIs
        left_panel = tk.Frame(main_frame, bg="#111827", width=290)
        left_panel.pack(side="left", fill="y", padx=(0, 12))
        left_panel.pack_propagate(False)

        tk.Label(left_panel, text="ENTERPRISE KPIs", font=("Arial", 16, "bold"),
                bg="#111827", fg="white").pack(pady=15)

        self.kpi_labels = {}
        kpis = [
            ("Daily Profit", "profit", "$1.245M", "#22ff88"),
            ("Carbon Index", "carbon", "42.3 kg/bbl", "#ffaa00"),
            ("Plant Health", "health", "96.5%", "#22ff88"),
        ]

        for label_text, key, val, color in kpis:
            frame = tk.Frame(left_panel, bg="#1f2937", height=88)
            frame.pack(fill="x", padx=15, pady=8)
            frame.pack_propagate(False)
            tk.Label(frame, text=label_text, font=("Arial", 11), bg="#1f2937", fg="#9ca3af").pack(anchor="w", padx=15, pady=(12,0))
            self.kpi_labels[key] = tk.Label(frame, text=val, font=("Arial", 22, "bold"), bg="#1f2937", fg=color)
            self.kpi_labels[key].pack(anchor="w", padx=15, pady=2)

        # Center - Process Flow
        center_panel = tk.Frame(main_frame, bg="#111827")
        center_panel.pack(side="left", fill="both", expand=True, padx=10)

        tk.Label(center_panel, text="REFINERY PROCESS FLOW DIAGRAM", 
                font=("Arial", 16, "bold"), bg="#111827", fg="white").pack(pady=10)

        self.canvas = tk.Canvas(center_panel, bg="#0a1428", height=520, highlightthickness=0)
        self.canvas.pack(fill="both", expand=True, padx=15, pady=10)
        self.draw_process_flow()

        # Right Panel
        right_panel = tk.Frame(main_frame, bg="#111827", width=360)
        right_panel.pack(side="right", fill="y")
        right_panel.pack_propagate(False)

        # Unit Monitoring
        tk.Label(right_panel, text="LIVE UNIT MONITORING", font=("Arial", 15, "bold"),
                bg="#111827", fg="white").pack(pady=(12,8))

        units = ["CDU", "FCC", "Hydrotreater"]
        self.unit_frames = {}
        for unit in units:
            uf = tk.Frame(right_panel, bg="#1f2937")
            uf.pack(fill="x", padx=12, pady=6)
            tk.Label(uf, text=unit, font=("Arial", 13, "bold"), bg="#1f2937", fg="#60a5fa").pack(anchor="w", padx=12, pady=6)
            self.unit_frames[unit] = {}
            for param in ["Temp", "Press", "Flow"]:
                pframe = tk.Frame(uf, bg="#1f2937")
                pframe.pack(fill="x", padx=12, pady=1)
                tk.Label(pframe, text=param, font=("Arial", 10), bg="#1f2937", fg="#9ca3af", width=6).pack(side="left")
                self.unit_frames[unit][param] = tk.Label(pframe, text="---", font=("Arial", 11, "bold"), bg="#1f2937", fg="#67e8f9")
                self.unit_frames[unit][param].pack(side="right", padx=5)

        # Predictive Maintenance Center
        tk.Label(right_panel, text="PREDICTIVE MAINTENANCE", font=("Arial", 15, "bold"),
                bg="#111827", fg="#eab308").pack(pady=(25,8))

        maint_frame = tk.Frame(right_panel, bg="#1f2937")
        maint_frame.pack(fill="x", padx=12, pady=6)

        self.maint_labels = {}
        equipment = ["Pump", "Compressor", "Furnace"]
        for eq in equipment:
            eqf = tk.Frame(maint_frame, bg="#1f2937")
            eqf.pack(fill="x", padx=12, pady=4)
            tk.Label(eqf, text=eq, font=("Arial", 11, "bold"), bg="#1f2937", fg="#93c5fd").pack(anchor="w")
            
            health_frame = tk.Frame(eqf, bg="#1f2937")
            health_frame.pack(fill="x")
            self.maint_labels[f"{eq}_health"] = tk.Label(health_frame, text="94%", font=("Arial", 18, "bold"), bg="#1f2937", fg="#22ff88")
            self.maint_labels[f"{eq}_health"].pack(side="left", padx=12)
            
            self.maint_labels[f"{eq}_rul"] = tk.Label(health_frame, text="245d", font=("Arial", 11), bg="#1f2937", fg="#a5b4fc")
            self.maint_labels[f"{eq}_rul"].pack(side="right", padx=12)

        # Failure Prediction
        fail_frame = tk.Frame(right_panel, bg="#1f2937")
        fail_frame.pack(fill="x", padx=12, pady=10)
        tk.Label(fail_frame, text="FAILURE PROBABILITY", font=("Arial", 12, "bold"), bg="#1f2937", fg="#f87171").pack(anchor="w", padx=12, pady=6)
        
        self.fail_labels = {}
        for eq in equipment:
            f = tk.Frame(fail_frame, bg="#1f2937")
            f.pack(fill="x", padx=12, pady=2)
            tk.Label(f, text=eq, font=("Arial", 10), bg="#1f2937", fg="#9ca3af").pack(side="left")
            self.fail_labels[eq] = tk.Label(f, text="2.8%", font=("Arial", 12, "bold"), bg="#1f2937", fg="#f87171")
            self.fail_labels[eq].pack(side="right")

        # Risk Classification
        risk_frame = tk.Frame(right_panel, bg="#1f2937")
        risk_frame.pack(fill="x", padx=12, pady=8)
        tk.Label(risk_frame, text="MAINTENANCE RISK", font=("Arial", 12, "bold"), bg="#1f2937", fg="#fbbf24").pack(anchor="w", padx=12, pady=6)
        self.risk_label = tk.Label(risk_frame, text="MEDIUM", font=("Arial", 16, "bold"), bg="#1f2937", fg="#fbbf24")
        self.risk_label.pack(pady=4)

        # AI Recommendations
        tk.Label(right_panel, text="AI RECOMMENDATIONS", font=("Arial", 15, "bold"),
                bg="#111827", fg="#eab308").pack(pady=(20,8))
        
        self.ai_text = tk.Text(right_panel, bg="#1f2937", fg="#bae6fd", font=("Arial", 11), height=9, wrap="word", relief="flat")
        self.ai_text.pack(fill="both", expand=True, padx=12, pady=5)
        self.update_ai_recommendations()

        # Bottom Graphs
        bottom_panel = tk.Frame(self.root, bg="#111827", height=390)
        bottom_panel.pack(fill="x", side="bottom", padx=12, pady=12)
        bottom_panel.pack_propagate(False)

        graph_frame = tk.Frame(bottom_panel, bg="#111827")
        graph_frame.pack(fill="both", expand=True)

        self.fig_profit, self.ax_profit = plt.subplots(figsize=(5.5, 3.4), facecolor="#111827")
        self.ax_profit.set_facecolor("#1f2937")
        self.canvas_profit = FigureCanvasTkAgg(self.fig_profit, graph_frame)
        self.canvas_profit.get_tk_widget().pack(side="left", fill="both", expand=True, padx=8)

        self.fig_temp, self.ax_temp = plt.subplots(figsize=(5.5, 3.4), facecolor="#111827")
        self.ax_temp.set_facecolor("#1f2937")
        self.canvas_temp = FigureCanvasTkAgg(self.fig_temp, graph_frame)
        self.canvas_temp.get_tk_widget().pack(side="left", fill="both", expand=True, padx=8)

        self.fig_carbon, self.ax_carbon = plt.subplots(figsize=(5.5, 3.4), facecolor="#111827")
        self.ax_carbon.set_facecolor("#1f2937")
        self.canvas_carbon = FigureCanvasTkAgg(self.fig_carbon, graph_frame)
        self.canvas_carbon.get_tk_widget().pack(side="left", fill="both", expand=True, padx=8)

        self.update_graphs()

        # Footer
        footer = tk.Frame(self.root, bg="#081229", height=32)
        footer.pack(fill="x", side="bottom")
        tk.Label(footer, text="© 2035 xAI Industrial • Digital Twin v4.2 • 1842 Sensors Online • AI Confidence 99.6%", 
                bg="#081229", fg="#64748b", font=("Arial", 9)).pack(pady=7)

    def draw_process_flow(self):
        for i in range(0, 1250, 40):
            self.canvas.create_line(i, 0, i, 520, fill="#1e2937", width=1)
        for i in range(0, 520, 40):
            self.canvas.create_line(0, i, 1250, i, fill="#1e2937", width=1)

        # CDU
        self.canvas.create_rectangle(80, 110, 280, 270, fill="#1e40af", outline="#60a5fa", width=4)
        self.canvas.create_text(180, 190, text="CDU", fill="white", font=("Arial", 14, "bold"))
        self.canvas.create_text(180, 215, text="Crude Distillation", fill="#bae6fd", font=("Arial", 10))

        # FCC
        self.canvas.create_rectangle(420, 70, 620, 230, fill="#7e22ce", outline="#c084fc", width=4)
        self.canvas.create_text(520, 150, text="FCC", fill="white", font=("Arial", 14, "bold"))

        # Hydrotreater
        self.canvas.create_rectangle(760, 150, 960, 310, fill="#166534", outline="#4ade80", width=4)
        self.canvas.create_text(860, 230, text="HYDROTREATER", fill="white", font=("Arial", 12, "bold"))

        # Products
        self.canvas.create_rectangle(1060, 90, 1190, 340, fill="#854d0e", outline="#fbbf24", width=4)
        self.canvas.create_text(1125, 215, text="PRODUCTS", fill="white", font=("Arial", 13, "bold"))

        # Flow lines
        self.canvas.create_line(280, 190, 420, 150, fill="#67e8f9", width=9, arrow=tk.LAST)
        self.canvas.create_line(620, 150, 760, 230, fill="#67e8f9", width=9, arrow=tk.LAST)
        self.canvas.create_line(960, 230, 1060, 215, fill="#67e8f9", width=9, arrow=tk.LAST)

        self.sensor_dots = {}
        pos = [(180,250), (520,210), (860,290)]
        for i, (x,y) in enumerate(pos):
            dot = self.canvas.create_oval(x-13, y-13, x+13, y+13, fill="#22ff88", outline="white", width=2)
            self.sensor_dots[i] = dot

    def update_clock(self):
        current_time = datetime.now().strftime("%H:%M:%S | %d %b %Y")
        self.clock_label.config(text=current_time)
        self.root.after(1000, self.update_clock)

    def update_ai_recommendations(self):
        self.ai_text.delete(1.0, tk.END)
        for rec in self.ai_recommendations:
            self.ai_text.insert(tk.END, f"→ {rec}\n\n")
        self.ai_text.insert(tk.END, "\nAI CONFIDENCE: 98.9%", "bold")
        self.ai_text.tag_config("bold", font=("Arial", 11, "bold"), foreground="#eab308")

    def simulate_maintenance(self):
        # Simulate degradation and recovery
        self.maintenance_data['Pump_Health'] = max(72, min(99.8, self.maintenance_data['Pump_Health'] + random.uniform(-0.45, 0.35)))
        self.maintenance_data['Compressor_Health'] = max(68, min(98.5, self.maintenance_data['Compressor_Health'] + random.uniform(-0.65, 0.4)))
        self.maintenance_data['Furnace_Health'] = max(75, min(99.2, self.maintenance_data['Furnace_Health'] + random.uniform(-0.55, 0.45)))

        # RUL calculation
        self.maintenance_data['Pump_RUL'] = int(self.maintenance_data['Pump_Health'] * 2.6)
        self.maintenance_data['Compressor_RUL'] = int(self.maintenance_data['Compressor_Health'] * 1.35)
        self.maintenance_data['Furnace_RUL'] = int(self.maintenance_data['Furnace_Health'] * 1.8)

        self.maintenance_data['Avg_Asset_Health'] = (self.maintenance_data['Pump_Health'] + 
                                                    self.maintenance_data['Compressor_Health'] + 
                                                    self.maintenance_data['Furnace_Health']) / 3

        self.maintenance_data['Reliability_Score'] = min(99.2, self.maintenance_data['Avg_Asset_Health'] * 0.97 + random.uniform(-1,1))
        self.maintenance_data['Maintenance_Readiness'] = min(98, self.maintenance_data['Avg_Asset_Health'] * 0.94 + 6)

    def calculate_failure_prob(self, health):
        base = (100 - health) * 0.85
        return max(0.3, min(42, base + random.uniform(-1.5, 2.2)))

    def determine_risk(self):
        max_fail = max([self.calculate_failure_prob(self.maintenance_data[k]) for k in ['Pump_Health','Compressor_Health','Furnace_Health']])
        if max_fail > 22:
            return "HIGH", "#ef4444"
        elif max_fail > 9:
            return "MEDIUM", "#fbbf24"
        else:
            return "LOW", "#4ade80"

    def generate_alerts(self):
        self.alerts = []
        if self.maintenance_data['Furnace_Health'] < 84:
            self.alerts.append("Furnace temperature anomaly detected")
        if self.calculate_failure_prob(self.maintenance_data['Compressor_Health']) > 18:
            self.alerts.append("Compressor failure risk elevated")
        if self.sensor_data['CDU_Temp'] > 398:
            self.alerts.append("CDU high temperature warning")

    def simulate_data(self):
        # Process sensors
        self.sensor_data['CDU_Temp'] += random.uniform(-1.1, 1.1)
        self.sensor_data['FCC_Temp'] += random.uniform(-1.6, 1.6)
        self.sensor_data['Hydro_Temp'] += random.uniform(-0.9, 0.9)
        
        self.sensor_data['Profit'] = max(960000, self.sensor_data['Profit'] + random.uniform(-12000, 24500))
        self.sensor_data['Carbon_Index'] = max(36, min(55, self.sensor_data['Carbon_Index'] + random.uniform(-0.35, 0.45)))
        self.sensor_data['Plant_Health'] = max(90, min(99.7, self.sensor_data['Plant_Health'] + random.uniform(-0.2, 0.18)))

        self.simulate_maintenance()
        self.generate_alerts()

        # History
        now = datetime.now().strftime("%H:%M")
        self.history['time'].append(now)
        self.history['profit'].append(self.sensor_data['Profit'] / 1000000)
        self.history['temp_cdu'].append(self.sensor_data['CDU_Temp'])
        self.history['carbon'].append(self.sensor_data['Carbon_Index'])
        
        if len(self.history['time']) > 22:
            for k in self.history.keys():
                self.history[k] = self.history[k][-22:]

    def update_ui(self):
        # KPIs
        self.kpi_labels["profit"].config(text=f"${self.sensor_data['Profit']/1000000:.2f}M")
        self.kpi_labels["carbon"].config(text=f"{self.sensor_data['Carbon_Index']:.1f} kg/bbl")
        self.kpi_labels["health"].config(text=f"{self.sensor_data['Plant_Health']:.1f}%")

        # Units
        self.unit_frames["CDU"]["Temp"].config(text=f"{self.sensor_data['CDU_Temp']:.1f}°C")
        self.unit_frames["CDU"]["Press"].config(text=f"{self.sensor_data['CDU_Press']:.1f}")
        self.unit_frames["CDU"]["Flow"].config(text=f"{int(self.sensor_data['CDU_Flow'])}")

        self.unit_frames["FCC"]["Temp"].config(text=f"{self.sensor_data['FCC_Temp']:.1f}°C")
        self.unit_frames["FCC"]["Press"].config(text=f"{self.sensor_data['FCC_Press']:.1f}")
        self.unit_frames["FCC"]["Flow"].config(text=f"{int(self.sensor_data['FCC_Flow'])}")

        self.unit_frames["Hydrotreater"]["Temp"].config(text=f"{self.sensor_data['Hydro_Temp']:.1f}°C")
        self.unit_frames["Hydrotreater"]["Press"].config(text=f"{self.sensor_data['Hydro_Press']:.1f}")
        self.unit_frames["Hydrotreater"]["Flow"].config(text=f"{int(self.sensor_data['Hydro_Flow'])}")

        # Maintenance
        colors = {"Pump": "#22ff88", "Compressor": "#eab308", "Furnace": "#4ade80"}
        for eq in ["Pump", "Compressor", "Furnace"]:
            health = self.maintenance_data[f"{eq}_Health"]
            col = "#22ff88" if health > 90 else "#fbbf24" if health > 80 else "#f87171"
            self.maint_labels[f"{eq}_health"].config(text=f"{health:.1f}%", fg=col)
            self.maint_labels[f"{eq}_rul"].config(text=f"{self.maintenance_data[f'{eq}_RUL']}d")

        # Failure Prob
        for eq in ["Pump", "Compressor", "Furnace"]:
            prob = self.calculate_failure_prob(self.maintenance_data[f"{eq}_Health"])
            col = "#f87171" if prob > 15 else "#fbbf24" if prob > 6 else "#4ade80"
            self.fail_labels[eq].config(text=f"{prob:.1f}%", fg=col)

        # Risk
        risk_level, risk_color = self.determine_risk()
        self.risk_label.config(text=risk_level, fg=risk_color)

        self.update_ai_recommendations()

    def update_graphs(self):
        # Profit
        self.ax_profit.clear()
        self.ax_profit.plot(self.history['time'], self.history['profit'], color="#22ff88", linewidth=3.5, marker='o', markersize=4)
        self.ax_profit.set_title("Profit Trend ($M)", color="white", fontsize=12)
        self.ax_profit.set_ylabel("$ Million", color="#9ca3af")
        self.ax_profit.tick_params(colors="#9ca3af")
        self.ax_profit.grid(True, alpha=0.25)
        self.fig_profit.tight_layout()
        self.canvas_profit.draw()

        # Temp
        self.ax_temp.clear()
        self.ax_temp.plot(self.history['time'], self.history['temp_cdu'], color="#f87171", linewidth=3.5, marker='o')
        self.ax_temp.set_title("CDU Temperature", color="white", fontsize=12)
        self.ax_temp.set_ylabel("°C", color="#9ca3af")
        self.ax_temp.tick_params(colors="#9ca3af")
        self.ax_temp.grid(True, alpha=0.25)
        self.fig_temp.tight_layout()
        self.canvas_temp.draw()

        # Carbon
        self.ax_carbon.clear()
        self.ax_carbon.plot(self.history['time'], self.history['carbon'], color="#fbbf24", linewidth=3.5, marker='o')
        self.ax_carbon.set_title("Carbon Intensity", color="white", fontsize=12)
        self.ax_carbon.set_ylabel("kg CO₂/bbl", color="#9ca3af")
        self.ax_carbon.tick_params(colors="#9ca3af")
        self.ax_carbon.grid(True, alpha=0.25)
        self.fig_carbon.tight_layout()
        self.canvas_carbon.draw()

    def refresh_all(self):
        self.simulate_data()
        self.update_ui()
        self.update_graphs()

        # Pulse sensors
        for dot in self.sensor_dots.values():
            if random.random() > 0.65:
                self.canvas.itemconfig(dot, fill="#22ff88")
            else:
                self.canvas.itemconfig(dot, fill="#86efac")

    def start_auto_refresh(self):
        def loop():
            while True:
                try:
                    self.root.after(0, self.refresh_all)
                    time.sleep(2.4)
                except:
                    break
        threading.Thread(target=loop, daemon=True).start()

    def run(self):
        self.root.mainloop()

if __name__ == "__main__":
    app = AIPlant2035DigitalTwinV42()
    app.run()