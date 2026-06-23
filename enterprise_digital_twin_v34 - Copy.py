import tkinter as tk
from tkinter import ttk, scrolledtext, messagebox
import sqlite3
import datetime
import random
import threading
import time
import os
import sys

# Optional libraries for reports and exports
try:
    from reportlab.lib.pagesizes import letter
    from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle
    from reportlab.lib.styles import getSampleStyleSheet
    from reportlab.lib import colors
    REPORTLAB_AVAILABLE = True
except ImportError:
    REPORTLAB_AVAILABLE = False

try:
    import pandas as pd
    PANDAS_AVAILABLE = True
except ImportError:
    PANDAS_AVAILABLE = False


class PlantCopilotV34:
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("AI PLANT 2035 - Autonomous AI Energy Enterprise V34")
        self.root.geometry("1620x940")
        self.root.configure(bg="#081229")
        self.root.protocol("WM_DELETE_WINDOW", self.on_close)
        
        self.db_path = "plant_historian_v34.db"
        self.conn = None
        self.init_database()
        
        self.last_report_time = "Never"
        self.last_export_time = "Never"
        
        self.setup_ui()
        self.load_chat_history()
        self.update_analytics_panel()
        self.simulate_plant_data()
        
    def init_database(self):
        try:
            self.conn = sqlite3.connect(self.db_path, check_same_thread=False)
            cursor = self.conn.cursor()
            
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
            
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS chat_history (
                    id INTEGER PRIMARY KEY,
                    timestamp TEXT,
                    question TEXT,
                    answer TEXT
                )
            ''')
            
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS sensor_history (
                    id INTEGER PRIMARY KEY,
                    timestamp TEXT,
                    sensor_type TEXT,
                    value REAL,
                    unit TEXT
                )
            ''')
            
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS alarm_history (
                    id INTEGER PRIMARY KEY,
                    timestamp TEXT,
                    unit TEXT,
                    description TEXT,
                    severity TEXT
                )
            ''')
            
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS ai_decisions (
                    id INTEGER PRIMARY KEY,
                    timestamp TEXT,
                    command TEXT,
                    recommendation TEXT,
                    confidence REAL
                )
            ''')
            
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS maintenance_history (
                    id INTEGER PRIMARY KEY,
                    timestamp TEXT,
                    unit TEXT,
                    action TEXT,
                    status TEXT
                )
            ''')
            
            self.conn.commit()
            
            cursor.execute("SELECT COUNT(*) FROM plant_metrics")
            if cursor.fetchone()[0] == 0:
                self.populate_sample_data()
                
        except Exception as e:
            messagebox.showerror("Database Error", f"Failed to connect to database:\n{str(e)}")
            sys.exit(1)
    
    def populate_sample_data(self):
        try:
            cursor = self.conn.cursor()
            now = datetime.datetime.now()
            for i in range(40):
                ts = (now - datetime.timedelta(minutes=i*18)).isoformat()
                cursor.execute('''
                    INSERT INTO plant_metrics 
                    (timestamp, plant_health, reliability, profit_daily, carbon_intensity, efficiency,
                     cdu_throughput, fcc_throughput, hydrotreater_throughput, avg_temperature, avg_pressure)
                    VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
                ''', (ts, round(random.uniform(90.5, 96.8),1), round(random.uniform(92.5, 98.5),1),
                      round(random.uniform(1.55, 1.78),2), round(random.uniform(39.0, 45.5),1),
                      round(random.uniform(93.2, 96.7),1), round(random.uniform(150, 165),1),
                      round(random.uniform(78, 92),1), round(random.uniform(58, 67),1),
                      round(random.uniform(350, 378),1), round(random.uniform(29.0, 34.8),1)))
                
                cursor.execute('INSERT INTO sensor_history (timestamp, sensor_type, value, unit) VALUES (?, ?, ?, ?)',
                              (ts, "Temperature", random.uniform(345, 375), "°C"))
            
            sample_alarms = [
                ("FCC", "High catalyst temperature", "Critical"),
                ("CDU", "Feed flow deviation", "Warning"),
                ("Hydrotreater", "Hydrogen pressure low", "High")
            ]
            for unit, desc, sev in sample_alarms:
                ts = (now - datetime.timedelta(minutes=random.randint(5, 240))).isoformat()
                cursor.execute('INSERT INTO alarms (timestamp, unit, description, severity) VALUES (?,?,?,?)', (ts, unit, desc, sev))
                cursor.execute('INSERT INTO alarm_history (timestamp, unit, description, severity) VALUES (?,?,?,?)', (ts, unit, desc, sev))
            
            self.conn.commit()
        except:
            pass
    
    def setup_ui(self):
        main_frame = tk.Frame(self.root, bg="#081229")
        main_frame.pack(fill=tk.BOTH, expand=True, padx=12, pady=12)
        
        # Header
        header = tk.Frame(main_frame, bg="#081229", height=80)
        header.pack(fill=tk.X, pady=(0,12))
        header.pack_propagate(False)
        
        tk.Label(header, text="AI PLANT 2035", font=("Arial", 28, "bold"), fg="#00ff99", bg="#081229").pack(side=tk.LEFT, padx=20)
        tk.Label(header, text="V34 | ENTERPRISE DIGITAL TWIN", font=("Arial", 14), fg="#55ddff", bg="#081229").pack(side=tk.LEFT, padx=8)
        tk.Label(header, text="● LIVE", font=("Arial", 13, "bold"), fg="#00ff99", bg="#081229").pack(side=tk.RIGHT, padx=25)
        
        # Paned
        paned = ttk.PanedWindow(main_frame, orient=tk.HORIZONTAL)
        paned.pack(fill=tk.BOTH, expand=True)
        
        # Sidebar
        sidebar = tk.Frame(paned, bg="#0f1a3a", width=360)
        sidebar.pack_propagate(False)
        paned.add(sidebar, weight=1)
        
        # Overview
        tk.Label(sidebar, text="PLANT OVERVIEW", font=("Arial", 14, "bold"), fg="#ffcc00", bg="#0f1a3a").pack(pady=(18,6), padx=18, anchor="w")
        self.overview_text = scrolledtext.ScrolledText(sidebar, height=11, bg="#081229", fg="#55ddff", font=("Consolas", 11), relief=tk.FLAT)
        self.overview_text.pack(fill=tk.X, padx=18, pady=6)
        
        # Analytics
        tk.Label(sidebar, text="EXECUTIVE ANALYTICS", font=("Arial", 14, "bold"), fg="#ffcc00", bg="#0f1a3a").pack(pady=(18,6), padx=18, anchor="w")
        self.analytics_text = scrolledtext.ScrolledText(sidebar, height=13, bg="#081229", fg="#ffffff", font=("Consolas", 11), relief=tk.FLAT)
        self.analytics_text.pack(fill=tk.X, padx=18, pady=6)
        
        # Report Center
        tk.Label(sidebar, text="ENTERPRISE REPORT CENTER", font=("Arial", 12, "bold"), fg="#ffcc00", bg="#0f1a3a").pack(pady=(18,6), padx=18, anchor="w")
        for name, rtype in [("Daily Report", "Daily"), ("Weekly Report", "Weekly"), ("Monthly Report", "Monthly"), ("CEO Executive Report", "CEO")]:
            tk.Button(sidebar, text=name, bg="#1e2a5a", fg="#00ff99", relief=tk.FLAT, padx=12, pady=7,
                      command=lambda rt=rtype: self.generate_report(rt)).pack(fill=tk.X, padx=18, pady=4)
        
        # Export Center
        tk.Label(sidebar, text="DATA EXPORT CENTER", font=("Arial", 12, "bold"), fg="#ffcc00", bg="#0f1a3a").pack(pady=(18,6), padx=18, anchor="w")
        for name, etype in [("Sensor Data", "Sensor"), ("Alarm History", "Alarm"), ("AI Decisions", "AI"), 
                           ("Maintenance History", "Maintenance"), ("Full Historian", "Full")]:
            tk.Button(sidebar, text=name, bg="#1e2a5a", fg="#55ddff", relief=tk.FLAT, padx=12, pady=7,
                      command=lambda et=etype: self.export_data(et)).pack(fill=tk.X, padx=18, pady=4)
        
        # Quick Commands
        tk.Label(sidebar, text="QUICK COMMANDS", font=("Arial", 12, "bold"), fg="#ffcc00", bg="#0f1a3a").pack(pady=(18,6), padx=18, anchor="w")
        cmds = ["plant health", "profit", "carbon", "recommendation", "executive summary", "show alarms", "database status"]
        for c in cmds:
            tk.Button(sidebar, text=c.upper(), bg="#1e2a5a", fg="#00ff99", relief=tk.FLAT,
                      command=lambda cmd=c: self.quick_command(cmd)).pack(fill=tk.X, padx=18, pady=3)
        
        # Chat Area
        chat_frame = tk.Frame(paned, bg="#081229")
        paned.add(chat_frame, weight=4)
        
        chat_header = tk.Frame(chat_frame, bg="#0f1a3a", height=55)
        chat_header.pack(fill=tk.X, pady=(0,8))
        chat_header.pack_propagate(False)
        
        tk.Label(chat_header, text="AI COPILOT PRO", font=("Arial", 17, "bold"), fg="#ffffff", bg="#0f1a3a").pack(side=tk.LEFT, padx=22, pady=12)
        self.confidence_var = tk.StringVar(value="Confidence: 98%")
        tk.Label(chat_header, textvariable=self.confidence_var, fg="#00ff99", bg="#0f1a3a", font=("Arial", 11)).pack(side=tk.RIGHT, padx=22)
        
        self.chat_display = scrolledtext.ScrolledText(chat_frame, bg="#0a1428", fg="#e0f0ff", font=("Consolas", 12), wrap=tk.WORD, relief=tk.FLAT)
        self.chat_display.pack(fill=tk.BOTH, expand=True, padx=12, pady=6)
        
        self.chat_display.tag_config("user", foreground="#55ddff", font=("Consolas", 12, "bold"))
        self.chat_display.tag_config("ai", foreground="#00ff99")
        self.chat_display.tag_config("system", foreground="#ffcc00")
        
        # Input
        input_frame = tk.Frame(chat_frame, bg="#081229", height=85)
        input_frame.pack(fill=tk.X, padx=12, pady=10)
        input_frame.pack_propagate(False)
        
        self.input_entry = tk.Entry(input_frame, bg="#1e2a5a", fg="#ffffff", font=("Consolas", 13), relief=tk.FLAT, insertbackground="#00ff99")
        self.input_entry.pack(side=tk.LEFT, fill=tk.X, expand=True, padx=(0,12), ipady=14)
        self.input_entry.bind("<Return>", lambda e: self.send_message())
        
        tk.Button(input_frame, text="SEND", bg="#00ff99", fg="#081229", font=("Arial", 13, "bold"), relief=tk.FLAT,
                  padx=32, pady=12, command=self.send_message).pack(side=tk.RIGHT)
        
        # Footer
        tk.Label(self.root, text="AI PLANT 2035 V34 • Run command: python enterprise_digital_twin_v34.py", 
                fg="#555577", bg="#081229", font=("Arial", 9)).pack(side=tk.BOTTOM, pady=10)
        
        self.add_chat_message("system", "System initialized successfully. Use the sidebar or type commands below.")
    
    def load_chat_history(self):
        try:
            cursor = self.conn.cursor()
            cursor.execute("SELECT question, answer FROM chat_history ORDER BY id DESC LIMIT 25")
            for q, a in reversed(cursor.fetchall()):
                self.add_chat_message("user", q)
                self.add_chat_message("ai", a)
        except:
            pass
    
    def update_analytics_panel(self):
        try:
            cursor = self.conn.cursor()
            metrics = cursor.execute("SELECT COUNT(*) FROM plant_metrics").fetchone()[0]
            alarms = cursor.execute("SELECT COUNT(*) FROM alarms").fetchone()[0]
            decisions = cursor.execute("SELECT COUNT(*) FROM ai_decisions").fetchone()[0]
            chats = cursor.execute("SELECT COUNT(*) FROM chat_history").fetchone()[0]
            size = os.path.getsize(self.db_path) / (1024*1024) if os.path.exists(self.db_path) else 0
            
            content = f"""RECORDS STORED
• Plant Metrics : {metrics}
• Alarms        : {alarms}
• AI Decisions  : {decisions}
• Chat History  : {chats}
• Database Size : {size:.2f} MB
• Last Report   : {self.last_report_time}
• Last Export   : {self.last_export_time}"""
            
            self.analytics_text.config(state=tk.NORMAL)
            self.analytics_text.delete(1.0, tk.END)
            self.analytics_text.insert(tk.END, content)
            self.analytics_text.config(state=tk.DISABLED)
        except:
            pass
    
    def simulate_plant_data(self):
        def updater():
            while True:
                try:
                    cursor = self.conn.cursor()
                    cursor.execute("SELECT plant_health, reliability, profit_daily, carbon_intensity, efficiency FROM plant_metrics ORDER BY timestamp DESC LIMIT 1")
                    row = cursor.fetchone()
                    if row:
                        ph, rel, prof, carb, eff = row
                        txt = f"PLANT HEALTH : {ph:.1f}%\nRELIABILITY   : {rel:.1f}%\nPROFIT        : ${prof:.2f}M/day\nCARBON        : {carb:.1f} kg/bbl\nEFFICIENCY    : {eff:.1f}%"
                        self.overview_text.config(state=tk.NORMAL)
                        self.overview_text.delete(1.0, tk.END)
                        self.overview_text.insert(tk.END, txt)
                        self.overview_text.config(state=tk.DISABLED)
                    self.root.after(0, self.update_analytics_panel)
                except:
                    pass
                time.sleep(14)
        threading.Thread(target=updater, daemon=True).start()
    
    def quick_command(self, cmd):
        self.input_entry.delete(0, tk.END)
        self.input_entry.insert(0, cmd)
        self.send_message()
    
    def send_message(self):
        question = self.input_entry.get().strip()
        if not question:
            return
        self.input_entry.delete(0, tk.END)
        self.add_chat_message("user", question)
        threading.Thread(target=self.process_ai_response, args=(question,), daemon=True).start()
    
    def add_chat_message(self, sender, message):
        self.chat_display.config(state=tk.NORMAL)
        ts = datetime.datetime.now().strftime("%H:%M:%S")
        if sender == "user":
            self.chat_display.insert(tk.END, f"[{ts}] YOU: ", "user")
            self.chat_display.insert(tk.END, f"{message}\n\n")
        elif sender == "ai":
            self.chat_display.insert(tk.END, f"[{ts}] AI COPILOT: ", "ai")
            self.chat_display.insert(tk.END, f"{message}\n\n")
        else:
            self.chat_display.insert(tk.END, f"[{ts}] {message}\n\n", sender)
        self.chat_display.config(state=tk.DISABLED)
        self.chat_display.see(tk.END)
    
    def save_to_history(self, question, answer):
        try:
            cursor = self.conn.cursor()
            cursor.execute("INSERT INTO chat_history (timestamp, question, answer) VALUES (?,?,?)",
                          (datetime.datetime.now().isoformat(), question, answer))
            self.conn.commit()
        except:
            pass
    
    def process_ai_response(self, question):
        try:
            response = self.generate_ai_response(question)
            confidence = random.randint(94, 99)
            full_response = f"{response}\n\nConfidence = {confidence}%"
            self.root.after(0, self.add_chat_message, "ai", full_response)
            self.root.after(0, self.save_to_history, question, response)
            self.root.after(0, lambda: self.confidence_var.set(f"Confidence: {confidence}%"))
            
            try:
                cursor = self.conn.cursor()
                cursor.execute("INSERT INTO ai_decisions (timestamp, command, recommendation, confidence) VALUES (?,?,?,?)",
                              (datetime.datetime.now().isoformat(), question, response[:180], confidence))
                self.conn.commit()
                self.root.after(0, self.update_analytics_panel)
            except:
                pass
        except Exception as e:
            self.root.after(0, self.add_chat_message, "system", f"Error processing request: {str(e)}")
    
    def generate_ai_response(self, command):
        cl = command.lower()
        cursor = self.conn.cursor()
        
        if "help" in cl:
            return "Supported commands: plant health, profit, carbon, efficiency, recommendation, executive summary, show alarms, database status"
        
        if "health" in cl or "status" in cl:
            cursor.execute("SELECT plant_health, reliability FROM plant_metrics ORDER BY timestamp DESC LIMIT 1")
            row = cursor.fetchone() or (94.2, 96.1)
            return f"Plant Health = {row[0]:.1f}%\nReliability = {row[1]:.1f}%\nOverall Status: Healthy"
        
        if "profit" in cl:
            cursor.execute("SELECT profit_daily FROM plant_metrics ORDER BY timestamp DESC LIMIT 1")
            val = (cursor.fetchone() or (1.67,))[0]
            return f"Current Profit = ${val:.2f}M / day"
        
        if "carbon" in cl:
            cursor.execute("SELECT carbon_intensity FROM plant_metrics ORDER BY timestamp DESC LIMIT 1")
            val = (cursor.fetchone() or (41.3,))[0]
            return f"Carbon Intensity = {val:.1f} kg CO₂/bbl"
        
        if "recommendation" in cl:
            return "• Increase FCC throughput by 2.8%\n• Optimize CDU pre-heat train\n• Expected profit uplift: +2.4%"
        
        if "executive" in cl or "summary" in cl:
            cursor.execute("SELECT plant_health, profit_daily, carbon_intensity, reliability FROM plant_metrics ORDER BY timestamp DESC LIMIT 1")
            row = cursor.fetchone() or (94.2, 1.67, 41.3, 96.1)
            return f"""EXECUTIVE SUMMARY
Plant Grade     : A-
Daily Profit    : ${row[1]:.2f}M
Carbon Intensity: {row[2]:.1f} kg/bbl
Reliability     : {row[3]:.1f}%"""
        
        if "alarm" in cl:
            cursor.execute("SELECT unit, description, severity FROM alarms ORDER BY timestamp DESC LIMIT 6")
            alarms = cursor.fetchall()
            if not alarms:
                return "No active alarms at this time."
            return "\n".join([f"{u} → {d} ({s})" for u,d,s in alarms])
        
        if "database" in cl:
            size = os.path.getsize(self.db_path)/(1024*1024) if os.path.exists(self.db_path) else 0
            return f"Database Status: Healthy\nSize: {size:.2f} MB\nRecords: Active"
        
        return "Command understood. For detailed metrics please use one of the supported keywords."
    
    def ensure_directory(self, folder):
        try:
            os.makedirs(folder, exist_ok=True)
        except:
            pass
    
    def generate_report(self, rtype):
        if not REPORTLAB_AVAILABLE:
            messagebox.showerror("Missing Library", "reportlab is not installed.\nRun: pip install reportlab")
            return
        try:
            self.ensure_directory("reports")
            filename = f"reports/{rtype}_Report_{datetime.datetime.now().strftime('%Y%m%d_%H%M')}.pdf"
            
            doc = SimpleDocTemplate(filename, pagesize=letter)
            styles = getSampleStyleSheet()
            elements = []
            
            elements.append(Paragraph(f"<b>AI PLANT 2035 - {rtype.upper()} REPORT</b>", styles['Title']))
            elements.append(Paragraph(f"Generated on: {datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')}", styles['Normal']))
            elements.append(Spacer(1, 20))
            
            cursor = self.conn.cursor()
            cursor.execute("SELECT * FROM plant_metrics ORDER BY timestamp DESC LIMIT 1")
            m = cursor.fetchone() or [0] * 12
            
            data = [
                ["Metric", "Value"],
                ["Plant Health", f"{m[2]:.1f}%" if len(m) > 2 else "94.2%"],
                ["Profit", f"${m[4]:.2f}M/day" if len(m) > 4 else "$1.67M"],
                ["Reliability", f"{m[3]:.1f}%" if len(m) > 3 else "96.1%"],
                ["Carbon Intensity", f"{m[5]:.1f} kg/bbl" if len(m) > 5 else "41.3"],
                ["Efficiency", f"{m[6]:.1f}%" if len(m) > 6 else "94.8%"]
            ]
            
            t = Table(data)
            t.setStyle(TableStyle([
                ('BACKGROUND', (0,0), (-1,0), colors.grey),
                ('TEXTCOLOR', (0,0), (-1,0), colors.whitesmoke),
                ('ALIGN', (0,0), (-1,-1), 'CENTER'),
                ('FONTNAME', (0,0), (-1,0), 'Helvetica-Bold'),
                ('BACKGROUND', (0,1), (-1,-1), colors.beige),
            ]))
            elements.append(t)
            elements.append(Spacer(1, 18))
            
            elements.append(Paragraph("<b>AI Copilot Recommendations</b>", styles['Heading2']))
            elements.append(Paragraph("Increase FCC throughput • Optimize energy usage in CDU", styles['Normal']))
            
            doc.build(elements)
            
            self.last_report_time = datetime.datetime.now().strftime("%H:%M")
            self.root.after(0, self.update_analytics_panel)
            messagebox.showinfo("Report Generated", f"{rtype} Report saved successfully:\n{filename}")
        except Exception as e:
            messagebox.showerror("Report Error", str(e))
    
    def export_data(self, etype):
        if not PANDAS_AVAILABLE:
            messagebox.showerror("Missing Library", "pandas is not installed.\nRun: pip install pandas openpyxl")
            return
        try:
            self.ensure_directory("exports")
            ts = datetime.datetime.now().strftime("%Y%m%d_%H%M")
            
            if etype == "Full":
                filename = f"exports/full_historian_{ts}.xlsx"
                with pd.ExcelWriter(filename) as writer:
                    for table, sheet in [("plant_metrics","Metrics"), ("alarms","Alarms"), ("sensor_history","Sensors"),
                                       ("ai_decisions","AI_Decisions"), ("maintenance_history","Maintenance"), ("chat_history","Chat")]:
                        pd.read_sql_query(f"SELECT * FROM {table}", self.conn).to_excel(writer, sheet_name=sheet, index=False)
            else:
                table_map = {"Sensor":"sensor_history", "Alarm":"alarm_history", "AI":"ai_decisions", "Maintenance":"maintenance_history"}
                df = pd.read_sql_query(f"SELECT * FROM {table_map[etype]} ORDER BY timestamp DESC", self.conn)
                filename = f"exports/{etype.lower()}_data_{ts}.xlsx"
                df.to_excel(filename, index=False)
            
            self.last_export_time = datetime.datetime.now().strftime("%H:%M")
            self.root.after(0, self.update_analytics_panel)
            messagebox.showinfo("Export Complete", f"{etype} data exported to:\n{filename}")
        except Exception as e:
            messagebox.showerror("Export Error", str(e))
    
    def on_close(self):
        if self.conn:
            try:
                self.conn.close()
            except:
                pass
        self.root.destroy()
    
    def run(self):
        self.root.mainloop()


if __name__ == "__main__":
    print("="*70)
    print("AI PLANT 2035 V34 - ENTERPRISE DIGITAL TWIN")
    print("Run command: python enterprise_digital_twin_v34.py")
    print("If you see this, you are running the script correctly.")
    print("="*70)
    app = PlantCopilotV34()
    app.run()