#!/usr/bin/env python3
"""
Simple test script to verify database models and connections
"""
import sys
from pathlib import Path

# Add backend to Python path
sys.path.insert(0, str(Path(__file__).parent))

from utils.database import get_db_session, DatabaseManager
from models.database_models import History, PhrasalVerb


def test_database_connection():
    """Test basic database connection"""
    print("Testing database connection...")
    
    try:
        health = DatabaseManager.health_check()
        if health:
            print("✅ Database connection successful")
            
            info = DatabaseManager.get_connection_info()
            print(f"   Connection info: {info}")
        else:
            print("❌ Database connection failed")
            return False
            
    except Exception as e:
        print(f"❌ Database connection error: {e}")
        return False
    
    return True


def test_models():
    """Test database models"""
    print("\nTesting database models...")
    
    try:
        with get_db_session() as db:
            # Test History model
            history = History(
                section='vocabulary',
                query='test word',
                result='palabra de prueba',
                explanation='This is a test',
                examples=['Test example 1', 'Test example 2'],
                tags=['test', 'vocabulary']
            )
            
            # Test PhrasalVerb model
            phrasal_verb = PhrasalVerb(
                verb='test out',
                definition='To try or examine something',
                examples=['Let\'s test out this new feature'],
                difficulty='beginner',
                status='pending'
            )
            
            print("✅ Model creation successful")
            print(f"   History: {history}")
            print(f"   PhrasalVerb: {phrasal_verb}")
            
            # Test serialization
            history_dict = history.to_dict()
            pv_dict = phrasal_verb.to_dict()
            
            print("✅ Model serialization successful")
            print(f"   History dict keys: {list(history_dict.keys())}")
            print(f"   PhrasalVerb dict keys: {list(pv_dict.keys())}")
            
    except Exception as e:
        print(f"❌ Model test error: {e}")
        return False
    
    return True


def main():
    """Run all tests"""
    print("🧪 Running database tests...\n")
    
    # Test connection
    if not test_database_connection():
        sys.exit(1)
    
    # Test models
    if not test_models():
        sys.exit(1)
    
    print("\n✅ All tests passed!")


if __name__ == "__main__":
    main()