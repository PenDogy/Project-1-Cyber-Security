import tkinter as tk
from tkinter import ttk, messagebox, scrolledtext
import threading
import subprocess
import ipaddress

class NetworkScanner:
    def __init__(self, notebook, main_app):
        self.main_app = main_app
        self.create_network_scanner_tab(notebook)
        
    def create_network_scanner_tab(self, notebook):
        # Network Scanner Tab
        self.network_frame = ttk.Frame(notebook)
        notebook.add(self.network_frame, text="Network Scanner")
        
        # Title
        ttk.Label(self.network_frame, text="Network Scanner", 
                 style='Title.TLabel').pack(pady=10)
        
        # Input frame
        input_frame = ttk.Frame(self.network_frame)
        input_frame.pack(fill='x', padx=20, pady=10)
        
        ttk.Label(input_frame, text="Target (IP/Network):").pack(side='left')
        self.network_target_var = tk.StringVar(value="192.168.1.1/24")
        ttk.Entry(input_frame, textvariable=self.network_target_var, 
                 width=20).pack(side='left', padx=5)
        
        ttk.Button(input_frame, text="Scan Network", 
                  command=self.scan_network).pack(side='left', padx=5)
        
        # Results
        ttk.Label(self.network_frame, text="Results:", 
                 style='Header.TLabel').pack(anchor='w', padx=20, pady=(20, 5))
        
        self.network_results = scrolledtext.ScrolledText(self.network_frame, 
                                                        height=20, width=100)
        self.network_results.pack(fill='both', expand=True, padx=20, pady=10)
        
    def scan_network(self):
        def scan_thread():
            try:
                self.main_app.update_status("Scanning network...")
                target = self.network_target_var.get()
                self.network_results.delete(1.0, tk.END)
                self.network_results.insert(tk.END, f"Scanning network: {target}\n")
                self.network_results.insert(tk.END, "=" * 50 + "\n")
                
                # Parse network range
                try:
                    network = ipaddress.ip_network(target, strict=False)
                    active_hosts = []
                    
                    for ip in network.hosts():
                        if self.ping_host(str(ip)):
                            active_hosts.append(str(ip))
                            self.network_results.insert(tk.END, f"✓ {ip} is alive\n")
                            self.network_results.see(tk.END)
                            self.main_app.root.update_idletasks()
                    
                    self.network_results.insert(tk.END, f"\nScan completed. Found {len(active_hosts)} active hosts.\n")
                    
                except Exception as e:
                    self.network_results.insert(tk.END, f"Error: {str(e)}\n")
                    
                self.main_app.update_status("Network scan completed")
                
            except Exception as e:
                messagebox.showerror("Error", f"Network scan failed: {str(e)}")
                self.main_app.update_status("Network scan failed")
                
        threading.Thread(target=scan_thread, daemon=True).start()
        
    def ping_host(self, host):
        try:
            result = subprocess.run(['ping', '-c', '1', '-W', '1', host], 
                                  capture_output=True, text=True, timeout=2)
            return result.returncode == 0
        except:
            return False