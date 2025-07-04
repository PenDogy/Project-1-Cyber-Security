import tkinter as tk
from tkinter import ttk, messagebox, scrolledtext, filedialog
import hashlib
import os

class HashTools:
    def __init__(self, notebook, main_app):
        self.main_app = main_app
        self.create_hash_tools_tab(notebook)
        
    def create_hash_tools_tab(self, notebook):
        # Hash Tools Tab
        self.hash_frame = ttk.Frame(notebook)
        notebook.add(self.hash_frame, text="Hash Tools")
        
        # Title
        ttk.Label(self.hash_frame, text="Hash Tools", 
                 style='Title.TLabel').pack(pady=10)
        
        # Input frame
        input_frame = ttk.Frame(self.hash_frame)
        input_frame.pack(fill='x', padx=20, pady=10)
        
        ttk.Label(input_frame, text="Input Text:").pack(anchor='w')
        self.hash_input = tk.Text(input_frame, height=3, width=80)
        self.hash_input.pack(fill='x', pady=5)
        
        # Buttons frame
        button_frame = ttk.Frame(input_frame)
        button_frame.pack(fill='x', pady=5)
        
        ttk.Button(button_frame, text="MD5", 
                  command=lambda: self.generate_hash('md5')).pack(side='left', padx=2)
        ttk.Button(button_frame, text="SHA1", 
                  command=lambda: self.generate_hash('sha1')).pack(side='left', padx=2)
        ttk.Button(button_frame, text="SHA256", 
                  command=lambda: self.generate_hash('sha256')).pack(side='left', padx=2)
        ttk.Button(button_frame, text="SHA512", 
                  command=lambda: self.generate_hash('sha512')).pack(side='left', padx=2)
        
        # File hash
        file_frame = ttk.Frame(input_frame)
        file_frame.pack(fill='x', pady=10)
        
        ttk.Label(file_frame, text="File Hash:").pack(side='left')
        ttk.Button(file_frame, text="Select File", 
                  command=self.hash_file).pack(side='left', padx=5)
        
        # Results
        ttk.Label(self.hash_frame, text="Results:", 
                 style='Header.TLabel').pack(anchor='w', padx=20, pady=(20, 5))
        
        self.hash_results = scrolledtext.ScrolledText(self.hash_frame, 
                                                     height=15, width=100)
        self.hash_results.pack(fill='both', expand=True, padx=20, pady=10)
        
    def generate_hash(self, algorithm):
        text = self.hash_input.get(1.0, tk.END).strip()
        if not text:
            messagebox.showwarning("Warning", "Please enter text to hash")
            return
            
        try:
            if algorithm == 'md5':
                hash_obj = hashlib.md5(text.encode())
            elif algorithm == 'sha1':
                hash_obj = hashlib.sha1(text.encode())
            elif algorithm == 'sha256':
                hash_obj = hashlib.sha256(text.encode())
            elif algorithm == 'sha512':
                hash_obj = hashlib.sha512(text.encode())
                
            hash_value = hash_obj.hexdigest()
            
            self.hash_results.insert(tk.END, f"{algorithm.upper()}: {hash_value}\n")
            self.hash_results.see(tk.END)
            
        except Exception as e:
            messagebox.showerror("Error", f"Hash generation failed: {str(e)}")
            
    def hash_file(self):
        filename = filedialog.askopenfilename(title="Select file to hash")
        if not filename:
            return
            
        try:
            self.hash_results.insert(tk.END, f"\nFile: {os.path.basename(filename)}\n")
            self.hash_results.insert(tk.END, "=" * 50 + "\n")
            
            with open(filename, 'rb') as f:
                content = f.read()
                
            # Generate multiple hashes
            for algorithm in ['md5', 'sha1', 'sha256', 'sha512']:
                if algorithm == 'md5':
                    hash_obj = hashlib.md5(content)
                elif algorithm == 'sha1':
                    hash_obj = hashlib.sha1(content)
                elif algorithm == 'sha256':
                    hash_obj = hashlib.sha256(content)
                elif algorithm == 'sha512':
                    hash_obj = hashlib.sha512(content)
                    
                hash_value = hash_obj.hexdigest()
                self.hash_results.insert(tk.END, f"{algorithm.upper()}: {hash_value}\n")
                
            self.hash_results.see(tk.END)
            
        except Exception as e:
            messagebox.showerror("Error", f"File hashing failed: {str(e)}")