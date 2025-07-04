import tkinter as tk
from tkinter import ttk, messagebox, scrolledtext
import threading
import requests

class WebScanner:
    def __init__(self, notebook, main_app):
        self.main_app = main_app
        self.create_web_scanner_tab(notebook)
        
    def create_web_scanner_tab(self, notebook):
        # Web Scanner Tab
        self.web_frame = ttk.Frame(notebook)
        notebook.add(self.web_frame, text="Web Scanner")
        
        # Title
        ttk.Label(self.web_frame, text="Basic Web Vulnerability Scanner", 
                 style='Title.TLabel').pack(pady=10)
        
        # Input frame
        input_frame = ttk.Frame(self.web_frame)
        input_frame.pack(fill='x', padx=20, pady=10)
        
        ttk.Label(input_frame, text="Target URL:").pack(side='left')
        self.web_target_var = tk.StringVar(value="http://example.com")
        ttk.Entry(input_frame, textvariable=self.web_target_var, 
                 width=40).pack(side='left', padx=5)
        
        ttk.Button(input_frame, text="Scan Website", 
                  command=self.scan_website).pack(side='left', padx=5)
        
        # Results
        ttk.Label(self.web_frame, text="Results:", 
                 style='Header.TLabel').pack(anchor='w', padx=20, pady=(20, 5))
        
        self.web_results = scrolledtext.ScrolledText(self.web_frame, 
                                                    height=20, width=100)
        self.web_results.pack(fill='both', expand=True, padx=20, pady=10)
        
    def scan_website(self):
        def scan_thread():
            try:
                self.main_app.update_status("Scanning website...")
                url = self.web_target_var.get()
                
                self.web_results.delete(1.0, tk.END)
                self.web_results.insert(tk.END, f"Scanning website: {url}\n")
                self.web_results.insert(tk.END, "=" * 50 + "\n")
                
                # Basic HTTP headers check
                try:
                    response = requests.get(url, timeout=10)
                    self.web_results.insert(tk.END, f"Status Code: {response.status_code}\n")
                    self.web_results.insert(tk.END, f"Server: {response.headers.get('Server', 'Unknown')}\n")
                    
                    # Security headers check
                    security_headers = {
                        'X-Content-Type-Options': 'nosniff',
                        'X-Frame-Options': 'DENY/SAMEORIGIN',
                        'X-XSS-Protection': '1; mode=block',
                        'Strict-Transport-Security': 'HSTS',
                        'Content-Security-Policy': 'CSP'
                    }
                    
                    self.web_results.insert(tk.END, "\nSecurity Headers:\n")
                    for header, description in security_headers.items():
                        if header in response.headers:
                            self.web_results.insert(tk.END, f"✓ {header}: {description}\n")
                        else:
                            self.web_results.insert(tk.END, f"✗ {header}: Missing\n")
                            
                    # Basic vulnerability checks
                    self.web_results.insert(tk.END, "\nBasic Vulnerability Checks:\n")
                    
                    # Check for common directories
                    common_dirs = ['/admin', '/login', '/wp-admin', '/phpmyadmin']
                    for directory in common_dirs:
                        try:
                            dir_response = requests.get(url + directory, timeout=5)
                            if dir_response.status_code == 200:
                                self.web_results.insert(tk.END, f"⚠ Found: {directory}\n")
                        except:
                            pass
                            
                except requests.RequestException as e:
                    self.web_results.insert(tk.END, f"Error connecting to website: {str(e)}\n")
                    
                self.web_results.insert(tk.END, "\nScan completed.\n")
                self.main_app.update_status("Website scan completed")
                
            except Exception as e:
                messagebox.showerror("Error", f"Website scan failed: {str(e)}")
                self.main_app.update_status("Website scan failed")
                
        threading.Thread(target=scan_thread, daemon=True).start()