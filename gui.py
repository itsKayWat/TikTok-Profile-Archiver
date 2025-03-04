import tkinter as tk
from tkinter import ttk, messagebox
import customtkinter as ctk
import threading
import os
import sys
from PIL import Image, ImageTk
from datetime import datetime
import importlib.util

# Import directly from the same directory
try:
    import sys
    import os
    
    # Add the project root directory to Python path
    project_root = os.path.dirname(os.path.abspath(__file__))
    if project_root not in sys.path:
        sys.path.append(project_root)
        
    # Try importing from current directory first
    module_path = os.path.join(project_root, "tt-backup.py")
    if os.path.exists(module_path):
        spec = importlib.util.spec_from_file_location("tt_backup", module_path)
        tt_backup = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(tt_backup)
        
        # Get the required functions
        create_backup_structure = tt_backup.create_backup_structure
        setup_chrome_profile = tt_backup.setup_chrome_profile
        scrape_profile_info = tt_backup.scrape_profile_info
        handle_tiktok_page_load = tt_backup.handle_tiktok_page_load
        scrape_pinned_videos = tt_backup.scrape_pinned_videos
        scrape_videos = tt_backup.scrape_videos
        install_dependencies = tt_backup.install_dependencies
    else:
        # If that fails, try importing from src directory
        module_path = os.path.join(project_root, "src", "tt-backup.py")
        if os.path.exists(module_path):
            spec = importlib.util.spec_from_file_location("tt_backup", module_path)
            tt_backup = importlib.util.module_from_spec(spec)
            spec.loader.exec_module(tt_backup)
            
            # Get the required functions
            create_backup_structure = tt_backup.create_backup_structure
            setup_chrome_profile = tt_backup.setup_chrome_profile
            scrape_profile_info = tt_backup.scrape_profile_info
            handle_tiktok_page_load = tt_backup.handle_tiktok_page_load
            scrape_pinned_videos = tt_backup.scrape_pinned_videos
            scrape_videos = tt_backup.scrape_videos
            install_dependencies = tt_backup.install_dependencies
        else:
            print("Error: Could not find tt-backup.py in either the current directory or src/ directory")
            print("Please ensure tt-backup.py exists in one of these locations:")
            print(f"- {os.path.join(project_root, 'tt-backup.py')}")
            print(f"- {os.path.join(project_root, 'src', 'tt-backup.py')}")
            sys.exit(1)
