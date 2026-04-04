#!/usr/bin/env python3
"""
INTENTRA Configuration Validator
Tests that all dependencies and configuration are correct
"""
import sys
from pathlib import Path

def print_status(msg: str, status: bool):
    """Print colored status message"""
    symbol = "✅" if status else "❌"
    print(f"{symbol} {msg}")

def main():
    print("🔍 Validating INTENTRA Configuration...\n")
    
    all_passed = True
    
    # Test 1: Python version
    print("📋 Checking Python version...")
    if sys.version_info >= (3, 9):
        print_status(f"Python {sys.version_info.major}.{sys.version_info.minor}.{sys.version_info.micro}", True)
    else:
        print_status(f"Python {sys.version_info.major}.{sys.version_info.minor} (requires 3.9+)", False)
        all_passed = False
    print()
    
    # Test 2: Core dependencies
    print("📦 Checking core dependencies...")
    dependencies = [
        ("fastapi", "FastAPI"),
        ("uvicorn", "Uvicorn"),
        ("pydantic", "Pydantic"),
        ("pydantic_settings", "Pydantic Settings"),
    ]
    
    for module, name in dependencies:
        try:
            __import__(module)
            print_status(name, True)
        except ImportError:
            print_status(f"{name} (not installed)", False)
            all_passed = False
    print()
    
    # Test 3: LangChain ecosystem
    print("🤖 Checking LangChain ecosystem...")
    langchain_deps = [
        ("langchain", "LangChain Core"),
        ("langchain_core", "LangChain Core Abstractions"),
        ("langchain_groq", "LangChain Groq"),
        ("langchain_community", "LangChain Community"),
    ]
    
    for module, name in langchain_deps:
        try:
            __import__(module)
            print_status(name, True)
        except ImportError:
            print_status(f"{name} (not installed)", False)
            all_passed = False
    print()
    
    # Test 4: Trading APIs
    print("💹 Checking trading APIs...")
    try:
        import alpaca_trade_api
        print_status("Alpaca Trade API", True)
    except ImportError:
        print_status("Alpaca Trade API (not installed)", False)
        all_passed = False
    print()
    
    # Test 5: Database
    print("🗄️  Checking database...")
    try:
        import sqlalchemy
        print_status("SQLAlchemy", True)
    except ImportError:
        print_status("SQLAlchemy (not installed)", False)
        all_passed = False
    print()
    
    # Test 6: Environment file
    print("⚙️  Checking configuration...")
    env_file = Path(".env")
    if env_file.exists():
        print_status(".env file exists", True)
        
        # Check if it's not just the example
        content = env_file.read_text()
        if "GROQ_API_KEY=" in content and len(content.split("GROQ_API_KEY=")[1].split("\n")[0].strip()) > 0:
            print_status("GROQ_API_KEY is set", True)
        else:
            print_status("GROQ_API_KEY is empty (needs configuration)", False)
            all_passed = False
            
        if "ALPACA_API_KEY=" in content and len(content.split("ALPACA_API_KEY=")[1].split("\n")[0].strip()) > 0:
            print_status("ALPACA_API_KEY is set", True)
        else:
            print_status("ALPACA_API_KEY is empty (needs configuration)", False)
            all_passed = False
    else:
        print_status(".env file (missing - run setup script)", False)
        all_passed = False
    print()
    
    # Test 7: Import application modules
    print("🏗️  Checking application modules...")
    app_modules = [
        ("config.settings", "Settings"),
        ("db.database", "Database"),
        ("db.models", "Models"),
        ("core.intent_compiler", "Intent Compiler"),
        ("core.policy_engine", "Policy Engine"),
        ("core.enforcement_layer", "Enforcement Layer"),
    ]
    
    for module, name in app_modules:
        try:
            __import__(module)
            print_status(name, True)
        except Exception as e:
            print_status(f"{name} ({str(e)})", False)
            all_passed = False
    print()
    
    # Final result
    print("=" * 50)
    if all_passed:
        print("✅ All checks passed! INTENTRA is ready to run.")
        print("\nTo start the server:")
        print("  python main.py")
    else:
        print("❌ Some checks failed. Please fix the issues above.")
        print("\nCommon fixes:")
        print("  - Run setup script: ./setup.sh (Linux/Mac) or setup.bat (Windows)")
        print("  - Install dependencies: pip install -r requirements.txt")
        print("  - Configure .env: cp .env.example .env and add API keys")
    print("=" * 50)
    
    return 0 if all_passed else 1

if __name__ == "__main__":
    sys.exit(main())
