from datetime import datetime, timedelta
import json
import os
import platform
import uuid
import hashlib

class TrialManager:
    def __init__(self, trial_file="trial_info.json"):
        self.trial_file = trial_file
        self.trial_duration = 7  # days
        self._load_trial_info()

    def _load_trial_info(self):
        if os.path.exists(self.trial_file):
            try:
                with open(self.trial_file, 'r') as f:
                    self.trial_info = json.load(f)
            except:
                self.trial_info = {}
        else:
            self.trial_info = {}

    def _save_trial_info(self):
        with open(self.trial_file, 'w') as f:
            json.dump(self.trial_info, f)

    def _get_device_info(self):
        system = platform.system()
        release = platform.release()
        machine = platform.machine()
        processor = platform.processor()
        
        # Create unique device ID
        device_id = f"{system}-{release}-{machine}-{processor}"
        device_id = hashlib.sha256(device_id.encode()).hexdigest()
        
        return {
            "system": system,
            "release": release,
            "machine": machine,
            "processor": processor,
            "device_id": device_id
        }

    def start_trial(self) -> bool:
        if self.is_valid():
            return True
            
        now = datetime.now()
        self.trial_info = {
            "start_date": now.isoformat(),
            "end_date": (now + timedelta(days=self.trial_duration)).isoformat(),
            "device_info": self._get_device_info()
        }
        self._save_trial_info()
        return True

    def is_valid(self) -> bool:
        if not self.trial_info:
            return False
            
        try:
            end_date = datetime.fromisoformat(self.trial_info["end_date"])
            return datetime.now() <= end_date
        except:
            return False

    def days_remaining(self) -> int:
        if not self.is_valid():
            return 0
            
        end_date = datetime.fromisoformat(self.trial_info["end_date"])
        remaining = end_date - datetime.now()
        return max(0, remaining.days)

    def get_trial_info(self) -> dict:
        return self.trial_info 