except Exception as e:
    print(f"Error importing tt-backup.py: {str(e)}")
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
            from src.licensing.license_manager import LicenseManager
            from src.licensing.activation_wizard import ActivationWizard
            
            self.license_manager = LicenseManager()
            status = self.license_manager.check_license_status()
            
            if status['status'] == 'unlicensed':
                self.show_activation_wizard()
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
        # Sidebar frame with no rounded corners
        self.sidebar = ctk.CTkFrame(
            self.root, 
            fg_color=COLORS['nav_dark'], 
            width=250,
            corner_radius=0  # Remove rounded corners
        )
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
        # Top navbar - attached to sidebar with no rounded corners
        self.navbar = ctk.CTkFrame(
            self.root, 
            fg_color=COLORS['nav_dark'], 
            height=80,
            corner_radius=0
        )
        self.navbar.grid(row=0, column=1, sticky="nsew")
        self.navbar.grid_propagate(False)
        
        # Page title on the left
        self.page_title = ctk.CTkLabel(
            self.navbar,
            text="Profile Backup",
            font=("TkDefaultFont", 20, "bold"),
            text_color=COLORS['text_white']
        )
        self.page_title.pack(side="left", padx=20, pady=20)
        
        # Right-side frame for buttons and status
        right_frame = ctk.CTkFrame(self.navbar, fg_color="transparent")
        right_frame.pack(side="right", padx=20, pady=20)
        
        # GitHub button (rightmost)
        self.github_btn = ctk.CTkButton(
            right_frame,
            text="GitHub",
            fg_color="transparent",
            hover_color=COLORS['secondary_dark'],
            width=70,
            height=30,
            command=self.open_github
        )
        self.github_btn.pack(side="right", padx=5)
        
        # Separator
        separator2 = ctk.CTkLabel(right_frame, text="|", text_color=COLORS['text_gray'])
        separator2.pack(side="right", padx=5)
        
        # Purchase button
        self.purchase_btn = ctk.CTkButton(
            right_frame,
            text="Purchase",
            fg_color=COLORS['accent_pink'],
            hover_color="#D42B4C",
            width=80,
            height=30,
            command=self.open_purchase
        )
        self.purchase_btn.pack(side="right", padx=5)
        
        # Separator
        separator1 = ctk.CTkLabel(right_frame, text="|", text_color=COLORS['text_gray'])
        separator1.pack(side="right", padx=5)
        
        # License status with clickable behavior
        self.license_status = ctk.CTkLabel(
            right_frame,
            text="Trial Mode 7 days left",
            text_color="#FFD700",
            cursor="hand2"
        )
        self.license_status.pack(side="right", padx=5)
        self.license_status.bind("<Button-1>", self.show_license_details)
        
        # Update the status periodically to ensure it stays visible
        def update_status():
            self.license_status.configure(text="Trial Mode 7 days left")
            self.root.after(1000, update_status)  # Check every second
        
        # Start the periodic update
        update_status()

    def update_license_status(self):
        """Update the license status display"""
        try:
            if hasattr(self, 'license_manager'):
                status = self.license_manager.check_license_status()
                
                # Always show trial mode
                text = f"Trial Mode {status.get('days_left', 7)} days left"
                color = "#FFD700"  # Yellow color for trial status
                
            self.license_status.configure(text=text, text_color=color)
            
        except Exception as e:
            print(f"Error updating license status: {e}")
            self.license_status.configure(text="Trial Mode 7 days left", text_color="#FFD700")

    def show_license_details(self, event=None):
        """Show license details in a popup window"""
        # Create popup window with more reasonable size
        popup = ctk.CTkToplevel(self.root)
        popup.title("License Information")
        
        # Set minimum size to ensure it can't be smaller
        popup.minsize(600, 400)
        
        # Set fixed size and disable resizing
        popup.geometry("600x400")
        popup.resizable(False, False)
        
        popup.configure(fg_color='#0F0F0F')
        
        # Center the popup
        screen_width = popup.winfo_screenwidth()
        screen_height = popup.winfo_screenheight()
        x = (screen_width - 600) // 2
        y = (screen_height - 400) // 2
        popup.geometry(f"600x400+{x}+{y}")
        
        # Make window modal
        popup.transient(self.root)
        popup.grab_set()
        
        # Main container with padding
        container = ctk.CTkFrame(popup, fg_color='#0F0F0F')
        container.pack(expand=True, fill="both", padx=40, pady=30)
        
        # Title
        title = ctk.CTkLabel(
            container,
            text="Trial License Details",
            font=("Arial", 28, "bold"),  # Slightly smaller font
            text_color="white"
        )
        title.pack(pady=(0, 40))
        
        # Information frame with dark background
        info_frame = ctk.CTkFrame(container, fg_color='#000000')
        info_frame.pack(fill="both", expand=True, padx=20)
        
        # Information labels with appropriate font size
        expiration = ctk.CTkLabel(
            info_frame,
            text="Expiration Date: March 11, 2025 02:30 PM",
            font=("Arial", 20),  # Adjusted font size
            text_color="#FFD700",
            anchor="w"
        )
        expiration.pack(anchor="w", padx=30, pady=(35, 25))
        
        days = ctk.CTkLabel(
            info_frame,
            text="Days Remaining: 7",
            font=("Arial", 20),
            text_color="#FFD700",
            anchor="w"
        )
        days.pack(anchor="w", padx=30, pady=25)
        
        device = ctk.CTkLabel(
            info_frame,
            text="Device Name: KayWat-Alienware",
            font=("Arial", 20),
            text_color="#FFD700",
            anchor="w"
        )
        device.pack(anchor="w", padx=30, pady=(25, 35))

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
        
        # Disable the start button while backup is running
        self.start_button.configure(state="disabled")
        
        # Create and start the backup thread
        self.backup_thread = threading.Thread(target=self.run_backup, args=(usernames,))
        self.backup_thread.daemon = True  # Make thread daemon so it exits when main thread exits
        self.backup_thread.start()
        
        # Schedule status updates using a safer method
        self.root.after(100, self.check_backup_status)

    def check_backup_status(self):
        """Periodically check backup status and update UI"""
        if hasattr(self, 'backup_thread') and self.backup_thread.is_alive():
            # Thread still running, check again in 100ms
            self.root.after(100, self.check_backup_status)
        else:
            # Thread finished, re-enable start button
            self.start_button.configure(state="normal")

    def run_backup(self, usernames):
        """Run the backup process in a separate thread"""
        try:
            # Update UI from the main thread
            self.root.after(0, lambda: self.update_status("Starting backup process..."))
            self.root.after(0, lambda: self.progress_bar.set(0))
            
            # Install dependencies first
            self.update_status("Checking and installing dependencies...")
            install_dependencies()
            
            # Initialize browser
            self.update_status("\nInitializing browser...")
            driver = setup_chrome_profile()
            
            try:
                # Process each username
                for i, username in enumerate(usernames, 1):
                    progress = (i) / len(usernames)
                    self.root.after(0, lambda: self.progress_bar.set(progress))
                    self.root.after(0, lambda msg=f"\nProcessing account {i}/{len(usernames)}: @{username}": 
                                  self.update_status(msg))
                    
                    # Create backup directory structure
                    base_dir = create_backup_structure(username)
                    
                    # Navigate to profile with handling for automation detection
                    profile_url = f"https://www.tiktok.com/@{username}"
                    if not handle_tiktok_page_load(driver, profile_url):
                        self.root.after(0, lambda msg=f"Failed to load TikTok page for @{username}, skipping to next account...": 
                                      self.update_status(msg))
                        continue
                    
                    # Scrape profile information
                    if not scrape_profile_info(driver, base_dir):
                        self.root.after(0, lambda msg=f"Warning: Failed to scrape profile information for @{username}": 
                                      self.update_status(msg))
                    
                    # Scrape pinned videos
                    if not scrape_pinned_videos(driver, base_dir):
                        self.root.after(0, lambda msg=f"Warning: Failed to scrape pinned videos for @{username}": 
                                      self.update_status(msg))
                    
                    # Scrape videos
                    if not scrape_videos(driver, base_dir):
                        self.root.after(0, lambda msg=f"Warning: Failed to scrape videos for @{username}": 
                                      self.update_status(msg))
                    
                    # Additional scraping based on selected options
                    if self.reposts_var.get():
                        self.update_status("Scraping reposts...")
                        # TODO: Implement reposts scraping
                    
                    if self.favorites_var.get():
                        self.update_status("Scraping favorites...")
                        # TODO: Implement favorites scraping
                    
                    if self.liked_var.get():
                        self.update_status("Scraping liked videos...")
                        # TODO: Implement liked videos scraping
                    
                    self.root.after(0, lambda msg=f"\nBackup completed for @{username}": 
                                  self.update_status(msg))
                
                # Final updates on completion
                self.root.after(0, lambda: self.update_status("\nAll accounts processed successfully!"))
                self.root.after(0, lambda: self.progress_bar.set(1))
                
            except Exception as e:
                error_msg = str(e)
                self.root.after(0, lambda: self.update_status(f"Error during backup: {error_msg}"))
                self.root.after(0, lambda: messagebox.showerror("Error", error_msg))
            finally:
                if driver:
                    driver.quit()
                
        except Exception as e:
            error_msg = str(e)
            self.root.after(0, lambda: self.update_status(f"Error initializing browser: {error_msg}"))
            self.root.after(0, lambda: messagebox.showerror("Error", error_msg))

    def update_status(self, message):
        """Update status text in a thread-safe way"""
        self.status_text.configure(state="normal")
        self.status_text.insert('end', f"{message}\n")
        self.status_text.see('end')
        self.status_text.configure(state="disabled")

    def cancel_backup(self):
        """Cancel the backup process"""
        if hasattr(self, 'backup_thread') and self.backup_thread.is_alive():
            self.update_status("Canceling backup...")
            # TODO: Implement proper cancellation logic
            self.start_button.configure(state="normal")

    def show_activation_wizard(self):
        """Show the activation wizard"""
        from src.licensing.activation_wizard import ActivationWizard
        ActivationWizard(self)
        
    def open_github(self):
        """Open GitHub repository"""
        import webbrowser
        webbrowser.open("https://github.com/itskaywat/tiktok-profile-archiver")

    def open_purchase(self):
        """Open purchase page"""
        import webbrowser
        webbrowser.open("https://www.paypal.com/donate/?hosted_button_id=J3ABMPG6MQF3L")

    def run(self):
        self.root.mainloop()

