"""
Simple test to debug import issues
"""

import sys
import os
from pathlib import Path

# Add project root to Python path
project_root = Path(__file__).parent
sys.path.insert(0, str(project_root))

print("Project root:", project_root)
print("Python path:", sys.path[:3])

try:
    print("Testing import of backend.main_simple...")
    from backend.main_simple import app
    print("✅ Successfully imported backend.main_simple")
except Exception as e:
    print(f"❌ Error importing backend.main_simple: {e}")
    print(f"Error type: {type(e)}")

try:
    print("Testing import of backend.services...")
    from backend.services import ai_integration_service
    print("✅ Successfully imported backend.services")
except Exception as e:
    print(f"❌ Error importing backend.services: {e}")
    print(f"Error type: {type(e)}")

try:
    print("Testing direct import...")
    import backend.main_simple
    print("✅ Successfully imported directly")
except Exception as e:
    print(f"❌ Error direct import: {e}")
    print(f"Error type: {type(e)}")
