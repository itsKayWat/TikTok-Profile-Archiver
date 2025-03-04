from PySide6.QtWidgets import QSplashScreen, QLabel, QVBoxLayout, QWidget, QProgressBar
from PySide6.QtCore import Qt, QTimer
from PySide6.QtGui import QPixmap, QPainter

class ActivationSplash(QSplashScreen):
    def __init__(self, pixmap=None):
        if pixmap is None:
            # Create a default pixmap if none provided
            pixmap = QPixmap(400, 200)
            pixmap.fill(Qt.transparent)
        super().__init__(pixmap, Qt.WindowStaysOnTopHint)
        
        # Create widget to hold content
        self.content = QWidget(self)
        layout = QVBoxLayout(self.content)
        layout.setContentsMargins(20, 20, 20, 20)
        
        # Add status label
        self.status_label = QLabel("Checking license status...")
        self.status_label.setStyleSheet("""
            QLabel {
                color: #E2E8F0;
                font-size: 14px;
                font-weight: bold;
            }
        """)
        self.status_label.setAlignment(Qt.AlignCenter)
        layout.addWidget(self.status_label)
        
        # Add progress bar
        self.progress = QProgressBar()
        self.progress.setTextVisible(False)
        self.progress.setStyleSheet("""
            QProgressBar {
                border: 1px solid #2D3139;
                border-radius: 4px;
                background: #24262B;
                height: 8px;
            }
            QProgressBar::chunk {
                background: #4ADE80;
                border-radius: 4px;
            }
        """)
        layout.addWidget(self.progress)
        
        # Size and position content
        self.content.setFixedSize(360, 80)
        self.content.move(20, 60)
        
        # Setup progress animation
        self.progress_timer = QTimer()
        self.progress_timer.timeout.connect(self._update_progress)
        self.progress_value = 0
        
    def start_progress(self):
        """Start the progress animation"""
        self.progress_value = 0
        self.progress.setValue(0)
        self.progress_timer.start(30)  # Update every 30ms
        
    def stop_progress(self):
        """Stop the progress animation"""
        self.progress_timer.stop()
        self.progress.setValue(100)
        
    def set_status(self, text):
        """Update the status text"""
        self.status_label.setText(text)
        
    def _update_progress(self):
        """Update progress bar animation"""
        self.progress_value = (self.progress_value + 1) % 100
        self.progress.setValue(self.progress_value)
        
    def paintEvent(self, event):
        """Custom paint event to create a modern look"""
        painter = QPainter(self)
        painter.setRenderHint(QPainter.Antialiasing)
        
        # Draw background
        painter.setBrush(Qt.black)
        painter.setPen(Qt.NoPen)
        painter.setOpacity(0.85)
        painter.drawRoundedRect(self.rect(), 10, 10) 