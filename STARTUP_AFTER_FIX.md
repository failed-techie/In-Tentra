# 🚀 INTENTRA - STARTUP INSTRUCTIONS AFTER FIX

## Quick Start (Recommended)

### Terminal 1 - Backend with Tests
```bash
cd C:\Users\praya\Desktop\In-Tentra
test_and_start.bat
```
This script will:
1. Activate virtual environment
2. Run all diagnostic tests
3. Start the backend if tests pass
4. Show diagnostic logs for every request

### Terminal 2 - Frontend
```bash
cd C:\Users\praya\Desktop\In-Tentra\in-tentra
npm run dev
```

### Test It
1. Open: http://localhost:3000
2. Type: **"Buy Apple stock for 300 dollars"**
3. Click Submit

**Expected Result:**
- ✅ Action: **BUY** (not UNKNOWN)
- ✅ Symbol: **AAPL** (not N/A)
- ✅ Amount: **300** (not 0)
- ✅ Confidence: **85-95%** (not 0.0%)
- ✅ Reasoning: Real explanation text
- ✅ Decision: ALLOW or BLOCK

---

## Manual Step-by-Step (If you prefer)

### Step 1: Test Components First

```bash
cd C:\Users\praya\Desktop\In-Tentra
venv\Scripts\activate
python tests\direct_test.py
```

**What to look for:**
- ✅ All 5 tests should pass (Test 5 may be skipped if backend not running)
- ❌ If any test fails, read the error and fix before continuing

**Common failures:**
- **Test 1 fails**: GROQ_API_KEY is missing or invalid
  - Fix: Check `.env` file has correct API key
- **Test 2 fails**: IntentCompiler cannot parse LLM output
  - Fix: Check diagnostic output for JSON parsing errors
- **Test 5 skipped**: Backend not running
  - This is normal - backend starts in Step 2

### Step 2: Start Backend

```bash
# (venv should still be active from Step 1)
uvicorn main:app --reload --port 8000
```

**What you should see:**
```
INFO:     Uvicorn running on http://0.0.0.0:8000 (Press CTRL+C to quit)
INFO:     Started reloader process [xxxxx] using WatchFiles
[STARTUP] Starting INTENTRA...
✅ Database initialized
✅ Policy engine loaded
✅ All agents ready
✅ Server running at http://localhost:8000
```

**Diagnostic Logs:**
The backend will now print detailed logs for every request:
- `[ENDPOINT]` - Request received and response sent
- `[MASTER]` - Pipeline orchestration steps
- `[INTENT_COMPILER]` - LLM calls and JSON parsing
- `[ENFORCEMENT]` - Policy validation decisions
- `[ANALYST]` - Market analysis (if using legacy API)

### Step 3: Start Frontend

**Open a NEW terminal:**
```bash
cd C:\Users\praya\Desktop\In-Tentra\in-tentra
npm run dev
```

**What you should see:**
```
  ▲ Next.js 15.x.x
  - Local:        http://localhost:3000
  - Network:      http://x.x.x.x:3000

 ✓ Starting...
 ✓ Ready in 2.3s
```

**If port 3000 is taken:**
- Next.js will automatically use 3001, 3002, etc.
- The URL will be shown in the terminal

### Step 4: Test from Frontend

1. **Open browser:** http://localhost:3000
2. **Type:** "Buy Apple stock for 300 dollars"
3. **Click:** Submit button
4. **Watch backend terminal** for diagnostic logs
5. **Check frontend modal** for results

---

## What to Check in Backend Logs

When you submit from frontend, backend terminal should show:

