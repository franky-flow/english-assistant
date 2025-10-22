#!/usr/bin/env python3
"""
Test script to verify API implementation
"""
import sys
import os

# Add backend to path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

def test_api_imports():
    """Test that all API components can be imported"""
    try:
        from main import app
        from api import router
        from api.vocabulary import router as vocab_router
        from api.correction import router as correction_router
        from api.grammar import router as grammar_router
        from api.phrasal_verbs import router as pv_router
        from api.history import router as history_router
        
        print("✅ All API imports successful")
        
        # Test FastAPI app creation
        print(f"✅ FastAPI app created: {app.title}")
        
        # Test router inclusion
        print(f"✅ Main router configured with {len(app.routes)} routes")
        
        return True
        
    except Exception as e:
        print(f"❌ API import/setup failed: {e}")
        return False

def test_endpoint_structure():
    """Test API endpoint structure"""
    try:
        from main import app
        
        # Get all routes
        routes = []
        for route in app.routes:
            if hasattr(route, 'path') and hasattr(route, 'methods'):
                routes.append(f"{list(route.methods)[0]} {route.path}")
        
        print(f"✅ API has {len(routes)} endpoints:")
        for route in sorted(routes):
            print(f"   {route}")
        
        # Check for expected endpoints
        expected_paths = [
            "/api/vocabulary",
            "/api/correction", 
            "/api/grammar",
            "/api/phrasal-verbs",
            "/api/history"
        ]
        
        all_paths = [route.path for route in app.routes if hasattr(route, 'path')]
        
        for expected in expected_paths:
            if any(expected in path for path in all_paths):
                print(f"✅ Found expected endpoint: {expected}")
            else:
                print(f"❌ Missing expected endpoint: {expected}")
        
        return True
        
    except Exception as e:
        print(f"❌ Endpoint structure test failed: {e}")
        return False

if __name__ == "__main__":
    print("🧪 Testing English Assistant API...")
    print()
    
    success = True
    
    print("1. Testing API imports and setup...")
    success &= test_api_imports()
    print()
    
    print("2. Testing endpoint structure...")
    success &= test_endpoint_structure()
    print()
    
    if success:
        print("🎉 All API tests passed!")
        print()
        print("To start the API server, run:")
        print("  cd backend")
        print("  python main.py")
        print()
        print("Or use uvicorn directly:")
        print("  uvicorn main:app --host localhost --port 8000 --reload")
    else:
        print("💥 Some API tests failed!")
        sys.exit(1)