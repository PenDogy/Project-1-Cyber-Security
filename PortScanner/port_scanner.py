import tkinter as tk
from tkinter import ttk, messagebox, scrolledtext
import threading
import socket

class PortScanner:
    def __init__(self, notebook, main_app):
        self.main_app = main_app
        self.create_port_scanner_tab(notebook)
        
    def create_port_scanner_tab(self, notebook):
        # Port Scanner Tab
        self.port_frame = ttk.Frame(notebook)
        notebook.add(self.port_frame, text="Port Scanner")
        
        # Title
        ttk.Label(self.port_frame, text="Port Scanner", 
                 style='Title.TLabel').pack(pady=10)
        
        # Input frame
        input_frame = ttk.Frame(self.port_frame)
        input_frame.pack(fill='x', padx=20, pady=10)
        
        ttk.Label(input_frame, text="Target IP:").pack(side='left')
        self.port_target_var = tk.StringVar(value="192.168.1.1")
        ttk.Entry(input_frame, textvariable=self.port_target_var, 
                 width=15).pack(side='left', padx=5)
        
        ttk.Label(input_frame, text="Port Range:").pack(side='left', padx=(10, 0))
        self.port_range_var = tk.StringVar(value="1-1000")
        ttk.Entry(input_frame, textvariable=self.port_range_var, 
                 width=10).pack(side='left', padx=5)
        
        ttk.Button(input_frame, text="Scan Ports", 
                  command=self.scan_ports).pack(side='left', padx=5)
        
        # Results
        ttk.Label(self.port_frame, text="Results:", 
                 style='Header.TLabel').pack(anchor='w', padx=20, pady=(20, 5))
        
        self.port_results = scrolledtext.ScrolledText(self.port_frame, 
                                                     height=20, width=100)
        self.port_results.pack(fill='both', expand=True, padx=20, pady=10)
        
    def scan_ports(self):
        def scan_thread():
            try:
                self.main_app.update_status("Scanning ports...")
                target = self.port_target_var.get()
                port_range = self.port_range_var.get()
                
                self.port_results.delete(1.0, tk.END)
                self.port_results.insert(tk.END, f"Scanning ports on {target}\n")
                self.port_results.insert(tk.END, f"Port range: {port_range}\n")
                self.port_results.insert(tk.END, "=" * 50 + "\n")
                
                # Parse port range
                if '-' in port_range:
                    start_port, end_port = map(int, port_range.split('-'))
                else:
                    start_port = end_port = int(port_range)
                
                open_ports = []
                for port in range(start_port, end_port + 1):
                    if self.check_port(target, port):
                        open_ports.append(port)
                        service = self.get_service_name(port)
                        self.port_results.insert(tk.END, f"✓ Port {port} is open ({service})\n")
                        self.port_results.see(tk.END)
                        self.main_app.root.update_idletasks()
                
                self.port_results.insert(tk.END, f"\nScan completed. Found {len(open_ports)} open ports.\n")
                self.main_app.update_status("Port scan completed")
                
            except Exception as e:
                messagebox.showerror("Error", f"Port scan failed: {str(e)}")
                self.main_app.update_status("Port scan failed")
                
        threading.Thread(target=scan_thread, daemon=True).start()
        
    def check_port(self, host, port):
        try:
            sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            sock.settimeout(1)
            result = sock.connect_ex((host, port))
            sock.close()
            return result == 0
        except:
            return False
            
    def get_service_name(self, port):
        common_ports = {
            21: "FTP", 22: "SSH", 23: "Telnet", 25: "SMTP",
            53: "DNS", 80: "HTTP", 110: "POP3", 143: "IMAP",
            443: "HTTPS", 993: "IMAPS", 995: "POP3S"
        }
        return common_ports.get(port, "Unknown")