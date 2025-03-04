from PySide6.QtWidgets import *
from PySide6.QtCore import Qt
import webbrowser

class LicenseDialog(QDialog):
    def __init__(self, parent=None, theme=None, license_validator=None):
        super().__init__(parent)
        self.theme = theme
        self.validator = license_validator
        self.setup_ui()
        
    def setup_ui(self):
        self.setWindowTitle("License Activation")
        self.setModal(True)
        
        layout = QVBoxLayout(self)
        layout.setSpacing(20)
        layout.setContentsMargins(30, 30, 30, 30)
        
        # Title
        title = QLabel("License Activation")
        layout.addWidget(title)
        
        # Status section
        status_frame = QFrame()
        status_layout = QVBoxLayout(status_frame)
        
        self.status_label = QLabel()
        self.status_label.setWordWrap(True)
        status_layout.addWidget(self.status_label)
        
        layout.addWidget(status_frame)
        
        # Activation section
        activation_frame = QFrame()
        activation_layout = QVBoxLayout(activation_frame)
        
        activation_layout.addWidget(QLabel("Enter License Key:"))
        
        self.key_input = QLineEdit()
        self.key_input.setPlaceholderText("XXXX-XXXX-XXXX-XXXX")
        activation_layout.addWidget(self.key_input)
        
        btn_layout = QHBoxLayout()
        
        activate_btn = QPushButton("Activate License")
        activate_btn.clicked.connect(self.activate_license)
        btn_layout.addWidget(activate_btn)
        
        purchase_btn = QPushButton("Purchase License")
        purchase_btn.clicked.connect(self.purchase_license)
        btn_layout.addWidget(purchase_btn)
        
        activation_layout.addLayout(btn_layout)
        layout.addWidget(activation_frame)
        
        # Add close button
        close_btn = QPushButton("Close")
        close_btn.clicked.connect(self.close)
        layout.addWidget(close_btn)
        
        # Initial status check
        self.check_status()

    def check_status(self):
        if self.validator:
            is_valid, message = self.validator.validate_license()
            self.status_label.setText(f"License Status: {message}")

    def activate_license(self):
        if not self.validator:
            return
            
        key = self.key_input.text().strip()
        if not key:
            QMessageBox.warning(self, "Error", "Please enter a license key")
            return
            
        success, message = self.validator.activate_license(key)
        if success:
            QMessageBox.information(self, "Success", message)
            self.check_status()
            self.key_input.clear()
        else:
            QMessageBox.warning(self, "Error", message)

    def purchase_license(self):
        webbrowser.open("https://your-purchase-url.com") 