import customtkinter as ctk
from PIL import Image, ImageTk
import os
import time
import threading

class ActivationSplash:
    def __init__(self):
        self.window = ctk.CTk()
        self.window.overrideredirect(True)  # Remove window decorations
        
        # Window size and position - adjusted height
        width = 600
        height = 250  # Further reduced height
        screen_width = self.window.winfo_screenwidth()
        screen_height = self.window.winfo_screenheight()
        x = (screen_width - width) // 2
        y = (screen_height - height) // 2
        self.window.geometry(f'{width}x{height}+{x}+{y}')
        
        # Configure background
        self.window.configure(fg_color='#121212')  # Darker background
        
        # Main frame with border
        main_frame = ctk.CTkFrame(
            self.window,
            fg_color='#1A1A1A',  # Slightly lighter than background
            border_width=1,
            border_color='#333333',  # Subtle border
            corner_radius=10
        )
        main_frame.pack(expand=True, fill="both", padx=20, pady=20)
        
        # Content frame inside main frame
        content_frame = ctk.CTkFrame(main_frame, fg_color='transparent')
        content_frame.pack(expand=True, fill="both", padx=20)
        
        # Title with icon - moved up with more padding
        title_frame = ctk.CTkFrame(content_frame, fg_color='transparent')
        title_frame.pack(pady=(20, 10))  # More padding at top
        
        # Load and display icon
        try:
            icon_path = os.path.join(os.path.dirname(__file__), "..", "assets", "icon.png")
            icon_image = Image.open(icon_path)
            icon_photo = ImageTk.PhotoImage(icon_image)
            icon_label = ctk.CTkLabel(title_frame, image=icon_photo, text="")
            icon_label.image = icon_photo
            icon_label.pack(side="left", padx=10)
        except:
            # Fallback if icon not found
            icon_label = ctk.CTkLabel(title_frame, text="🔑", font=("Arial", 24))
            icon_label.pack(side="left", padx=10)

        title_label = ctk.CTkLabel(
            title_frame,
            text="TikTok Profile Archiver",
            font=("Arial", 24, "bold"),
            text_color="#00FF00"
        )
        title_label.pack(side="left")
        
        # Developer credit with minimal spacing
        dev_label = ctk.CTkLabel(
            content_frame,
            text="developed by",
            font=("Arial", 12),
            text_color="#00FF00"
        )
        dev_label.pack(pady=2)
        
        name_label = ctk.CTkLabel(
            content_frame,
            text="unnamed coder",
            font=("Arial", 16),
            text_color="#FF0000"  # Changed to bright red
        )
        name_label.pack()
        
        # Status message
        self.status_label = ctk.CTkLabel(
            content_frame,
            text="Checking license status...",
            font=("Arial", 14),
            text_color="#00FF00"
        )
        self.status_label.pack(pady=(10, 5))
        
        # Progress bar - moved up
        self.progress_bar = ctk.CTkProgressBar(
            content_frame,
            width=400,
            height=20,
            progress_color="#00FF00",
            corner_radius=10
        )
        self.progress_bar.pack(pady=(0, 15))  # Less padding at bottom
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