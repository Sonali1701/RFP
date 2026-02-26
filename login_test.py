#!/usr/bin/env python3
"""
Auto-Login Test Script for RFP Automation Platform
Creates a test user account automatically for frontend login
"""

import requests
import json
import time
import sys

# Configuration
API_BASE_URL = "http://localhost:8000/api/v1"
TEST_USER = {
    "email": "test@rfp.com",
    "password": "test123456",
    "full_name": "Test User",
    "role": "admin"
}

def check_backend_health():
    """Check if backend is running"""
    try:
        response = requests.get("http://localhost:8000/health", timeout=5)
        if response.status_code == 200:
            print("✅ Backend is running")
            print(f"📊 Backend response: {response.json()}")
            return True
        else:
            print(f"❌ Backend returned status: {response.status_code}")
            return False
    except requests.exceptions.RequestException as e:
        print(f"❌ Cannot connect to backend: {e}")
        print("💡 Make sure backend is running: python main.py backend")
        return False

def create_test_user():
    """Create test user account"""
    try:
        print(f"🔧 Creating test user: {TEST_USER['email']}")
        
        response = requests.post(
            f"{API_BASE_URL}/auth/register",
            json=TEST_USER,
            headers={"Content-Type": "application/json"},
            timeout=10
        )
        
        if response.status_code == 200:
            user_data = response.json()
            print("✅ Test user created successfully!")
            print(f"📧 Email: {TEST_USER['email']}")
            print(f"🔑 Password: {TEST_USER['password']}")
            print(f"👤 User ID: {user_data.get('id', 'N/A')}")
            return True
        else:
            print(f"❌ Failed to create user: {response.status_code}")
            print(f"📄 Response: {response.text}")
            return False
            
    except requests.exceptions.RequestException as e:
        print(f"❌ Network error: {e}")
        return False

def test_login():
    """Test login with created user"""
    try:
        print(f"🔐 Testing login...")
        
        login_data = {
            "email": TEST_USER["email"],
            "password": TEST_USER["password"]
        }
        
        response = requests.post(
            f"{API_BASE_URL}/auth/login",
            json=login_data,
            headers={"Content-Type": "application/json"},
            timeout=10
        )
        
        if response.status_code == 200:
            token_data = response.json()
            print("✅ Login successful!")
            print(f"🎫 Access Token: {token_data.get('access_token', 'N/A')[:50]}...")
            print(f"👤 User: {token_data.get('user', {}).get('email', 'N/A')}")
            return True
        else:
            print(f"❌ Login failed: {response.status_code}")
            print(f"📄 Response: {response.text}")
            return False
            
    except requests.exceptions.RequestException as e:
        print(f"❌ Network error: {e}")
        return False

def show_frontend_info():
    """Show frontend login information"""
    print("\n" + "="*60)
    print("🌐 FRONTEND LOGIN INFORMATION")
    print("="*60)
    print(f"📱 Frontend URL: http://localhost:8501")
    print(f"📧 Email: {TEST_USER['email']}")
    print(f"🔑 Password: {TEST_USER['password']}")
    print(f"👤 Role: {TEST_USER['role']}")
    print("\n📋 STEPS:")
    print("1. Open http://localhost:8501 in browser")
    print("2. Click 'Login' button")
    print("3. Enter email and password above")
    print("4. Click 'Sign In'")
    print("5. You're now logged in! 🎉")
    print("\n💡 TIP: Keep this script running for reference")
    print("="*60)

def main():
    """Main function"""
    print("🚀 RFP Platform - Auto Login Test (Testing Mode)")
    print("="*55)
    
    # Check if backend is running
    if not check_backend_health():
        sys.exit(1)
    
    # Wait a moment for backend to be fully ready
    time.sleep(1)
    
    # Create test user (simulated for testing mode)
    if not create_test_user():
        print("❌ Failed to create test user")
        sys.exit(1)
    
    # Test login (simulated for testing mode)
    if not test_login():
        print("❌ Failed to login")
        sys.exit(1)
    
    # Show frontend info
    show_frontend_info()
    
    print("\n🎯 SUCCESS! You can now login to frontend!")
    print("💾 Save these credentials for future use")

if __name__ == "__main__":
    main()