```
================================================================================
[ENDPOINT] Received request - prompt: Buy Apple stock for 300 dollars
[ENDPOINT] Received request - market_context: None
================================================================================
[ENDPOINT] MasterAgent initialized
[ENDPOINT] Calling MasterAgent.run() with prompt...
[MASTER] ========================================
[MASTER] STARTING PIPELINE
[MASTER] Prompt: Buy Apple stock for 300 dollars
[MASTER] Market context: None
[MASTER] ========================================
[MASTER] Mode: NATURAL_LANGUAGE
[MASTER] ===== MODE 1: NATURAL LANGUAGE =====
[MASTER] Calling IntentCompiler.compile('Buy Apple stock for 300 dollars')
[INTENT_COMPILER] ===== STARTING COMPILATION =====
[INTENT_COMPILER] Input received: 'Buy Apple stock for 300 dollars'
[INTENT_COMPILER] Sending to Groq model: openai/gpt-oss-120b
[INTENT_COMPILER] Using API key: gsk_xxxx...
[INTENT_COMPILER] Using model: openai/gpt-oss-120b
[INTENT_COMPILER] Invoking LLM chain...
[INTENT_COMPILER] Raw LLM response type: <class '...'>
[INTENT_COMPILER] Raw LLM response: content='...'
[INTENT_COMPILER] Extracted text: {"action": "BUY", "symbol": "AAPL", ...}
[INTENT_COMPILER] After removing <think> tags: {"action": "BUY", ...}
[INTENT_COMPILER] After removing markdown fences: {"action": "BUY", ...}
[INTENT_COMPILER] Successfully parsed JSON: {...}
[INTENT_COMPILER] Final parsed intent:
  - action: BUY
  - symbol: AAPL
  - amount: 300.0
  - confidence: 0.95
  - reasoning: Clear buy intent for Apple (AAPL) with specific amount $300
[INTENT_COMPILER] ===== COMPILATION SUCCESSFUL =====
[MASTER] IntentCompiler result:
  - action: BUY
  - symbol: AAPL
  - amount: 300.0
  - confidence: 0.95
[MASTER] ===== STEP 3: ENFORCEMENT LAYER =====
[MASTER] Calling EnforcementLayer.enforce() with intent: {...}
[ENFORCEMENT] ===== ENFORCEMENT CHECK =====
[ENFORCEMENT] Received intent: {'action': 'BUY', 'symbol': 'AAPL', ...}
[ENFORCEMENT] Policy validation result: {'valid': True, 'violations': []}
[ENFORCEMENT] Runtime checks: {'passed': True, ...}
[ENFORCEMENT] Decision: ALLOW
[ENFORCEMENT] Reason: All enforcement checks passed
[ENFORCEMENT] ===========================
[MASTER] EnforcementLayer decision: ALLOW
[MASTER] EnforcementLayer reason: All enforcement checks passed
[MASTER] ========================================
[MASTER] PIPELINE COMPLETE
[MASTER] Final response being returned:
  - mode: NATURAL_LANGUAGE
  - intent action: BUY
  - intent symbol: AAPL
  - intent amount: 300.0
  - enforcement_decision: ALLOW
  - trade_result: {...}
  - errors: []
[MASTER] ========================================
[ENDPOINT] MasterAgent returned result
================================================================================
[ENDPOINT] Result keys: [...]
[ENDPOINT] Result intent: {'action': 'BUY', 'symbol': 'AAPL', ...}
[ENDPOINT] Result parsed_intent: {'action': 'BUY', 'symbol': 'AAPL', ...}
[ENDPOINT] Result enforcement_decision: ALLOW
================================================================================
```

**Key things to verify:**
- ✅ No ERROR messages
- ✅ `action: BUY` (not UNKNOWN)
- ✅ `symbol: AAPL` (not N/A or UNKNOWN)
- ✅ `amount: 300.0` (not 0.0)
- ✅ `confidence: 0.95` (not 0.0)
- ✅ `enforcement_decision: ALLOW` (or BLOCK with valid reason)

---

## If You Still See UNKNOWN/N/A

### Step 1: Check Backend Logs
Look for these patterns:

**Pattern A - LLM not being called:**
```
[INTENT_COMPILER] ERROR: GROQ_API_KEY is not set!
```
**Fix:** Set GROQ_API_KEY in `.env` file

**Pattern B - LLM response not parseable:**
```
[INTENT_COMPILER] Raw LLM response: <think>...</think>{"action": ...}
[INTENT_COMPILER] ERROR: json.decoder.JSONDecodeError
```
**Fix:** This should be fixed by the `<think>` tag removal. If still failing:
- Check the "After removing <think> tags" line
- Ensure regex is working correctly

**Pattern C - LLM returns unexpected format:**
```
[INTENT_COMPILER] Successfully parsed JSON: {'status': 'ok'}
```
**Fix:** LLM didn't follow the prompt. Check:
- Model is correct: `openai/gpt-oss-120b`
- Temperature is low: `0.3`
- Prompt includes format instructions

### Step 2: Run Direct Test
```bash
python tests\direct_test.py
```
This will show exactly which component is broken.

