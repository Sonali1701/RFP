#!/usr/bin/env python3
"""
Agentic AI RFP Automation Platform

A comprehensive platform for automating Request for Proposal (RFP) processes
through AI-driven document parsing, intelligent response generation, and
workflow automation.

Author: AI Assistant
Version: 1.0.0
"""

import sys
import os
import argparse
from pathlib import Path

# Add the project root to Python path
project_root = Path(__file__).parent
sys.path.insert(0, str(project_root))

def run_backend():
    """Run the FastAPI backend server"""
    import uvicorn
    from backend.core.config import settings
    
    if settings.testing_mode:
        # Use simple backend for testing mode
        from backend.main_simple import app
        app_module = "backend.main_simple:app"
        print("TESTING MODE: Using Memory Storage")
    else:
        # Use full backend for production
        from backend.main import app
        app_module = "backend.main:app"
        print("PRODUCTION MODE: Using Database Storage")
    
    print("Starting RFP Automation Platform Backend...")
    print("API Documentation: http://localhost:8000/docs")
    print("Health Check: http://localhost:8000/health")
    print("ReDoc: http://localhost:8000/redoc")
    
    uvicorn.run(
        app_module,
        host="0.0.0.0",
        port=8000,
        reload=True,
        log_level="info"
    )

def run_frontend():
    """Run the Streamlit frontend dashboard"""
    import subprocess
    
    print("🎨 Starting RFP Automation Platform Frontend...")
    print("📍 Dashboard: http://localhost:8501")
    
    subprocess.run([
        "streamlit", "run", 
        "frontend/dashboard.py",
        "--server.port", "8501",
        "--server.address", "0.0.0.0"
    ])

def setup_database():
    """Set up the database with migrations"""
    import subprocess
    import sys
    
    print("🗄️ Setting up database...")
    
    # Change to database directory
    os.chdir("database")
    
    try:
        # Initialize Alembic if not already done
        if not os.path.exists("migrations/versions"):
            subprocess.run([sys.executable, "-m", "alembic", "init", "migrations"], check=True)
        
        # Create initial migration
        subprocess.run([sys.executable, "-m", "alembic", "revision", "--autogenerate", "-m", "Initial schema"], check=True)
        
        # Apply migrations
        subprocess.run([sys.executable, "-m", "alembic", "upgrade", "head"], check=True)
        
        print("✅ Database setup completed successfully!")
        
    except subprocess.CalledProcessError as e:
        print(f"❌ Database setup failed: {e}")
        sys.exit(1)
    finally:
        # Return to project root
        os.chdir("..")

def run_tests():
    """Run the test suite"""
    import subprocess
    
    print("🧪 Running test suite...")
    
    try:
        # Run pytest with coverage
        subprocess.run([
            sys.executable, "-m", "pytest", 
            "tests/",
            "-v",
            "--cov=backend",
            "--cov-report=html",
            "--cov-report=term-missing"
        ], check=True)
        
        print("✅ All tests passed!")
        
    except subprocess.CalledProcessError as e:
        print(f"❌ Tests failed: {e}")
        sys.exit(1)

def install_dependencies():
    """Install project dependencies"""
    import subprocess
    
    print("📦 Installing dependencies...")
    
    try:
        subprocess.run([
            sys.executable, "-m", "pip", "install", "-r", "requirements.txt"
        ], check=True)
        
        print("✅ Dependencies installed successfully!")
        
    except subprocess.CalledProcessError as e:
        print(f"❌ Failed to install dependencies: {e}")
        sys.exit(1)

def create_env_file():
    """Create .env file from template"""
    env_example = ".env"
    env_file = ".env"
    
    if os.path.exists(env_file):
        print("⚠️ .env file already exists!")
        return
    
    if os.path.exists(env_example):
        import shutil
        shutil.copy(env_example, env_file)
        print("✅ Created .env file from template")
        print("📝 Please edit .env file with your configuration")
    else:
        print("❌ .env file not found!")
        sys.exit(1)

def show_help():
    """Show help information"""
    help_text = """
🤖 Agentic AI RFP Automation Platform

Usage: python main.py [COMMAND]

Commands:
    backend         Run the FastAPI backend server
    frontend        Run the Streamlit frontend dashboard
    setup           Set up the database and run migrations
    test            Run the test suite
    install         Install project dependencies
    env             Create .env file from template
    help            Show this help message

Examples:
    python main.py setup          # Set up database
    python main.py env            # Create .env file
    python main.py backend         # Start backend server
    python main.py frontend        # Start frontend dashboard
    python main.py test            # Run tests

Development Workflow:
    1. python main.py env         # Create .env file
    2. python main.py install      # Install dependencies
    3. python main.py setup        # Set up database
    4. python main.py backend       # Start backend (in terminal 1)
    5. python main.py frontend      # Start frontend (in terminal 2)

Configuration:
    - Edit .env file for database and API keys
    - Ensure PostgreSQL is running
    - Configure OpenAI/Anthropic API keys for AI features

For more information, see README.md
    """
    print(help_text)

def main():
    """Main entry point"""
    parser = argparse.ArgumentParser(
        description="Agentic AI RFP Automation Platform",
        add_help=False
    )
    
    parser.add_argument(
        "command",
        choices=["backend", "frontend", "setup", "test", "install", "env", "help"],
        help="Command to run"
    )
    
    args = parser.parse_args()
    
    if args.command == "backend":
        run_backend()
    elif args.command == "frontend":
        run_frontend()
    elif args.command == "setup":
        setup_database()
    elif args.command == "test":
        run_tests()
    elif args.command == "install":
        install_dependencies()
    elif args.command == "env":
        create_env_file()
    elif args.command == "help":
        show_help()
    else:
        show_help()

if __name__ == "__main__":
    main()
