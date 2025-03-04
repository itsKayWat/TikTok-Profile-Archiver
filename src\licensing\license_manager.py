import os
import json
from datetime import datetime

class LicenseManager:
    def __init__(self):
        self.app_data_dir = os.path.join(os.path.expanduser('~'), '.tiktok_backup')
        os.makedirs(self.app_data_dir, exist_ok=True)
        self.license_file = os.path.join(self.app_data_dir, 'license.json')
        self.trial_file = os.path.join(self.app_data_dir, 'trial.json')
        
    def check_license_status(self):
        """Check current license status"""
        # Check for full license
        if os.path.exists(self.license_file):
            try:
                with open(self.license_file, 'r') as f:
                    license_data = json.load(f)
                return {
                    'status': 'licensed',
                    'key': license_data.get('key'),
                    'activation_date': license_data.get('activation_date')
                }
            except:
                pass
                
        # Check for trial
        if os.path.exists(self.trial_file):
            try:
                with open(self.trial_file, 'r') as f:
                    trial_data = json.load(f)
                    end_date = datetime.fromisoformat(trial_data['end_date'])
                    if datetime.now() < end_date:
                        days_left = (end_date - datetime.now()).days
                        return {
                            'status': 'trial',
                            'days_left': days_left,
                            'end_date': trial_data['end_date']
                        }
            except:
                pass
                
        return {'status': 'unlicensed'} 