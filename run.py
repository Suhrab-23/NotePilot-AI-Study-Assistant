"""
NotePilot - One-command run script
"""
import os
import subprocess
import sys

def check_ollama():
    """Check if Ollama is running."""
    try:
        import requests
        response = requests.get('http://localhost:11434/api/tags', timeout=2)
        return response.status_code == 200
    except:
        return False

def main():
    print("=" * 70)
    print("NotePilot - AI Study Assistant")
    print("=" * 70)
    print()
    
    # Check if Ollama is running
    print("[1/3] Checking Ollama...")
    if not check_ollama():
        print("❌ Ollama is not running!")
        print("   Please start Ollama first:")
        print("   - Open a new terminal")
        print("   - Run: ollama serve")
        print()
        sys.exit(1)
    print("✓ Ollama is running")
    print()
    
    # Check dependencies
    print("[2/3] Checking dependencies...")
    try:
        import flask
        import PyPDF2
        import sentence_transformers
        import faiss
        print("✓ All dependencies installed")
    except ImportError as e:
        print(f"❌ Missing dependency: {e.name}")
        print("   Installing dependencies...")
        subprocess.check_call([sys.executable, '-m', 'pip', 'install', '-r', 'requirements.txt'])
        print("✓ Dependencies installed")
    print()
    
    # Create required directories
    os.makedirs('uploads', exist_ok=True)
    os.makedirs('logs', exist_ok=True)
    
    # Start Flask app
    print("[3/3] Starting NotePilot...")
    print()
    print("=" * 70)
    print("🚀 NotePilot is running!")
    print("   Open your browser and navigate to: http://localhost:5000")
    print("   Press Ctrl+C to stop the server")
    print("=" * 70)
    print()
    
    from app import app
    app.run(debug=False, host='0.0.0.0', port=5000)

if __name__ == '__main__':
    main()
