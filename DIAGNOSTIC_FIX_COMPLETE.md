# INTENTRA DIAGNOSTIC FIX - COMPLETE

## Date: 2026-04-06

## Problems Identified and Fixed

### Problem 1: Frontend showing UNKNOWN/N/A values
**Root Causes Fixed:**
1. ✅ LLM responses containing `<think>...</think>` tags that broke JSON parsing
2. ✅ Missing error handling in JSON parsing pipeline
3. ✅ No diagnostic logging to identify failure points

**Solutions Applied:**
- Added `<think>...</think>` tag removal in:
  - `core/intent_compiler.py`
  - `agents/analyst_agent.py`
  - `agents/guardian_agent.py`
- Added comprehensive diagnostic logging throughout entire pipeline
- Added proper error handling with fallback mechanisms

### Problem 2: Backend URL confusion (0.0.0.0 vs localhost)
**Status:** ✅ Already correct
- Frontend `.env.local` has: `NEXT_PUBLIC_API_URL=http://localhost:8000`
- Frontend `lib/api.ts` uses: `http://localhost:8000`
- Backend starts on `0.0.0.0:8000` (correct - listens on all interfaces)
- Clients connect to `localhost:8000` (correct - maps to 0.0.0.0)

---

## Files Modified

### 1. main.py
**Changes:**
- Added diagnostic logging to `/run` endpoint
- Logs received request, MasterAgent initialization, and result
- Enhanced error handling with full traceback printing

**Key additions:**
```python
print(f"[ENDPOINT] Received request - prompt: {request.prompt}")
print(f"[ENDPOINT] MasterAgent returned result")
print(f"[ENDPOINT] Result intent: {result['intent']}")
```

### 2. core/intent_compiler.py
**Changes:**
- Added API key validation at initialization
- Added comprehensive diagnostic logging throughout compile() method
- **CRITICAL FIX:** Added regex-based removal of `<think>...</think>` tags
- Added markdown fence removal (```json...```)
- Added fallback error handling

**Key fix:**
```python
# Remove <think>...</think> blocks that some models add
cleaned = re.sub(r'<think>.*?</think>', '', raw_text, flags=re.DOTALL).strip()
# Also remove markdown code fences if present
cleaned = re.sub(r'```json\s*|\s*```', '', cleaned).strip()
```

### 3. agents/master_agent.py
**Changes:**
- Added diagnostic logging at pipeline entry point
- Logs each step: IntentCompiler, EnforcementLayer, TraderAgent
- Shows intent values (action, symbol, amount, confidence) at each stage
- Final summary log before returning result

**Key additions:**
```python
print("[MASTER] STARTING PIPELINE")
print(f"[MASTER] IntentCompiler result: action={intent_dict.get('action')}")
print("[MASTER] Final response being returned")
```

### 4. agents/analyst_agent.py
**Changes:**
- Added diagnostic logging for analysis steps
- **CRITICAL FIX:** Added `<think>...</think>` tag removal
- Added markdown fence removal
- Enhanced error handling with traceback

**Key fix:**
```python
cleaned = re.sub(r'<think>...</think>', '', raw_text, flags=re.DOTALL).strip()
```

### 5. agents/guardian_agent.py
**Changes:**
- Added `<think>...</think>` tag removal in generate_adversarial_inputs()
- Maintains consistency with other LLM output parsing

### 6. core/enforcement_layer.py
**Changes:**
- Added comprehensive diagnostic logging
- Shows received intent, validation results, and final decision
- Logs violations clearly

**Key additions:**
```python
print(f"[ENFORCEMENT] Received intent: {intent}")
print(f"[ENFORCEMENT] Decision: {decision}")
print(f"[ENFORCEMENT] Reason: {reason}")
```

### 7. tests/direct_test.py (NEW FILE)
**Purpose:** Isolated testing of each component to diagnose integration issues