if __name__ == "__main__":
    # Check license before anything else
    try:
        from src.licensing.license_manager import LicenseManager
        license_manager = LicenseManager()
        status = license_manager.check_license_status()
        
        if status['status'] == 'unlicensed':
            # Show activation splash first
            from src.licensing.activation_splash import ActivationSplash
            activation_splash = ActivationSplash()
            activation_splash.run()
            
            # Create temporary root for activation wizard
            temp_root = ctk.CTk()
            temp_root.withdraw()  # Hide the temporary root
            
            # Show activation wizard
            from src.licensing.activation_wizard import ActivationWizard
            wizard = ActivationWizard(temp_root)
            wizard.wait_window()  # Wait for activation window to close
            
            # Recheck license status after activation
            status = license_manager.check_license_status()
            if status['status'] == 'unlicensed':
                # If still unlicensed, exit
                sys.exit()
                
            temp_root.destroy()
        
        # Only if licensed/trial, show main splash and start app
        from src.splash_screen import SplashScreen
        splash = SplashScreen()
        splash.run()
        
        # Start main application
        app = TikTokBackupGUI()
        app.run()
        
    except Exception as e:
        import tkinter.messagebox as messagebox
        messagebox.showerror("Error", f"Failed to start application: {str(e)}")
        sys.exit(1) 
