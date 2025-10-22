#!/usr/bin/env python3
"""
Test script to verify agent implementations
"""
import sys
import os

# Add backend to path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

def test_imports():
    """Test that all agents can be imported"""
    try:
        from agents import VocabularyAgent, CorrectionAgent, GrammarAgent, PhrasalVerbAgent
        from utils import get_model_manager
        
        print("✅ All agent imports successful")
        
        # Test agent initialization
        vocab_agent = VocabularyAgent()
        correction_agent = CorrectionAgent()
        grammar_agent = GrammarAgent()
        phrasal_verb_agent = PhrasalVerbAgent()
        
        print("✅ All agents initialized successfully")
        
        # Test model manager
        model_manager = get_model_manager()
        model_info = model_manager.get_model_info()
        print(f"✅ Model manager initialized with {model_info['total_models']} models")
        
        return True
        
    except Exception as e:
        print(f"❌ Import/initialization failed: {e}")
        return False

def test_agent_health_checks():
    """Test agent health checks"""
    try:
        from agents import VocabularyAgent, CorrectionAgent, GrammarAgent, PhrasalVerbAgent
        
        agents = {
            "VocabularyAgent": VocabularyAgent(),
            "CorrectionAgent": CorrectionAgent(),
            "GrammarAgent": GrammarAgent(),
            "PhrasalVerbAgent": PhrasalVerbAgent()
        }
        
        for name, agent in agents.items():
            health = agent.health_check()
            status = health.get("status", "unknown")
            print(f"✅ {name} health check: {status}")
        
        return True
        
    except Exception as e:
        print(f"❌ Health check failed: {e}")
        return False

if __name__ == "__main__":
    print("🧪 Testing English Assistant Agents...")
    print()
    
    success = True
    
    print("1. Testing imports and initialization...")
    success &= test_imports()
    print()
    
    print("2. Testing agent health checks...")
    success &= test_agent_health_checks()
    print()
    
    if success:
        print("🎉 All tests passed!")
    else:
        print("💥 Some tests failed!")
        sys.exit(1)