# 🚀 INTENTRA STARTUP GUIDE

Complete instructions to run INTENTRA multi-agent AI trading system after fixes.

---

## ✅ PREREQUISITES

1. **Python 3.11+** installed and in PATH
2. **Node.js 18+** installed (for frontend)
3. **Virtual environment** created and activated
4. **API Keys** configured in `.env` file

---

## 🔑 STEP 1: Configure API Keys

Edit the `.env` file in the root directory:

```bash
# Required - Groq API for LLM agents
GROQ_API_KEY=your-groq-api-key-here

# Required - Alpaca Paper Trading API
ALPACA_API_KEY=your-alpaca-api-key-here
ALPACA_SECRET_KEY=your-alpaca-secret-key-here
ALPACA_BASE_URL=https://paper-api.alpaca.markets

# Optional - LangSmith Tracing (for debugging and monitoring)
LANGCHAIN_TRACING_V2=true
LANGCHAIN_ENDPOINT=https://api.smith.langchain.com
LANGCHAIN_API_KEY=your-langsmith-api-key-here
LANGCHAIN_PROJECT=intentra

# Trading Mode
DRY_RUN=false  # Set to false for real paper trading, true for simulation
```

**Where to get API keys:**
- **Groq**: https://console.groq.com (free tier available)
- **Alpaca**: https://alpaca.markets (paper trading is free)
- **LangSmith**: https://smith.langchain.com (optional, for tracing)

---

## 🧪 STEP 2: Verify APIs Work

Before starting the servers, verify all APIs are working:

```bash
# Activate virtual environment
venv\Scripts\activate

# Run API verification tests
python tests\verify_apis.py
```

**Expected output:**
```
✅ PASS  Groq API
✅ PASS  Alpaca API
✅ PASS  LangSmith API
✅ PASS  Full Pipeline
✅ PASS  Guardian Agent

🎉 ALL TESTS PASSED! INTENTRA is ready to run.
```

**If any test fails**, check the error messages and fix the corresponding API key in `.env`.

---

## 🖥️ STEP 3: Start Backend Server

Open **Terminal 1** (PowerShell or Command Prompt):

```bash
cd C:\Users\praya\Desktop\In-Tentra

# Activate virtual environment
venv\Scripts\activate

# Start FastAPI backend
uvicorn main:app --reload --host 0.0.0.0 --port 8000
```

**Expected output:**
```
==================================================
INTENTRA CONFIGURATION - Startup Report
==================================================
✅ GROQ_API_KEY:        Loaded (length: 56)
   Model:               llama3-70b-8192
✅ ALPACA_API_KEY:      Loaded (length: 20)
✅ ALPACA_SECRET_KEY:   Loaded (length: 40)
   Base URL:            https://paper-api.alpaca.markets
✅ LANGCHAIN_API_KEY:   Loaded (length: 58)
   Tracing:             ENABLED
   Project:             intentra
==================================================

INFO:     Started server process [12345]
INFO:     Waiting for application startup.
✅ Database initialized
✅ Policy engine loaded
✅ All agents ready
✅ Server running at http://localhost:8000
INFO:     Application startup complete.
INFO:     Uvicorn running on http://0.0.0.0:8000
```

**Backend is now running!** Leave this terminal open.

---

## 🌐 STEP 4: Start Frontend Server

Open **Terminal 2** (separate window):

```bash
cd C:\Users\praya\Desktop\In-Tentra\in-tentra

# Install dependencies (first time only)
npm install

# Start Next.js frontend
npm run dev
```

**Expected output:**
```
   ▲ Next.js 14.x.x
   - Local:        http://localhost:3000
   - Network:      http://192.168.x.x:3000

 ✓ Ready in 2.5s
```

**Frontend is now running!** Leave this terminal open.

---

## 🎯 STEP 5: Test the System

1. **Open your browser**: http://localhost:3000

2. **Click "Start Trading"** button in the hero section

3. **Enter a trade prompt** in the modal, for example:
   - `Buy Apple stock for 300 dollars`
   - `Sell Tesla for 500 dollars`
   - `Invest 200 in Microsoft`

4. **Click "Execute Trade"**

5. **Verify the results:**

   **✅ For ALLOWED trade (e.g., "Buy Apple for 300 dollars"):**
   - Symbol: `AAPL`
   - Action: `BUY`
   - Amount: `$300.00`
   - Decision: Green `ALLOW` badge
   - Order ID: Real Alpaca order ID (e.g., `a1b2c3d4-...`) or `DRY_RUN_...` if in dry-run mode
   - Confidence: >0.7

   **❌ For BLOCKED trade (e.g., "Sell NVDA for 500 dollars"):**
   - Symbol: `NVDA`
   - Action: `SELL`
   - Amount: `$500.00`
   - Decision: Red `BLOCK` badge
   - Reason: `Symbol 'NVDA' not in allowed list: ['AAPL', 'TSLA', 'MSFT', 'GOOGL']`

6. **Check Trade History:**
   - Scroll down to "Trade History" section
   - Your trade should appear in the log with correct timestamp
   - Use filters: All / Allowed / Blocked

7. **Verify LangSmith Traces** (optional, if enabled):
   - Go to: https://smith.langchain.com
   - Select project: `intentra`
   - You should see traces for:
     - `IntentCompiler` (parsing your prompt)
     - `AnalystAgent` (if using market context mode)
     - `GuardianAgent` (adversarial testing)

---

## 🧪 STEP 6: Test Different Scenarios

### Test 1: Successful Trade (ALLOW)
**Input:** `Buy Apple stock for 300 dollars`

