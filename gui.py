import tkinter as tk
from tkinter import ttk, messagebox
import customtkinter as ctk
import threading
import os
import sys
from PIL import Image, ImageTk

# TikTok-themed colors
COLORS = {
    'bg_dark': '#121212',
    'secondary_dark': '#2A2A2A',
    'accent_pink': '#FE2C55',
    'accent_blue': '#25F4EE',
    'text_white': '#FFFFFF',
    'text_gray': '#8A8B91',
    'success_green': '#25B43A'
}

class TikTokBackupGUI:
    def __init__(self):
        self.root = ctk.CTk()
        self.root.title("TikTok Profile Backup Tool")
        self.root.geometry("900x600")
        self.root.configure(fg_color=COLORS['bg_dark'])
        
        # Configure custom appearance
        ctk.set_appearance_mode("dark")
        ctk.set_default_color_theme("dark-blue")
        
        self.setup_gui()
        
    def setup_gui(self):
        # Create main container
        self.main_frame = ctk.CTkFrame(self.root, fg_color=COLORS['bg_dark'])
        self.main_frame.pack(fill='both', expand=True, padx=20, pady=20)
        
        # Header with logo
        self.header_frame = ctk.CTkFrame(self.main_frame, fg_color=COLORS['bg_dark'])
        self.header_frame.pack(fill='x', pady=(0, 20))
        
        self.title_label = ctk.CTkLabel(
            self.header_frame,
            text="TikTok Profile Backup",
            font=("TkDefaultFont", 24, "bold"),
            text_color=COLORS['text_white']
        )
        self.title_label.pack(pady=10)
        
        # Input section
        self.input_frame = ctk.CTkFrame(self.main_frame, fg_color=COLORS['secondary_dark'])
        self.input_frame.pack(fill='x', pady=10, padx=5)
        
        self.username_label = ctk.CTkLabel(
            self.input_frame,
            text="Enter TikTok Usernames (separated by commas):",
            text_color=COLORS['text_white']
        )
        self.username_label.pack(pady=(10, 5), padx=10, anchor='w')
        
        self.username_entry = ctk.CTkEntry(
            self.input_frame,
            placeholder_text="e.g., username1, username2",
            width=400,
            height=35
        )
        self.username_entry.pack(pady=(0, 10), padx=10)
        
        # Backup options
        self.options_frame = ctk.CTkFrame(self.main_frame, fg_color=COLORS['secondary_dark'])
        self.options_frame.pack(fill='x', pady=10, padx=5)
        
        self.options_label = ctk.CTkLabel(
            self.options_frame,
            text="Select Backup Options:",
            text_color=COLORS['text_white']
        )
        self.options_label.pack(pady=(10, 5), padx=10, anchor='w')
        
        # Checkboxes for options
        self.reposts_var = tk.BooleanVar()
        self.favorites_var = tk.BooleanVar()
        self.liked_var = tk.BooleanVar()
        
        self.reposts_cb = ctk.CTkCheckBox(
            self.options_frame,
            text="Reposts",
            variable=self.reposts_var,
            text_color=COLORS['text_white']
        )
        self.reposts_cb.pack(pady=5, padx=10, anchor='w')
        
        self.favorites_cb = ctk.CTkCheckBox(
            self.options_frame,
            text="Favorites",
            variable=self.favorites_var,
            text_color=COLORS['text_white']
        )
        self.favorites_cb.pack(pady=5, padx=10, anchor='w')
        
        self.liked_cb = ctk.CTkCheckBox(
            self.options_frame,
            text="Liked Videos",
            variable=self.liked_var,
            text_color=COLORS['text_white']
        )
        self.liked_cb.pack(pady=(5, 10), padx=10, anchor='w')
        
        # Progress section
        self.progress_frame = ctk.CTkFrame(self.main_frame, fg_color=COLORS['secondary_dark'])
        self.progress_frame.pack(fill='x', pady=10, padx=5)
        
        self.progress_label = ctk.CTkLabel(
            self.progress_frame,
            text="Progress:",
            text_color=COLORS['text_white']
        )
        self.progress_label.pack(pady=(10, 5), padx=10, anchor='w')
        
        self.progress_bar = ctk.CTkProgressBar(
            self.progress_frame,
            width=400,
            height=20,
            progress_color=COLORS['accent_pink']
        )
        self.progress_bar.pack(pady=(0, 10), padx=10)
        self.progress_bar.set(0)
        
        # Status text
        self.status_text = ctk.CTkTextbox(
            self.main_frame,
            height=150,
            fg_color=COLORS['secondary_dark'],
            text_color=COLORS['text_white']
        )
        self.status_text.pack(fill='x', pady=10, padx=5)
        
        # Buttons
        self.button_frame = ctk.CTkFrame(self.main_frame, fg_color=COLORS['bg_dark'])
        self.button_frame.pack(fill='x', pady=10)
        
        self.start_button = ctk.CTkButton(
            self.button_frame,
            text="Start Backup",
            command=self.start_backup,
            fg_color=COLORS['accent_pink'],
            hover_color='#D42B4C'
        )
        self.start_button.pack(side='left', padx=5)
        
        self.cancel_button = ctk.CTkButton(
            self.button_frame,
            text="Cancel",
            command=self.cancel_backup,
            fg_color=COLORS['secondary_dark'],
            hover_color='#3A3A3A'
        )
        self.cancel_button.pack(side='left', padx=5)
        
    def start_backup(self):
        usernames = [u.strip() for u in self.username_entry.get().split(',')]
        if not usernames:
            messagebox.showerror("Error", "Please enter at least one username")
            return
            
        # Start backup in separate thread
        self.backup_thread = threading.Thread(target=self.run_backup, args=(usernames,))
        self.backup_thread.start()
        
    def run_backup(self, usernames):
        # Here we'll integrate with the main backup functionality
        self.update_status("Starting backup process...")
        self.progress_bar.set(0)
        
        # Import main backup functionality
        from tt_backup import create_backup_structure, setup_chrome_profile, scrape_profile_info
        
        try:
            driver = setup_chrome_profile()
            for i, username in enumerate(usernames):
                progress = (i + 1) / len(usernames)
                self.progress_bar.set(progress)
                self.update_status(f"Processing @{username}...")
                
                base_dir = create_backup_structure(username)
                # Call other backup functions here
                
            self.update_status("Backup completed successfully!")
            self.progress_bar.set(1)
            
        except Exception as e:
            self.update_status(f"Error: {str(e)}")
            messagebox.showerror("Error", str(e))
            
    def cancel_backup(self):
        if hasattr(self, 'backup_thread') and self.backup_thread.is_alive():
            # Implement cancellation logic
            self.update_status("Canceling backup...")
    
    def update_status(self, message):
        self.status_text.insert('end', f"{message}\n")
        self.status_text.see('end')
        
    def run(self):
        self.root.mainloop()

if __name__ == "__main__":
    app = TikTokBackupGUI()
    app.run() 