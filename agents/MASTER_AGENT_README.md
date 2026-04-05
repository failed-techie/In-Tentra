# Master Agent - End-to-End Pipeline Orchestrator

The **Master Agent** is the central orchestrator that sequences all agents and modules into a complete end-to-end trading pipeline for INTENTRA.

## Purpose

The Master Agent:
- **Orchestrates** all components in the correct sequence
- **Coordinates** data flow between agents
- **Manages** parallel execution of adversarial testing
- **Handles** errors gracefully (fail-safe design)
- **Logs** all actions and decisions
- **Returns** comprehensive run summaries

## Key Design Principle

**NO LLM** - The Master Agent is pure orchestration logic. It does NOT use any language model itself; it simply coordinates other agents that may use LLMs.

## Architecture

```
MasterAgent.run(market_context)
    │
    ├─[Sequential]────────────────────────────────┐
    │                                              │
    │  1. AnalystAgent.analyze()                  │
    │     ↓ trade_suggestion                      │
    │                                              │
    │  2. IntentCompiler.compile()                │
    │     ↓ structured_intent                     │
    │                                              │
    │  3. EnforcementLayer.enforce()              │
    │     ↓ ALLOW or BLOCK                        │
    │                                              │
    │  4. TraderAgent.execute()  (if ALLOW)       │
    │     ↓ trade_result                          │
    │                                              │
    └──────────────────────────────────────────────┘
    │
    ├─[Parallel]──────────────────────────────────┐
    │                                              │
    │  5. GuardianAgent.run_adversarial_test()    │
    │     ↓ adversarial_report                    │
    │                                              │
    └──────────────────────────────────────────────┘
    │
    └─ 6. Logger.log(all_actions)
       ↓ complete_summary
```

## Pipeline Steps

### Step 1: Analyst Agent
```python
market_context → AnalystAgent.analyze() → trade_suggestion
```
- Analyzes market conditions
- Generates trade recommendations
- Returns: `{"action": "BUY", "symbol": "AAPL", "amount": 500, "confidence": 0.85, "reasoning": "..."}`

### Step 2: Intent Compiler
```python
trade_suggestion → IntentCompiler.compile() → structured_intent
```
- Converts suggestion to natural language
- Parses into structured format
- Returns: `{"action": "BUY", "symbol": "AAPL", "amount": 500, "confidence": 0.85, "raw_input": "..."}`

### Step 3: Enforcement Layer
```python
structured_intent → EnforcementLayer.enforce() → ALLOW | BLOCK
```
- Validates against policies
- Checks max amount, allowed symbols, blocked actions
- Returns: `{"decision": "ALLOW", "reason": "...", "violations": []}`

### Step 4: Trader Agent
```python
(if ALLOW) → TraderAgent.execute() → trade_result
```
- Executes trade via Alpaca API
- Only runs if enforcement decision is ALLOW
- Returns: `{"success": True, "order_id": "...", "status": "submitted"}`

### Step 5: Guardian Agent (Parallel)
```python
pipeline → GuardianAgent.run_adversarial_test() → report
```
- Runs in background (non-blocking)
- Generates adversarial inputs
- Tests enforcement layer
- Returns: `{"total": 10, "blocked": 10, "allowed": 0, "block_rate": "100%"}`

### Step 6: Logging
```python
all_actions → Logger.log() → logged
```
- Logs analyst suggestions
- Logs enforcement decisions
- Logs trade executions
- Logs adversarial test results

## API

### Class: `MasterAgent`

```python
from agents.master_agent import MasterAgent

# Initialize (components lazy-load as needed)
master = MasterAgent()

# Or provide components explicitly
master = MasterAgent(
    analyst_agent=my_analyst,
    guardian_agent=my_guardian,
    intent_compiler=my_compiler,
    enforcement_layer=my_enforcement,
    trader_agent=my_trader,
    logger=my_logger
)
```

### Method: `run(market_context: dict) → dict`

Execute the complete end-to-end pipeline.

**Parameters:**
- `market_context` (dict): Market data with keys:
  - `symbol` (str): Stock symbol (e.g., "AAPL")
  - `current_price` (float): Current stock price
  - `trend` (str): Market trend ("upward", "downward", "sideways")
  - `volume` (str): Volume level ("high", "medium", "low")
  - `news_sentiment` (str): News sentiment ("positive", "negative", "neutral")

**Returns:**
- `dict` with comprehensive summary:
  ```python
  {
      "analyst_suggestion": {...},      # Trade suggestion from AnalystAgent
      "intent": {...},                  # Structured intent from IntentCompiler
      "enforcement_decision": "ALLOW",  # ALLOW or BLOCK
      "enforcement_details": {...},     # Full enforcement result
      "trade_result": {...} or None,    # Trade execution result (if ALLOW)
      "adversarial_report": {...},      # Adversarial test report
      "timestamp": "2026-04-05T...",    # ISO timestamp
      "duration_seconds": 2.34,         # Execution time
      "status": "completed",            # completed | completed_with_errors | failed
      "errors": []                      # List of error messages (if any)
  }
  ```

## Usage Examples

### Example 1: Basic Usage

```python
from agents.master_agent import MasterAgent

# Initialize
master = MasterAgent()

# Prepare market context
market_context = {
    "symbol": "AAPL",
    "current_price": 175.0,
    "trend": "upward",
    "volume": "high",
    "news_sentiment": "positive"
}

# Run pipeline
result = master.run(market_context)

# Check decision
if result["enforcement_decision"] == "ALLOW":
    print(f"✅ Trade executed: {result['trade_result']}")
else:
    print(f"🛡️  Trade blocked: {result['enforcement_details']['reason']}")

# Check for errors
if result["errors"]:
    print(f"⚠️  Errors occurred: {result['errors']}")
```

