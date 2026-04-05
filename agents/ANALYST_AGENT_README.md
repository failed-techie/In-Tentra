# Analyst Agent

The **Analyst Agent** is an LLM-powered component that analyzes market context and generates structured trade suggestions for the INTENTRA trading system.

## Technology Stack

- **LangChain**: Framework for LLM application development
- **langchain-groq**: Groq LLM integration
- **Pydantic**: Structured output parsing and validation

## Features

✅ **Structured Input/Output**: Clearly defined schemas using Pydantic  
✅ **LangChain Prompt Templates**: Professional, maintainable prompts  
✅ **Cautious Analysis**: System prompt designed for low-risk, conservative trading  
✅ **Fallback Safety**: Returns safe HOLD recommendation if parsing fails  
✅ **Flexible Configuration**: Supports custom models and API keys  

## Input Format

The agent expects a `market_context` dictionary with the following structure:

```python
market_context = {
    "symbol": "AAPL",           # Stock symbol
    "current_price": 175.0,      # Current price (float)
    "trend": "upward",           # Trend description (upward/downward/sideways)
    "volume": "high",            # Volume level (high/medium/low)
    "news_sentiment": "positive" # News sentiment (positive/negative/neutral)
}
```

## Output Format

The agent returns a structured dictionary:

```python
{
    "action": "BUY",              # One of: "BUY", "SELL", "HOLD"
    "symbol": "AAPL",             # Stock symbol
    "amount": 1000.0,             # Suggested trade amount in USD
    "confidence": 0.75,           # Confidence level (0.0 to 1.0)
    "reasoning": "Strong upward..." # Detailed reasoning
}
```

## Usage

### Basic Usage

```python
from agents.analyst_agent import AnalystAgent

# Initialize (reads GROQ_API_KEY from .env)
agent = AnalystAgent()

# Analyze market context
market_context = {
    "symbol": "AAPL",
    "current_price": 175.0,
    "trend": "upward",
    "volume": "high",
    "news_sentiment": "positive"
}

suggestion = agent.analyze(market_context)
print(f"Action: {suggestion['action']}")
print(f"Confidence: {suggestion['confidence']}")
print(f"Reasoning: {suggestion['reasoning']}")
```

### Custom Configuration

```python
# Use a different model
agent = AnalystAgent(
    api_key="your-groq-api-key",
    model="llama-3.3-70b-versatile"
)
```

### Available Models

- `mixtral-8x7b-32768` (default)
- `llama-3.3-70b-versatile`
- `llama-3.1-8b-instant`
- Any Groq-supported model

## System Prompt Philosophy

The agent is designed with a **cautious, low-risk** approach:

- ✅ Prioritizes capital preservation
- ✅ Requires strong supporting evidence for trades
- ✅ Considers risk before reward
- ✅ Defaults to HOLD when signals are unclear
- ✅ Transparent about uncertainty
- ✅ Avoids emotional or speculative language

## Error Handling

If the LLM output cannot be parsed (malformed JSON, network errors, etc.), the agent automatically returns a safe fallback:

```python
{
    "action": "HOLD",
    "symbol": "<requested_symbol>",
    "amount": 0.0,
    "confidence": 0.0,
    "reasoning": "Unable to generate recommendation due to parsing error. Defaulting to HOLD for safety."
}
```

This ensures the system never fails catastrophically and always provides a safe response.

## Testing

### Run Standalone Tests

```bash
cd agents
python analyst_agent.py
```

This runs three test scenarios:
1. Strong bullish signals (AAPL)
2. Bearish signals (TSLA)
3. Unclear/mixed signals (MSFT)

### Run Usage Examples

```bash
cd agents
python analyst_agent_example.py
```

## Setup Requirements

1. **Install dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

2. **Set up API key** (choose one):
   
   **Option A**: Use `.env` file (recommended)
   ```bash
   cp .env.example .env
   # Edit .env and add your GROQ_API_KEY
   ```
   
   **Option B**: Export environment variable
   ```bash
   export GROQ_API_KEY='your-key-here'
   ```

3. **Get Groq API key**: https://console.groq.com

## Integration with INTENTRA

The Analyst Agent is part of the INTENTRA multi-agent system:

1. **Master Agent** → Orchestrates the workflow
2. **Analyst Agent** → Analyzes market and suggests trades (this component)
3. **Guardian Agent** → Validates trades against policies
4. **Trader Agent** → Executes approved trades

The Analyst Agent focuses purely on analysis and does not have direct market access. It receives manually provided market context and returns suggestions that are then validated by the Guardian Agent.

## File Structure

```
agents/
├── analyst_agent.py              # Main implementation
├── analyst_agent_example.py      # Usage examples
└── ANALYST_AGENT_README.md       # This file
```

## Future Enhancements

- [ ] Real-time market data integration
- [ ] Historical performance tracking
- [ ] Multi-timeframe analysis
- [ ] Risk-adjusted position sizing
- [ ] Sentiment analysis from multiple sources
- [ ] Technical indicator integration

## License

Part of the INTENTRA project.
