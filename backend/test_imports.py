#!/usr/bin/env python3
"""
Test script to verify all imports work correctly
"""
import sys
from pathlib import Path

# Add backend to path
sys.path.insert(0, str(Path(__file__).parent))

def test_imports():
    """Test all critical imports"""
    try:
        print("Testing core imports...")
        
        # Test config
        from config import settings
        print("✅ Config imported")
        
        # Test models
        from models.api_models import VocabularyRequest, VocabularyResponse
        print("✅ API models imported")
        
        # Test utils
        from utils.model_manager import get_model_manager
        from utils.response_formatter import ResponseFormatter
        from utils.error_handler import ErrorHandler
        print("✅ Utils imported")
        
        # Test agents
        from agents.vocabulary_agent import VocabularyAgent
        from agents.correction_agent import CorrectionAgent
        from agents.grammar_agent import GrammarAgent
        from agents.phrasal_verb_agent import PhrasalVerbAgent
        print("✅ Agents imported")
        
        # Test API
        from api.routes import router
        print("✅ API routes imported")
        
        # Test main app
        from main import app
        print("✅ Main app imported")
        
        print("\n🎉 All imports successful!")
        return True
        
    except Exception as e:
        print(f"❌ Import failed: {e}")
        import traceback
        traceback.print_exc()
        return False

if __name__ == "__main__":
    success = test_imports()
    sys.exit(0 if success else 1)