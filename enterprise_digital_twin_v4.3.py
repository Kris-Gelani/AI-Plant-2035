import tkinter as tk
from tkinter import ttk
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import numpy as np
import random
from datetime import datetime
import threading
import time

class AIPlant2035DigitalTwinV43:
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("AI Plant 2035 Enterprise Digital Twin v4.3 | Reliance • ExxonMobil • Shell • Saudi Aramco")
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
            'Pump_Health': 94.2, 'Compressor_Health': 87.8, 'Furnace_Health': 91.5,
            'Pump_RUL': 245, 'Compressor_RUL': 118, 'Furnace_RUL': 167,
            'Avg_Asset_Health': 91.2, 'Reliability_Score': 93.7, 'Maintenance_Readiness': 89.4
        }

        # Optimization Data
        self.optimization_data = {
            'Dist_Efficiency': 96.4,
            'FCC_Conversion': 78.9,
            'Hydro_Efficiency': 94.2,
            'Overall_Efficiency': 89.7,
            'Gasoline_Yield': 42.8,
            'Diesel_Yield': 31.5,
            'LPG_Yield': 12.4,
            'Jet_Yield': 18.3,
            'H2_Consumption': 1850,
            'H2_Recovery': 92.6,
            'H2_Purity': 99.4,
            'H2_Opt_Score': 96.8,
            'Steam_Cons': 1240,
            'Power_Cons': 875,
            'Furnace_Duty': 285,
            'Energy_Eff': 91.3,
            'Carbon_Reduction_Potential': 14.8,
            'CO2_Savings': 24500,
            'ESG_Score': 88.9,
            'Production_Util': 94.2,
            'Asset_Util': 92.7,
            'Throughput_Eff': 89.5,
            'Margin_Opt': 93.1,
            'Opt_Furnace_Temp': 392,
            'Opt_FCC_Feed': 1380,
            'Opt_Reactor_Temp': 518,
            'Opt_H2_Rate': 1720
        }

        self.history = {
            'time': [],
            'profit': [],
            'temp_cdu': [],
            'carbon': [],
            'efficiency': [],
            'h2_cons': [],
            'energy_eff': []
        }

        self.ai_recommendations = [
            "Increase FCC feed rate by 4.2% for higher gasoline yield",
            "Reduce Furnace duty by 3% to improve energy efficiency",
            "Optimize Hydrogen recycle rate for 1.8% recovery gain",
            "Maintain current CDU operation - optimal conditions",
            "Improve heat integration between CDU and Hydrotreater"
        ]

        self.setup_ui()
        self.start_auto_refresh()

    def setup_ui(self):
        # Header
        header = tk.Frame(self.root, bg="#111827", height=85)
        header.pack(fill="x")
        header.pack_propagate(False)

        tk.Label(header, text="AI PLANT 2035", font=("Arial", 28, "bold"), 
                bg="#111827", fg="#22ff88").pack(side="left", padx=30, pady=18)
        
        tk.Label(header, text="ENTERPRISE DIGITAL TWIN v4.3 • LIVE", 
                font=("Arial", 14, "bold"), bg="#111827", fg="#22ff88").pack(side="left", padx=20)

        self.clock_label = tk.Label(header, text="", font=("Arial", 16), bg="#111827", fg="#a1a1aa")
        self.clock_label.pack(side="right", padx=30)
        self.update_clock()

        status_frame = tk.Frame(header, bg="#111827")
        status_frame.pack(side="right", padx=20)
        self.plant_status = tk.Label(status_frame, text="● ALL SYSTEMS OPTIMAL", 
                                    font=("Arial", 14, "bold"), bg="#111827", fg="#22ff88")
        self.plant_status.pack()

        # Main Frame
        main_frame = tk.Frame(self.root, bg="#081229")
        main_frame.pack(fill="both", expand=True, padx=12, pady=10)

        # Left Panel
        left_panel = tk.Frame(main_frame, bg="#111827", width=300)
        left_panel.pack(side="left", fill="y", padx=(0, 10))
        left_panel.pack_propagate(False)

        tk.Label(left_panel, text="ENTERPRISE KPIs", font=("Arial", 16, "bold"),
                bg="#111827", fg="white").pack(pady=12)

        self.kpi_labels = {}
        kpis = [
            ("Daily Profit", "profit", "$1.245M", "#22ff88"),
            ("Carbon Index", "carbon", "42.3", "#ffaa00"),
            ("Plant Health", "health", "96.5%", "#22ff88"),
        ]
        for label_text, key, val, color in kpis:
            frame = tk.Frame(left_panel, bg="#1f2937", height=85)
            frame.pack(fill="x", padx=15, pady=6)
            frame.pack_propagate(False)
            tk.Label(frame, text=label_text, font=("Arial", 11), bg="#1f2937", fg="#9ca3af").pack(anchor="w", padx=15, pady=(10,0))
            self.kpi_labels[key] = tk.Label(frame, text=val, font=("Arial", 21, "bold"), bg="#1f2937", fg=color)
            self.kpi_labels[key].pack(anchor="w", padx=15, pady=3)

        # Executive Command Center
        tk.Label(left_panel, text="EXECUTIVE COMMAND CENTER", font=("Arial", 15, "bold"),
                bg="#111827", fg="#eab308").pack(pady=(20,8))
        exec_frame = tk.Frame(left_panel, bg="#1f2937")
        exec_frame.pack(fill="x", padx=15, pady=6)
        self.exec_labels = {}
        exec_items = ["Refinery Grade", "Optimization Score", "AI Confidence", "Enterprise Risk"]
        for item in exec_items:
            f = tk.Frame(exec_frame, bg="#1f2937")
            f.pack(fill="x", padx=12, pady=4)
            tk.Label(f, text=item, font=("Arial", 10), bg="#1f2937", fg="#9ca3af").pack(anchor="w")
            self.exec_labels[item] = tk.Label(f, text="A+", font=("Arial", 14, "bold"), bg="#1f2937", fg="#22ff88")
            self.exec_labels[item].pack(anchor="e", padx=12)

        # Center Panel - Process Flow
        center_panel = tk.Frame(main_frame, bg="#111827")
        center_panel.pack(side="left", fill="both", expand=True, padx=10)

        tk.Label(center_panel, text="REFINERY PROCESS FLOW DIAGRAM", 
                font=("Arial", 16, "bold"), bg="#111827", fg="white").pack(pady=8)

        self.canvas = tk.Canvas(center_panel, bg="#0a1428", height=480, highlightthickness=0)
        self.canvas.pack(fill="both", expand=True, padx=15, pady=5)
        self.draw_process_flow()

        # Right Panel
        right_panel = tk.Frame(main_frame, bg="#111827", width=380)
        right_panel.pack(side="right", fill="y")
        right_panel.pack_propagate(False)

        # Process Optimization
        tk.Label(right_panel, text="AI PROCESS OPTIMIZATION", font=("Arial", 15, "bold"),
                bg="#111827", fg="#22ff88").pack(pady=(10,6))

        opt_frame = tk.Frame(right_panel, bg="#1f2937")
        opt_frame.pack(fill="x", padx=12, pady=6)
        self.opt_labels = {}
        opts = [
            ("Distillation Eff", "Dist_Efficiency", "96.4%"),
            ("FCC Conversion", "FCC_Conversion", "78.9%"),
            ("Hydro Efficiency", "Hydro_Efficiency", "94.2%"),
            ("Overall Efficiency", "Overall_Efficiency", "89.7%")
        ]
        for label, key, val in opts:
            f = tk.Frame(opt_frame, bg="#1f2937")
            f.pack(fill="x", padx=12, pady=3)
            tk.Label(f, text=label, font=("Arial", 10), bg="#1f2937", fg="#9ca3af").pack(side="left")
            self.opt_labels[key] = tk.Label(f, text=val, font=("Arial", 13, "bold"), bg="#1f2937", fg="#67e8f9")
            self.opt_labels[key].pack(side="right")

        # FCC Yields
        tk.Label(right_panel, text="FCC YIELD PREDICTION", font=("Arial", 14, "bold"),
                bg="#111827", fg="#c084fc").pack(pady=(18,6))
        yield_frame = tk.Frame(right_panel, bg="#1f2937")
        yield_frame.pack(fill="x", padx=12, pady=6)
        self.yield_labels = {}
        yields = ["Gasoline", "Diesel", "LPG", "Jet Fuel"]
        for y in yields:
            f = tk.Frame(yield_frame, bg="#1f2937")
            f.pack(fill="x", padx=12, pady=2)
            tk.Label(f, text=y, font=("Arial", 10), bg="#1f2937", fg="#9ca3af").pack(side="left")
            self.yield_labels[y] = tk.Label(f, text="42.8%", font=("Arial", 12, "bold"), bg="#1f2937", fg="#c4d0ff")
            self.yield_labels[y].pack(side="right")

        # Hydrogen & Energy
        tk.Label(right_panel, text="H2 & ENERGY OPTIMIZATION", font=("Arial", 14, "bold"),
                bg="#111827", fg="#eab308").pack(pady=(18,6))
        h2_frame = tk.Frame(right_panel, bg="#1f2937")
        h2_frame.pack(fill="x", padx=12, pady=6)
        h2_items = ["H2 Consumption", "H2 Recovery", "Energy Eff"]
        for item in h2_items:
            f = tk.Frame(h2_frame, bg="#1f2937")
            f.pack(fill="x", padx=12, pady=3)
            tk.Label(f, text=item, font=("Arial", 10), bg="#1f2937", fg="#9ca3af").pack(side="left")
            key = item.replace(" ", "_").replace("Eff", "Efficiency").lower()
            self.opt_labels[key] = tk.Label(f, text="---", font=("Arial", 12, "bold"), bg="#1f2937", fg="#67e8f9")
            self.opt_labels[key].pack(side="right")

        # Predictive Maintenance
        tk.Label(right_panel, text="PREDICTIVE MAINTENANCE", font=("Arial", 14, "bold"),
                bg="#111827", fg="#f87171").pack(pady=(20,8))
        maint_frame = tk.Frame(right_panel, bg="#1f2937")
        maint_frame.pack(fill="x", padx=12, pady=6)
        self.maint_labels = {}
        for eq in ["Pump", "Compressor", "Furnace"]:
            eqf = tk.Frame(maint_frame, bg="#1f2937")
            eqf.pack(fill="x", padx=12, pady=4)
            tk.Label(eqf, text=eq, font=("Arial", 11), bg="#1f2937", fg="#93c5fd").pack(anchor="w")
            hf = tk.Frame(eqf, bg="#1f2937")
            hf.pack(fill="x")
            self.maint_labels[f"{eq}_health"] = tk.Label(hf, text="94%", font=("Arial", 16, "bold"), bg="#1f2937", fg="#22ff88")
            self.maint_labels[f"{eq}_health"].pack(side="left", padx=12)
            self.maint_labels[f"{eq}_rul"] = tk.Label(hf, text="245d", font=("Arial", 11), bg="#1f2937", fg="#a5b4fc")
            self.maint_labels[f"{eq}_rul"].pack(side="right", padx=12)

        # AI Recommendations
        tk.Label(right_panel, text="AI RECOMMENDATIONS", font=("Arial", 14, "bold"),
                bg="#111827", fg="#eab308").pack(pady=(22,6))
        
        self.ai_text = tk.Text(right_panel, bg="#1f2937", fg="#bae6fd", 
                              font=("Arial", 11), height=8, wrap=tk.WORD, relief="flat")
        self.ai_text.pack(fill="both", expand=True, padx=12, pady=5)
        self.update_ai_recommendations()

        # Bottom Panel
        bottom_panel = tk.Frame(self.root, bg="#111827", height=380)
        bottom_panel.pack(fill="x", side="bottom", padx=12, pady=10)
        bottom_panel.pack_propagate(False)

        graph_frame = tk.Frame(bottom_panel, bg="#111827")
        graph_frame.pack(fill="both", expand=True)

        self.fig_profit, self.ax_profit = plt.subplots(figsize=(4.8, 3.2), facecolor="#111827")
        self.ax_profit.set_facecolor("#1f2937")
        self.canvas_profit = FigureCanvasTkAgg(self.fig_profit, graph_frame)
        self.canvas_profit.get_tk_widget().pack(side="left", fill="both", expand=True, padx=6)

        self.fig_temp, self.ax_temp = plt.subplots(figsize=(4.8, 3.2), facecolor="#111827")
        self.ax_temp.set_facecolor("#1f2937")
        self.canvas_temp = FigureCanvasTkAgg(self.fig_temp, graph_frame)
        self.canvas_temp.get_tk_widget().pack(side="left", fill="both", expand=True, padx=6)

        self.fig_carbon, self.ax_carbon = plt.subplots(figsize=(4.8, 3.2), facecolor="#111827")
        self.ax_carbon.set_facecolor("#1f2937")
        self.canvas_carbon = FigureCanvasTkAgg(self.fig_carbon, graph_frame)
        self.canvas_carbon.get_tk_widget().pack(side="left", fill="both", expand=True, padx=6)

        self.fig_eff, self.ax_eff = plt.subplots(figsize=(4.8, 3.2), facecolor="#111827")
        self.ax_eff.set_facecolor("#1f2937")
        self.canvas_eff = FigureCanvasTkAgg(self.fig_eff, graph_frame)
        self.canvas_eff.get_tk_widget().pack(side="left", fill="both", expand=True, padx=6)

        self.update_graphs()

        # Footer
        footer = tk.Frame(self.root, bg="#081229", height=30)
        footer.pack(fill="x", side="bottom")
        tk.Label(footer, text="© 2035 xAI Industrial • Digital Twin v4.3 • 2146 Sensors • AI Confidence 99.7% • Production Mode", 
                bg="#081229", fg="#64748b", font=("Arial", 9)).pack(pady=6)

    def draw_process_flow(self):
        for i in range(0, 1300, 40):
            self.canvas.create_line(i, 0, i, 480, fill="#1e2937", width=1)
        for i in range(0, 480, 40):
            self.canvas.create_line(0, i, 1300, i, fill="#1e2937", width=1)

        self.canvas.create_rectangle(70, 100, 260, 250, fill="#1e40af", outline="#60a5fa", width=4)
        self.canvas.create_text(165, 175, text="CDU", fill="white", font=("Arial", 14, "bold"))

        self.canvas.create_rectangle(400, 60, 590, 210, fill="#7e22ce", outline="#c084fc", width=4)
        self.canvas.create_text(495, 135, text="FCC", fill="white", font=("Arial", 14, "bold"))

        self.canvas.create_rectangle(730, 140, 920, 290, fill="#166534", outline="#4ade80", width=4)
        self.canvas.create_text(825, 215, text="HYDROTREATER", fill="white", font=("Arial", 12, "bold"))

        self.canvas.create_rectangle(1050, 80, 1180, 310, fill="#854d0e", outline="#fbbf24", width=4)
        self.canvas.create_text(1115, 195, text="PRODUCTS", fill="white", font=("Arial", 13, "bold"))

        self.canvas.create_line(260, 175, 400, 135, fill="#67e8f9", width=8, arrow=tk.LAST)
        self.canvas.create_line(590, 135, 730, 215, fill="#67e8f9", width=8, arrow=tk.LAST)
        self.canvas.create_line(920, 215, 1050, 195, fill="#67e8f9", width=8, arrow=tk.LAST)

        self.sensor_dots = {}
        positions = [(165,230), (495,190), (825,270)]
        for i, (x,y) in enumerate(positions):
            dot = self.canvas.create_oval(x-12, y-12, x+12, y+12, fill="#22ff88", outline="white", width=2.5)
            self.sensor_dots[i] = dot

    def update_clock(self):
        current_time = datetime.now().strftime("%H:%M:%S | %d %b %Y")
        self.clock_label.config(text=current_time)
        self.root.after(1000, self.update_clock)

    def update_ai_recommendations(self):
        self.ai_text.delete(1.0, tk.END)
        for rec in self.ai_recommendations:
            self.ai_text.insert(tk.END, f"→ {rec}\n\n")
        self.ai_text.insert(tk.END, "AI CONFIDENCE: 99.1%", "bold")
        self.ai_text.tag_config("bold", font=("Arial", 11, "bold"), foreground="#eab308")

    def simulate_data(self):
        self.sensor_data['CDU_Temp'] += random.uniform(-1.2, 1.2)
        self.sensor_data['FCC_Temp'] += random.uniform(-2.0, 2.0)
        self.sensor_data['Hydro_Temp'] += random.uniform(-1.0, 1.0)
        self.sensor_data['Profit'] = max(950000, self.sensor_data['Profit'] + random.uniform(-15000, 28000))
        self.sensor_data['Carbon_Index'] = max(37, min(54, self.sensor_data['Carbon_Index'] + random.uniform(-0.5, 0.5)))
        self.sensor_data['Plant_Health'] = max(91, min(99.8, self.sensor_data['Plant_Health'] + random.uniform(-0.25, 0.22)))

        self.optimization_data['Dist_Efficiency'] = max(92, min(98.5, self.optimization_data['Dist_Efficiency'] + random.uniform(-0.3, 0.4)))
        self.optimization_data['FCC_Conversion'] = max(74, min(82, self.optimization_data['FCC_Conversion'] + random.uniform(-0.6, 0.7)))
        self.optimization_data['Hydro_Efficiency'] = max(90, min(97, self.optimization_data['Hydro_Efficiency'] + random.uniform(-0.4, 0.45)))
        self.optimization_data['Overall_Efficiency'] = (self.optimization_data['Dist_Efficiency'] + self.optimization_data['FCC_Conversion']*0.6 + self.optimization_data['Hydro_Efficiency']*0.8) / 2.4

        self.optimization_data['Gasoline_Yield'] = max(39, min(46, self.optimization_data['Gasoline_Yield'] + random.uniform(-0.4, 0.5)))
        self.optimization_data['Diesel_Yield'] = max(29, min(34, self.optimization_data['Diesel_Yield'] + random.uniform(-0.3, 0.4)))
        self.optimization_data['LPG_Yield'] = max(11, min(14, self.optimization_data['LPG_Yield'] + random.uniform(-0.2, 0.25)))
        self.optimization_data['Jet_Yield'] = max(16, min(20, self.optimization_data['Jet_Yield'] + random.uniform(-0.25, 0.3)))

        self.optimization_data['H2_Consumption'] += random.uniform(-45, 55)
        self.optimization_data['H2_Recovery'] = max(89, min(95.5, self.optimization_data['H2_Recovery'] + random.uniform(-0.3, 0.35)))
        self.optimization_data['H2_Purity'] = max(98.5, min(99.8, self.optimization_data['H2_Purity'] + random.uniform(-0.1, 0.15)))
        self.optimization_data['Energy_Eff'] = max(87, min(94.5, self.optimization_data['Energy_Eff'] + random.uniform(-0.35, 0.4)))

        self.maintenance_data['Pump_Health'] = max(75, min(99, self.maintenance_data['Pump_Health'] + random.uniform(-0.5, 0.4)))
        self.maintenance_data['Compressor_Health'] = max(70, min(98, self.maintenance_data['Compressor_Health'] + random.uniform(-0.7, 0.5)))
        self.maintenance_data['Furnace_Health'] = max(78, min(99, self.maintenance_data['Furnace_Health'] + random.uniform(-0.6, 0.45)))

        self.maintenance_data['Pump_RUL'] = int(self.maintenance_data['Pump_Health'] * 2.55)
        self.maintenance_data['Compressor_RUL'] = int(self.maintenance_data['Compressor_Health'] * 1.4)
        self.maintenance_data['Furnace_RUL'] = int(self.maintenance_data['Furnace_Health'] * 1.85)

        now = datetime.now().strftime("%H:%M")
        self.history['time'].append(now)
        self.history['profit'].append(self.sensor_data['Profit'] / 1000000)
        self.history['temp_cdu'].append(self.sensor_data['CDU_Temp'])
        self.history['carbon'].append(self.sensor_data['Carbon_Index'])
        self.history['efficiency'].append(self.optimization_data['Overall_Efficiency'])
        self.history['h2_cons'].append(self.optimization_data['H2_Consumption'] / 1000)
        self.history['energy_eff'].append(self.optimization_data['Energy_Eff'])

        if len(self.history['time']) > 20:
            for k in self.history:
                self.history[k] = self.history[k][-20:]

    def update_ui(self):
        self.kpi_labels["profit"].config(text=f"${self.sensor_data['Profit']/1000000:.2f}M")
        self.kpi_labels["carbon"].config(text=f"{self.sensor_data['Carbon_Index']:.1f}")
        self.kpi_labels["health"].config(text=f"{self.sensor_data['Plant_Health']:.1f}%")

        self.opt_labels["Dist_Efficiency"].config(text=f"{self.optimization_data['Dist_Efficiency']:.1f}%")
        self.opt_labels["FCC_Conversion"].config(text=f"{self.optimization_data['FCC_Conversion']:.1f}%")
        self.opt_labels["Hydro_Efficiency"].config(text=f"{self.optimization_data['Hydro_Efficiency']:.1f}%")
        self.opt_labels["Overall_Efficiency"].config(text=f"{self.optimization_data['Overall_Efficiency']:.1f}%")

        self.yield_labels["Gasoline"].config(text=f"{self.optimization_data['Gasoline_Yield']:.1f}%")
        self.yield_labels["Diesel"].config(text=f"{self.optimization_data['Diesel_Yield']:.1f}%")
        self.yield_labels["LPG"].config(text=f"{self.optimization_data['LPG_Yield']:.1f}%")
        self.yield_labels["Jet Fuel"].config(text=f"{self.optimization_data['Jet_Yield']:.1f}%")

        self.opt_labels["h2_consumption"].config(text=f"{int(self.optimization_data['H2_Consumption'])} kg/h")
        self.opt_labels["h2_recovery"].config(text=f"{self.optimization_data['H2_Recovery']:.1f}%")
        self.opt_labels["energy_efficiency"].config(text=f"{self.optimization_data['Energy_Eff']:.1f}%")

        for eq in ["Pump", "Compressor", "Furnace"]:
            h = self.maintenance_data[f"{eq}_Health"]
            col = "#22ff88" if h > 90 else "#fbbf24" if h > 80 else "#f87171"
            self.maint_labels[f"{eq}_health"].config(text=f"{h:.1f}%", fg=col)
            self.maint_labels[f"{eq}_rul"].config(text=f"{self.maintenance_data[f'{eq}_RUL']}d")

        self.exec_labels["Refinery Grade"].config(text="A+")
        self.exec_labels["Optimization Score"].config(text=f"{int(self.optimization_data['Overall_Efficiency'])}")
        self.exec_labels["AI Confidence"].config(text="99.2%")
        self.exec_labels["Enterprise Risk"].config(text="LOW", fg="#22ff88")

    def update_graphs(self):
        self.ax_profit.clear()
        self.ax_profit.plot(self.history['time'], self.history['profit'], color="#22ff88", linewidth=3, marker='o')
        self.ax_profit.set_title("Profit Trend ($M)", color="white", fontsize=11)
        self.ax_profit.tick_params(colors="#9ca3af")
        self.ax_profit.grid(True, alpha=0.2)
        self.fig_profit.tight_layout()
        self.canvas_profit.draw()

        self.ax_temp.clear()
        self.ax_temp.plot(self.history['time'], self.history['temp_cdu'], color="#f87171", linewidth=3, marker='o')
        self.ax_temp.set_title("CDU Temperature", color="white", fontsize=11)
        self.ax_temp.tick_params(colors="#9ca3af")
        self.ax_temp.grid(True, alpha=0.2)
        self.fig_temp.tight_layout()
        self.canvas_temp.draw()

        self.ax_carbon.clear()
        self.ax_carbon.plot(self.history['time'], self.history['carbon'], color="#fbbf24", linewidth=3, marker='o')
        self.ax_carbon.set_title("Carbon Intensity", color="white", fontsize=11)
        self.ax_carbon.tick_params(colors="#9ca3af")
        self.ax_carbon.grid(True, alpha=0.2)
        self.fig_carbon.tight_layout()
        self.canvas_carbon.draw()

        self.ax_eff.clear()
        self.ax_eff.plot(self.history['time'], self.history['efficiency'], color="#67e8f9", linewidth=3, marker='o')
        self.ax_eff.set_title("Refinery Efficiency %", color="white", fontsize=11)
        self.ax_eff.tick_params(colors="#9ca3af")
        self.ax_eff.grid(True, alpha=0.2)
        self.fig_eff.tight_layout()
        self.canvas_eff.draw()

    def refresh_all(self):
        self.simulate_data()
        self.update_ui()
        self.update_graphs()
        self.update_ai_recommendations()

        for dot in self.sensor_dots.values():
            if random.random() > 0.6:
                self.canvas.itemconfig(dot, fill="#22ff88")
            else:
                self.canvas.itemconfig(dot, fill="#86efac")

    def start_auto_refresh(self):
        def loop():
            while True:
                try:
                    self.root.after(0, self.refresh_all)
                    time.sleep(2.3)
                except:
                    break
        threading.Thread(target=loop, daemon=True).start()

    def run(self):
        self.root.mainloop()


if __name__ == "__main__":
    app = AIPlant2035DigitalTwinV43()
    app.run()