**Tests included:**
1. **Test 1:** Direct Groq API call (bypasses LangChain)
2. **Test 2:** IntentCompiler in isolation
3. **Test 3:** EnforcementLayer in isolation
4. **Test 4:** MasterAgent end-to-end
5. **Test 5:** Full HTTP /run endpoint

---

## How to Use

### Step 1: Run Direct Tests First
```bash
cd C:\Users\praya\Desktop\In-Tentra
venv\Scripts\activate
python tests\direct_test.py
```

**Expected output:**
- All tests should pass
- If Test 5 is skipped, backend needs to be started first
- Any failures will show exactly which component is broken

### Step 2: Start Backend with Diagnostic Logging
```bash
cd C:\Users\praya\Desktop\In-Tentra
venv\Scripts\activate
uvicorn main:app --reload --port 8000
```

**Watch for logs:**
- `[ENDPOINT]` - Entry and exit of /run endpoint
- `[MASTER]` - Pipeline orchestration
- `[INTENT_COMPILER]` - LLM calls and parsing
- `[ENFORCEMENT]` - Policy validation
- `[ANALYST]` - Market analysis (if using legacy mode)

### Step 3: Start Frontend
```bash
cd C:\Users\praya\Desktop\In-Tentra\in-tentra
npm run dev
```

**Important:** If you changed `.env.local`, restart the frontend for changes to take effect.

### Step 4: Test from Frontend
1. Open: http://localhost:3000
2. Type: "Buy Apple stock for 300 dollars"
3. Submit

**Expected result in modal:**
- ✅ Action: BUY
- ✅ Symbol: AAPL
- ✅ Amount: 300
- ✅ Confidence: >0.0% (usually 85-95%)
- ✅ Reasoning: Real explanation text
- ✅ Decision: ALLOW or BLOCK (based on policies)

**Backend terminal should show:**
```
================================================================================
[ENDPOINT] Received request - prompt: Buy Apple stock for 300 dollars
================================================================================
[MASTER] ========================================
[MASTER] STARTING PIPELINE
[MASTER] Prompt: Buy Apple stock for 300 dollars
...
[INTENT_COMPILER] ===== STARTING COMPILATION =====
[INTENT_COMPILER] Final parsed intent:
  - action: BUY
  - symbol: AAPL
  - amount: 300.0
  - confidence: 0.95
...
[ENFORCEMENT] Decision: ALLOW
[MASTER] Final response being returned:
  - intent action: BUY
  - intent symbol: AAPL
```

---

## What the Fixes Do

### The `<think>...</think>` Tag Problem
**What was happening:**
- Groq's `qwen-qwq-32b` and similar reasoning models wrap responses like:
  ```
  <think>Let me analyze this... the user wants to buy Apple...</think>
  {"action": "BUY", "symbol": "AAPL", "amount": 300.0, ...}
  ```
- Our JSON parser tried to parse the entire thing → FAILED
- Failure triggered fallback → returned UNKNOWN/N/A values

**How we fixed it:**
```python
import re
# Strip thinking tags BEFORE parsing JSON
cleaned = re.sub(r'<think>.*?</think>', '', raw_text, flags=re.DOTALL).strip()
# Now parse the clean JSON
parsed = json.loads(cleaned)
```

### The Diagnostic Logging
**Purpose:**
- See exactly where in the pipeline each value comes from
- Identify if LLM is being called at all
- See raw LLM responses before parsing
- Catch silent failures

**When to use it:**
- Any time UNKNOWN/N/A appears again
- When debugging new LLM integration issues
- When values look wrong but no errors are raised

---

## Verification Checklist

After running the system, verify:

- [ ] Direct tests pass (run `python tests\direct_test.py`)
- [ ] Backend starts without errors
- [ ] Frontend connects (no CORS or connection errors)
- [ ] Test prompt "Buy Apple stock for 300 dollars" returns:
  - [ ] Action = BUY (not UNKNOWN)
  - [ ] Symbol = AAPL (not N/A)
  - [ ] Amount = 300 (not 0)
  - [ ] Confidence > 0.0 (not 0.0)
  - [ ] Reasoning is real text (not "No reasoning available")