**Expected Result:**
- ✅ Symbol: AAPL (allowed)
- ✅ Amount: $300 (under $1000 limit)
- ✅ Action: BUY (allowed)
- ✅ Decision: **ALLOW**
- ✅ Order executed via Alpaca

---

### Test 2: Amount Overflow (BLOCK)
**Input:** `Buy Tesla for 5000 dollars`

**Expected Result:**
- ✅ Symbol: TSLA (allowed)
- ❌ Amount: $5000 (exceeds $1000 limit)
- ✅ Action: BUY (allowed)
- ❌ Decision: **BLOCK**
- ❌ Reason: "Trade amount $5000 exceeds maximum $1000"

---

### Test 3: Disallowed Symbol (BLOCK)
**Input:** `Sell NVDA for 200 dollars`

**Expected Result:**
- ❌ Symbol: NVDA (not in allowed list)
- ✅ Amount: $200 (under limit)
- ✅ Action: SELL (allowed)
- ❌ Decision: **BLOCK**
- ❌ Reason: "Symbol 'NVDA' not in allowed list"

---

### Test 4: Blocked Action (BLOCK)
**Input:** `Short MSFT for 500 dollars`

**Expected Result:**
- ✅ Symbol: MSFT (allowed)
- ✅ Amount: $500 (under limit)
- ❌ Action: SHORT (blocked - converted to SELL in parsing, but still blocked)
- ❌ Decision: **BLOCK**
- ❌ Reason: "Action 'SHORT' is blocked by policy"

---

### Test 5: Multiple Symbols (First Symbol Used)
**Input:** `Buy Apple and Tesla for 400 dollars`

**Expected Result:**
- ✅ Symbol: AAPL (first symbol mentioned)
- ✅ Amount: $400 (under limit)
- ✅ Action: BUY (allowed)
- ✅ Decision: **ALLOW** (if AAPL is first)
- 💡 Reasoning mentions both symbols but uses first one

---

## 📊 STEP 7: Monitor System Health

### Check Backend Health
```bash
curl http://localhost:8000/health
```

**Expected:**
```json
{
  "status": "healthy",
  "database": "connected",
  "agents": "available"
}
```

### Check Portfolio (if Alpaca is configured)
```bash
curl http://localhost:8000/portfolio
```

### View Trade Logs
```bash
curl http://localhost:8000/logs?limit=10
```

---

## 🛑 TROUBLESHOOTING

### Issue: "Agents not available" error

**Solution:**
1. Check backend terminal for errors during startup
2. Verify all API keys are set in `.env`
3. Run `python tests\verify_apis.py` to diagnose

---

### Issue: Trades return UNKNOWN/N/A/0.0 values

**Solution:**
- This was the original bug! If you still see this:
  1. Make sure you pulled the latest fixes
  2. Restart backend server
  3. Check that MasterAgent is calling `trader_agent.execute()` not mock code

---

### Issue: LangSmith traces not appearing

**Solution:**
1. Check that `LANGCHAIN_TRACING_V2=true` in `.env`
2. Verify `LANGCHAIN_API_KEY` is set
3. Restart backend server (env vars must be set at startup)
4. Run: `python -c "from evaluation.langsmith_evaluator import verify_tracing; verify_tracing()"`
5. Wait 10-30 seconds for traces to appear in dashboard

---

### Issue: "Market is closed" error from Alpaca

**Solution:**
- Alpaca paper trading follows real market hours (9:30 AM - 4:00 PM ET, Mon-Fri)
- Wait until market opens, or set `DRY_RUN=true` to simulate trades anytime

---

### Issue: Frontend shows "Network Error"

**Solution:**
1. Verify backend is running on port 8000
2. Check CORS settings in `main.py` allow `http://localhost:3000`
3. Check browser console for detailed error

---

## 🔄 STOPPING THE SYSTEM

1. **Stop Frontend**: Press `Ctrl+C` in Terminal 2
2. **Stop Backend**: Press `Ctrl+C` in Terminal 1
3. **Deactivate venv**: Type `deactivate`

---

## 📝 MAINTENANCE TASKS

### Update Dependencies

```bash
# Backend
pip install -r requirements.txt --upgrade

# Frontend
cd in-tentra
npm update
```

### Clear Database (reset logs)

```bash
# Delete SQLite database
del intentra.db

# Restart backend - database will be recreated
```

### View All Endpoints

Open API docs: http://localhost:8000/docs

---

## 🎉 SUCCESS CHECKLIST

Before considering the system "working", verify:

- [ ] Backend starts without errors
- [ ] Frontend loads at http://localhost:3000
- [ ] Can enter natural language trade prompt
- [ ] Prompt is parsed correctly (not UNKNOWN)
- [ ] Symbol is extracted (not N/A)
- [ ] Confidence is > 0 (not 0.0)
- [ ] Enforcement decision is ALLOW or BLOCK (not undefined)
- [ ] If ALLOW, real order ID appears (not test-order-123)
- [ ] Trade logs show correct timestamp (current date, not 1970)
- [ ] LangSmith traces appear (if enabled)
- [ ] Portfolio endpoint returns real Alpaca data (if not DRY_RUN)

---

## 📧 SUPPORT

If you encounter issues not covered here:

1. Check backend terminal for detailed error messages
2. Check browser console (F12) for frontend errors
3. Review API verification test output: `python tests\verify_apis.py`
4. Check LangSmith dashboard for trace errors
5. Verify all API keys are valid and have correct permissions

---

**INTENTRA is now fully operational!** 🚀

The system is now calling:
- ✅ Groq API for real LLM intent parsing and analysis
- ✅ Alpaca API for real paper trading execution
- ✅ LangSmith API for distributed tracing and monitoring

No more hardcoded/mock responses!
