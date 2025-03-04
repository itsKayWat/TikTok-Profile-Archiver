from PySide6.QtWidgets import *
from PySide6.QtCore import Qt, Signal
import webbrowser

class ActivationWizard(QWizard):
    """
    License activation wizard shown on first launch
    """
    activation_complete = Signal(bool)  # Emits True if activation successful

    def __init__(self, theme=None, trial_manager=None):
        super().__init__()
        self.theme = theme
        self.trial_manager = trial_manager
        if not self.trial_manager:
            raise ValueError("Trial manager is required")
        self.setup_ui()

    def setup_ui(self):
        """Set up the wizard UI"""
        self.setWindowTitle("Product Activation")
        self.setWizardStyle(QWizard.ModernStyle)
        
        # Set button text
        self.setButtonText(QWizard.NextButton, "Next >")
        self.setButtonText(QWizard.BackButton, "< Back")
        self.setButtonText(QWizard.CancelButton, "Cancel")
        self.setButtonText(QWizard.FinishButton, "Finish")
        
        # Add pages
        self.addPage(self.create_welcome_page())
        self.addPage(self.create_license_page())
        self.addPage(self.create_activation_page())
        
        # Set window size
        self.setMinimumSize(600, 400)

    def create_welcome_page(self):
        page = QWizardPage()
        page.setTitle("Welcome")
        
        layout = QVBoxLayout()
        layout.setSpacing(20)
        
        title = QLabel("Welcome to Product Activation!")
        title.setStyleSheet("""
            font-size: 24px;
            color: #4ADE80;
            font-weight: bold;
            margin-bottom: 20px;
        """)
        layout.addWidget(title)
        
        desc = QLabel(
            "This wizard will help you activate your product.\n"
            "You can choose one of the following options:"
        )
        desc.setWordWrap(True)
        layout.addWidget(desc)
        
        options = QLabel(
            "• Start a free trial (7 days)\n"
            "• Activate with a license key\n"
            "• Purchase a license"
        )
        layout.addWidget(options)
        
        layout.addStretch()
        page.setLayout(layout)
        return page

    def create_license_page(self):
        page = QWizardPage()
        page.setTitle("Choose Activation Method")
        
        layout = QVBoxLayout()
        
        # Radio button group
        group_box = QGroupBox("Select Activation Method")
        group_layout = QVBoxLayout()
        
        # Trial option
        self.trial_radio = QRadioButton("Start Free Trial (7 days)")
        self.trial_radio.setChecked(True)
        self.trial_radio.clicked.connect(self.update_license_page)
        group_layout.addWidget(self.trial_radio)
        
        # License option
        self.license_radio = QRadioButton("Activate with License Key")
        self.license_radio.clicked.connect(self.update_license_page)
        group_layout.addWidget(self.license_radio)
        
        group_box.setLayout(group_layout)
        layout.addWidget(group_box)
        
        # License key input
        self.key_frame = QFrame()
        key_layout = QVBoxLayout(self.key_frame)
        
        key_label = QLabel("License Key:")
        key_layout.addWidget(key_label)
        
        self.key_input = QLineEdit()
        self.key_input.setPlaceholderText("Enter your license key")
        self.key_input.setEnabled(False)
        key_layout.addWidget(self.key_input)
        
        layout.addWidget(self.key_frame)
        
        # Purchase button
        purchase_btn = QPushButton("Purchase License")
        purchase_btn.clicked.connect(
            lambda: webbrowser.open("https://your-purchase-url.com")
        )
        layout.addWidget(purchase_btn)
        
        page.setLayout(layout)
        return page

    def create_activation_page(self):
        page = QWizardPage()
        page.setTitle("Completing Activation")
        
        layout = QVBoxLayout()
        
        self.status_label = QLabel()
        self.status_label.setWordWrap(True)
        layout.addWidget(self.status_label)
        
        page.setLayout(layout)
        return page

    def validateCurrentPage(self):
        if self.currentPage() == self.page(1):  # License page
            if self.license_radio.isChecked():
                key = self.key_input.text().strip()
                if not key:
                    QMessageBox.warning(self, "Error", "Please enter a license key")
                    return False
                    
                # Implement your license key validation here
                return False
                
            else:  # Trial mode
                if self.trial_manager.start_trial():
                    self.status_label.setText("Trial activated successfully!\n\nYour 7-day trial period has started.")
                    self.activation_complete.emit(True)
                    return True
                else:
                    QMessageBox.warning(
                        self,
                        "Trial Error",
                        "Unable to start trial. Please try again or contact support."
                    )
                    return False
                    
        return True

    def update_license_page(self):
        self.key_input.setEnabled(self.license_radio.isChecked()) 