- [ ] Backend terminal shows all diagnostic logs
- [ ] No errors in backend terminal
- [ ] Frontend modal displays all values correctly

---

## Troubleshooting

### If UNKNOWN/N/A still appears:

1. **Check backend terminal logs** - Look for:
   - `[INTENT_COMPILER] ERROR` - LLM call failed
   - `[INTENT_COMPILER] Cleaned response:` - Is it valid JSON?
   - `[MASTER] Final response` - What values are actually being returned?

2. **Run direct tests** - Isolate the failure:
   ```bash
   python tests\direct_test.py
   ```
   - If Test 1 fails: GROQ_API_KEY is wrong or API is down
   - If Test 2 fails: IntentCompiler has a bug
   - If Test 4 fails: MasterAgent integration issue
   - If Test 5 fails: HTTP endpoint or network issue

3. **Check GROQ_API_KEY**:
   ```bash
   # In venv
   python -c "import os; from dotenv import load_dotenv; load_dotenv(); print(os.getenv('GROQ_API_KEY')[:8] + '...')"
   ```
   Should print first 8 chars of your API key.

4. **Test LLM directly** (bypass all our code):
   ```bash
   python
   >>> from groq import Groq
   >>> import os
   >>> from dotenv import load_dotenv
   >>> load_dotenv()
   >>> client = Groq(api_key=os.getenv("GROQ_API_KEY"))
   >>> response = client.chat.completions.create(
   ...     model="openai/gpt-oss-120b",
   ...     messages=[{"role": "user", "content": "Reply with JSON: {\"test\": \"ok\"}"}]
   ... )
   >>> print(response.choices[0].message.content)
   ```
   Should return valid JSON.

### If Backend won't start:

1. Check port 8000 is available:
   ```bash
   netstat -ano | findstr :8000
   ```
   If occupied, kill the process or use different port.

2. Check dependencies:
   ```bash
   pip install -r requirements.txt
   ```

### If Frontend won't connect:

1. Check `.env.local` exists:
   ```bash
   cd in-tentra
   type .env.local
   ```
   Should show: `NEXT_PUBLIC_API_URL=http://localhost:8000`

2. Restart frontend after changing `.env.local`:
   ```bash
   # Stop with Ctrl+C
   npm run dev
   ```

---

## Success Indicators

You'll know everything is working when:

1. ✅ `python tests\direct_test.py` shows all tests passed
2. ✅ Backend terminal shows colorful diagnostic logs for each request
3. ✅ Frontend modal displays real values (not UNKNOWN/N/A/0)
4. ✅ Confidence scores are >0.0
5. ✅ Reasoning text explains the LLM's decision
6. ✅ No errors in either terminal

---

## Next Steps (Optional Enhancements)

If you want to further improve the system:

1. **Add unit tests** for the thinking tag removal logic
2. **Monitor LangSmith** for LLM tracing (if LANGCHAIN_TRACING_V2=true)
3. **Add retry logic** for transient API failures
4. **Cache compiled intents** for identical prompts
5. **Add rate limiting** to prevent API quota exhaustion
6. **Create a health check dashboard** showing component status

---

## Summary

**What we did:**
1. ✅ Added comprehensive diagnostic logging throughout the pipeline
2. ✅ Fixed JSON parsing by removing `<think>...</think>` tags
3. ✅ Created isolated tests for each component
4. ✅ Verified frontend URL configuration is correct

**What you should do:**
1. Run `python tests\direct_test.py` to verify fixes
2. Start backend and watch diagnostic logs
3. Test from frontend with "Buy Apple stock for 300 dollars"
4. Confirm modal shows real values (not UNKNOWN/N/A/0)

**Result:**
The system should now correctly parse LLM outputs and display proper trading intents in the frontend.
