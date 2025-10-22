#!/usr/bin/env python3
"""
Development server script for English Assistant API
"""
import sys
import os
from pathlib import Path

# Add backend to path
sys.path.insert(0, str(Path(__file__).parent))

def main():
    """Run the development server"""
    try:
        import uvicorn
        from config import settings
        
        print("🚀 Starting English Assistant API Server...")
        print(f"   Host: {settings.api_host}")
        print(f"   Port: {settings.api_port}")
        print(f"   Debug: {settings.api_debug}")
        print()
        print("📖 API Documentation:")
        print(f"   Swagger UI: http://{settings.api_host}:{settings.api_port}/docs")
        print(f"   ReDoc: http://{settings.api_host}:{settings.api_port}/redoc")
        print()
        print("🔗 API Endpoints:")
        print(f"   Health: http://{settings.api_host}:{settings.api_port}/health")
        print(f"   Vocabulary: http://{settings.api_host}:{settings.api_port}/api/vocabulary")
        print(f"   Correction: http://{settings.api_host}:{settings.api_port}/api/correction")
        print(f"   Grammar: http://{settings.api_host}:{settings.api_port}/api/grammar")
        print(f"   Phrasal Verbs: http://{settings.api_host}:{settings.api_port}/api/phrasal-verbs")
        print(f"   History: http://{settings.api_host}:{settings.api_port}/api/history")
        print()
        print("Press Ctrl+C to stop the server")
        print("=" * 60)
        
        uvicorn.run(
            "main:app",
            host=settings.api_host,
            port=settings.api_port,
            reload=settings.api_debug,
            log_level=settings.log_level.lower()
        )
        
    except KeyboardInterrupt:
        print("\n👋 Server stopped by user")
    except ImportError as e:
        print(f"❌ Missing dependency: {e}")
        print("Please install required packages:")
        print("  pip install -r requirements.txt")
        sys.exit(1)
    except Exception as e:
        print(f"❌ Server startup failed: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()