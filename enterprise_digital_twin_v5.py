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
import os

class AIPlant2035DigitalTwinV5:
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("AI PLANT 2035 - Enterprise Digital Twin v5.0 | ExxonMobil • Shell • Reliance • Saudi Aramco")
        self.root.geometry("1920x1080")
        self.root.configure(bg="#081229")
        self.root.state('zoomed')

        # Database Setup
        self.conn = sqlite3.connect('plant_data_v5.db')
        self.create_db()

        # Data
        self.sensor_data = {
            'CDU_Temp': 385.2, 'CDU_Press': 2.8, 'CDU_Flow': 1450,
            'FCC_Temp': 520.5, 'FCC_Press': 1.9, 'FCC_Flow': 920,
            'Hydro_Temp': 340.8, 'Hydro_Press': 85.4, 'Hydro_Flow': 680,
            'Profit': 1245000, 'Carbon_Index': 42.3, 'Plant_Health': 96.5
        }

        self.maintenance_data = {
            'Pump_Health': 94.2, 'Compressor_Health': 87.8, 'HeatEx_Health': 91.5,
            'Furnace_Health': 89.7, 'Valve_Health': 95.1,
            'Pump_RUL': 245, 'Compressor_RUL': 118, 'HeatEx_RUL': 167,
            'Furnace_RUL': 142, 'Valve_RUL': 289
        }

        self.optimization_data = {
            'Dist_Efficiency': 96.4, 'FCC_Conversion': 78.9, 'Hydro_Efficiency': 94.2,
            'Overall_Efficiency': 89.7, 'Gasoline_Yield': 42.8, 'Diesel_Yield': 31.5,
            'H2_Consumption': 1850, 'Energy_Eff': 91.3, 'Carbon_Reduction': 14.8
        }

        self.history = {k: [] for k in ['time', 'profit', 'temp', 'carbon', 'efficiency', 'energy', 'maintenance']}

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
        cursor.execute('''CREATE TABLE IF NOT EXISTS readings (
            timestamp TEXT, profit REAL, cdu_temp REAL, carbon REAL, 
            efficiency REAL, pump_health REAL)''')
        self.conn.commit()

    def load_initial_data(self):
        now = datetime.now().strftime("%H:%M")
        for _ in range(10):
            self.history['time'].append(now)
            self.history['profit'].append(1.24)
            self.history['temp'].append(385)
            self.history['carbon'].append(42)
            self.history['efficiency'].append(89.7)
            self.history['energy'].append(91)
            self.history['maintenance'].append(92)

    def setup_ui(self):
        # Header
        header = tk.Frame(self.root, bg="#111827", height=90)
        header.pack(fill="x")
        header.pack_propagate(False)
        tk.Label(header, text="AI PLANT 2035", font=("Arial", 32, "bold"), bg="#111827", fg="#22ff88").pack(side="left", padx=30, pady=20)
        tk.Label(header, text="ENTERPRISE DIGITAL TWIN v5.0 • LIVE", font=("Arial", 16, "bold"), bg="#111827", fg="#22ff88").pack(side="left", padx=20)
        
        self.clock_label = tk.Label(header, text="", font=("Arial", 16), bg="#111827", fg="#a1a1aa")
        self.clock_label.pack(side="right", padx=30)
        self.update_clock()

        # Main Frame
        main_frame = tk.Frame(self.root, bg="#081229")
        main_frame.pack(fill="both", expand=True, padx=10, pady=10)

        # Left Panel
        left_panel = tk.Frame(main_frame, bg="#111827", width=320)
        left_panel.pack(side="left", fill="y", padx=(0, 10))
        left_panel.pack_propagate(False)

        tk.Label(left_panel, text="EXECUTIVE CONTROL ROOM", font=("Arial", 16, "bold"), bg="#111827", fg="white").pack(pady=12)
        
        self.exec_labels = {}
        exec_items = ["Plant Grade", "Profit Score", "Risk Index", "AI Maturity", "Overall Score"]
        for item in exec_items:
            f = tk.Frame(left_panel, bg="#1f2937")
            f.pack(fill="x", padx=15, pady=6)
            tk.Label(f, text=item, font=("Arial", 11), bg="#1f2937", fg="#9ca3af").pack(anchor="w", padx=12)
            self.exec_labels[item] = tk.Label(f, text="A+", font=("Arial", 18, "bold"), bg="#1f2937", fg="#22ff88")
            self.exec_labels[item].pack(anchor="e", padx=12, pady=4)

        # Center Panel
        center_panel = tk.Frame(main_frame, bg="#111827")
        center_panel.pack(side="left", fill="both", expand=True, padx=10)

        tk.Label(center_panel, text="REFINERY DIGITAL TWIN", font=("Arial", 16, "bold"), bg="#111827", fg="white").pack(pady=8)
        
        self.canvas = tk.Canvas(center_panel, bg="#0a1428", height=460, highlightthickness=0)
        self.canvas.pack(fill="both", expand=True, padx=15, pady=5)
        self.draw_process_flow()

        # Simulator Controls
        sim_frame = tk.Frame(center_panel, bg="#1f2937")
        sim_frame.pack(fill="x", padx=15, pady=8)
        tk.Label(sim_frame, text="DIGITAL TWIN SIMULATOR", font=("Arial", 14, "bold"), bg="#1f2937", fg="#eab308").pack(pady=5)
        
        btn_frame = tk.Frame(sim_frame, bg="#1f2937")
        btn_frame.pack(pady=8)
        tk.Button(btn_frame, text="+10% Feed", command=self.sim_feed_plus, bg="#22ff88", fg="black", font=("Arial", 10, "bold")).pack(side="left", padx=5)
        tk.Button(btn_frame, text="-10% Feed", command=self.sim_feed_minus, bg="#fbbf24", fg="black", font=("Arial", 10, "bold")).pack(side="left", padx=5)
        tk.Button(btn_frame, text="Crude Switch", command=self.sim_crude_switch, bg="#60a5fa", fg="black", font=("Arial", 10, "bold")).pack(side="left", padx=5)
        tk.Button(btn_frame, text="Emergency Shutdown", command=self.sim_shutdown, bg="#ef4444", fg="white", font=("Arial", 10, "bold")).pack(side="left", padx=5)

        # Right Panel
        right_panel = tk.Frame(main_frame, bg="#111827", width=380)
        right_panel.pack(side="right", fill="y")
        right_panel.pack_propagate(False)

        # Predictive Maintenance
        tk.Label(right_panel, text="PREDICTIVE MAINTENANCE AI", font=("Arial", 15, "bold"), bg="#111827", fg="#f87171").pack(pady=10)
        self.maint_labels = {}
        eqs = ["Pump", "Compressor", "Heat Exchanger", "Furnace", "Control Valve"]
        for eq in eqs:
            f = tk.Frame(right_panel, bg="#1f2937")
            f.pack(fill="x", padx=12, pady=5)
            tk.Label(f, text=eq, bg="#1f2937", fg="#93c5fd", font=("Arial", 11, "bold")).pack(anchor="w", padx=12)
            hf = tk.Frame(f, bg="#1f2937")
            hf.pack(fill="x", padx=12)
            self.maint_labels[f"{eq}_h"] = tk.Label(hf, text="92%", font=("Arial", 16, "bold"), bg="#1f2937", fg="#22ff88")
            self.maint_labels[f"{eq}_h"].pack(side="left")
            self.maint_labels[f"{eq}_f"] = tk.Label(hf, text="3.2%", font=("Arial", 12), bg="#1f2937", fg="#f87171")
            self.maint_labels[f"{eq}_f"].pack(side="right")

        # Net Zero Center
        tk.Label(right_panel, text="NET ZERO CENTER", font=("Arial", 15, "bold"), bg="#111827", fg="#22ff88").pack(pady=(20,8))
        nz_frame = tk.Frame(right_panel, bg="#1f2937")
        nz_frame.pack(fill="x", padx=12, pady=6)
        self.nz_labels = {}
        for label in ["CO2 Emissions", "Carbon Intensity", "Net Zero Progress"]:
            f = tk.Frame(nz_frame, bg="#1f2937")
            f.pack(fill="x", padx=12, pady=4)
            tk.Label(f, text=label, bg="#1f2937", fg="#9ca3af").pack(anchor="w")
            self.nz_labels[label] = tk.Label(f, text="124 kt", font=("Arial", 14, "bold"), bg="#1f2937", fg="#67e8f9")
            self.nz_labels[label].pack(anchor="e")

        # AI Decision Engine
        tk.Label(right_panel, text="AI DECISION ENGINE", font=("Arial", 15, "bold"), bg="#111827", fg="#eab308").pack(pady=(20,8))
        self.ai_text = tk.Text(right_panel, bg="#1f2937", fg="#bae6fd", font=("Arial", 11), height=9, wrap=tk.WORD)
        self.ai_text.pack(fill="both", expand=True, padx=12, pady=5)
        self.update_ai_recommendations()

        # AI Copilot
        tk.Label(right_panel, text="AI COPILOT", font=("Arial", 14, "bold"), bg="#111827", fg="#c084fc").pack(pady=(15,5))
        self.chat_entry = tk.Entry(right_panel, bg="#1f2937", fg="white", font=("Arial", 11))
        self.chat_entry.pack(fill="x", padx=12, pady=5)
        self.chat_entry.bind("<Return>", self.copilot_response)
        self.chat_log = tk.Text(right_panel, bg="#1f2937", fg="#a5f3fc", height=6, font=("Arial", 10))
        self.chat_log.pack(fill="both", expand=True, padx=12, pady=5)

        # Report Center
        report_frame = tk.Frame(right_panel, bg="#111827")
        report_frame.pack(fill="x", padx=12, pady=15)
        tk.Label(report_frame, text="REPORT CENTER", font=("Arial", 14, "bold"), bg="#111827", fg="#eab308").pack()
        tk.Button(report_frame, text="Export Excel", command=self.export_excel, bg="#22ff88", fg="black").pack(side="left", padx=5, pady=8)
        tk.Button(report_frame, text="Export PDF", command=self.export_pdf, bg="#60a5fa", fg="white").pack(side="left", padx=5, pady=8)

        # Bottom Graphs
        bottom = tk.Frame(self.root, bg="#111827", height=380)
        bottom.pack(fill="x", side="bottom", padx=12, pady=8)
        graph_frame = tk.Frame(bottom, bg="#111827")
        graph_frame.pack(fill="both", expand=True)

        self.figures = []
        self.axes = []
        self.canvases = []
        titles = ["Profit Trend", "Carbon Trend", "Efficiency Trend", "Maintenance Trend"]
        colors = ["#22ff88", "#f87171", "#67e8f9", "#fbbf24"]
        for i in range(4):
            fig, ax = plt.subplots(figsize=(5, 3), facecolor="#111827")
            ax.set_facecolor("#1f2937")
            ax.set_title(titles[i], color="white", fontsize=12)
            canvas = FigureCanvasTkAgg(fig, graph_frame)
            canvas.get_tk_widget().pack(side="left", fill="both", expand=True, padx=6)
            self.figures.append(fig)
            self.axes.append(ax)
            self.canvases.append(canvas)

        self.update_graphs()

        # Footer
        footer = tk.Frame(self.root, bg="#081229", height=35)
        footer.pack(fill="x", side="bottom")
        tk.Label(footer, text="© 2035 xAI Industrial • Digital Twin v5.0 • 2846 Sensors Online • AI Confidence 99.8%", bg="#081229", fg="#64748b", font=("Arial", 10)).pack(pady=8)

    def draw_process_flow(self):
        self.canvas.delete("all")
        for i in range(0, 1300, 40):
            self.canvas.create_line(i, 0, i, 460, fill="#1e2937")
        for i in range(0, 460, 40):
            self.canvas.create_line(0, i, 1300, i, fill="#1e2937")

        units = [("CDU", 80, 100, "#1e40af"), ("FCC", 380, 70, "#7e22ce"), ("Hydrotreater", 720, 150, "#166534")]
        for name, x, y, color in units:
            self.canvas.create_rectangle(x, y, x+180, y+140, fill=color, outline="#60a5fa", width=4)
            self.canvas.create_text(x+90, y+70, text=name, fill="white", font=("Arial", 14, "bold"))

        self.canvas.create_line(260, 170, 380, 140, fill="#67e8f9", width=9, arrow=tk.LAST)
        self.canvas.create_line(560, 140, 720, 210, fill="#67e8f9", width=9, arrow=tk.LAST)

    def update_clock(self):
        self.clock_label.config(text=datetime.now().strftime("%H:%M:%S | %d %b %Y"))
        self.root.after(1000, self.update_clock)

    def update_ai_recommendations(self):
        self.ai_text.delete(1.0, tk.END)
        for rec in self.ai_recommendations:
            self.ai_text.insert(tk.END, f"→ {rec}\n\n")
        self.ai_text.insert(tk.END, "\nAI CONFIDENCE: 99.4%", "bold")
        self.ai_text.tag_config("bold", foreground="#eab308", font=("Arial", 11, "bold"))

    def copilot_response(self, event=None):
        query = self.chat_entry.get().strip().lower()
        self.chat_entry.delete(0, tk.END)
        response = "AI Copilot: "
        if "profit" in query:
            response += "Profit dropped due to lower FCC conversion. Recommendation: Increase feed rate."
        elif "carbon" in query:
            response += "To reduce carbon: Optimize furnace duty and improve heat integration."
        elif "maintenance" in query:
            response += "Schedule Compressor inspection. RUL is low."
        else:
            response += "Understood. Optimizing parameters for maximum profitability."
        self.chat_log.insert(tk.END, response + "\n\n")
        self.chat_log.see(tk.END)

    def simulate_data(self):
        self.sensor_data['Profit'] += random.uniform(-12000, 28000)
        self.sensor_data['Carbon_Index'] += random.uniform(-0.6, 0.6)
        self.sensor_data['Plant_Health'] = max(90, min(99.8, self.sensor_data['Plant_Health'] + random.uniform(-0.3, 0.3)))

        for key in list(self.maintenance_data.keys()):
            if "Health" in key:
                self.maintenance_data[key] = max(75, min(99, self.maintenance_data[key] + random.uniform(-0.8, 0.7)))

        self.optimization_data['Overall_Efficiency'] = max(86, min(94, self.optimization_data['Overall_Efficiency'] + random.uniform(-0.4, 0.5)))

        # Save to DB
        cursor = self.conn.cursor()
        cursor.execute("INSERT INTO readings VALUES (?,?,?,?,?,?)", 
                      (datetime.now().isoformat(), self.sensor_data['Profit'], 
                       self.sensor_data['CDU_Temp'], self.sensor_data['Carbon_Index'],
                       self.optimization_data['Overall_Efficiency'], self.maintenance_data['Pump_Health']))
        self.conn.commit()

        now = datetime.now().strftime("%H:%M")
        self.history['time'].append(now)
        self.history['profit'].append(self.sensor_data['Profit']/1000000)
        self.history['temp'].append(self.sensor_data['CDU_Temp'])
        self.history['carbon'].append(self.sensor_data['Carbon_Index'])
        self.history['efficiency'].append(self.optimization_data['Overall_Efficiency'])
        self.history['energy'].append(self.optimization_data['Energy_Eff'])
        self.history['maintenance'].append(sum(self.maintenance_data[k] for k in self.maintenance_data if "Health" in k)/5)

        if len(self.history['time']) > 25:
            for k in self.history:
                self.history[k] = self.history[k][-25:]

    def update_ui(self):
        eq_map = {"Pump": "Pump_Health", "Compressor": "Compressor_Health", "Heat Exchanger": "HeatEx_Health",
                  "Furnace": "Furnace_Health", "Control Valve": "Valve_Health"}
        for eq in eq_map:
            h = self.maintenance_data[eq_map[eq]]
            col = "#22ff88" if h > 90 else "#fbbf24" if h > 80 else "#ef4444"
            self.maint_labels[f"{eq}_h"].config(text=f"{h:.1f}%", fg=col)

        self.nz_labels["CO2 Emissions"].config(text=f"{int(self.sensor_data['Carbon_Index']*120)} kt")
        self.nz_labels["Carbon Intensity"].config(text=f"{self.sensor_data['Carbon_Index']:.1f}")
        self.nz_labels["Net Zero Progress"].config(text="76.4%")

        self.exec_labels["Overall Score"].config(text=f"{int(self.optimization_data['Overall_Efficiency'])}")
        self.update_ai_recommendations()

    def update_graphs(self):
        titles = ["Profit Trend", "Carbon Trend", "Efficiency Trend", "Maintenance Trend"]
        data_keys = ['profit', 'carbon', 'efficiency', 'maintenance']
        colors = ["#22ff88", "#f87171", "#67e8f9", "#fbbf24"]
        for i, ax in enumerate(self.axes):
            ax.clear()
            ax.plot(self.history['time'], self.history[data_keys[i]], color=colors[i], linewidth=3, marker='o')
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
                    time.sleep(3)
                except:
                    break
        threading.Thread(target=loop, daemon=True).start()

    def sim_feed_plus(self):
        self.sensor_data['FCC_Flow'] += 80
        messagebox.showinfo("Simulator", "Feed rate increased by 10%")

    def sim_feed_minus(self):
        self.sensor_data['FCC_Flow'] -= 80
        messagebox.showinfo("Simulator", "Feed rate decreased by 10%")

    def sim_crude_switch(self):
        self.sensor_data['Carbon_Index'] -= 2
        messagebox.showinfo("Simulator", "Crude blend switched successfully")

    def sim_shutdown(self):
        messagebox.showwarning("Emergency", "Shutdown initiated. All units safe.")

    def export_excel(self):
        df = pd.DataFrame(self.history)
        df.to_excel("plant_report_v5.xlsx", index=False)
        messagebox.showinfo("Export", "Excel report generated: plant_report_v5.xlsx")

    def export_pdf(self):
        with open("plant_summary_v5.txt", "w") as f:
            f.write("AI PLANT 2035 EXECUTIVE REPORT\n")
            f.write(f"Profit: ${self.sensor_data['Profit']/1000000:.2f}M\n")
            f.write(f"Carbon Intensity: {self.sensor_data['Carbon_Index']:.1f}\n")
            f.write(f"Overall Efficiency: {self.optimization_data['Overall_Efficiency']:.1f}%\n")
        messagebox.showinfo("Export", "Summary report saved as plant_summary_v5.txt")

    def run(self):
        self.root.mainloop()


if __name__ == "__main__":
    app = AIPlant2035DigitalTwinV5()
    app.run()