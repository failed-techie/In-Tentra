# 🔑 Quick API Key Fix Guide

## Problem

You're seeing errors like:
- "UNKNOWN action"
- "N/A symbol"
- "0.0 confidence"  
- "Error code: 401 - Invalid API Key"

## Root Cause

The `GROQ_API_KEY` in your `.env` file is invalid or expired.

## Solution (2 minutes)

### Step 1: Get a Valid Groq API Key

1. Go to https://console.groq.com
2. Sign in or create account (free)
3. Navigate to: **API Keys** section
4. Click **"Create API Key"**
5. Copy the key (starts with `gsk_`)

### Step 2: Update .env File

Open `.env` in the project root and update:

```env
# OLD (invalid):
GROQ_API_KEY=<your_old_or_invalid_key>

# NEW (paste your key here):
GROQ_API_KEY=gsk_your_actual_key_from_console_groq_com
```

### Step 3: Verify the Fix

```bash
# Activate venv
venv\Scripts\activate

# Run verification
python tests\verify_apis.py
```

**Expected output:**
```
✅ PASS   Groq API
✅ PASS   Alpaca API
✅ PASS   LangSmith API  
✅ PASS   Full Pipeline
✅ PASS   Guardian Agent

🎉 ALL TESTS PASSED!
```

### Step 4: Restart Backend

If backend was already running, restart it:

```bash
# Stop: Ctrl+C

# Start:
uvicorn main:app --reload --host 0.0.0.0 --port 8000
```

### Step 5: Test the System

1. Open http://localhost:3000
2. Type: "Buy Apple stock for 300 dollars"
3. Click "Execute Trade"

**✅ Should now show:**
- Symbol: **AAPL** (not UNKNOWN)
- Action: **BUY** (not UNKNOWN)
- Amount: **$300.00**
- Confidence: **0.85** (not 0.0)
- Decision: **ALLOW** or **BLOCK**
- Order ID: Real Alpaca order ID

## Common Questions

### Q: Where do I find my .env file?

**A:** In the project root:
```
C:\Users\praya\Desktop\In-Tentra\.env
```

Open with any text editor (Notepad, VS Code, etc.)

---

### Q: What if I don't have a .env file?

**A:** Create one:

```bash
cd C:\Users\praya\Desktop\In-Tentra
copy .env.example .env
# Then edit .env and add your API keys
```

---

### Q: Do I need to update any other API keys?

**A:** Check these in your `.env`:

```env
# Required for trading (you should already have these):
ALPACA_API_KEY=your_alpaca_key
ALPACA_SECRET_KEY=your_alpaca_secret

# Optional for tracing:
LANGCHAIN_API_KEY=your_langsmith_key
```

If Alpaca or LangSmith keys are missing/invalid, get them from:
- Alpaca: https://alpaca.markets (paper trading account)
- LangSmith: https://smith.langchain.com

---

### Q: Why did my key become invalid?

**A:** Common reasons:
- Free tier API key expired
- Account suspended/deactivated
- Key was regenerated on the console
- Copy-paste error (extra spaces, incomplete key)

**Fix:** Generate a new key from the console

---

### Q: Can I test without fixing the Groq API?

**A:** No. Groq powers all agents:
- **IntentCompiler** - parses your plain English prompts
- **AnalystAgent** - analyzes market conditions
- **GuardianAgent** - generates adversarial tests

Without a valid Groq key, you'll get:
- UNKNOWN actions
- N/A symbols
- 0.0 confidence
- All trades blocked

---

## Troubleshooting

### Still seeing "Invalid API Key" after update?

1. Check for typos in `.env`
2. Ensure no extra spaces: `GROQ_API_KEY=gsk_...` (no spaces around `=`)
3. Key should start with `gsk_`
4. Restart backend after editing `.env`
5. Try generating a new key from console.groq.com

---

### Tests pass but frontend still shows UNKNOWN?

1. Restart backend: `Ctrl+C` then `uvicorn main:app --reload ...`
2. Hard refresh frontend: `Ctrl+Shift+R`
3. Check browser console (F12) for errors
4. Verify backend is running on port 8000

---

### How do I know my API key is valid?

Run this quick test:

```bash
python -c "from langchain_groq import ChatGroq; from config.settings import settings; ChatGroq(model='llama3-70b-8192', api_key=settings.GROQ_API_KEY).invoke('test')"
```

**Success:** Returns a response  
**Failure:** Shows 401 Unauthorized error

---

## Summary

✅ **Before fix:**
- Groq API: ❌ 401 Unauthorized
- Intent parsing: Returns UNKNOWN
- Full pipeline: Fails

✅ **After fix:**
- Groq API: ✅ Connected
- Intent parsing: Real symbols (AAPL, TSLA, etc.)
- Full pipeline: Operational

**Time to fix:** 2 minutes  
**Cost:** Free (Groq free tier available)

---

**Need help?**

1. Check `AUDIT_REPORT.md` for detailed system status
2. Review `STARTUP.md` for full startup instructions
3. Run `python tests\verify_apis.py` to diagnose issues
