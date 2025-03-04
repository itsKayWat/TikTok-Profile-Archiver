import customtkinter as ctk
from PIL import Image, ImageTk
import os
import time
import threading

class SplashScreen:
    def __init__(self):
        self.window = ctk.CTk()
        self.window.overrideredirect(True)
        
        # Window size and position
        width = 600
        height = 250
        screen_width = self.window.winfo_screenwidth()
        screen_height = self.window.winfo_screenheight()
        x = (screen_width - width) // 2
        y = (screen_height - height) // 2
        self.window.geometry(f'{width}x{height}+{x}+{y}')
        
        # Configure background
        self.window.configure(fg_color='#0F0F0F')  # Darker background
        
        # Main frame with subtle gradient effect
        main_frame = ctk.CTkFrame(
            self.window,
            fg_color='#141414',
            border_width=1,
            border_color='#2A2A2A',
            corner_radius=15
        )
        main_frame.pack(expand=True, fill="both", padx=20, pady=20)
        
        # Content frame
        content_frame = ctk.CTkFrame(main_frame, fg_color='transparent')
        content_frame.pack(expand=True, fill="both", padx=30, pady=20)
        
        # Title frame with icon
        title_frame = ctk.CTkFrame(content_frame, fg_color='transparent')
        title_frame.pack(pady=(0, 5))
        
        # Load and display icon
        try:
            icon_path = os.path.join(os.path.dirname(__file__), "assets", "icon.png")
            icon_image = Image.open(icon_path)
            icon_photo = ImageTk.PhotoImage(icon_image)
            icon_label = ctk.CTkLabel(title_frame, image=icon_photo, text="")
            icon_label.image = icon_photo
            icon_label.pack(side="left", padx=10)
        except:
            # Fallback if icon not found - using music note instead of game controller
            icon_label = ctk.CTkLabel(title_frame, text="🎵", font=("Arial", 24))
            icon_label.pack(side="left", padx=10)

        # Title with glowing effect
        title_label = ctk.CTkLabel(
            title_frame,
            text="TikTok Profile Archiver",
            font=("Arial", 28, "bold"),
            text_color="#00FF00"
        )
        title_label.pack(side="left")
        
        # Separator line
        separator = ctk.CTkFrame(
            content_frame,
            height=1,
            fg_color='#2A2A2A',
            width=200
        )
        separator.pack(pady=(5, 0))
        
        # Developer credit
        dev_label = ctk.CTkLabel(
            content_frame,
            text="developed by",
            font=("Arial", 12),
            text_color="#00FF00"
        )
        dev_label.pack(pady=(5, 0))
        
        name_label = ctk.CTkLabel(
            content_frame,
            text="unnamed coder",
            font=("Arial", 16, "bold"),
            text_color="#FF0000"
        )
        name_label.pack(pady=(0, 5))
        
        # Status message with custom styling
        self.status_label = ctk.CTkLabel(
            content_frame,
            text="Installing required packages...",
            font=("Arial", 14),
            text_color="#00FF00"
        )
        self.status_label.pack(pady=(10, 5))
        
        # Custom styled progress bar
        progress_frame = ctk.CTkFrame(content_frame, fg_color='transparent')
        progress_frame.pack(fill="x", pady=(5, 0))
        
        self.progress_bar = ctk.CTkProgressBar(
            progress_frame,
            width=400,
            height=15,
            progress_color="#00FF00",
            corner_radius=7,
            fg_color='#1A1A1A',
            border_color='#2A2A2A',
            border_width=1
        )
        self.progress_bar.pack()
        self.progress_bar.set(0)
        
        # Start progress simulation
        self.progress_thread = threading.Thread(target=self.simulate_progress)
        self.progress_thread.start()
        
    def simulate_progress(self):
        """Simulate loading progress"""
        for i in range(101):
            time.sleep(0.02)
            self.progress_bar.set(i / 100)
            if i == 100:
                self.window.after(200, self.finish)
                
    def finish(self):
        """Clean up and close splash screen"""
        self.window.destroy()
        
    def run(self):
        self.window.mainloop() 