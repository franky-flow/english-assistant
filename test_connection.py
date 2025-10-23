#!/usr/bin/env python3
"""
Test script to check backend connectivity
"""
import requests
import json

def test_backend_connection():
    """Test if backend is accessible"""
    base_url = "http://localhost:8000"
    
    print("🔍 Testing Backend Connection...")
    print(f"Base URL: {base_url}")
    print()
    
    # Test health endpoint
    try:
        print("Testing health endpoint...")
        response = requests.get(f"{base_url}/health", timeout=5)
        if response.status_code == 200:
            print("✅ Health check passed")
            print(f"   Response: {response.json()}")
        else:
            print(f"❌ Health check failed: {response.status_code}")
            print(f"   Response: {response.text}")
    except requests.exceptions.ConnectionError:
        print("❌ Connection refused - Backend not running on port 8000")
        return False
    except requests.exceptions.Timeout:
        print("❌ Connection timeout")
        return False
    except Exception as e:
        print(f"❌ Unexpected error: {e}")
        return False
    
    # Test API root
    try:
        print("\nTesting API root...")
        response = requests.get(f"{base_url}/api/", timeout=5)
        if response.status_code == 200:
            print("✅ API root accessible")
            print(f"   Response: {response.json()}")
        else:
            print(f"❌ API root failed: {response.status_code}")
    except Exception as e:
        print(f"❌ API root error: {e}")
    
    # Test CORS
    try:
        print("\nTesting CORS...")
        headers = {
            'Origin': 'http://localhost:3000',
            'Access-Control-Request-Method': 'GET'
        }
        response = requests.options(f"{base_url}/api/", headers=headers, timeout=5)
        print(f"   CORS preflight status: {response.status_code}")
        print(f"   CORS headers: {dict(response.headers)}")
    except Exception as e:
        print(f"❌ CORS test error: {e}")
    
    return True

def check_ports():
    """Check if ports are in use"""
    import socket
    
    print("\n🔍 Checking Port Status...")
    
    ports = [8000, 3000]
    for port in ports:
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.settimeout(1)
        result = sock.connect_ex(('localhost', port))
        sock.close()
        
        if result == 0:
            print(f"✅ Port {port} is in use")
        else:
            print(f"❌ Port {port} is not in use")

if __name__ == "__main__":
    check_ports()
    print()
    test_backend_connection()