"""
Master Agent - Simple Demo
Shows the orchestration structure and flow without requiring API keys
"""
import json


def demo_without_api_key():
    """Demonstrate Master Agent structure without API calls"""
    print("=" * 80)
    print("MASTER AGENT - ARCHITECTURE DEMO")
    print("=" * 80)
    print()
    
    print("Master Agent Orchestration Flow:")
    print("-" * 80)
    print()
    
    # Simulate a run
    print("INPUT: Market Context")
    market_context = {
        "symbol": "AAPL",
        "current_price": 175.0,
        "trend": "upward",
        "volume": "high",
        "news_sentiment": "positive"
    }
    print(json.dumps(market_context, indent=2))
    print()
    
    print("-" * 80)
    print("PIPELINE EXECUTION:")
    print("-" * 80)
    print()
    
    # Step 1
    print("Step 1: AnalystAgent.analyze(market_context)")
    print("  → Analyzes market conditions")
    print("  → Generates trade suggestion")
    analyst_suggestion = {
        "action": "BUY",
        "symbol": "AAPL",
        "amount": 500.0,
        "confidence": 0.85,
        "reasoning": "Strong upward trend with high volume and positive sentiment"
    }
    print(f"  Output: {json.dumps(analyst_suggestion, indent=10)}")
    print()
    
    # Step 2
    print("Step 2: IntentCompiler.compile(suggestion)")
    print("  → Converts suggestion to natural language")
    print("  → Parses into structured intent")
    intent = {
        "action": "BUY",
        "symbol": "AAPL",
        "amount": 500.0,
        "confidence": 0.85,
        "raw_input": "BUY 500.0 dollars of AAPL"
    }
    print(f"  Output: {json.dumps(intent, indent=10)}")
    print()
    
    # Step 3
    print("Step 3: EnforcementLayer.enforce(intent)")
    print("  → Validates against policies")
    print("  → Checks: max amount ($1000), allowed symbols, blocked actions")
    enforcement_result = {
        "decision": "ALLOW",
        "reason": "All enforcement checks passed",
        "violations": []
    }
    print(f"  Output: {json.dumps(enforcement_result, indent=10)}")
    print()
    
    # Step 4
    print("Step 4: TraderAgent.execute(intent)")
    print("  → (Only if decision == ALLOW)")
    print("  → Executes trade via Alpaca API")
    trade_result = {
        "success": True,
        "order_id": "ORDER_20260405_001",
        "symbol": "AAPL",
        "action": "BUY",
        "amount": 500.0,
        "status": "submitted"
    }
    print(f"  Output: {json.dumps(trade_result, indent=10)}")
    print()
    
    # Step 5
    print("Step 5: GuardianAgent.run_adversarial_test(pipeline)")
    print("  → Runs in parallel (non-blocking)")
    print("  → Generates adversarial inputs")
    print("  → Tests enforcement layer")
    adversarial_report = {
        "status": "completed",
        "total_attacks": 10,
        "blocked": 10,
        "allowed": 0,
        "block_rate": "100.0%"
    }
    print(f"  Output: {json.dumps(adversarial_report, indent=10)}")
    print()
    
    # Step 6
    print("Step 6: Logger.log(all_actions)")
    print("  → Logs analyst suggestion")
    print("  → Logs enforcement decision")
    print("  → Logs trade execution")
    print("  → Logs adversarial test results")
    print()
    
    print("=" * 80)
    print("FINAL OUTPUT:")
    print("=" * 80)
    print()
    
    final_result = {
        "analyst_suggestion": analyst_suggestion,
        "intent": intent,
        "enforcement_decision": enforcement_result["decision"],
        "enforcement_details": enforcement_result,
        "trade_result": trade_result,
        "adversarial_report": adversarial_report,
        "timestamp": "2026-04-05T04:42:26.018Z",
        "duration_seconds": 2.34,
        "status": "completed",
        "errors": []
    }
    
    print(json.dumps(final_result, indent=2))
    print()
    
    print("=" * 80)
    print("KEY FEATURES:")
    print("=" * 80)
    print()
    print("✅ Pure orchestration (NO LLM in Master Agent)")
    print("✅ Sequential execution of main pipeline")
    print("✅ Parallel execution of adversarial testing")
    print("✅ Comprehensive error handling (fail-safe)")
    print("✅ Complete logging of all actions")
    print("✅ Structured output with all results")
    print()
    
    print("=" * 80)
    print("ERROR HANDLING:")
    print("=" * 80)
    print()
    print("If AnalystAgent fails:")
    print("  → Logs error, continues with HOLD/0.0 confidence")
    print()
    print("If IntentCompiler fails:")
    print("  → Logs error, creates fallback intent")
    print()
    print("If EnforcementLayer fails:")
    print("  → Logs error, defaults to BLOCK (fail-safe)")
    print()
    print("If TraderAgent fails:")
    print("  → Logs error, returns trade_result with success=False")
    print()
    print("If GuardianAgent fails:")
    print("  → Logs warning, continues (non-blocking)")
    print()
    print("Master Agent NEVER crashes - always returns a result")
    print()


def show_api_usage():
    """Show how to use Master Agent with API"""
    print("=" * 80)
    print("USAGE WITH API")
    print("=" * 80)
    print()
    
    print("from agents.master_agent import MasterAgent")
    print()
    print("# Initialize")
    print("master = MasterAgent()")
    print()
    print("# Prepare market context")
    print("market_context = {")
    print('    "symbol": "AAPL",')
    print('    "current_price": 175.0,')
    print('    "trend": "upward",')
    print('    "volume": "high",')
    print('    "news_sentiment": "positive"')
    print("}")
    print()
    print("# Run complete pipeline")
    print("result = master.run(market_context)")
    print()
    print("# Check results")
    print('if result["enforcement_decision"] == "ALLOW":')
    print('    print(f"✅ Trade executed: {result[\'trade_result\']}")')
    print("else:")
    print('    print(f"🛡️  Trade blocked: {result[\'enforcement_details\']}")')
    print()
    print('if result["errors"]:')
    print('    print(f"⚠️  Errors: {result[\'errors\']}")')
    print()


def main():
    print()
    print("╔" + "=" * 78 + "╗")
    print("║" + " MASTER AGENT - ORCHESTRATION DEMO ".center(78) + "║")
    print("╚" + "=" * 78 + "╝")
    print()
    
    demo_without_api_key()
    show_api_usage()
    
    print("=" * 80)
    print()
    print("To run with real API:")
    print("  1. Set GROQ_API_KEY in environment or .env file")
    print("  2. Run: python agents/master_agent.py")
    print()
    print("=" * 80)


if __name__ == "__main__":
    main()