### Example 2: Multiple Scenarios

```python
master = MasterAgent()

scenarios = [
    {
        "symbol": "AAPL",
        "current_price": 175.0,
        "trend": "upward",
        "volume": "high",
        "news_sentiment": "positive"
    },
    {
        "symbol": "TSLA",
        "current_price": 250.0,
        "trend": "downward",
        "volume": "high",
        "news_sentiment": "negative"
    }
]

for scenario in scenarios:
    result = master.run(scenario)
    print(f"{scenario['symbol']}: {result['enforcement_decision']}")
```

### Example 3: Error Handling

```python
master = MasterAgent()

market_context = {"symbol": "AAPL", ...}

try:
    result = master.run(market_context)
    
    # Master Agent never crashes - check status instead
    if result["status"] == "failed":
        print(f"Pipeline failed: {result['errors']}")
    elif result["status"] == "completed_with_errors":
        print(f"Completed with warnings: {result['errors']}")
    else:
        print("Pipeline completed successfully!")
        
except Exception as e:
    # This should never happen - Master Agent catches all errors
    print(f"Unexpected error: {e}")
```

## Error Handling

The Master Agent implements **fail-safe** error handling. If any component fails:

| Component | Failure Behavior |
|-----------|------------------|
| **AnalystAgent** | Logs error, continues with HOLD/0.0 confidence |
| **IntentCompiler** | Logs error, creates fallback intent |
| **EnforcementLayer** | Logs error, defaults to BLOCK (safe) |
| **TraderAgent** | Logs error, returns `{success: False, error: "..."}` |
| **GuardianAgent** | Logs warning, continues (non-blocking) |

**Key Guarantee:** The Master Agent **NEVER crashes**. It always returns a result, even if all components fail.

## Parallel Execution

The Guardian Agent adversarial test runs in parallel using `concurrent.futures.ThreadPoolExecutor`:

```python
# In run() method:
adversarial_future = self.executor.submit(
    self._run_adversarial_test_safe,
    market_context
)

# Don't block - get result with timeout
try:
    report = adversarial_future.result(timeout=5.0)
except TimeoutError:
    # Adversarial test still running in background
    report = {"status": "running_async"}
```

This ensures the main pipeline doesn't wait for adversarial testing.

## Logging

The Master Agent uses a `SimpleLogger` that logs to both:
1. Python's built-in logging (console output)
2. Log files (`logs/master_agent.log`)

Log levels:
- **INFO**: Normal pipeline steps
- **WARNING**: Non-critical issues (e.g., adversarial test timeout)
- **ERROR**: Component failures (logged but execution continues)

## Testing

### Run Standalone Demo

```bash
python agents/demo_master_agent.py
```

Shows the complete architecture and data flow without requiring API keys.

### Run with API

```bash
# Set API key
export GROQ_API_KEY='your-key-here'

# Run test
python agents/master_agent.py
```

### Run Comprehensive Tests

```bash
python agents/test_master_agent.py
```

Runs multiple scenarios and shows detailed results.

## Output Structure

Complete output from `master.run()`:

```json
{
  "analyst_suggestion": {
    "action": "BUY",
    "symbol": "AAPL",
    "amount": 500.0,
    "confidence": 0.85,
    "reasoning": "Strong upward trend with high volume"
  },
  "intent": {
    "action": "BUY",
    "symbol": "AAPL",
    "amount": 500.0,
    "confidence": 0.85,
    "raw_input": "BUY 500.0 dollars of AAPL"
  },
  "enforcement_decision": "ALLOW",
  "enforcement_details": {
    "decision": "ALLOW",
    "reason": "All enforcement checks passed",
    "violations": []
  },
  "trade_result": {
    "success": true,
    "order_id": "ORDER_20260405_001",
    "symbol": "AAPL",
    "action": "BUY",
    "amount": 500.0,
    "status": "submitted"
  },
  "adversarial_report": {
    "status": "completed",
    "total_attacks": 10,
    "blocked": 10,
    "allowed": 0,
    "block_rate": "100.0%"
  },
  "timestamp": "2026-04-05T04:42:26.018Z",
  "duration_seconds": 2.34,
  "status": "completed",
  "errors": []
}
```

## Component Lazy Loading

Components are lazy-loaded to avoid initialization failures:

```python
master = MasterAgent()  # No components initialized yet

# Components load when run() is called
result = master.run(market_context)  # All components auto-initialized
```

This allows the Master Agent to start even if some dependencies are missing.

## Integration with INTENTRA

The Master Agent is the **central coordinator** in INTENTRA:

```
User Input
    ↓
Market Context (from API or manual)
    ↓
MasterAgent.run()
    ├→ AnalystAgent (market analysis)
    ├→ IntentCompiler (parsing)
    ├→ EnforcementLayer (policy validation)
    ├→ TraderAgent (execution)
    └→ GuardianAgent (security testing)
    ↓
Complete Result
```

## File Structure

```
agents/
├── master_agent.py              # Main implementation
├── demo_master_agent.py         # Demo without API keys
├── test_master_agent.py         # Comprehensive tests
└── MASTER_AGENT_README.md       # This file
```

## Performance

- **Sequential pipeline**: 1-3 seconds (depends on LLM response time)
- **Parallel adversarial test**: Runs in background (5-10 seconds)
- **Total with all components**: ~2-5 seconds for typical case

## Future Enhancements

- [ ] Async/await support for better concurrency
- [ ] WebSocket streaming for real-time updates
- [ ] Database persistence for all runs
- [ ] Retry logic with exponential backoff
- [ ] Circuit breaker pattern for failing components
- [ ] Metrics and monitoring integration

## License

Part of the INTENTRA project.
