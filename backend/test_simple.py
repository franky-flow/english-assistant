#!/usr/bin/env python3
"""
Simple test script to verify core functionality works
"""
import sys
from pathlib import Path

# Add backend to path
sys.path.insert(0, str(Path(__file__).parent))

def test_core_imports():
    """Test core imports without circular dependencies"""
    try:
        print("Testing core imports...")
        
        # Test config
        from config import settings
        print("✅ Config imported")
        
        # Test API models directly
        from models.api_models import VocabularyRequest, VocabularyResponse
        print("✅ API models imported")
        
        # Test model manager
        from utils.model_manager import get_model_manager
        model_manager = get_model_manager()
        print("✅ Model manager imported")
        
        # Test agents
        from agents.vocabulary_agent import VocabularyAgent
        vocab_agent = VocabularyAgent()
        print("✅ Vocabulary agent imported")
        
        # Test FastAPI app creation
        from fastapi import FastAPI
        app = FastAPI()
        print("✅ FastAPI imported")
        
        print("\n🎉 Core imports successful!")
        print("\n📝 Notes:")
        if model_manager.language_tool is None:
            print("⚠️  LanguageTool not available (Java not installed)")
            print("   Grammar correction will use AI models only")
        else:
            print("✅ LanguageTool available")
            
        return True
        
    except Exception as e:
        print(f"❌ Import failed: {e}")
        import traceback
        traceback.print_exc()
        return False

if __name__ == "__main__":
    success = test_core_imports()
    sys.exit(0 if success else 1)