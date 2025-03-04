import tkinter as tk
from tkinter import ttk, messagebox
import customtkinter as ctk
import threading
import os
import sys
from PIL import Image, ImageTk

# Import directly from the same directory
try:
    import sys
    import os
    
    # Add the project root directory to Python path
    project_root = os.path.dirname(os.path.abspath(__file__))
    if project_root not in sys.path:
        sys.path.append(project_root)
        
    # Try importing from current directory first
    from tt_backup import create_backup_structure, setup_chrome_profile, scrape_profile_info
except ImportError:
    # If that fails, try importing from src directory
    try:
        from src.tt_backup import create_backup_structure, setup_chrome_profile, scrape_profile_info
    except ImportError:
        print("Error: Could not find tt_backup.py in either the current directory or src/ directory")
        print("Please ensure tt_backup.py exists in one of these locations:")
        print(f"- {os.path.join(project_root, 'tt_backup.py')}")
        print(f"- {os.path.join(project_root, 'src', 'tt_backup.py')}")
        sys.exit(1)

# TikTok-themed colors
COLORS = {
    'bg_dark': '#121212',
    'secondary_dark': '#2A2A2A',
    'accent_pink': '#FE2C55',
    'accent_blue': '#25F4EE',
    'text_white': '#FFFFFF',
    'text_gray': '#8A8B91',
    'success_green': '#25B43A',
    'nav_dark': '#1A1A1A'
}

