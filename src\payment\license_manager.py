import json
from pathlib import Path
from datetime import datetime, timedelta

class LicenseManager:
    def __init__(self):
        self.app_data_dir = Path.home() / '.tiktok_backup'
        self.app_data_dir.mkdir(exist_ok=True)
        self.license_file = self.app_data_dir / 'license.json'
        
    def save_license(self, key, expiry_date=None):
        """Save license information to file"""
        license_data = {
            'key': key,
            'activation_date': datetime.now().isoformat(),
            'expiry_date': expiry_date.isoformat() if expiry_date else None
        }
        
        with open(self.license_file, 'w') as f:
            json.dump(license_data, f)
            
    def check_license(self):
        """Check current license status"""
        if not self.license_file.exists():
            return {"status": "unlicensed"}
            
        try:
            with open(self.license_file, 'r') as f:
                license_data = json.load(f)
                
            if not license_data.get('expiry_date'):
                return {"status": "licensed"}
                
            expiry_date = datetime.fromisoformat(license_data['expiry_date'])
            if expiry_date > datetime.now():
                days_left = (expiry_date - datetime.now()).days
                return {"status": "trial", "days_left": days_left}
            else:
                return {"status": "expired"}
                
        except Exception as e:
            print(f"Error checking license: {e}")
            return {"status": "error"} 