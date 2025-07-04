import tkinter as tk
from tkinter import ttk, messagebox, scrolledtext
import platform
import psutil
from datetime import datetime

class SystemInfo:
    def __init__(self, notebook, main_app):
        self.main_app = main_app
        self.root = main_app.root  # ถ้าต้องใช้ update_idletasks()
        self.create_system_info_tab(notebook)

    def create_system_info_tab(self, notebook):
        self.sys_frame = ttk.Frame(notebook)
        notebook.add(self.sys_frame, text="System Info")

        ttk.Label(self.sys_frame, text="System Information", style='Title.TLabel').pack(pady=10)

        btn_frame = ttk.Frame(self.sys_frame)
        btn_frame.pack(fill='x', padx=20, pady=10)

        ttk.Button(btn_frame, text="Get System Info", command=self.get_system_info).pack(side='left', padx=5)
        ttk.Button(btn_frame, text="Get Network Interfaces", command=self.get_network_interfaces).pack(side='left', padx=5)
        ttk.Button(btn_frame, text="Get Running Processes", command=self.get_processes).pack(side='left', padx=5)

        ttk.Label(self.sys_frame, text="Results:", style='Header.TLabel').pack(anchor='w', padx=20)

        self.system_results = scrolledtext.ScrolledText(self.sys_frame, wrap='word', height=30)
        self.system_results.pack(fill='both', expand=True, padx=20, pady=10)

    def get_system_info(self):
        try:
            self.system_results.delete(1.0, tk.END)
            self.system_results.insert(tk.END, "System Information\n")
            self.system_results.insert(tk.END, "=" * 50 + "\n")

            # OS Version
            self.system_results.insert(tk.END, "OS Version:\n")
            self.system_results.insert(tk.END, f"  System: {platform.system()}\n")
            self.system_results.insert(tk.END, f"  Node Name: {platform.node()}\n")
            self.system_results.insert(tk.END, f"  Release: {platform.release()}\n")
            self.system_results.insert(tk.END, f"  Version: {platform.version()}\n")
            self.system_results.insert(tk.END, f"  Machine: {platform.machine()}\n")
            self.system_results.insert(tk.END, f"  Processor: {platform.processor()}\n\n")

            # CPU Info
            self.system_results.insert(tk.END, "CPU Information:\n")
            self.system_results.insert(tk.END, f"  Physical Cores: {psutil.cpu_count(logical=False)}\n")
            self.system_results.insert(tk.END, f"  Logical Cores: {psutil.cpu_count(logical=True)}\n")
            self.system_results.insert(tk.END, f"  Current CPU Usage: {psutil.cpu_percent(interval=1)}%\n\n")

            # Memory Info
            mem = psutil.virtual_memory()
            self.system_results.insert(tk.END, "Memory Information:\n")
            self.system_results.insert(tk.END, f"  Total: {round(mem.total / (1024**3), 2)} GB\n")
            self.system_results.insert(tk.END, f"  Available: {round(mem.available / (1024**3), 2)} GB\n")
            self.system_results.insert(tk.END, f"  Used: {round(mem.used / (1024**3), 2)} GB\n")
            self.system_results.insert(tk.END, f"  Percentage: {mem.percent}%\n\n")

            # Disk Usage
            self.system_results.insert(tk.END, "Disk Usage:\n")
            for part in psutil.disk_partitions():
                try:
                    usage = psutil.disk_usage(part.mountpoint)
                    self.system_results.insert(tk.END, f"  Device: {part.device}\n")
                    self.system_results.insert(tk.END, f"    Mountpoint: {part.mountpoint}\n")
                    self.system_results.insert(tk.END, f"    File System Type: {part.fstype}\n")
                    self.system_results.insert(tk.END, f"    Total Size: {round(usage.total / (1024**3), 2)} GB\n")
                    self.system_results.insert(tk.END, f"    Used: {round(usage.used / (1024**3), 2)} GB\n")
                    self.system_results.insert(tk.END, f"    Free: {round(usage.free / (1024**3), 2)} GB\n")
                    self.system_results.insert(tk.END, f"    Percentage: {usage.percent}%\n\n")
                except Exception as e:
                    self.system_results.insert(tk.END, f"  Error getting disk info for {part.mountpoint}: {e}\n\n")

            # Uptime
            boot_time_timestamp = psutil.boot_time()
            bt = datetime.fromtimestamp(boot_time_timestamp)
            self.system_results.insert(tk.END, "System Uptime:\n")
            self.system_results.insert(tk.END, f"  Boot Time: {bt.strftime('%Y-%m-%d %H:%M:%S')}\n")
            uptime_seconds = datetime.now().timestamp() - boot_time_timestamp
            days, remainder = divmod(uptime_seconds, 86400)
            hours, remainder = divmod(remainder, 3600)
            minutes, seconds = divmod(remainder, 60)
            self.system_results.insert(tk.END, f"  Uptime: {int(days)} days, {int(hours)} hours, {int(minutes)} minutes\n\n")

            self.system_results.see(tk.END)  # Scroll to end
            self.main_app.update_status("System information retrieved")

        except Exception as e:
            messagebox.showerror("Error", f"System info retrieval failed: {str(e)}")
            self.main_app.update_status("System information retrieval failed")

    def get_network_interfaces(self):
        try:
            self.system_results.delete(1.0, tk.END)
            self.system_results.insert(tk.END, "Network Interfaces\n")
            self.system_results.insert(tk.END, "=" * 50 + "\n")

            import netifaces
            interfaces = netifaces.interfaces()
            for iface in interfaces:
                self.system_results.insert(tk.END, f"Interface: {iface}\n")
                addrs = netifaces.ifaddresses(iface)

                # MAC address
                mac = addrs.get(netifaces.AF_LINK)
                if mac and mac[0].get('addr'):
                    self.system_results.insert(tk.END, f"  MAC Address: {mac[0]['addr']}\n")

                # IP address
                inet = addrs.get(netifaces.AF_INET)
                if inet and inet[0].get('addr'):
                    self.system_results.insert(tk.END, f"  IPv4 Address: {inet[0]['addr']}\n")
                    self.system_results.insert(tk.END, f"  Netmask: {inet[0].get('netmask', '-')}\n")

                self.system_results.insert(tk.END, "-" * 40 + "\n")

            self.main_app.update_status("Network interfaces retrieved")

        except Exception as e:
            messagebox.showerror("Error", f"Failed to get network interfaces: {str(e)}")
            self.main_app.update_status("Failed to retrieve network interfaces")

    def get_processes(self):
        try:
            self.system_results.delete(1.0, tk.END)
            self.system_results.insert(tk.END, "Running Processes\n")
            self.system_results.insert(tk.END, "=" * 50 + "\n")

            self.system_results.insert(tk.END, "{:<8} {:<15} {:<8} {:<8} {:<10} {:<10} {:<15}\n".format(
                "PID", "Name", "CPU%", "MEM%", "Status", "Started", "Command"
            ))
            self.system_results.insert(tk.END, "{:-<8} {:-<15} {:-<8} {:-<8} {:-<10} {:-<10} {:-<15}\n".format(
                "", "", "", "", "", "", ""
            ))

            for proc in psutil.process_iter(['pid', 'name', 'cpu_percent', 'memory_percent', 'status', 'create_time', 'cmdline']):
                try:
                    pid = proc.info['pid']
                    name = proc.info['name']
                    cpu_percent = proc.info['cpu_percent']
                    mem_percent = round(proc.info['memory_percent'], 2)
                    status = proc.info['status']
                    create_time_ts = proc.info['create_time']
                    create_time = datetime.fromtimestamp(create_time_ts).strftime('%H:%M:%S')

                    cmdline = ' '.join(proc.info['cmdline']) if proc.info['cmdline'] else ''
                    if len(cmdline) > 50:
                        cmdline = cmdline[:47] + "..."

                    self.system_results.insert(tk.END, "{:<8} {:<15} {:<8.2f} {:<8.2f} {:<10} {:<10} {:<15}\n".format(
                        pid, name, cpu_percent, mem_percent, status, create_time, cmdline
                    ))
                    self.system_results.see(tk.END)
                    self.root.update_idletasks()
                except (psutil.NoSuchProcess, psutil.AccessDenied, psutil.ZombieProcess):
                    continue

            self.main_app.update_status("Running processes retrieved")

        except Exception as e:
            messagebox.showerror("Error", f"Failed to get running processes: {str(e)}")
            self.main_app.update_status("Failed to retrieve running processes")