class TikTokBackupGUI:
    def __init__(self):
        self.root = ctk.CTk()
        self.root.title("TikTok Profile Backup Tool")
        self.root.geometry("1200x800")
        self.root.configure(fg_color=COLORS['bg_dark'])
        
        # Configure custom appearance
        ctk.set_appearance_mode("dark")
        ctk.set_default_color_theme("dark-blue")
        
        self.setup_gui()
        
        # Show activation wizard on first run
        try:
            from src.payment.license_manager import LicenseManager
            from src.payment.activation_wizard import ActivationWizard
            
            self.license_manager = LicenseManager()
            if not self.license_manager.license_file.exists():
                # Schedule activation wizard to open after main window is ready
                self.root.after(1000, self.show_activation_wizard)
        except ImportError as e:
            print(f"License management modules not found: {e}")
            print("Running in unrestricted mode")
        
    def setup_gui(self):
        # Create main container with grid
        self.root.grid_rowconfigure(1, weight=1)
        self.root.grid_columnconfigure(1, weight=1)
        
        # Create sidebar
        self.setup_sidebar()
        
        # Create top navbar
        self.setup_navbar()
        
        # Create main content area
        self.setup_main_content()
        
    def setup_sidebar(self):
        # Sidebar frame
        self.sidebar = ctk.CTkFrame(self.root, fg_color=COLORS['nav_dark'], width=250)
        self.sidebar.grid(row=0, column=0, rowspan=2, sticky="nsew")
        self.sidebar.grid_propagate(False)
        
        # Logo frame at the top of sidebar
        logo_frame = ctk.CTkFrame(self.sidebar, fg_color="transparent", height=100)
        logo_frame.pack(fill="x", padx=20, pady=20)
        
        # Logo label
        logo_label = ctk.CTkLabel(
            logo_frame,
            text="TikTok Backup",
            font=("TkDefaultFont", 24, "bold"),
            text_color=COLORS['text_white']
        )
        logo_label.pack(pady=10)
        
        # Navigation buttons
        nav_buttons = [
            ("Profile Backup", "profile"),
            ("Video Archive", "videos"),
            ("Settings", "settings"),
            ("Help", "help")
        ]
        
        for text, cmd in nav_buttons:
            btn = ctk.CTkButton(
                self.sidebar,
                text=text,
                fg_color="transparent",
                hover_color=COLORS['secondary_dark'],
                anchor="w",
                height=50,
                command=lambda c=cmd: self.nav_button_click(c)
            )
            btn.pack(fill="x", padx=10, pady=5)
            
    def setup_navbar(self):
        # Top navbar
        self.navbar = ctk.CTkFrame(self.root, fg_color=COLORS['nav_dark'], height=60)
        self.navbar.grid(row=0, column=1, sticky="ew")
        self.navbar.grid_propagate(False)
        
        # Page title
        self.page_title = ctk.CTkLabel(
            self.navbar,
            text="Profile Backup",
            font=("TkDefaultFont", 20, "bold"),
            text_color=COLORS['text_white']
        )
        self.page_title.pack(side="left", padx=20)
        
        # User info/settings on the right
        user_frame = ctk.CTkFrame(self.navbar, fg_color="transparent")
        user_frame.pack(side="right", padx=20)
        
        self.settings_btn = ctk.CTkButton(
            user_frame,
            text="Settings",
            fg_color="transparent",
            hover_color=COLORS['secondary_dark'],
            width=100
        )
        self.settings_btn.pack(side="right", padx=10)
        
        # License status on the right
        self.license_status = ctk.CTkLabel(
            user_frame,
            text="Checking license...",
            text_color=COLORS['text_gray']
        )
        self.license_status.pack(side="right", padx=10)
        
        # Update license status
        self.update_license_status()
        
    def update_license_status(self):
        """Update the license status display"""
        try:
            if hasattr(self, 'license_manager'):
                status = self.license_manager.check_license()
                
                if status["status"] == "licensed":
                    text = "Licensed Version"
                    color = COLORS['success_green']
                elif status["status"] == "trial":
                    text = f"Trial Version ({status['days_left']} days left)"
                    color = COLORS['accent_blue']
                else:
                    text = "License Expired"
                    color = COLORS['accent_pink']
            else:
                text = "Unrestricted Version"
                color = COLORS['success_green']
                
            self.license_status.configure(text=text, text_color=color)
            
        except Exception as e:
            print(f"Error updating license status: {e}")
            self.license_status.configure(text="Error", text_color=COLORS['accent_pink'])

    def setup_main_content(self):
        # Main content area
        self.main_content = ctk.CTkFrame(self.root, fg_color=COLORS['bg_dark'])
        self.main_content.grid(row=1, column=1, sticky="nsew", padx=20, pady=20)
        
        # Input section
        self.input_frame = ctk.CTkFrame(self.main_content, fg_color=COLORS['secondary_dark'])
        self.input_frame.pack(fill="x", pady=10)
        
        self.username_label = ctk.CTkLabel(
            self.input_frame,
            text="Enter TikTok Usernames (separated by commas):",
            text_color=COLORS['text_white']
        )
        self.username_label.pack(pady=(10, 5), padx=10, anchor="w")
        
        self.username_entry = ctk.CTkEntry(
            self.input_frame,
            placeholder_text="e.g., username1, username2",
            width=400,
            height=35
        )
        self.username_entry.pack(pady=(0, 10), padx=10)
        
        # Options section
        self.options_frame = ctk.CTkFrame(self.main_content, fg_color=COLORS['secondary_dark'])
        self.options_frame.pack(fill="x", pady=10)
        
        self.options_label = ctk.CTkLabel(
            self.options_frame,
            text="Select Backup Options:",
            text_color=COLORS['text_white']
        )
        self.options_label.pack(pady=(10, 5), padx=10, anchor="w")
        
        # Checkboxes
        self.profile_var = tk.BooleanVar(value=True)
        self.reposts_var = tk.BooleanVar()
        self.favorites_var = tk.BooleanVar()
        self.liked_var = tk.BooleanVar()
        
        checkboxes = [
            ("Profile Information", self.profile_var),
            ("Reposts", self.reposts_var),
            ("Favorites", self.favorites_var),
            ("Liked Videos", self.liked_var)
        ]
        
        for text, var in checkboxes:
            cb = ctk.CTkCheckBox(
                self.options_frame,
                text=text,
                variable=var,
                text_color=COLORS['text_white']
            )
            cb.pack(pady=5, padx=10, anchor="w")
        
        # Progress section
        self.progress_frame = ctk.CTkFrame(self.main_content, fg_color=COLORS['secondary_dark'])
        self.progress_frame.pack(fill="x", pady=10)
        
        self.progress_label = ctk.CTkLabel(
            self.progress_frame,
            text="Progress:",
            text_color=COLORS['text_white']
        )
        self.progress_label.pack(pady=(10, 5), padx=10, anchor="w")
        
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
            self.main_content,
            height=150,
            fg_color=COLORS['secondary_dark'],
            text_color=COLORS['text_white']
        )
        self.status_text.pack(fill="x", pady=10)
        
        # Buttons
        self.button_frame = ctk.CTkFrame(self.main_content, fg_color="transparent")
        self.button_frame.pack(fill="x", pady=10)
        
        self.start_button = ctk.CTkButton(
            self.button_frame,
            text="Start Backup",
            command=self.start_backup,
            fg_color=COLORS['accent_pink'],
            hover_color='#D42B4C'
        )
        self.start_button.pack(side="left", padx=5)
        
        self.cancel_button = ctk.CTkButton(
            self.button_frame,
            text="Cancel",
            command=self.cancel_backup,
            fg_color=COLORS['secondary_dark'],
            hover_color='#3A3A3A'
        )
        self.cancel_button.pack(side="left", padx=5)
        
    def nav_button_click(self, section):
        """Handle navigation button clicks"""
        # Update page title
        self.page_title.configure(text=section.title())
        
        # Hide all content frames
        for widget in self.main_content.winfo_children():
            widget.pack_forget()
        
        # Show appropriate content based on section
        if section == "profile":
            # Show profile backup content
            self.show_profile_content()
        else:
            # Show coming soon message for other sections
            self.show_coming_soon(section)

    def show_coming_soon(self, section):
        """Display coming soon message for unimplemented sections"""
        coming_soon_frame = ctk.CTkFrame(self.main_content, fg_color=COLORS['secondary_dark'])
        coming_soon_frame.pack(fill="both", expand=True, padx=20, pady=20)
        
        # Section icon/image placeholder
        icon_label = ctk.CTkLabel(
            coming_soon_frame,
            text="🔜",  # You can replace this with an actual icon
            font=("TkDefaultFont", 48),
            text_color=COLORS['accent_pink']
        )
        icon_label.pack(pady=(50, 20))
        
        # Coming soon title
        title_label = ctk.CTkLabel(
            coming_soon_frame,
            text=f"{section.title()} - Coming Soon!",
            font=("TkDefaultFont", 24, "bold"),
            text_color=COLORS['text_white']
        )
        title_label.pack(pady=10)
        
        # Feature descriptions based on section
        features = {
            "videos": [
                "📥 Bulk video downloads",
                "🎵 Music extraction",
                "📊 Video analytics",
                "🏷️ Advanced tagging"
            ],
            "settings": [
                "⚙️ Customize backup options",
                "📁 Set default save locations",
                "🔄 Auto-backup scheduling",
                "🎨 Theme customization"
            ],
            "help": [
                "📚 User documentation",
                "❓ FAQ section",
                "🎥 Video tutorials",
                "📧 Support contact"
            ]
        }
        
        if section in features:
            feature_frame = ctk.CTkFrame(coming_soon_frame, fg_color="transparent")
            feature_frame.pack(pady=20)
            
            for feature in features[section]:
                feature_label = ctk.CTkLabel(
                    feature_frame,
                    text=feature,
                    font=("TkDefaultFont", 14),
                    text_color=COLORS['text_gray']
                )
                feature_label.pack(pady=5)
        
        # Notification signup
        notify_frame = ctk.CTkFrame(coming_soon_frame, fg_color="transparent")
        notify_frame.pack(pady=30)
        
        notify_label = ctk.CTkLabel(
            notify_frame,
            text="Get notified when this feature launches:",
            text_color=COLORS['text_white']
        )
        notify_label.pack(pady=5)
        
        email_entry = ctk.CTkEntry(
            notify_frame,
            placeholder_text="Enter your email",
            width=300
        )
        email_entry.pack(pady=5)
        
        notify_btn = ctk.CTkButton(
            notify_frame,
            text="Notify Me",
            fg_color=COLORS['accent_pink'],
            hover_color='#D42B4C',
            command=lambda: self.handle_notify(email_entry.get(), section)
        )
        notify_btn.pack(pady=5)

    def show_profile_content(self):
        """Show the profile backup interface"""
        # Input section
        self.input_frame.pack(fill="x", pady=10)
        
        # Options section
        self.options_frame.pack(fill="x", pady=10)
        
        # Progress section
        self.progress_frame.pack(fill="x", pady=10)
        
        # Status text
        self.status_text.pack(fill="x", pady=10)
        
        # Buttons
        self.button_frame.pack(fill="x", pady=10)

    def handle_notify(self, email, section):
        """Handle notification signup"""
        if '@' in email and '.' in email:
            messagebox.showinfo(
                "Thank You!", 
                f"We'll notify you when the {section.title()} feature launches!\nEmail: {email}"
            )
        else:
            messagebox.showerror("Error", "Please enter a valid email address.")

    def start_backup(self):
        usernames = [u.strip() for u in self.username_entry.get().split(',')]
        if not usernames:
            messagebox.showerror("Error", "Please enter at least one username")
            return
        
        self.backup_thread = threading.Thread(target=self.run_backup, args=(usernames,))
        self.backup_thread.start()
        
    def run_backup(self, usernames):
        self.update_status("Starting backup process...")
        self.progress_bar.set(0)
        
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
            self.update_status("Canceling backup...")
    
    def update_status(self, message):
        self.status_text.insert('end', f"{message}\n")
        self.status_text.see('end')
        
    def show_activation_wizard(self):
        """Show the activation wizard"""
        from src.payment.activation_wizard import ActivationWizard
        ActivationWizard(self)
        
    def run(self):
        self.root.mainloop()

if __name__ == "__main__":
    app = TikTokBackupGUI()
    app.run() 
