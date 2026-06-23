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
import sys

class AIPlant2035DigitalTwin:
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("AI Plant 2035 - Enterprise Digital Twin | Reliance | ExxonMobil | Saudi Aramco")
        self.root.geometry("1920x1080")
        self.root.configure(bg="#081229")
        self.root.state('zoomed')

        # Data storage
        self.sensor_data = {
            'CDU_Temp': 385.2, 'CDU_Press': 2.8, 'CDU_Flow': 1450,
            'FCC_Temp': 520.5, 'FCC_Press': 1.9, 'FCC_Flow': 920,
            'Hydro_Temp': 340.8, 'Hydro_Press': 85.4, 'Hydro_Flow': 680,
            'Profit': 1245000, 'Carbon_Index': 42.3, 'Maintenance_Score': 92,
            'Plant_Health': 96.5
        }

        self.history = {
            'time': [],
            'profit': [],
            'temp_cdu': [],
            'carbon': []
        }

        self.ai_recommendations = [
            "Optimize CDU reflux ratio by +3.2% for 1.8% yield improvement",
            "Schedule FCC catalyst replacement in 14 days",
            "Reduce Hydrotreater H2 consumption by adjusting severity",
            "Carbon capture efficiency at 87% - target 94%"
        ]

        self.setup_ui()
        self.start_auto_refresh()

    def setup_ui(self):
        # Top Header
        header = tk.Frame(self.root, bg="#111827", height=80)
        header.pack(fill="x")
        header.pack_propagate(False)

        tk.Label(header, text="AI PLANT 2035", font=("Arial", 28, "bold"), 
                bg="#111827", fg="#22ff88").pack(side="left", padx=30, pady=15)
        
        tk.Label(header, text="ENTERPRISE DIGITAL TWIN • LIVE", font=("Arial", 14), 
                bg="#111827", fg="#22ff88").pack(side="left", padx=20, pady=20)

        # Clock
        self.clock_label = tk.Label(header, text="", font=("Arial", 16), 
                                   bg="#111827", fg="#a1a1aa")
        self.clock_label.pack(side="right", padx=30)
        self.update_clock()

        # Status
        status_frame = tk.Frame(header, bg="#111827")
        status_frame.pack(side="right", padx=20)
        self.plant_status = tk.Label(status_frame, text="● ALL SYSTEMS NOMINAL", 
                                    font=("Arial", 14, "bold"), bg="#111827", fg="#22ff88")
        self.plant_status.pack()

        # Main Content Frame
        main_frame = tk.Frame(self.root, bg="#081229")
        main_frame.pack(fill="both", expand=True, padx=10, pady=10)

        # Left Panel - KPIs
        left_panel = tk.Frame(main_frame, bg="#111827", width=280)
        left_panel.pack(side="left", fill="y", padx=(0, 10))
        left_panel.pack_propagate(False)

        tk.Label(left_panel, text="ENTERPRISE KPIs", font=("Arial", 16, "bold"),
                bg="#111827", fg="white").pack(pady=15)

        self.kpi_labels = {}
        kpis = [
            ("Daily Profit", "profit", "$1.24M", "#22ff88"),
            ("Carbon Index", "carbon", "42.3 kg/bbl", "#ffaa00"),
            ("Plant Health", "health", "96.5%", "#22ff88"),
            ("Maintenance", "maint", "92/100", "#22ff88")
        ]

        for label_text, key, val, color in kpis:
            frame = tk.Frame(left_panel, bg="#1f2937", height=90)
            frame.pack(fill="x", padx=15, pady=8)
            frame.pack_propagate(False)
            
            tk.Label(frame, text=label_text, font=("Arial", 11), bg="#1f2937", fg="#9ca3af").pack(anchor="w", padx=15, pady=(12, 0))
            self.kpi_labels[key] = tk.Label(frame, text=val, font=("Arial", 22, "bold"), 
                                          bg="#1f2937", fg=color)
            self.kpi_labels[key].pack(anchor="w", padx=15, pady=2)

        # Center - Process Flow
        center_panel = tk.Frame(main_frame, bg="#111827")
        center_panel.pack(side="left", fill="both", expand=True, padx=10)

        tk.Label(center_panel, text="REFINERY PROCESS FLOW DIAGRAM", font=("Arial", 16, "bold"),
                bg="#111827", fg="white").pack(pady=10)

        self.canvas = tk.Canvas(center_panel, bg="#0a1428", height=520, highlightthickness=0)
        self.canvas.pack(fill="both", expand=True, padx=15, pady=10)
        self.draw_process_flow()

        # Right Panel - Units & AI
        right_panel = tk.Frame(main_frame, bg="#111827", width=340)
        right_panel.pack(side="right", fill="y")
        right_panel.pack_propagate(False)

        # Units Monitor
        tk.Label(right_panel, text="UNIT MONITORING", font=("Arial", 15, "bold"),
                bg="#111827", fg="white").pack(pady=12)

        units = ["CDU", "FCC", "Hydrotreater"]
        self.unit_frames = {}
        for unit in units:
            uf = tk.Frame(right_panel, bg="#1f2937")
            uf.pack(fill="x", padx=12, pady=6)
            tk.Label(uf, text=unit, font=("Arial", 13, "bold"), bg="#1f2937", fg="#60a5fa").pack(anchor="w", padx=12, pady=6)
            
            self.unit_frames[unit] = {}
            for param in ["Temp", "Press", "Flow"]:
                pframe = tk.Frame(uf, bg="#1f2937")
                pframe.pack(fill="x", padx=12, pady=2)
                tk.Label(pframe, text=param, font=("Arial", 10), bg="#1f2937", fg="#9ca3af", width=6).pack(side="left")
                self.unit_frames[unit][param] = tk.Label(pframe, text="---", font=("Arial", 11, "bold"), 
                                                       bg="#1f2937", fg="#67e8f9")
                self.unit_frames[unit][param].pack(side="right")

        # AI Recommendations
        tk.Label(right_panel, text="AI DECISION ENGINE", font=("Arial", 15, "bold"),
                bg="#111827", fg="#eab308").pack(pady=(25, 8))

        self.ai_text = tk.Text(right_panel, bg="#1f2937", fg="#a5f3fc", font=("Arial", 11), 
                              height=12, wrap="word", relief="flat")
        self.ai_text.pack(fill="both", expand=True, padx=12, pady=5)
        self.update_ai_recommendations()

        # Bottom Panel
        bottom_panel = tk.Frame(self.root, bg="#111827", height=380)
        bottom_panel.pack(fill="x", side="bottom", padx=10, pady=10)
        bottom_panel.pack_propagate(False)

        # Graphs
        graph_frame = tk.Frame(bottom_panel, bg="#111827")
        graph_frame.pack(fill="both", expand=True)

        # Profit Trend
        self.fig_profit, self.ax_profit = plt.subplots(figsize=(6, 3.5), facecolor="#111827")
        self.ax_profit.set_facecolor("#1f2937")
        self.canvas_profit = FigureCanvasTkAgg(self.fig_profit, graph_frame)
        self.canvas_profit.get_tk_widget().pack(side="left", fill="both", expand=True, padx=8)

        # Temperature Trend
        self.fig_temp, self.ax_temp = plt.subplots(figsize=(6, 3.5), facecolor="#111827")
        self.ax_temp.set_facecolor("#1f2937")
        self.canvas_temp = FigureCanvasTkAgg(self.fig_temp, graph_frame)
        self.canvas_temp.get_tk_widget().pack(side="left", fill="both", expand=True, padx=8)

        # Carbon Forecast
        self.fig_carbon, self.ax_carbon = plt.subplots(figsize=(6, 3.5), facecolor="#111827")
        self.ax_carbon.set_facecolor("#1f2937")
        self.canvas_carbon = FigureCanvasTkAgg(self.fig_carbon, graph_frame)
        self.canvas_carbon.get_tk_widget().pack(side="left", fill="both", expand=True, padx=8)

        self.update_graphs()

        # Footer
        footer = tk.Frame(self.root, bg="#081229", height=30)
        footer.pack(fill="x", side="bottom")
        tk.Label(footer, text="© 2035 xAI Industrial • Digital Twin v4.2 • Connected to 1842 Sensors • Confidence: 99.4%", 
                bg="#081229", fg="#64748b", font=("Arial", 9)).pack(pady=6)

    def draw_process_flow(self):
        # Background grid
        for i in range(0, 1200, 40):
            self.canvas.create_line(i, 0, i, 520, fill="#1e2937", width=1)
        for i in range(0, 520, 40):
            self.canvas.create_line(0, i, 1200, i, fill="#1e2937", width=1)

        # CDU
        self.canvas.create_rectangle(80, 120, 280, 280, fill="#1e40af", outline="#60a5fa", width=3)
        self.canvas.create_text(180, 200, text="CDU\nCrude Distillation", fill="white", font=("Arial", 12, "bold"))
        
        # FCC
        self.canvas.create_rectangle(420, 80, 620, 240, fill="#7e22ce", outline="#c084fc", width=3)
        self.canvas.create_text(520, 160, text="FCC\nFluid Catalytic Cracking", fill="white", font=("Arial", 12, "bold"))
        
        # Hydrotreater
        self.canvas.create_rectangle(760, 160, 960, 320, fill="#166534", outline="#4ade80", width=3)
        self.canvas.create_text(860, 240, text="HYDROTREATER\nHydrodesulfurization", fill="white", font=("Arial", 12, "bold"))
        
        # Products
        self.canvas.create_rectangle(1060, 100, 1180, 340, fill="#854d0e", outline="#fbbf24", width=3)
        self.canvas.create_text(1120, 220, text="PRODUCTS\nGasoline • Diesel • Jet", fill="white", font=("Arial", 11, "bold"))

        # Pipes
        self.canvas.create_line(280, 200, 420, 160, fill="#67e8f9", width=8, arrow=tk.LAST)
        self.canvas.create_line(620, 160, 760, 240, fill="#67e8f9", width=8, arrow=tk.LAST)
        self.canvas.create_line(960, 240, 1060, 220, fill="#67e8f9", width=8, arrow=tk.LAST)

        # Sensor indicators
        self.sensor_dots = {}
        positions = [(180, 260), (520, 220), (860, 300)]
        labels = ["CDU", "FCC", "HT"]
        for i, (x, y) in enumerate(positions):
            dot = self.canvas.create_oval(x-12, y-12, x+12, y+12, fill="#22ff88", outline="white")
            self.sensor_dots[labels[i]] = dot

    def update_clock(self):
        current_time = datetime.now().strftime("%H:%M:%S | %d %b %Y")
        self.clock_label.config(text=current_time)
        self.root.after(1000, self.update_clock)

    def update_ai_recommendations(self):
        self.ai_text.delete(1.0, tk.END)
        for rec in self.ai_recommendations:
            self.ai_text.insert(tk.END, "→ " + rec + "\n\n")
        self.ai_text.insert(tk.END, "\nAI CONFIDENCE: 98.7%", "bold")
        self.ai_text.tag_config("bold", font=("Arial", 11, "bold"), foreground="#eab308")

    def simulate_data(self):
        # Simulate sensor variations
        self.sensor_data['CDU_Temp'] += random.uniform(-0.8, 0.8)
        self.sensor_data['FCC_Temp'] += random.uniform(-1.2, 1.2)
        self.sensor_data['Hydro_Temp'] += random.uniform(-0.6, 0.6)
        
        self.sensor_data['CDU_Flow'] += random.uniform(-12, 12)
        self.sensor_data['FCC_Flow'] += random.uniform(-8, 8)
        self.sensor_data['Hydro_Flow'] += random.uniform(-6, 6)
        
        self.sensor_data['Profit'] = max(980000, self.sensor_data['Profit'] + random.uniform(-8500, 18500))
        self.sensor_data['Carbon_Index'] = max(35, min(58, self.sensor_data['Carbon_Index'] + random.uniform(-0.4, 0.4)))
        self.sensor_data['Maintenance_Score'] = max(78, min(99, self.sensor_data['Maintenance_Score'] + random.uniform(-0.3, 0.2)))
        self.sensor_data['Plant_Health'] = max(89, min(99.8, self.sensor_data['Plant_Health'] + random.uniform(-0.15, 0.12)))

        # Update history
        now = datetime.now().strftime("%H:%M")
        self.history['time'].append(now)
        self.history['profit'].append(self.sensor_data['Profit'] / 1000000)
        self.history['temp_cdu'].append(self.sensor_data['CDU_Temp'])
        self.history['carbon'].append(self.sensor_data['Carbon_Index'])
        
        if len(self.history['time']) > 20:
            for k in self.history:
                self.history[k] = self.history[k][-20:]

    def update_ui_panels(self):
        # Update KPIs
        self.kpi_labels["profit"].config(text=f"${self.sensor_data['Profit']/1000000:.2f}M")
        self.kpi_labels["carbon"].config(text=f"{self.sensor_data['Carbon_Index']:.1f} kg/bbl")
        self.kpi_labels["health"].config(text=f"{self.sensor_data['Plant_Health']:.1f}%")
        self.kpi_labels["maint"].config(text=f"{int(self.sensor_data['Maintenance_Score'])}/100")

        # Update Units
        self.unit_frames["CDU"]["Temp"].config(text=f"{self.sensor_data['CDU_Temp']:.1f}°C")
        self.unit_frames["CDU"]["Press"].config(text=f"{self.sensor_data['CDU_Press']:.1f} bar")
        self.unit_frames["CDU"]["Flow"].config(text=f"{int(self.sensor_data['CDU_Flow'])} bbl/h")
        
        self.unit_frames["FCC"]["Temp"].config(text=f"{self.sensor_data['FCC_Temp']:.1f}°C")
        self.unit_frames["FCC"]["Press"].config(text=f"{self.sensor_data['FCC_Press']:.1f} bar")
        self.unit_frames["FCC"]["Flow"].config(text=f"{int(self.sensor_data['FCC_Flow'])} bbl/h")
        
        self.unit_frames["Hydrotreater"]["Temp"].config(text=f"{self.sensor_data['Hydro_Temp']:.1f}°C")
        self.unit_frames["Hydrotreater"]["Press"].config(text=f"{self.sensor_data['Hydro_Press']:.1f} bar")
        self.unit_frames["Hydrotreater"]["Flow"].config(text=f"{int(self.sensor_data['Hydro_Flow'])} bbl/h")

    def update_graphs(self):
        # Profit Trend
        self.ax_profit.clear()
        self.ax_profit.plot(self.history['time'], self.history['profit'], color="#22ff88", linewidth=3, marker='o')
        self.ax_profit.set_title("Profit Trend (Million $)", color="white", fontsize=12)
        self.ax_profit.set_ylabel("Profit $M", color="#9ca3af")
        self.ax_profit.tick_params(colors="#9ca3af")
        self.ax_profit.grid(True, alpha=0.2)
        self.fig_profit.tight_layout()
        self.canvas_profit.draw()

        # Temperature Trend
        self.ax_temp.clear()
        self.ax_temp.plot(self.history['time'], self.history['temp_cdu'], color="#f87171", linewidth=3, marker='o', label="CDU")
        self.ax_temp.set_title("CDU Temperature Trend", color="white", fontsize=12)
        self.ax_temp.set_ylabel("Temperature °C", color="#9ca3af")
        self.ax_temp.tick_params(colors="#9ca3af")
        self.ax_temp.grid(True, alpha=0.2)
        self.fig_temp.tight_layout()
        self.canvas_temp.draw()

        # Carbon Forecast
        self.ax_carbon.clear()
        self.ax_carbon.plot(self.history['time'], self.history['carbon'], color="#fbbf24", linewidth=3, marker='o')
        self.ax_carbon.set_title("Carbon Intensity Forecast", color="white", fontsize=12)
        self.ax_carbon.set_ylabel("kg CO₂ / bbl", color="#9ca3af")
        self.ax_carbon.tick_params(colors="#9ca3af")
        self.ax_carbon.grid(True, alpha=0.2)
        self.fig_carbon.tight_layout()
        self.canvas_carbon.draw()

    def refresh_all(self):
        self.simulate_data()
        self.update_ui_panels()
        self.update_graphs()
        
        # Randomly pulse sensor dots
        for dot in self.sensor_dots.values():
            if random.random() > 0.7:
                self.canvas.itemconfig(dot, fill="#22ff88")
            else:
                self.canvas.itemconfig(dot, fill="#86efac")

    def start_auto_refresh(self):
        def auto_loop():
            while True:
                try:
                    self.root.after(0, self.refresh_all)
                    time.sleep(2.8)
                except:
                    break
        threading.Thread(target=auto_loop, daemon=True).start()

    def run(self):
        self.root.mainloop()

if __name__ == "__main__":
    app = AIPlant2035DigitalTwin()
    app.run()