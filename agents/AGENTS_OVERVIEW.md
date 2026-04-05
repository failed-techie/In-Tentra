# INTENTRA - Complete Agent System Overview

This document provides a comprehensive overview of all three agents built for INTENTRA.

## System Architecture

```
┌─────────────────────────────────────────────────────────────────┐
│                        MASTER AGENT                             │
│                  (Orchestration - NO LLM)                       │
│                                                                 │
│  Coordinates:                                                   │
│  ┌─────────────────┬───────────────┬──────────────────────┐    │
│  │ AnalystAgent    │ GuardianAgent │ IntentCompiler       │    │
│  │ (LLM-powered)   │ (LLM-powered) │ (LLM-powered)        │    │
│  │ Market Analysis │ Adv. Testing  │ Intent Parsing       │    │
│  └─────────────────┴───────────────┴──────────────────────┘    │
│  ┌─────────────────┬───────────────┬──────────────────────┐    │
│  │ EnforcementLayer│ TraderAgent   │ Logger               │    │
│  │ (Deterministic) │ (API calls)   │ (Logging)            │    │
│  │ Policy Check    │ Execution     │ Action Logs          │    │
│  └─────────────────┴───────────────┴──────────────────────┘    │
└─────────────────────────────────────────────────────────────────┘
```

## Agent Summaries

### 1. Analyst Agent 📊

**Purpose:** Analyzes market context and generates trade suggestions

**Tech Stack:**
- LangChain + langchain-groq
- Pydantic structured output
- ChatPromptTemplate

**Input:**
```python
{
    "symbol": "AAPL",
    "current_price": 175.0,
    "trend": "upward",
    "volume": "high",
    "news_sentiment": "positive"
}
```

**Output:**
```python
{
    "action": "BUY" | "SELL" | "HOLD",
    "symbol": "AAPL",
    "amount": 500.0,
    "confidence": 0.85,
    "reasoning": "Strong upward trend..."
}
```

**Key Features:**
- ✅ Cautious, low-risk system prompt
- ✅ Pydantic validation for output
- ✅ Fallback to HOLD on error
- ✅ Temperature: 0.3 (consistent)

**Files:**
- `agents/analyst_agent.py` - Main implementation
- `agents/analyst_agent_example.py` - Usage examples
- `agents/ANALYST_AGENT_README.md` - Documentation

---

### 2. Guardian Agent 🛡️

**Purpose:** Generates adversarial inputs to stress-test enforcement

**Tech Stack:**
- LangChain + langchain-groq
- High temperature (0.9) for creativity
- 5+ attack categories

**Attack Categories:**
1. Amount Overflow - Exceeds $1000 max
2. Policy Bypass - Tries to override rules
3. Disallowed Symbols - Non-whitelisted stocks/crypto
4. Blocked Actions - SHORT, MARGIN, etc.
5. Prompt Injection - Manipulates LLM parser

**Methods:**
```python
# Generate adversarial inputs (LLM-creative, not hardcoded)
attacks = agent.generate_adversarial_inputs(n=10)

# Run full stress test
pipeline = {"compiler": compiler, "enforcement": enforcement}
report = agent.run_adversarial_test(pipeline)
```

**Output:**
```python
{
    "total": 10,
    "blocked": 10,    # Goal: 100%
    "allowed": 0,     # Goal: 0
    "details": [...]
}
```

**Key Features:**
- ✅ LLM-generated attacks (unique every time)
- ✅ Comprehensive test reporting
- ✅ Fallback mode without API key
- ✅ Temperature: 0.9 (creative)

**Files:**
- `agents/guardian_agent.py` - Main implementation
- `agents/demo_guardian.py` - Interactive demo
- `agents/test_guardian_agent.py` - Test suite
- `agents/guardian_examples.py` - Usage examples
- `agents/GUARDIAN_AGENT_README.md` - Documentation

---

### 3. Master Agent 🎯

**Purpose:** Orchestrates all agents into end-to-end pipeline

**Tech Stack:**
- Pure Python orchestration (NO LLM)
- concurrent.futures for parallel execution
- Comprehensive error handling

**Pipeline Flow:**
```
1. AnalystAgent      → trade_suggestion
2. IntentCompiler    → structured_intent
3. EnforcementLayer  → ALLOW or BLOCK
4. TraderAgent       → trade_result (if ALLOW)
5. GuardianAgent     → adversarial_report (parallel)
6. Logger            → logged
```

**Method:**
```python
master = MasterAgent()

market_context = {
    "symbol": "AAPL",
    "current_price": 175.0,
    "trend": "upward",
    "volume": "high",
    "news_sentiment": "positive"
}

result = master.run(market_context)
```

**Output:**
```python
{
    "analyst_suggestion": {...},
    "intent": {...},
    "enforcement_decision": "ALLOW" | "BLOCK",
    "enforcement_details": {...},
    "trade_result": {...} or None,
    "adversarial_report": {...},
    "timestamp": "2026-04-05T...",
    "duration_seconds": 2.34,
    "status": "completed",
    "errors": []
}
```

**Key Features:**
- ✅ Pure orchestration (NO LLM)
- ✅ Lazy component loading
- ✅ Parallel adversarial testing
- ✅ Fail-safe (never crashes)
- ✅ Comprehensive logging

**Error Handling:**
- AnalystAgent fails → HOLD/0.0 confidence
- IntentCompiler fails → fallback intent
- EnforcementLayer fails → BLOCK (safe)
- TraderAgent fails → success=False
- GuardianAgent fails → warning (non-blocking)

