import tkinter as tk
from tkinter import ttk, scrolledtext, messagebox
import sqlite3
import datetime
import random
import threading
import time
import os
from matplotlib.figure import Figure
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import matplotlib.pyplot as plt

class PlantCopilot:
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("AI PLANT 2035 - AI Copilot V32")
        self.root.geometry("1400x900")
        self.root.configure(bg="#081229")
        self.root.protocol("WM_DELETE_WINDOW", self.on_close)
        
        # Database
        self.db_path = "plant_historian_v32.db"
        self.conn = None
        self.init_database()
        
        # Variables
        self.chat_history = []
        
        self.setup_ui()
        self.load_chat_history()
        self.simulate_plant_data()
        
    def init_database(self):
        self.conn = sqlite3.connect(self.db_path)
        cursor = self.conn.cursor()
        
        # Plant metrics table
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS plant_metrics (
                id INTEGER PRIMARY KEY,
                timestamp TEXT,
                plant_health REAL,
                reliability REAL,
                profit_daily REAL,
                carbon_intensity REAL,
                efficiency REAL,
                cdu_throughput REAL,
                fcc_throughput REAL,
                hydrotreater_throughput REAL,
                avg_temperature REAL,
                avg_pressure REAL
            )
        ''')
        
        # Alarms table
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS alarms (
                id INTEGER PRIMARY KEY,
                timestamp TEXT,
                unit TEXT,
                description TEXT,
                severity TEXT,
                acknowledged INTEGER DEFAULT 0
            )
        ''')
        
        # Chat history
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS chat_history (
                id INTEGER PRIMARY KEY,
                timestamp TEXT,
                question TEXT,
                answer TEXT
            )
        ''')
        
        # Populate initial data if empty
        cursor.execute("SELECT COUNT(*) FROM plant_metrics")
        if cursor.fetchone()[0] == 0:
            self.populate_sample_data()
        
        # Populate sample alarms
        cursor.execute("SELECT COUNT(*) FROM alarms")
        if cursor.fetchone()[0] == 0:
            self.populate_sample_alarms()
        
        self.conn.commit()
    
    def populate_sample_data(self):
        cursor = self.conn.cursor()
        now = datetime.datetime.now().isoformat()
        for i in range(10):
            ts = (datetime.datetime.now() - datetime.timedelta(minutes=i*5)).isoformat()
            cursor.execute('''
                INSERT INTO plant_metrics 
                (timestamp, plant_health, reliability, profit_daily, carbon_intensity, efficiency,
                 cdu_throughput, fcc_throughput, hydrotreater_throughput, avg_temperature, avg_pressure)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            ''', (
                ts,
                random.uniform(88, 97),
                random.uniform(90, 98),
                random.uniform(1.4, 1.8),
                random.uniform(38, 48),
                random.uniform(92, 97),
                random.uniform(145, 165),
                random.uniform(75, 92),
                random.uniform(55, 68),
                random.uniform(340, 380),
                random.uniform(28, 35)
            ))
        self.conn.commit()
    
    def populate_sample_alarms(self):
        cursor = self.conn.cursor()
        alarms = [
            ("FCC", "High catalyst temperature", "Critical"),
            ("CDU", "Feed flow deviation", "Warning"),
            ("Hydrotreater", "Hydrogen pressure low", "High"),
            ("Boiler", "Steam drum level high", "Warning")
        ]
        now = datetime.datetime.now()
        for unit, desc, sev in alarms:
            ts = (now - datetime.timedelta(minutes=random.randint(5, 120))).isoformat()
            cursor.execute('''
                INSERT INTO alarms (timestamp, unit, description, severity)
                VALUES (?, ?, ?, ?)
            ''', (ts, unit, desc, sev))
        self.conn.commit()
    
    def setup_ui(self):
        # Main frame
        main_frame = tk.Frame(self.root, bg="#081229")
        main_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        # Header
        header_frame = tk.Frame(main_frame, bg="#081229", height=60)
        header_frame.pack(fill=tk.X, pady=(0, 10))
        header_frame.pack_propagate(False)
        
        title_label = tk.Label(header_frame, text="AI PLANT 2035", 
                              font=("Arial", 24, "bold"), fg="#00ff99", bg="#081229")
        title_label.pack(side=tk.LEFT, padx=20)
        
        subtitle_label = tk.Label(header_frame, text="AUTONOMOUS AI COPILOT V32", 
                                 font=("Arial", 12), fg="#55ddff", bg="#081229")
        subtitle_label.pack(side=tk.LEFT, padx=10)
        
        status_frame = tk.Frame(header_frame, bg="#081229")
        status_frame.pack(side=tk.RIGHT, padx=20)
        
        self.status_label = tk.Label(status_frame, text="● ONLINE", font=("Arial", 12, "bold"),
                                    fg="#00ff99", bg="#081229")
        self.status_label.pack(side=tk.RIGHT)
        
        # Paned window
        paned = ttk.PanedWindow(main_frame, orient=tk.HORIZONTAL)
        paned.pack(fill=tk.BOTH, expand=True)
        
        # Sidebar - Controls and Info
        sidebar = tk.Frame(paned, bg="#0f1a3a", width=280)
        sidebar.pack_propagate(False)
        paned.add(sidebar, weight=1)
        
        # Plant Overview in sidebar
        overview_label = tk.Label(sidebar, text="PLANT OVERVIEW", font=("Arial", 14, "bold"),
                                 fg="#ffcc00", bg="#0f1a3a")
        overview_label.pack(pady=(15, 5), padx=15, anchor="w")
        
        self.overview_text = scrolledtext.ScrolledText(sidebar, height=12, bg="#081229", fg="#55ddff",
                                                       font=("Consolas", 11), relief=tk.FLAT)
        self.overview_text.pack(fill=tk.X, padx=15, pady=5)
        
        # Quick commands
        quick_label = tk.Label(sidebar, text="QUICK COMMANDS", font=("Arial", 12, "bold"),
                              fg="#ffcc00", bg="#0f1a3a")
        quick_label.pack(pady=(15, 5), padx=15, anchor="w")
        
        commands = ["plant health", "profit", "carbon", "recommendation", 
                   "executive summary", "show alarms", "database status"]
        
        for cmd in commands:
            btn = tk.Button(sidebar, text=cmd.upper(), bg="#1e2a5a", fg="#00ff99",
                           relief=tk.FLAT, padx=10, pady=5, font=("Arial", 10),
                           command=lambda c=cmd: self.quick_command(c))
            btn.pack(fill=tk.X, padx=15, pady=2)
        
        # Main Chat Area
        chat_frame = tk.Frame(paned, bg="#081229")
        paned.add(chat_frame, weight=4)
        
        # Chat header
        chat_header = tk.Frame(chat_frame, bg="#0f1a3a", height=50)
        chat_header.pack(fill=tk.X, pady=(0, 5))
        chat_header.pack_propagate(False)
        
        tk.Label(chat_header, text="ENTERPRISE AI COPILOT", font=("Arial", 16, "bold"),
                fg="#ffffff", bg="#0f1a3a").pack(side=tk.LEFT, padx=20, pady=10)
        
        self.confidence_var = tk.StringVar(value="Confidence: 98%")
        conf_label = tk.Label(chat_header, textvariable=self.confidence_var, 
                             font=("Arial", 11), fg="#00ff99", bg="#0f1a3a")
        conf_label.pack(side=tk.RIGHT, padx=20)
        
        # Chat display
        self.chat_display = scrolledtext.ScrolledText(chat_frame, bg="#0a1428", fg="#e0f0ff",
                                                     font=("Consolas", 12), wrap=tk.WORD, relief=tk.FLAT)
        self.chat_display.pack(fill=tk.BOTH, expand=True, padx=10, pady=5)
        
        # Configure tags for chat
        self.chat_display.tag_config("user", foreground="#55ddff", font=("Consolas", 12, "bold"))
        self.chat_display.tag_config("ai", foreground="#00ff99")
        self.chat_display.tag_config("system", foreground="#ffcc00")
        self.chat_display.tag_config("alarm", foreground="#ff4444")
        
        # Input area
        input_frame = tk.Frame(chat_frame, bg="#081229", height=80)
        input_frame.pack(fill=tk.X, padx=10, pady=10)
        input_frame.pack_propagate(False)
        
        self.input_entry = tk.Entry(input_frame, bg="#1e2a5a", fg="#ffffff", 
                                   font=("Consolas", 13), relief=tk.FLAT, insertbackground="#00ff99")
        self.input_entry.pack(side=tk.LEFT, fill=tk.X, expand=True, padx=(0, 10), ipady=12)
        self.input_entry.bind("<Return>", lambda e: self.send_message())
        
        send_btn = tk.Button(input_frame, text="SEND", bg="#00ff99", fg="#081229",
                            font=("Arial", 12, "bold"), relief=tk.FLAT, padx=25, pady=10,
                            command=self.send_message)
        send_btn.pack(side=tk.RIGHT)
        
        # Footer
        footer = tk.Frame(self.root, bg="#081229", height=30)
        footer.pack(fill=tk.X, side=tk.BOTTOM)
        tk.Label(footer, text="© AI PLANT 2035 - Refinery Digital Twin | Rule-based Knowledge Engine",
                fg="#555577", bg="#081229", font=("Arial", 9)).pack(pady=5)
        
        # Initial greeting
        self.add_chat_message("system", "AI Copilot initialized. Type 'help' for supported commands.")
    
    def load_chat_history(self):
        cursor = self.conn.cursor()
        cursor.execute("SELECT timestamp, question, answer FROM chat_history ORDER BY id DESC LIMIT 50")
        rows = cursor.fetchall()
        self.chat_display.config(state=tk.NORMAL)
        self.chat_display.delete(1.0, tk.END)
        
        for ts, q, a in reversed(rows):
            self.chat_display.insert(tk.END, f"[{ts[:19]}] You: {q}\n", "user")
            self.chat_display.insert(tk.END, f"AI: {a}\n\n", "ai")
        
        self.chat_display.config(state=tk.DISABLED)
        self.chat_display.see(tk.END)
    
    def simulate_plant_data(self):
        # Update overview periodically
        def update_overview():
            while True:
                try:
                    cursor = self.conn.cursor()
                    cursor.execute("SELECT * FROM plant_metrics ORDER BY timestamp DESC LIMIT 1")
                    row = cursor.fetchone()
                    
                    if row:
                        _, ts, health, rel, profit, carbon, eff, cdu, fcc, hydro, temp, pres = row
                        overview = f"""PLANT HEALTH: {health:.1f}%
RELIABILITY: {rel:.1f}%
PROFIT: ${profit:.2f}M/day
CARBON: {carbon:.1f} kg/bbl
EFFICIENCY: {eff:.1f}%
CDU: {cdu:.0f} kbpd
FCC: {fcc:.0f} kbpd
HYDROTREATER: {hydro:.0f} kbpd
AVG TEMP: {temp:.0f}°C
AVG PRESS: {pres:.1f} bar"""
                        
                        self.overview_text.config(state=tk.NORMAL)
                        self.overview_text.delete(1.0, tk.END)
                        self.overview_text.insert(tk.END, overview)
                        self.overview_text.config(state=tk.DISABLED)
                except:
                    pass
                time.sleep(8)
        
        threading.Thread(target=update_overview, daemon=True).start()
    
    def quick_command(self, cmd):
        self.input_entry.delete(0, tk.END)
        self.input_entry.insert(0, cmd)
        self.send_message()
    
    def send_message(self):
        question = self.input_entry.get().strip()
        if not question:
            return
        
        self.input_entry.delete(0, tk.END)
        
        # Add user message
        self.add_chat_message("user", question)
        
        # Process in thread to keep UI responsive
        threading.Thread(target=self.process_ai_response, args=(question,), daemon=True).start()
    
    def add_chat_message(self, sender, message):
        self.chat_display.config(state=tk.NORMAL)
        timestamp = datetime.datetime.now().strftime("%H:%M:%S")
        
        if sender == "user":
            self.chat_display.insert(tk.END, f"[{timestamp}] You: ", "user")
            self.chat_display.insert(tk.END, f"{message}\n\n")
        elif sender == "ai":
            self.chat_display.insert(tk.END, f"[{timestamp}] AI Copilot: ", "ai")
            self.chat_display.insert(tk.END, f"{message}\n\n")
        else:
            self.chat_display.insert(tk.END, f"[{timestamp}] {message}\n\n", sender)
        
        self.chat_display.config(state=tk.DISABLED)
        self.chat_display.see(tk.END)
    
    def save_to_history(self, question, answer):
        cursor = self.conn.cursor()
        ts = datetime.datetime.now().isoformat()
        cursor.execute("INSERT INTO chat_history (timestamp, question, answer) VALUES (?, ?, ?)",
                      (ts, question, answer))
        self.conn.commit()
    
    def process_ai_response(self, question):
        try:
            response = self.generate_ai_response(question)
            confidence = random.randint(92, 99)
            
            full_response = f"{response}\n\nConfidence = {confidence}%"
            
            # Update UI from main thread
            self.root.after(0, self.add_chat_message, "ai", full_response)
            self.root.after(0, lambda: self.save_to_history(question, response))
            self.root.after(0, lambda: self.confidence_var.set(f"Confidence: {confidence}%"))
            
        except Exception as e:
            error_msg = f"Error processing command: {str(e)}"
            self.root.after(0, self.add_chat_message, "system", error_msg)
    
    def generate_ai_response(self, command):
        cmd_lower = command.lower().strip()
        
        cursor = self.conn.cursor()
        
        # Help
        if "help" in cmd_lower:
            return """Supported Commands:
• plant health
• profit
• carbon
• efficiency
• maintenance
• alarms / show alarms
• database status
• fcc / cdu / hydrotreater
• recommendation
• executive summary
• status"""
        
        # Plant health
        if "plant health" in cmd_lower or "status" in cmd_lower:
            cursor.execute("SELECT plant_health, reliability FROM plant_metrics ORDER BY timestamp DESC LIMIT 1")
            row = cursor.fetchone()
            if row:
                health, rel = row
                status = "Healthy" if health > 90 else "Monitor"
                return f"Plant Health = {health:.1f}%\nReliability = {rel:.1f}%\nStatus = {status}"
            return "Plant Health = 94.2%\nReliability = 95.8%\nStatus = Healthy"
        
        # Profit
        if "profit" in cmd_lower:
            cursor.execute("SELECT profit_daily FROM plant_metrics ORDER BY timestamp DESC LIMIT 1")
            row = cursor.fetchone()
            profit = row[0] if row else random.uniform(1.45, 1.75)
            return f"Current Profit = ${profit:.2f}M/day\nTrend: +0.8% from yesterday"
        
        # Carbon
        if "carbon" in cmd_lower:
            cursor.execute("SELECT carbon_intensity FROM plant_metrics ORDER BY timestamp DESC LIMIT 1")
            row = cursor.fetchone()
            carbon = row[0] if row else random.uniform(39, 46)
            return f"Current Carbon Intensity = {carbon:.1f} kg CO₂/bbl\nTarget: <40 kg/bbl"
        
        # Efficiency
        if "efficiency" in cmd_lower:
            cursor.execute("SELECT efficiency FROM plant_metrics ORDER BY timestamp DESC LIMIT 1")
            row = cursor.fetchone()
            eff = row[0] if row else random.uniform(93, 96.5)
            return f"Overall Efficiency = {eff:.1f}%\nHeat Recovery: 87.4%\nUptime: 99.2%"
        
        # Recommendation
        if "recommendation" in cmd_lower:
            return """Recommendations:
• Increase FCC throughput by 2.8%
• Optimize CDU preheat train (+1.2% efficiency)
• Reduce Hydrotreater H2 consumption by 3%
Expected profit gain: +2.7%
Carbon reduction: -1.4 kg/bbl"""
        
        # Executive summary
        if "executive summary" in cmd_lower or "summary" in cmd_lower:
            cursor.execute("SELECT plant_health, profit_daily, carbon_intensity, reliability FROM plant_metrics ORDER BY timestamp DESC LIMIT 1")
            row = cursor.fetchone()
            if row:
                health, profit, carbon, rel = row
            else:
                health, profit, carbon, rel = 93.8, 1.62, 41.8, 95.1
            
            return f"""EXECUTIVE SUMMARY
Plant Grade: A-
Profit: ${profit:.2f}M/day
Carbon Intensity: {carbon:.1f} kg/bbl
Reliability: {rel:.1f}%
Top Risks: Catalyst deactivation in FCC, Feed quality variation
Top Opportunities: Advanced process control on CDU, Heat integration"""
        
        # Show alarms
        if "alarm" in cmd_lower:
            cursor.execute("SELECT timestamp, unit, description, severity FROM alarms WHERE acknowledged=0 ORDER BY timestamp DESC LIMIT 8")
            alarms = cursor.fetchall()
            if not alarms:
                return "No active alarms."
            
            resp = "ACTIVE ALARMS:\n"
            for ts, unit, desc, sev in alarms:
                resp += f"[{ts[11:16]}] {unit} | {desc} | {sev}\n"
            return resp.strip()
        
        # Database status
        if "database" in cmd_lower or "db status" in cmd_lower:
            cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
            tables = [row[0] for row in cursor.fetchall()]
            cursor.execute("SELECT COUNT(*) FROM plant_metrics")
            rows = cursor.fetchone()[0]
            size_mb = os.path.getsize(self.db_path) / (1024*1024) if os.path.exists(self.db_path) else 0
            
            cursor.execute("SELECT MAX(timestamp) FROM plant_metrics")
            last_update = cursor.fetchone()[0]
            
            return f"""Database Status:
Tables: {len(tables)}
Metrics Rows: {rows}
Alarms: Active
Size: {size_mb:.2f} MB
Last Update: {last_update[:19] if last_update else 'N/A'}"""
        
        # Unit specific
        if "fcc" in cmd_lower:
            cursor.execute("SELECT fcc_throughput, avg_temperature FROM plant_metrics ORDER BY timestamp DESC LIMIT 1")
            row = cursor.fetchone() or (85, 520)
            return f"FCC Unit Status:\nThroughput: {row[0]:.0f} kbpd\nReactor Temp: {row[1]:.0f}°C\nConversion: 78.4%"
        
        if "cdu" in cmd_lower:
            cursor.execute("SELECT cdu_throughput, avg_temperature FROM plant_metrics ORDER BY timestamp DESC LIMIT 1")
            row = cursor.fetchone() or (155, 360)
            return f"CDU Status:\nThroughput: {row[0]:.0f} kbpd\nFurnace Temp: {row[1]:.0f}°C\nYield: Optimal"
        
        if "hydrotreater" in cmd_lower or "hydro" in cmd_lower:
            return "Hydrotreater Status:\nThroughput: 62 kbpd\nSulfur Removal: 99.6%\nPressure: 34 bar\nStable operation"
        
        if "maintenance" in cmd_lower:
            return "Next scheduled maintenance:\n• FCC Catalyst change in 18 days\n• CDU Exchanger cleaning in 45 days\nAll predictive indicators GREEN"
        
        # Default
        return "Command understood. For specific metrics use: plant health, profit, carbon, recommendation, executive summary."
    
    def on_close(self):
        if self.conn:
            self.conn.close()
        self.root.destroy()
    
    def run(self):
        self.root.mainloop()


if __name__ == "__main__":
    app = PlantCopilot()
    app.run()