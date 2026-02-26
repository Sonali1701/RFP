#!/usr/bin/env python3
"""
Restore your real API keys from backup
Run this script to restore your actual API keys from a backup file
"""

import os
import shutil
from datetime import datetime

def list_backups():
    """List all available backup files"""
    backups = []
    for file in os.listdir('.'):
        if file.startswith('.env.backup.'):
            backups.append(file)
    
    backups.sort(reverse=True)  # Most recent first
    return backups

def restore_api_keys(backup_file=None):
    """Restore API keys from backup file"""
    
    backups = list_backups()
    
    if not backups:
        print("[ERROR] No backup files found!")
        return
    
    if backup_file is None:
        print("\n[INFO] Available backup files:")
        for i, backup in enumerate(backups, 1):
            print(f"  {i}. {backup}")
        
        try:
            choice = int(input(f"\n[INPUT] Enter backup number (1-{len(backups)}): ")) - 1
            if 0 <= choice < len(backups):
                backup_file = backups[choice]
            else:
                print("[ERROR] Invalid choice!")
                return
        except ValueError:
            print("[ERROR] Please enter a valid number!")
            return
    
    if not os.path.exists(backup_file):
        print(f"[ERROR] Backup file {backup_file} not found!")
        return
    
    # Create current .env backup before restoring
    if os.path.exists('.env'):
        current_backup = f'.env.before_restore.{datetime.now().strftime("%Y%m%d_%H%M%S")}'
        shutil.copy2('.env', current_backup)
        print(f"[INFO] Current .env backed up to: {current_backup}")
    
    # Restore from backup
    shutil.copy2(backup_file, '.env')
    print(f"[SUCCESS] API keys restored from: {backup_file}")
    
    # Show what was restored (without showing actual keys)
    with open('.env', 'r') as f:
        lines = f.readlines()
    
    print("\n[INFO] Restored configuration:")
    for line in lines:
        if '=' in line and not line.startswith('#'):
            key, value = line.split('=', 1)
            if any(api_key in key.upper() for api_key in ['KEY', 'SECRET', 'PASSWORD', 'TOKEN']):
                print(f"  {key.strip()} = {'*' * len(value.strip())}")
            else:
                print(f"  {key.strip()} = {value.strip()}")

if __name__ == "__main__":
    restore_api_keys()
