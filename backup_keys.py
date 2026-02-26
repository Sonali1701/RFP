#!/usr/bin/env python3
"""
Backup your real API keys before committing to Git
Run this script to save your actual API keys to a local backup file
"""

import os
import shutil
from datetime import datetime

def backup_api_keys():
    """Backup real API keys from .env file"""
    
    # Read current .env file
    env_file = '.env'
    backup_file = f'.env.backup.{datetime.now().strftime("%Y%m%d_%H%M%S")}'
    
    if os.path.exists(env_file):
        # Create backup
        shutil.copy2(env_file, backup_file)
        print(f"[SUCCESS] API keys backed up to: {backup_file}")
        
        # Show what was backed up (without showing actual keys)
        with open(env_file, 'r') as f:
            lines = f.readlines()
            
        print("\n[INFO] Backed up configuration:")
        for line in lines:
            if '=' in line and not line.startswith('#'):
                key, value = line.split('=', 1)
                if any(api_key in key.upper() for api_key in ['KEY', 'SECRET', 'PASSWORD', 'TOKEN']):
                    print(f"  {key.strip()} = {'*' * len(value.strip())}")
                else:
                    print(f"  {key.strip()} = {value.strip()}")
        
        print(f"\n[SECURITY] Keep this backup file safe and local!")
        print(f"   Do NOT commit {backup_file} to Git!")
        
    else:
        print(f"[ERROR] {env_file} not found")

if __name__ == "__main__":
    backup_api_keys()
