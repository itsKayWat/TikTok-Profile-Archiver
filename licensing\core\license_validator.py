from PySide6.QtCore import QObject, Signal

class LicenseValidator(QObject):
    license_valid = Signal(bool, str)  # Emits (is_valid, message)
    license_error = Signal(str)  # Emits error messages

    def __init__(self):
        super().__init__()
        self.valid_licenses = set()  # Store valid license keys

    def validate_license(self) -> tuple[bool, str]:
        """Validate current license"""
        # Implement your license validation logic here
        return True, "Trial Mode"

    def activate_license(self, key: str) -> tuple[bool, str]:
        """Activate a new license"""
        if key in self.valid_licenses:
            return True, "License activated successfully"
        return False, "Invalid license key" 