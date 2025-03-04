import customtkinter as ctk
from tkinter import messagebox
import webbrowser
from datetime import datetime, timedelta
import json
import os

class ActivationWizard(ctk.CTkToplevel):
    def __init__(self, parent):
        super().__init__(parent)
        self.parent = parent
        self.title("Activation Wizard")
        self.geometry("500x450")  # Slightly increased height for footer
        self.resizable(False, False)
        
        # Theme colors
        self.colors = {
            'bg_dark': '#121212',
            'secondary_dark': '#1E1E1E',
            'button_gray': '#2A2A2A',
            'accent_pink': '#FF2C55',
            'text_white': '#FFFFFF',
            'text_gray': '#8A8B91',
            'input_border': '#333333'
        }
        
        # Make window modal
        self.transient(parent)
        self.grab_set()
        
        # Configure theme
        self.configure(fg_color=self.colors['bg_dark'])
        
        # Center window
        self.center_window()
        
        self.setup_ui()
        
    def setup_ui(self):
        # Main container
        container = ctk.CTkFrame(self, fg_color=self.colors['bg_dark'])
        container.pack(expand=True, fill="both")
        
        # Content area
        content_area = ctk.CTkFrame(container, fg_color='transparent')
        content_area.pack(expand=True, fill="both", padx=20, pady=20)
        
        # Title
        title = ctk.CTkLabel(
            content_area,
            text="Welcome to TikTok Profile Archiver",
            font=("Arial", 20, "bold"),
            text_color=self.colors['text_white']
        )
        title.pack(pady=(0, 10))
        
        # Subtitle
        subtitle = ctk.CTkLabel(
            content_area,
            text="Choose your license type to continue:",
            font=("Arial", 12),
            text_color=self.colors['text_gray']
        )
        subtitle.pack(pady=(0, 20))
        
        # Trial button
        trial_btn = ctk.CTkButton(
            content_area,
            text="Start 7-Day Trial",
            command=self.start_trial,
            height=40,
            font=("Arial", 14),
            fg_color=self.colors['button_gray'],
            hover_color="#333333"
        )
        trial_btn.pack(pady=(0, 10), padx=20, fill="x")
        
        # Purchase button
        purchase_btn = ctk.CTkButton(
            content_area,
            text="Purchase License",
            command=self.purchase_license,
            height=40,
            font=("Arial", 14),
            fg_color=self.colors['accent_pink'],
            hover_color="#FF1F4B"
        )
        purchase_btn.pack(pady=(0, 20), padx=20, fill="x")
        
        # License section
        license_frame = ctk.CTkFrame(content_area, fg_color=self.colors['secondary_dark'])
        license_frame.pack(pady=(0, 10), padx=20, fill="x")
        
        license_label = ctk.CTkLabel(
            license_frame,
            text="Already have a license?",
            font=("Arial", 12),
            text_color=self.colors['text_gray']
        )
        license_label.pack(pady=(10, 5))
        
        self.license_key_entry = ctk.CTkEntry(
            license_frame,
            placeholder_text="Enter License Key",
            height=35,
            font=("Arial", 12),
            fg_color=self.colors['bg_dark'],
            border_color=self.colors['input_border'],
            text_color=self.colors['text_white']
        )
        self.license_key_entry.pack(pady=5, padx=20, fill="x")
        
        activate_btn = ctk.CTkButton(
            license_frame,
            text="Activate License",
            command=self.activate_license,
            height=35,
            font=("Arial", 12),
            fg_color=self.colors['accent_pink'],
            hover_color="#FF1F4B"
        )
        activate_btn.pack(pady=10, padx=20, fill="x")
        
        # Footer frame at the bottom
        footer_frame = ctk.CTkFrame(self, fg_color='transparent', height=30)
        footer_frame.pack(fill="x", side="bottom", pady=5)
        footer_frame.pack_propagate(False)  # Prevent frame from shrinking
        
        # Footer text with developer credit
        footer_text = ctk.CTkLabel(
            footer_frame,
            text="developed by unnamed coder",
            font=("Arial", 11),
            text_color="#404040"  # Very subtle gray
        )
        footer_text.pack(expand=True)
        
    def center_window(self):
        self.update_idletasks()
        width = self.winfo_width()
        height = self.winfo_height()
        x = (self.winfo_screenwidth() // 2) - (width // 2)
        y = (self.winfo_screenheight() // 2) - (height // 2)
        self.geometry(f'{width}x{height}+{x}+{y}')
        
    def start_trial(self):
        """Start 7-day trial"""
        try:
            trial_file = os.path.join(os.path.expanduser('~'), '.tiktok_backup', 'trial.json')
            os.makedirs(os.path.dirname(trial_file), exist_ok=True)
            
            if os.path.exists(trial_file):
                with open(trial_file, 'r') as f:
                    trial_data = json.load(f)
                    end_date = datetime.fromisoformat(trial_data['end_date'])
                    if datetime.now() < end_date:
                        messagebox.showerror(
                            "Trial Active",
                            "You already have an active trial that expires on "
                            f"{end_date.strftime('%Y-%m-%d')}"
                        )
                        return
            
            # Start new trial
            trial_data = {
                'start_date': datetime.now().isoformat(),
                'end_date': (datetime.now() + timedelta(days=7)).isoformat()
            }
            
            with open(trial_file, 'w') as f:
                json.dump(trial_data, f)
                
            messagebox.showinfo(
                "Trial Started",
                "Your 7-day trial has been activated!\n\n"
                f"Expires: {trial_data['end_date'].split('T')[0]}"
            )
            self.grab_release()  # Release modal state
            self.destroy()
            
        except Exception as e:
            messagebox.showerror("Error", f"Could not start trial: {str(e)}")
    
    def purchase_license(self):
        """Open purchase webpage"""
        webbrowser.open("https://your-purchase-url.com")
        
    def activate_license(self):
        """Validate and activate license key"""
        key = self.license_key_entry.get().strip()
        if not key:
            messagebox.showerror("Error", "Please enter a license key")
            return
            
        # Here you would validate the license key with your server
        # For now, we'll accept any key
        try:
            license_file = os.path.join(os.path.expanduser('~'), '.tiktok_backup', 'license.json')
            os.makedirs(os.path.dirname(license_file), exist_ok=True)
            
            license_data = {
                'key': key,
                'activation_date': datetime.now().isoformat()
            }
            
            with open(license_file, 'w') as f:
                json.dump(license_data, f)
                
            messagebox.showinfo(
                "Success",
                "License activated successfully!"
            )
            self.grab_release()  # Release modal state
            self.destroy()
            
        except Exception as e:
            messagebox.showerror("Error", f"Could not activate license: {str(e)}") 