**Files:**
- `agents/master_agent.py` - Main implementation
- `agents/demo_master_agent.py` - Demo without API
- `agents/test_master_agent.py` - Test suite
- `agents/MASTER_AGENT_README.md` - Documentation

---

## Complete Data Flow

```
User Input: Market Context
    ↓
┌────────────────────────────────────────────────────────┐
│ MASTER AGENT                                           │
│                                                        │
│ Step 1: AnalystAgent                                   │
│   Input: market_context                                │
│   Output: {action: BUY, amount: 500, confidence: 0.85} │
│                                                        │
│ Step 2: IntentCompiler                                 │
│   Input: "BUY 500 dollars of AAPL"                     │
│   Output: {action: BUY, symbol: AAPL, amount: 500}     │
│                                                        │
│ Step 3: EnforcementLayer                               │
│   Input: structured_intent                             │
│   Checks: max_amount, allowed_symbols, blocked_actions │
│   Output: {decision: ALLOW, violations: []}            │
│                                                        │
│ Step 4: TraderAgent (if ALLOW)                         │
│   Input: intent                                        │
│   Output: {success: true, order_id: "..."}             │
│                                                        │
│ Step 5: GuardianAgent (parallel)                       │
│   Generates: 10 adversarial attacks                    │
│   Tests: enforcement pipeline                          │
│   Output: {blocked: 10, allowed: 0}                    │
│                                                        │
│ Step 6: Logger                                         │
│   Logs all actions to file and console                 │
│                                                        │
└────────────────────────────────────────────────────────┘
    ↓
Complete Result Dictionary
```

## Quick Start

### 1. Setup

```bash
# Install dependencies
pip install -r requirements.txt

# Set up API key
cp .env.example .env
# Edit .env and add GROQ_API_KEY
```

### 2. Test Individual Agents

```bash
# Test Analyst Agent
python agents/analyst_agent.py

# Test Guardian Agent
python agents/guardian_agent.py

# Test Master Agent (demo)
python agents/demo_master_agent.py
```

### 3. Run Complete Pipeline

```python
from agents.master_agent import MasterAgent

master = MasterAgent()

market_context = {
    "symbol": "AAPL",
    "current_price": 175.0,
    "trend": "upward",
    "volume": "high",
    "news_sentiment": "positive"
}

result = master.run(market_context)

print(f"Decision: {result['enforcement_decision']}")
print(f"Status: {result['status']}")
```

## Testing Summary

| Agent | Test File | Demo File | Requires API Key |
|-------|-----------|-----------|------------------|
| **Analyst** | `analyst_agent.py` (bottom) | `analyst_agent_example.py` | Yes (or fallback) |
| **Guardian** | `guardian_agent.py` (bottom) | `demo_guardian.py` | Yes (or fallback) |
| **Master** | `test_master_agent.py` | `demo_master_agent.py` | No (demo mode) |

## File Structure

```
agents/
├── analyst_agent.py                Main implementation
├── analyst_agent_example.py        Usage examples
├── ANALYST_AGENT_README.md         Documentation
│
├── guardian_agent.py               Main implementation
├── demo_guardian.py                Interactive demo
├── test_guardian_agent.py          Test suite
├── guardian_examples.py            Usage examples
├── GUARDIAN_AGENT_README.md        Documentation
│
├── master_agent.py                 Main implementation
├── demo_master_agent.py            Demo (no API needed)
├── test_master_agent.py            Test suite
├── MASTER_AGENT_README.md          Documentation
│
└── AGENTS_OVERVIEW.md              This file
```

## Performance

| Component | Typical Duration | Notes |
|-----------|-----------------|-------|
| AnalystAgent | 1-2s | LLM call |
| IntentCompiler | 0.5-1s | LLM parsing |
| EnforcementLayer | <0.1s | Deterministic |
| TraderAgent | 0.5-1s | API call |
| GuardianAgent | 5-10s | Parallel, non-blocking |
| **Total Pipeline** | **2-5s** | Without guardian wait |

## Error Rates

**Goal:** 100% uptime with graceful degradation

| Scenario | Behavior | Status Code |
|----------|----------|-------------|
| All components working | Normal execution | `completed` |
| Some components fail | Continues with fallbacks | `completed_with_errors` |
| Critical failure | Safe defaults (BLOCK) | `failed` |

**Master Agent never crashes** - always returns a result.

## Security

1. **Enforcement Layer** (Deterministic)
   - No LLM involvement in security decisions
   - Pure rule-based validation
   - Fail-safe: defaults to BLOCK

2. **Guardian Agent** (Adversarial Testing)
   - Continuously tests enforcement
   - Generates creative attacks
   - Reports: blocked/allowed ratio

3. **Master Agent** (Orchestration)
   - Logs all decisions
   - Error tracking
   - Audit trail

## Future Enhancements

### Analyst Agent
- [ ] Real-time market data integration
- [ ] Multi-timeframe analysis
- [ ] Historical performance tracking

### Guardian Agent
- [ ] Automated daily security scans
- [ ] Attack success alerting
- [ ] Multi-language attacks

### Master Agent
- [ ] Async/await support
- [ ] WebSocket streaming
- [ ] Circuit breaker pattern
- [ ] Metrics and monitoring

## License

Part of the INTENTRA project.

---

**Built with:**
- LangChain
- langchain-groq
- Pydantic
- Python concurrent.futures
- Groq LLMs (Mixtral, Llama)
