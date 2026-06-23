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

class AIPlant2035V31:
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("AI PLANT 2035 - Autonomous AI Energy Enterprise V31 | ExxonMobil • Shell • Reliance")
        self.root.geometry("1920x1080")
        self.root.configure(bg="#081229")
        self.root.state('zoomed')

        self.db_path = "plant_data.db"
        self.conn = None
        self.init_database()

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
            'Overall_Efficiency': 89.7
        }

        self.history = {k: [] for k in ['time', 'profit', 'temp', 'carbon', 'efficiency', 'maintenance']}
        self.ai_recommendations = [
            "Increase FCC feed rate by 4.2% → +1.8% Profit",
            "Reduce Furnace duty by 3% → Energy saving",
            "Optimize Hydrogen recycle → +1.8% recovery"
        ]

        self.alarms = []

        self.setup_ui()
        self.load_initial_data()
        self.start_auto_refresh()

    def init_database(self):
        try:
            self.conn = sqlite3.connect(self.db_path)
            cursor = self.conn.cursor()
            
            cursor.execute('''CREATE TABLE IF NOT EXISTS sensor_history (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                timestamp TEXT,
                temperature REAL,
                pressure REAL,
                flowrate REAL,
                profit REAL,
                carbon REAL,
                efficiency REAL
            )''')
            
            cursor.execute('''CREATE TABLE IF NOT EXISTS alarm_history (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                timestamp TEXT,
                alarm TEXT
            )''')
            
            cursor.execute('''CREATE TABLE IF NOT EXISTS ai_decisions (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                timestamp TEXT,
                decision TEXT
            )''')
            
            cursor.execute('''CREATE TABLE IF NOT EXISTS maintenance_history (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                timestamp TEXT,
                equipment TEXT,
                health REAL
            )''')
            
            self.conn.commit()
        except Exception as e:
            print("Database init error:", e)

    def save_sensor_data(self):
        try:
            cursor = self.conn.cursor()
            cursor.execute("""INSERT INTO sensor_history 
                (timestamp, temperature, pressure, flowrate, profit, carbon, efficiency)
                VALUES (?,?,?,?,?,?,?)""", (
                    datetime.now().isoformat(),
                    self.sensor_data['CDU_Temp'],
                    self.sensor_data['CDU_Press'],
                    self.sensor_data['CDU_Flow'],
                    self.sensor_data['Profit'],
                    self.sensor_data['Carbon_Index'],
                    self.optimization_data['Overall_Efficiency']
                ))
            self.conn.commit()
        except:
            pass

    def save_alarm(self, alarm_text):
        try:
            cursor = self.conn.cursor()
            cursor.execute("INSERT INTO alarm_history (timestamp, alarm) VALUES (?,?)",
                          (datetime.now().isoformat(), alarm_text))
            self.conn.commit()
            self.alarms.append(alarm_text)
        except:
            pass

    def save_ai_decision(self, decision):
        try:
            cursor = self.conn.cursor()
            cursor.execute("INSERT INTO ai_decisions (timestamp, decision) VALUES (?,?)",
                          (datetime.now().isoformat(), decision))
            self.conn.commit()
        except:
            pass

    def setup_ui(self):
        # Header
        header = tk.Frame(self.root, bg="#111827", height=85)
        header.pack(fill="x")
        header.pack_propagate(False)
        tk.Label(header, text="AI PLANT 2035", font=("Arial", 28, "bold"), bg="#111827", fg="#22ff88").pack(side="left", padx=30, pady=18)
        tk.Label(header, text="AUTONOMOUS AI ENERGY ENTERPRISE V31", font=("Arial", 14, "bold"), bg="#111827", fg="#22ff88").pack(side="left", padx=20)
        
        self.clock_label = tk.Label(header, text="", font=("Arial", 16), bg="#111827", fg="#a1a1aa")
        self.clock_label.pack(side="right", padx=30)
        self.update_clock()

        main_frame = tk.Frame(self.root, bg="#081229")
        main_frame.pack(fill="both", expand=True, padx=10, pady=10)

        # Left Panel - Executive + Historian
        left_panel = tk.Frame(main_frame, bg="#111827", width=340)
        left_panel.pack(side="left", fill="y", padx=(0,10))
        left_panel.pack_propagate(False)

        tk.Label(left_panel, text="CEO WAR ROOM", font=("Arial", 16, "bold"), bg="#111827", fg="white").pack(pady=12)
        
        self.exec_labels = {}
        items = ["Plant Score", "Profit Score", "Reliability", "ESG Score", "AI Maturity"]
        for item in items:
            f = tk.Frame(left_panel, bg="#1f2937")
            f.pack(fill="x", padx=15, pady=6)
            tk.Label(f, text=item, font=("Arial", 11), bg="#1f2937", fg="#9ca3af").pack(anchor="w", padx=12)
            self.exec_labels[item] = tk.Label(f, text="A+", font=("Arial", 18, "bold"), bg="#1f2937", fg="#22ff88")
            self.exec_labels[item].pack(anchor="e", padx=12)

        # Historian Panel
        tk.Label(left_panel, text="PLANT HISTORIAN", font=("Arial", 15, "bold"), bg="#111827", fg="#67e8f9").pack(pady=(25,8))
        self.hist_stats = {}
        hist_items = ["Records Stored", "Last Record", "Total Alarms", "AI Decisions"]
        for item in hist_items:
            f = tk.Frame(left_panel, bg="#1f2937")
            f.pack(fill="x", padx=15, pady=4)
            tk.Label(f, text=item, bg="#1f2937", fg="#9ca3af").pack(anchor="w", padx=12)
            self.hist_stats[item] = tk.Label(f, text="1248", bg="#1f2937", fg="#67e8f9", font=("Arial", 13, "bold"))
            self.hist_stats[item].pack(anchor="e", padx=12)

        # Database Status
        tk.Label(left_panel, text="DATABASE STATUS", font=("Arial", 15, "bold"), bg="#111827", fg="#eab308").pack(pady=(20,8))
        self.db_status = tk.Label(left_panel, text="CONNECTED • HEALTHY", bg="#1f2937", fg="#22ff88", font=("Arial", 12, "bold"))
        self.db_status.pack(pady=8)

        # Center Panel
        center_panel = tk.Frame(main_frame, bg="#111827")
        center_panel.pack(side="left", fill="both", expand=True, padx=10)

        tk.Label(center_panel, text="REAL-TIME DIGITAL TWIN", font=("Arial", 16, "bold"), bg="#111827", fg="white").pack(pady=8)
        self.canvas = tk.Canvas(center_panel, bg="#0a1428", height=460, highlightthickness=0)
        self.canvas.pack(fill="both", expand=True, padx=15, pady=5)
        self.draw_process_flow()

        # Simulator Controls
        sim_frame = tk.Frame(center_panel, bg="#1f2937")
        sim_frame.pack(fill="x", padx=15, pady=8)
        tk.Label(sim_frame, text="AUTONOMOUS SIMULATOR", font=("Arial", 14, "bold"), bg="#1f2937", fg="#eab308").pack(pady=5)
        btn_frame = tk.Frame(sim_frame, bg="#1f2937")
        btn_frame.pack()
        tk.Button(btn_frame, text="+10% Feed", command=self.sim_feed_plus, bg="#22ff88", fg="black", font=("Arial", 10, "bold")).pack(side="left", padx=5)
        tk.Button(btn_frame, text="-10% Feed", command=self.sim_feed_minus, bg="#fbbf24", fg="black", font=("Arial", 10, "bold")).pack(side="left", padx=5)
        tk.Button(btn_frame, text="Emergency Shutdown", command=self.sim_shutdown, bg="#ef4444", fg="white", font=("Arial", 10, "bold")).pack(side="left", padx=5)

        # Right Panel
        right_panel = tk.Frame(main_frame, bg="#111827", width=380)
        right_panel.pack(side="right", fill="y")
        right_panel.pack_propagate(False)

        # Predictive Maintenance
        tk.Label(right_panel, text="PREDICTIVE MAINTENANCE", font=("Arial", 15, "bold"), bg="#111827", fg="#f87171").pack(pady=10)
        self.maint_labels = {}
        for eq in ["Pump", "Compressor", "Furnace"]:
            f = tk.Frame(right_panel, bg="#1f2937")
            f.pack(fill="x", padx=12, pady=6)
            tk.Label(f, text=eq, bg="#1f2937", fg="#93c5fd", font=("Arial", 11, "bold")).pack(anchor="w", padx=12)
            self.maint_labels[eq] = tk.Label(f, text="92.4%", font=("Arial", 16, "bold"), bg="#1f2937", fg="#22ff88")
            self.maint_labels[eq].pack(pady=4)

        # AI Copilot
        tk.Label(right_panel, text="AI COPILOT PRO", font=("Arial", 15, "bold"), bg="#111827", fg="#c084fc").pack(pady=(20,5))
        self.chat_entry = tk.Entry(right_panel, bg="#1f2937", fg="white", font=("Arial", 11))
        self.chat_entry.pack(fill="x", padx=12, pady=5)
        self.chat_entry.bind("<Return>", self.copilot_response)
        self.chat_log = tk.Text(right_panel, bg="#1f2937", fg="#bae6fd", height=8, font=("Arial", 10))
        self.chat_log.pack(fill="both", expand=True, padx=12, pady=5)

        # Alarms
        tk.Label(right_panel, text="ALARM CONSOLE", font=("Arial", 14, "bold"), bg="#111827", fg="#ef4444").pack(pady=(15,5))
        self.alarm_list = tk.Listbox(right_panel, bg="#1f2937", fg="#fda4af", height=6)
        self.alarm_list.pack(fill="x", padx=12, pady=5)

        # Bottom Graphs
        bottom_panel = tk.Frame(self.root, bg="#111827", height=360)
        bottom_panel.pack(fill="x", side="bottom", padx=12, pady=10)
        graph_frame = tk.Frame(bottom_panel, bg="#111827")
        graph_frame.pack(fill="both", expand=True)

        self.figures = []
        self.axes = []
        self.canvases = []
        chart_titles = ["Profit Trend", "Carbon Trend", "Efficiency Trend", "Maintenance Trend"]
        colors = ["#22ff88", "#f87171", "#67e8f9", "#fbbf24"]
        for i in range(4):
            fig, ax = plt.subplots(figsize=(5, 2.8), facecolor="#111827")
            ax.set_facecolor("#1f2937")
            ax.set_title(chart_titles[i], color="white", fontsize=11)
            canvas = FigureCanvasTkAgg(fig, graph_frame)
            canvas.get_tk_widget().pack(side="left", fill="both", expand=True, padx=6)
            self.figures.append(fig)
            self.axes.append(ax)
            self.canvases.append(canvas)

        self.update_graphs()

        # Footer
        footer = tk.Frame(self.root, bg="#081229", height=32)
        footer.pack(fill="x", side="bottom")
        tk.Label(footer, text="© 2035 xAI Industrial • V31 Historian Platform • 2846 Sensors Online • LIVE", bg="#081229", fg="#64748b", font=("Arial", 9)).pack(pady=7)

    def draw_process_flow(self):
        self.canvas.delete("all")
        for i in range(0, 1300, 40):
            self.canvas.create_line(i, 0, i, 460, fill="#1e2937", width=1)
        for i in range(0, 460, 40):
            self.canvas.create_line(0, i, 1300, i, fill="#1e2937", width=1)

        self.canvas.create_rectangle(80, 100, 260, 250, fill="#1e40af", outline="#60a5fa", width=4)
        self.canvas.create_text(170, 175, text="CDU", fill="white", font=("Arial", 14, "bold"))
        
        self.canvas.create_rectangle(400, 70, 590, 220, fill="#7e22ce", outline="#c084fc", width=4)
        self.canvas.create_text(495, 145, text="FCC", fill="white", font=("Arial", 14, "bold"))
        
        self.canvas.create_rectangle(730, 150, 920, 300, fill="#166534", outline="#4ade80", width=4)
        self.canvas.create_text(825, 225, text="HYDROTREATER", fill="white", font=("Arial", 12, "bold"))

        self.canvas.create_line(260, 175, 400, 145, fill="#67e8f9", width=8, arrow=tk.LAST)
        self.canvas.create_line(590, 145, 730, 225, fill="#67e8f9", width=8, arrow=tk.LAST)

    def update_clock(self):
        self.clock_label.config(text=datetime.now().strftime("%H:%M:%S | %d %b %Y"))
        self.root.after(1000, self.update_clock)

    def load_initial_data(self):
        now = datetime.now().strftime("%H:%M")
        for _ in range(15):
            self.history['time'].append(now)
            self.history['profit'].append(1.245)
            self.history['temp'].append(385)
            self.history['carbon'].append(42.3)
            self.history['efficiency'].append(89.7)
            self.history['maintenance'].append(92.0)

    def simulate_data(self):
        self.sensor_data['CDU_Temp'] += random.uniform(-1.5, 1.5)
        self.sensor_data['Profit'] += random.uniform(-18000, 35000)
        self.sensor_data['Carbon_Index'] += random.uniform(-0.6, 0.6)
        self.optimization_data['Overall_Efficiency'] = max(84, min(95, self.optimization_data['Overall_Efficiency'] + random.uniform(-0.6, 0.7)))

        for k in self.maintenance_data:
            self.maintenance_data[k] = max(75, min(99, self.maintenance_data[k] + random.uniform(-0.9, 0.8)))

        self.save_sensor_data()

        if self.sensor_data['CDU_Temp'] > 398:
            self.save_alarm("HIGH TEMPERATURE CDU")
            self.alarm_list.insert(0, "HIGH TEMP CDU")

        now = datetime.now().strftime("%H:%M")
        self.history['time'].append(now)
        self.history['profit'].append(self.sensor_data['Profit']/1000000)
        self.history['temp'].append(self.sensor_data['CDU_Temp'])
        self.history['carbon'].append(self.sensor_data['Carbon_Index'])
        self.history['efficiency'].append(self.optimization_data['Overall_Efficiency'])
        self.history['maintenance'].append(sum(self.maintenance_data.values()) / len(self.maintenance_data))

        if len(self.history['time']) > 30:
            for k in self.history:
                self.history[k] = self.history[k][-30:]

    def update_ui(self):
        self.exec_labels["Plant Score"].config(text=f"{int(self.optimization_data['Overall_Efficiency'])}")

        for eq in self.maint_labels:
            h = self.maintenance_data.get(eq + "_Health", 88)
            col = "#22ff88" if h > 90 else "#fbbf24" if h > 80 else "#ef4444"
            self.maint_labels[eq].config(text=f"{h:.1f}%", fg=col)

        # Historian Stats
        try:
            cursor = self.conn.cursor()
            cursor.execute("SELECT COUNT(*) FROM sensor_history")
            records = cursor.fetchone()[0]
            self.hist_stats["Records Stored"].config(text=str(records))
            
            cursor.execute("SELECT COUNT(*) FROM alarm_history")
            alarms = cursor.fetchone()[0]
            self.hist_stats["Total Alarms"].config(text=str(alarms))
            
            cursor.execute("SELECT COUNT(*) FROM ai_decisions")
            decisions = cursor.fetchone()[0]
            self.hist_stats["AI Decisions"].config(text=str(decisions))
        except:
            pass

    def update_graphs(self):
        titles = ["Profit Trend", "Carbon Trend", "Efficiency Trend", "Maintenance Trend"]
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
        try:
            self.simulate_data()
            self.update_ui()
            self.update_graphs()
        except Exception as e:
            print("Refresh error:", e)

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
        self.sensor_data['FCC_Flow'] += 85
        messagebox.showinfo("Simulator", "Feed rate +10%")

    def sim_feed_minus(self):
        self.sensor_data['FCC_Flow'] -= 85
        messagebox.showinfo("Simulator", "Feed rate -10%")

    def sim_shutdown(self):
        messagebox.showwarning("ALERT", "Emergency Shutdown Activated")

    def copilot_response(self, event=None):
        query = self.chat_entry.get().strip().lower()
        self.chat_entry.delete(0, tk.END)
        resp = "AI: "
        if "profit" in query:
            resp += "Recommend increasing FCC feed for higher yield."
        elif "carbon" in query:
            resp += "Reduce furnace duty to lower carbon intensity."
        else:
            resp += "System optimizing for maximum profitability."
        self.chat_log.insert(tk.END, resp + "\n\n")
        self.chat_log.see(tk.END)
        self.save_ai_decision(resp)

    def run(self):
        self.root.mainloop()


if __name__ == "__main__":
    app = AIPlant2035V31()
    app.run()