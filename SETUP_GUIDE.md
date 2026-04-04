# INTENTRA Setup Guide

## Quick Start

### Windows
```bash
setup.bat
```

### Linux/Mac
```bash
chmod +x setup.sh
./setup.sh
```

## Manual Setup (if scripts fail)

### 1. Create Virtual Environment

**Windows:**
```bash
python -m venv venv
venv\Scripts\activate
```

**Linux/Mac:**
```bash
python3 -m venv venv
source venv/bin/activate
```

### 2. Install Dependencies

```bash
pip install --upgrade pip
pip install -r requirements.txt
```

### 3. Configure Environment

```bash
# Copy template
cp .env.example .env

# Edit .env and add your API keys
```

### 4. Run the Application

```bash
python main.py
```

## Getting API Keys

### Groq API Key
1. Go to https://console.groq.com
2. Sign up or log in
3. Navigate to API Keys
4. Create a new API key
5. Copy and paste into `.env` as `GROQ_API_KEY`

### Alpaca API Keys
1. Go to https://alpaca.markets
2. Sign up for a free account
3. Navigate to Paper Trading
4. Get your API Key and Secret Key
5. Copy both into `.env` as:
   - `ALPACA_API_KEY`
   - `ALPACA_SECRET_KEY`

**IMPORTANT:** Always use paper trading (`https://paper-api.alpaca.markets`) for development!

## Version Compatibility Notes

### Critical Dependencies

**Pydantic v2.x:**
- `pydantic==2.6.1` and `pydantic-settings==2.1.0` are compatible
- LangChain 0.1.x requires pydantic v2
- Do NOT mix pydantic v1 and v2

**LangChain Ecosystem:**
- `langchain==0.1.7` is the core package
- `langchain-core==0.1.23` provides base abstractions
- `langchain-groq==0.0.1` is the Groq integration
- `langchain-community==0.0.20` provides additional tools
- All versions must be compatible (0.1.x or 0.0.x)

**FastAPI:**
- `fastapi==0.109.2` is compatible with pydantic v2.6.1
- Requires `uvicorn[standard]` for async support

**Alpaca:**
- `alpaca-trade-api==3.1.1` is stable
- Newer versions may have breaking changes

### Known Conflicts to Avoid

⚠️ **DO NOT:**
- Mix pydantic v1 (1.x) with pydantic v2 (2.x)
- Use langchain-groq > 0.0.1 without testing (may require newer langchain)
- Use fastapi > 0.110.x without testing pydantic compatibility
- Upgrade packages individually - always test together

✅ **SAFE UPGRADES:**
- Minor version bumps within same major version (e.g., 0.1.7 → 0.1.9)
- Patch versions (e.g., 2.6.1 → 2.6.3)
- Security patches when announced

### Testing Compatibility

After any upgrade:
```bash
# Test imports
python -c "from config.settings import settings; print('✅ Settings OK')"
python -c "from agents.master_agent import MasterAgent; print('✅ Agents OK')"
python -c "from langchain_groq import ChatGroq; print('✅ LangChain OK')"
python -c "import alpaca_trade_api; print('✅ Alpaca OK')"
```

## Troubleshooting

### "No module named 'pydantic_settings'"
```bash
pip install pydantic-settings==2.1.0
```

### "ValidationError: GROQ_API_KEY is required"
- Make sure you copied `.env.example` to `.env`
- Edit `.env` and add your actual API keys
- Keys must be at least 10 characters long

### "Python version too old"
- Requires Python 3.9 or higher
- Check version: `python --version`
- Install from https://www.python.org

### Import errors with LangChain
```bash
# Reinstall LangChain packages in correct order
pip uninstall -y langchain langchain-core langchain-groq langchain-community
pip install langchain-core==0.1.23
pip install langchain==0.1.7
pip install langchain-groq==0.0.1
pip install langchain-community==0.0.20
```

### Alpaca connection errors
- Verify `ALPACA_BASE_URL` includes `https://`
- Check API keys are from same environment (paper vs live)
- Test with Alpaca's health endpoint first

## Environment Variables Reference

| Variable | Required | Default | Description |
|----------|----------|---------|-------------|
| `GROQ_API_KEY` | ✅ Yes | - | Groq API key from console.groq.com |
| `ALPACA_API_KEY` | ✅ Yes | - | Alpaca API key |
| `ALPACA_SECRET_KEY` | ✅ Yes | - | Alpaca secret key |
| `ALPACA_BASE_URL` | No | `https://paper-api.alpaca.markets` | Alpaca endpoint |
| `HOST` | No | `0.0.0.0` | Server host |
| `PORT` | No | `8000` | Server port |
| `DEBUG` | No | `True` | Debug mode |
| `GROQ_MODEL` | No | `llama-3.3-70b-versatile` | Groq model name |
| `DATABASE_URL` | No | `sqlite:///./logs/intentra.db` | Database path |
| `MAX_RETRIES` | No | `3` | Agent retry attempts |
| `TIMEOUT_SECONDS` | No | `30` | Agent timeout |
| `POLICY_FILE` | No | `config/policies.json` | Policy config path |

## Support

If setup fails:
1. Check Python version (3.9+ required)
2. Try manual setup steps
3. Check for antivirus blocking pip/venv
4. Ensure stable internet connection
5. Review error messages carefully

For dependency conflicts:
1. Delete `venv` folder
2. Run setup script again
3. Do not modify `requirements.txt` unless necessary
