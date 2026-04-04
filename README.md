# INTENTRA - Multi-Agent AI Trading System

A sophisticated Python-based trading system that uses multiple AI agents to analyze, validate, and execute trades through a rule-based intent compilation framework.

## 🏗️ Architecture

INTENTRA uses a multi-agent architecture where each agent has a specific responsibility:

- **Master Agent**: Orchestrates the workflow between all other agents
- **Analyst Agent**: Performs market analysis and generates trading recommendations
- **Guardian Agent**: Validates trades against policies and risk parameters
- **Trader Agent**: Executes approved trades via Alpaca API

## 📁 Project Structure

```
In-Tentra/
├── main.py                 # FastAPI application entry point
├── requirements.txt        # Python dependencies
├── .env.example           # Environment variables template
├── README.md              # This file
│
├── agents/                # AI agent implementations
│   ├── __init__.py
│   ├── master_agent.py    # Main orchestrator
│   ├── analyst_agent.py   # Market analysis
│   ├── guardian_agent.py  # Policy validation
│   └── trader_agent.py    # Trade execution
│
├── core/                  # Core business logic
│   ├── __init__.py
│   ├── intent_compiler.py # Intent parsing & normalization
│   ├── policy_engine.py   # Policy evaluation
│   └── enforcement_layer.py # Final validation checks
│
├── db/                    # Database layer
│   ├── __init__.py
│   ├── database.py        # Database configuration
│   └── models.py          # SQLAlchemy models
│
├── config/                # Configuration
│   ├── __init__.py
│   ├── settings.py        # Application settings
│   └── policies.json      # Trading policies
│
└── logs/                  # Logs and database
    └── .gitkeep
```

## 🚀 Quick Start

### 1. Install Dependencies

```bash
pip install -r requirements.txt
```

### 2. Configure Environment

Copy `.env.example` to `.env` and fill in your API keys:

```bash
cp .env.example .env
```

Required API keys:
- **Groq API**: Get from https://console.groq.com
- **Alpaca API**: Get from https://alpaca.markets (use paper trading for testing)

### 3. Run the Server

```bash
python main.py
```

The API will be available at `http://localhost:8000`

### 4. Test the API

```bash
# Health check
curl http://localhost:8000/health

# Submit a trading intent
curl -X POST http://localhost:8000/intent/submit \
  -H "Content-Type: application/json" \
  -d '{
    "symbol": "AAPL",
    "action": "buy",
    "quantity": 10,
    "order_type": "market"
  }'
```

## 🔧 Tech Stack

- **FastAPI**: Modern web framework for building APIs
- **LangChain**: Framework for LLM-powered applications
- **Groq**: Fast LLM inference via langchain-groq
- **Alpaca**: Stock trading API
- **SQLAlchemy**: SQL toolkit and ORM
- **SQLite**: Lightweight database for intent logging

## 📊 Workflow

1. **Intent Submission**: User submits trading intent (structured or natural language)
2. **Intent Compilation**: Intent is parsed and normalized into standard format
3. **Market Analysis**: Analyst agent evaluates market conditions
4. **Policy Validation**: Guardian agent checks against policies and risk limits
5. **Enforcement**: Final real-time checks (buying power, market hours, etc.)
6. **Execution**: Trader agent places order via Alpaca API
7. **Logging**: Results stored in database for audit trail

## 🛡️ Safety Features

- **Policy Engine**: Enforces position limits, order value caps, and symbol restrictions
- **Risk Assessment**: Evaluates risk level before execution
- **Enforcement Layer**: Real-time validation of account balance and market conditions
- **Audit Trail**: All intents and executions logged to database

## 📝 Configuration

### Trading Policies (`config/policies.json`)

Customize trading rules:
- Position and order limits
- Risk parameters
- Symbol restrictions
- Compliance requirements

### Environment Variables (`.env`)

Configure API keys and system settings:
- Server configuration
- API credentials
- Database URL
- Agent parameters

## 🔄 Development Status

This is a **starter template** with:
- ✅ Complete project structure
- ✅ All modules with proper imports
- ✅ Placeholder functions ready for implementation
- ✅ No circular dependencies
- ⚠️ TODO: Implement actual LLM calls
- ⚠️ TODO: Implement Alpaca API integration
- ⚠️ TODO: Add comprehensive error handling
- ⚠️ TODO: Add authentication/authorization

## 📚 Next Steps

1. **Implement LLM Integration**: Complete the LLM invocations in analyst and compiler
2. **Activate Alpaca API**: Uncomment and test Alpaca trading functions
3. **Add Tests**: Create unit and integration tests
4. **Enhance Policies**: Customize policies for your trading strategy
5. **Add Authentication**: Secure the API endpoints
6. **Deploy**: Set up production environment

## ⚠️ Disclaimer

This is a development framework. **DO NOT use with real money without thorough testing.** Always use Alpaca's paper trading environment during development.

## 📄 License

MIT License - See LICENSE file for details

---

**Note**: This project structure is designed to be modular and extensible. Each component can be enhanced independently without affecting the others.