### Step 3: Test LLM Directly
```bash
python
>>> from groq import Groq
>>> import os
>>> from dotenv import load_dotenv
>>> load_dotenv()
True
>>> client = Groq(api_key=os.getenv("GROQ_API_KEY"))
>>> response = client.chat.completions.create(
...     model="openai/gpt-oss-120b",
...     messages=[{"role": "user", "content": "Reply with JSON: {\"action\": \"BUY\", \"symbol\": \"AAPL\"}"}],
...     temperature=0.1
... )
>>> print(response.choices[0].message.content)
```
Should return valid JSON.

---

## Troubleshooting Common Issues

### Backend won't start
```
ERROR: Address already in use
```
**Fix:** Port 8000 is occupied
```bash
# Find and kill the process using port 8000
netstat -ano | findstr :8000
taskkill /PID <PID> /F
```

### Frontend can't connect
```
Failed to fetch
ERR_CONNECTION_REFUSED
```
**Fix:** Backend is not running or wrong URL
1. Check backend is running at http://localhost:8000
2. Check `.env.local` has: `NEXT_PUBLIC_API_URL=http://localhost:8000`
3. Restart frontend after changing `.env.local`

### CORS errors
```
Access to fetch blocked by CORS policy
```
**Fix:** Backend CORS is misconfigured (should not happen - already fixed)
- Check `main.py` has `http://localhost:3000` in allowed origins

### ModuleNotFoundError
```
ModuleNotFoundError: No module named 'langchain_groq'
```
**Fix:** Dependencies not installed
```bash
venv\Scripts\activate
pip install -r requirements.txt
```

---

## Test Cases to Try

After basic test works, try these:

### Valid Trades (should ALLOW)
1. "Buy Apple stock for 300 dollars" → BUY AAPL 300
2. "Sell Tesla shares worth 500" → SELL TSLA 500
3. "Invest 200 in Microsoft" → BUY MSFT 200
4. "Purchase 100 dollars of Google stock" → BUY GOOGL 100

### Policy Violations (should BLOCK)
1. "Buy 5000 dollars of Apple stock" → Amount exceeds $1000 limit
2. "Buy Bitcoin for 500 dollars" → BTC not in whitelist
3. "Short Tesla for 300 dollars" → SHORT action not allowed
4. "Buy NVDA for 400 dollars" → NVDA not in whitelist

### Edge Cases
1. "Maybe buy some Apple" → Low confidence, may BLOCK
2. "Sell everything now" → No symbol → BLOCK
3. "Buy stock" → No symbol → BLOCK
4. "AAPL buy now" → Unusual phrasing → Test parser robustness

---

## Success Checklist

- [ ] Direct tests pass (`python tests\direct_test.py`)
- [ ] Backend starts without errors
- [ ] Backend shows diagnostic logs
- [ ] Frontend connects to backend
- [ ] "Buy Apple stock for 300 dollars" returns BUY AAPL 300
- [ ] Confidence > 0.0%
- [ ] Reasoning text is meaningful
- [ ] Decision is ALLOW or BLOCK (not undefined)
- [ ] No UNKNOWN or N/A values anywhere

---

## What's Next?

Once everything works:

1. **Remove diagnostic logging** (optional):
   - Keep it for debugging
   - Or comment out print statements if too verbose

2. **Enable LangSmith tracing** (optional):
   - Set `LANGCHAIN_TRACING_V2=true` in `.env`
   - Set `LANGCHAIN_API_KEY` to your LangSmith key
   - View traces at https://smith.langchain.com/

3. **Configure policies**:
   - Edit `config/policies.json`
   - Adjust max_trade_amount, allowed_symbols, etc.

4. **Connect real trading**:
   - Set Alpaca API keys in `.env`
   - Set `DRY_RUN=false` to enable real trades
   - **⚠️ Be careful - real money!**

5. **Deploy to production**:
   - Use proper WSGI server (gunicorn/uvicorn)
   - Set up reverse proxy (nginx)
   - Enable HTTPS
   - Set up monitoring

---

## Support

If issues persist:
1. Check `DIAGNOSTIC_FIX_COMPLETE.md` for detailed fix explanation
2. Review backend terminal logs for error patterns
3. Run `python tests\direct_test.py` to isolate component failures
4. Check Groq API status at https://console.groq.com/

---

**You should now have a fully working INTENTRA system with comprehensive diagnostic logging!** 🎉
