"""
Test script for Docker container setup
"""

import os
import requests
import time
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

def test_docker_setup():
    """Test the Docker container setup"""
    print("🐳 Testing Docker Container Setup...")
    
    # Test health endpoint
    print("🔍 Testing health endpoint...")
    try:
        response = requests.get("http://localhost:5000/health", timeout=10)
        if response.status_code == 200:
            data = response.json()
            print(f"✅ Health check passed: {data}")
        else:
            print(f"❌ Health check failed: {response.status_code}")
    except Exception as e:
        print(f"❌ Health check error: {e}")
    
    # Test home endpoint
    print("\n🏠 Testing home endpoint...")
    try:
        response = requests.get("http://localhost:5000/", timeout=10)
        if response.status_code == 200:
            data = response.json()
            print(f"✅ Home endpoint: {data}")
        else:
            print(f"❌ Home endpoint failed: {response.status_code}")
    except Exception as e:
        print(f"❌ Home endpoint error: {e}")
    
    # Test Ollama connection
    print("\n🤖 Testing Ollama connection...")
    try:
        response = requests.get("http://localhost:11434/api/tags", timeout=10)
        if response.status_code == 200:
            print("✅ Ollama is running")
        else:
            print(f"❌ Ollama connection failed: {response.status_code}")
    except Exception as e:
        print(f"❌ Ollama connection error: {e}")
    
    print("\n✨ Docker setup test completed!")

if __name__ == "__main__":
    test_docker_setup()
