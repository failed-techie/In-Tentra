#!/bin/bash

# ================================================================
# INTENTRA - Multi-Agent AI Trading System
# Setup Script for Linux/Mac
# ================================================================

set -e  # Exit on any error

echo "🚀 Setting up INTENTRA..."
echo ""

# Check Python version
echo "📋 Checking Python version..."
PYTHON_CMD=""

if command -v python3 &> /dev/null; then
    PYTHON_CMD="python3"
    PYTHON_VERSION=$(python3 --version 2>&1 | awk '{print $2}')
elif command -v python &> /dev/null; then
    PYTHON_CMD="python"
    PYTHON_VERSION=$(python --version 2>&1 | awk '{print $2}')
else
    echo "❌ Error: Python is not installed"
    echo "Please install Python 3.9 or higher from https://www.python.org"
    exit 1
fi

echo "✅ Found Python $PYTHON_VERSION"

# Check if Python version is 3.9+
PYTHON_MAJOR=$(echo $PYTHON_VERSION | cut -d. -f1)
PYTHON_MINOR=$(echo $PYTHON_VERSION | cut -d. -f2)

if [ "$PYTHON_MAJOR" -lt 3 ] || ([ "$PYTHON_MAJOR" -eq 3 ] && [ "$PYTHON_MINOR" -lt 9 ]); then
    echo "❌ Error: Python 3.9+ is required (found $PYTHON_VERSION)"
    exit 1
fi

# Create virtual environment
echo ""
echo "📦 Creating virtual environment..."
if [ -d "venv" ]; then
    echo "⚠️  Virtual environment already exists. Skipping creation."
else
    $PYTHON_CMD -m venv venv
    echo "✅ Virtual environment created"
fi

# Activate virtual environment
echo ""
echo "🔌 Activating virtual environment..."
source venv/bin/activate

# Upgrade pip
echo ""
echo "⬆️  Upgrading pip..."
pip install --upgrade pip setuptools wheel

# Install requirements
echo ""
echo "📚 Installing dependencies..."
pip install -r requirements.txt

# Copy .env.example to .env if it doesn't exist
echo ""
if [ -f ".env" ]; then
    echo "⚠️  .env file already exists. Skipping copy."
    echo "💡 To reset, delete .env and run this script again."
else
    echo "📄 Creating .env file from template..."
    cp .env.example .env
    echo "✅ .env file created"
    echo ""
    echo "⚠️  IMPORTANT: Edit .env and add your API keys!"
fi

# Create logs directory if it doesn't exist
echo ""
echo "📁 Creating logs directory..."
mkdir -p logs
echo "✅ Logs directory ready"

# Success message
echo ""
echo "=========================================="
echo "✅ Setup Complete!"
echo "=========================================="
echo ""
echo "Next steps:"
echo "  1. Edit .env and add your API keys:"
echo "     - GROQ_API_KEY (from https://console.groq.com)"
echo "     - ALPACA_API_KEY (from https://alpaca.markets)"
echo "     - ALPACA_SECRET_KEY"
echo ""
echo "  2. Activate the virtual environment:"
echo "     source venv/bin/activate"
echo ""
echo "  3. Run the application:"
echo "     python main.py"
echo ""
echo "  4. Access the API at http://localhost:8000"
echo ""
