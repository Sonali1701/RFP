"""
Clean Startup Script for Simple Proposal System
"""

import sys
import os
from pathlib import Path

# Add the project root to Python path
project_root = Path(__file__).parent
sys.path.insert(0, str(project_root))

# Add the backend directory to Python path
backend_dir = project_root / "backend"
sys.path.insert(0, str(backend_dir))

# Change to backend directory
os.chdir(backend_dir)

# Now import and run the clean app
if __name__ == "__main__":
    import uvicorn
    from main_clean import app
    
    print("🚀 Starting Simple Proposal Processing System...")
    print("📍 Current Directory:", os.getcwd())
    print("🐍 Python Path:", sys.path[:3])
    print("📊 API Documentation: http://localhost:8000/docs")
    print("🔍 Health Check: http://localhost:8000/health")
    print("📚 ReDoc: http://localhost:8000/redoc")
    print("=" * 60)
    
    uvicorn.run(
        "main_clean:app",
        host="0.0.0.0",
        port=8000,
        reload=True,
        log_level="info"
    )
