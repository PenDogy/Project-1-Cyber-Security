import tkinter as tk
from tkinter import ttk, messagebox
from datetime import datetime

from NetworkScanner.network_scanner import NetworkScanner
from PortScanner.port_scanner import PortScanner
from PasswordChecker.password_checker import PasswordChecker
from HashTools.hash_tools import HashTools
from WebScanner.web_scanner import WebScanner
from LogAnalyzer.log_analyzer import LogAnalyzer
from SystemInfo.system_info import SystemInfo

class CyberSecurityToolkit:
    def __init__(self, root):
        self.root = root
        self.root.title("Cyber Security By Dan")
        self.root.geometry("1200x800")
        self.root.configure(bg='#2c3e50')
        
        # สร้าง style
        self.setup_styles()
        
        # สร้าง main frame
        self.main_frame = ttk.Frame(root)
        self.main_frame.pack(fill='both', expand=True, padx=10, pady=10)
        
        # สร้าง notebook สำหรับ tabs
        self.notebook = ttk.Notebook(self.main_frame)
        self.notebook.pack(fill='both', expand=True)
        
        # สร้าง instances ของแต่ละ class
        self.network_scanner = NetworkScanner(self.notebook, self)
        self.port_scanner = PortScanner(self.notebook, self)
        self.password_checker = PasswordChecker(self.notebook, self)
        self.hash_tools = HashTools(self.notebook, self)
        self.web_scanner = WebScanner(self.notebook, self)
        self.log_analyzer = LogAnalyzer(self.notebook, self)
        self.system_info = SystemInfo(self.notebook, self)
        
        # Status bar
        self.status_var = tk.StringVar()
        self.status_var.set("Ready")
        self.status_bar = ttk.Label(self.main_frame, textvariable=self.status_var, 
                                   relief='sunken', anchor='w')
        self.status_bar.pack(side='bottom', fill='x', pady=(5, 0))
        
    def setup_styles(self):
        style = ttk.Style()
        style.theme_use('clam')
        
        # Configure styles
        style.configure('Title.TLabel', font=('Arial', 14, 'bold'))
        style.configure('Header.TLabel', font=('Arial', 10, 'bold'))
        
    def update_status(self, message):
        self.status_var.set(f"{datetime.now().strftime('%H:%M:%S')} - {message}")
        self.root.update_idletasks()

if __name__ == "__main__":
    root = tk.Tk()
    app = CyberSecurityToolkit(root)
    root.mainloop()