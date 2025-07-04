import tkinter as tk
from tkinter import ttk, filedialog, messagebox, scrolledtext
import os
import re
from collections import Counter

class LogAnalyzer:
    def __init__(self, notebook, main_app):
        self.main_app = main_app
        self.create_log_analyzer_tab(notebook)

    def create_log_analyzer_tab(self, notebook):
        self.log_frame = ttk.Frame(notebook)
        notebook.add(self.log_frame, text="Log Analyzer")

        ttk.Label(self.log_frame, text="Log File Analyzer", style='Title.TLabel').pack(pady=10)

        input_frame = ttk.Frame(self.log_frame)
        input_frame.pack(fill='x', padx=20, pady=10)

        ttk.Button(input_frame, text="Select Log File", command=self.analyze_log_file).pack(side='left', padx=5)

        ttk.Label(self.log_frame, text="Analysis Results:", style='Header.TLabel').pack(anchor='w', padx=20)

        self.log_results = scrolledtext.ScrolledText(self.log_frame, wrap='word', height=25)
        self.log_results.pack(fill='both', expand=True, padx=20, pady=10)

    def analyze_log_file(self):
        filename = filedialog.askopenfilename(
            title="Select log file",
            filetypes=[("Log files", "*.log"), ("Text files", "*.txt"), ("All files", "*.*")]
        )
        if not filename:
            return

        self.main_app.update_status("Analyzing log file...")

        try:
            self.log_results.delete(1.0, tk.END)
            self.log_results.insert(tk.END, f"Analyzing log file: {os.path.basename(filename)}\n")
            self.log_results.insert(tk.END, "=" * 50 + "\n")

            ip_addresses = []
            suspicious_patterns = []

            with open(filename, 'r', encoding='utf-8', errors='ignore') as f:
                lines = f.readlines()

            for line in lines:
                # Extract IP addresses
                ip_matches = re.findall(r'\b(?:[0-9]{1,3}\.){3}[0-9]{1,3}\b', line)
                ip_addresses.extend(ip_matches)

                # Check for suspicious patterns
                if any(pattern in line.lower() for pattern in ['union', 'select', 'script', 'alert', 'drop', 'insert']):
                    suspicious_patterns.append(line.strip())

            # Top IP addresses
            if ip_addresses:
                top_ips = Counter(ip_addresses).most_common(10)
                self.log_results.insert(tk.END, "Top 10 IP addresses:\n")
                for ip, count in top_ips:
                    self.log_results.insert(tk.END, f"{ip}: {count} requests\n")

            # Suspicious patterns
            if suspicious_patterns:
                self.log_results.insert(tk.END, f"\nSuspicious patterns found ({len(suspicious_patterns)}):\n")
                for pattern in suspicious_patterns[:10]:  # Show first 10
                    self.log_results.insert(tk.END, f"⚠ {pattern}\n")

            self.log_results.insert(tk.END, f"\nAnalysis completed. Processed {len(lines)} lines.\n")
            self.main_app.update_status("Log analysis completed.")

        except Exception as e:
            messagebox.showerror("Error", f"Log analysis failed: {str(e)}")
            self.main_app.update_status("Error analyzing log file.")
