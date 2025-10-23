#!/usr/bin/env python3
"""
Test API requests to debug 422 errors
"""
import requests
import json

def test_vocabulary_api():
    """Test vocabulary API endpoint"""
    url = "http://localhost:8000/api/vocabulary"
    
    # Test data
    data = {
        "query": "hello",
        "source_language": "en",
        "target_language": "es"
    }
    
    print("🔍 Testing Vocabulary API...")
    print(f"URL: {url}")
    print(f"Data: {json.dumps(data, indent=2)}")
    
    try:
        response = requests.post(url, json=data, timeout=10)
        print(f"Status: {response.status_code}")
        print(f"Response: {response.text}")
        
        if response.status_code == 422:
            print("❌ Validation error (422)")
            try:
                error_detail = response.json()
                print(f"Error details: {json.dumps(error_detail, indent=2)}")
            except:
                pass
        elif response.status_code == 200:
            print("✅ Success!")
        else:
            print(f"❌ Unexpected status: {response.status_code}")
            
    except Exception as e:
        print(f"❌ Request failed: {e}")

def test_correction_api():
    """Test correction API endpoint"""
    url = "http://localhost:8000/api/correction"
    
    # Test data
    data = {
        "text": "I are going to the store",
        "correction_level": "comprehensive"
    }
    
    print("\n🔍 Testing Correction API...")
    print(f"URL: {url}")
    print(f"Data: {json.dumps(data, indent=2)}")
    
    try:
        response = requests.post(url, json=data, timeout=10)
        print(f"Status: {response.status_code}")
        print(f"Response: {response.text}")
        
        if response.status_code == 422:
            print("❌ Validation error (422)")
            try:
                error_detail = response.json()
                print(f"Error details: {json.dumps(error_detail, indent=2)}")
            except:
                pass
        elif response.status_code == 200:
            print("✅ Success!")
        else:
            print(f"❌ Unexpected status: {response.status_code}")
            
    except Exception as e:
        print(f"❌ Request failed: {e}")

def test_grammar_api():
    """Test grammar API endpoint"""
    url = "http://localhost:8000/api/grammar"
    
    # Test data
    data = {
        "question": "What is the difference between affect and effect?",
        "question_type": "comparison"
    }
    
    print("\n🔍 Testing Grammar API...")
    print(f"URL: {url}")
    print(f"Data: {json.dumps(data, indent=2)}")
    
    try:
        response = requests.post(url, json=data, timeout=10)
        print(f"Status: {response.status_code}")
        print(f"Response: {response.text}")
        
        if response.status_code == 422:
            print("❌ Validation error (422)")
            try:
                error_detail = response.json()
                print(f"Error details: {json.dumps(error_detail, indent=2)}")
            except:
                pass
        elif response.status_code == 200:
            print("✅ Success!")
        else:
            print(f"❌ Unexpected status: {response.status_code}")
            
    except Exception as e:
        print(f"❌ Request failed: {e}")

if __name__ == "__main__":
    test_vocabulary_api()
    test_correction_api()
    test_grammar_api()