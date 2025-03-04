import tkinter as tk
from tkinter import ttk, messagebox
import customtkinter as ctk
import webbrowser
from datetime import datetime, timedelta

class ActivationWizard:
    def __init__(self, parent):
        self.parent = parent
        self.dialog = ctk.CTkToplevel()
        self.dialog.title("Activation Wizard")
        self.dialog.geometry("500x400")
        self.dialog.transient(parent.root)
        self.dialog.grab_set()
        
        # Center the dialog
        self.center_window()
        
        self.setup_ui()
        
    def center_window(self):
        self.dialog.update_idletasks()
        width = self.dialog.winfo_width()
        height = self.dialog.winfo_height()
        x = (self.dialog.winfo_screenwidth() // 2) - (width // 2)
        y = (self.dialog.winfo_screenheight() // 2) - (height // 2)
        self.dialog.geometry(f'{width}x{height}+{x}+{y}')
        
    def setup_ui(self):
        # Welcome message
        welcome_label = ctk.CTkLabel(
            self.dialog,
            text="Welcome to TikTok Profile Backup Tool",
            font=("TkDefaultFont", 20, "bold")
        )
        welcome_label.pack(pady=20)
        
        info_text = ctk.CTkLabel(
            self.dialog,
            text="Choose your license type to continue:",
            wraplength=400
        )
        info_text.pack(pady=10)
        
        # License options
        options_frame = ctk.CTkFrame(self.dialog)
        options_frame.pack(pady=20, fill="x", padx=20)
        
        # Trial button
        trial_btn = ctk.CTkButton(
            options_frame,
            text="Start 30-Day Trial",
            command=self.activate_trial
        )
        trial_btn.pack(pady=10, fill="x")
        
        # Purchase button
        purchase_btn = ctk.CTkButton(
            options_frame,
            text="Purchase License",
            command=self.open_purchase_page
        )
        purchase_btn.pack(pady=10, fill="x")
        
        # Activate button
        activate_frame = ctk.CTkFrame(self.dialog)
        activate_frame.pack(pady=20, fill="x", padx=20)
        
        self.license_key_entry = ctk.CTkEntry(
            activate_frame,
            placeholder_text="Enter License Key"
        )
        self.license_key_entry.pack(pady=10, fill="x")
        
        activate_btn = ctk.CTkButton(
            activate_frame,
            text="Activate License",
            command=self.activate_license
        )
        activate_btn.pack(pady=10, fill="x")
        
    def activate_trial(self):
        """Activate 30-day trial"""
        expiry_date = datetime.now() + timedelta(days=30)
        self.parent.license_manager.save_license("TRIAL", expiry_date)
        self.parent.update_license_status()
        messagebox.showinfo(
            "Trial Activated",
            f"Your 30-day trial has been activated. Expires: {expiry_date.strftime('%Y-%m-%d')}"
        )
        self.dialog.destroy()
        
    def open_purchase_page(self):
        """Open the purchase page in web browser"""
        webbrowser.open("https://your-purchase-page.com")
        
    def activate_license(self):
        """Activate full license"""
        key = self.license_key_entry.get().strip()
        if not key:
            messagebox.showerror("Error", "Please enter a license key")
            return
            
        # Here you would typically validate the license key with your server
        # For this example, we'll accept any key
        self.parent.license_manager.save_license(key)
        self.parent.update_license_status()
        messagebox.showinfo("Success", "License activated successfully!")
        self.dialog.destroy() 