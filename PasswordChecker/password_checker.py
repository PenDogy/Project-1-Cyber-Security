import tkinter as tk
from tkinter import ttk, messagebox, scrolledtext
import re

class PasswordChecker:
    def __init__(self, notebook, main_app):
        self.main_app = main_app
        self.create_password_checker_tab(notebook)
        
    def create_password_checker_tab(self, notebook):
        # Password Checker Tab
        self.password_frame = ttk.Frame(notebook)
        notebook.add(self.password_frame, text="Password Checker")
        
        # Title
        ttk.Label(self.password_frame, text="Password Strength Checker", 
                 style='Title.TLabel').pack(pady=10)
        
        # Input frame
        input_frame = ttk.Frame(self.password_frame)
        input_frame.pack(fill='x', padx=20, pady=10)
        
        ttk.Label(input_frame, text="Password:").pack(side='left')
        self.password_var = tk.StringVar()
        self.password_entry = ttk.Entry(input_frame, textvariable=self.password_var, 
                                       width=30, show="*")
        self.password_entry.pack(side='left', padx=5)
        
        ttk.Button(input_frame, text="Check Strength", 
                  command=self.check_password).pack(side='left', padx=5)
        
        # Show/Hide password
        self.show_password_var = tk.BooleanVar()
        ttk.Checkbutton(input_frame, text="Show Password", 
                       variable=self.show_password_var,
                       command=self.toggle_password_visibility).pack(side='left', padx=5)
        
        # Results
        ttk.Label(self.password_frame, text="Analysis:", 
                 style='Header.TLabel').pack(anchor='w', padx=20, pady=(20, 5))
        
        self.password_results = scrolledtext.ScrolledText(self.password_frame, 
                                                         height=20, width=100)
        self.password_results.pack(fill='both', expand=True, padx=20, pady=10)
        
    def toggle_password_visibility(self):
        if self.show_password_var.get():
            self.password_entry.config(show="")
        else:
            self.password_entry.config(show="*")
        
    def check_password(self):
        password = self.password_var.get()
        if not password:
            messagebox.showwarning("Warning", "Please enter a password")
            return
            
        self.password_results.delete(1.0, tk.END)
        self.password_results.insert(tk.END, "Password Strength Analysis\n")
        self.password_results.insert(tk.END, "=" * 50 + "\n")
        
        score = 0
        feedback = []
        
        # Length check
        if len(password) >= 8:
            score += 1
            self.password_results.insert(tk.END, "✓ Length: Good (8+ characters)\n")
        else:
            feedback.append("Password should be at least 8 characters long")
            self.password_results.insert(tk.END, "✗ Length: Too short\n")
            
        # Uppercase check
        if re.search(r"[A-Z]", password):
            score += 1
            self.password_results.insert(tk.END, "✓ Uppercase: Found\n")
        else:
            feedback.append("Should contain uppercase letters")
            self.password_results.insert(tk.END, "✗ Uppercase: Missing\n")
            
        # Lowercase check
        if re.search(r"[a-z]", password):
            score += 1
            self.password_results.insert(tk.END, "✓ Lowercase: Found\n")
        else:
            feedback.append("Should contain lowercase letters")
            self.password_results.insert(tk.END, "✗ Lowercase: Missing\n")
            
        # Number check
        if re.search(r"\d", password):
            score += 1
            self.password_results.insert(tk.END, "✓ Numbers: Found\n")
        else:
            feedback.append("Should contain numbers")
            self.password_results.insert(tk.END, "✗ Numbers: Missing\n")
            
        # Special characters check
        if re.search(r"[!@#$%^&*(),.?\":{}|<>]", password):
            score += 1
            self.password_results.insert(tk.END, "✓ Special Characters: Found\n")
        else:
            feedback.append("Should contain special characters")
            self.password_results.insert(tk.END, "✗ Special Characters: Missing\n")
            
        # Overall strength
        self.password_results.insert(tk.END, f"\nOverall Score: {score}/5\n")
        
        if score >= 4:
            strength = "Strong"
        elif score >= 3:
            strength = "Medium"
        else:
            strength = "Weak"
            
        self.password_results.insert(tk.END, f"Password Strength: {strength}\n")
        
        if feedback:
            self.password_results.insert(tk.END, "\nRecommendations:\n")
            for item in feedback:
                self.password_results.insert(tk.END, f"- {item}\n")