"""
Test script for Master Agent
Demonstrates the complete end-to-end pipeline orchestration
"""
import sys
import os
import json

# Add parent directory to path
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))


def print_section(title: str, width: int = 80):
    """Print formatted section header"""
    print("\n" + "=" * width)
    print(title.center(width))
    print("=" * width + "\n")


def print_subsection(title: str, width: int = 80):
    """Print formatted subsection"""
    print("\n" + "-" * width)
    print(title)
    print("-" * width + "\n")


def test_master_agent_basic():
    """Test 1: Basic Master Agent orchestration"""
    print_section("TEST 1: Basic Master Agent Orchestration")
    
    # Import MasterAgent directly
    import importlib.util
    spec = importlib.util.spec_from_file_location('master_agent', 'agents/master_agent.py')
    master_module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(master_module)
    MasterAgent = master_module.MasterAgent
    
    # Check for API key
    api_key = os.getenv("GROQ_API_KEY")
    if not api_key:
        try:
            from config.settings import settings
            api_key = settings.GROQ_API_KEY
            print("✓ Using API key from config\n")
        except:
            print("⚠️  GROQ_API_KEY not found - test will use mock components\n")
    else:
        print("✓ Using API key from environment\n")
    
    if not api_key:
        print("This test requires GROQ_API_KEY to demonstrate the full pipeline.")
        print("Showing structure without execution...\n")
        
        # Show what would happen
        print("Pipeline Structure:")
        print("  1. AnalystAgent: Analyze market context → trade suggestion")
        print("  2. IntentCompiler: Compile suggestion → structured intent")
        print("  3. EnforcementLayer: Validate → ALLOW or BLOCK")
        print("  4. TraderAgent: Execute trade (if allowed)")
        print("  5. GuardianAgent: Run adversarial test (parallel)")
        print("  6. Logger: Log all actions")
        print("\nSet GROQ_API_KEY to see the full execution.")
        return
    
    # Initialize Master Agent with lazy loading
    print("Initializing Master Agent with lazy loading...\n")
    master = MasterAgent()
    
    # Create market context
    market_context = {
        "symbol": "AAPL",
        "current_price": 175.0,
        "trend": "upward",
        "volume": "high",
        "news_sentiment": "positive"
    }
    
    print(f"Market Context:")
    print(json.dumps(market_context, indent=2))
    
    # Run the pipeline
    print_subsection("Running Complete Pipeline...")
    
    try:
        result = master.run(market_context)
        
        # Display results
        print_section("PIPELINE RESULTS")
        
        print("Status:", result.get("status", "unknown"))
        print("Duration:", f"{result.get('duration_seconds', 0):.2f} seconds")
        print("Timestamp:", result.get("timestamp"))
        
        if result.get("errors"):
            print("\n⚠️  Errors:", len(result["errors"]))
            for error in result["errors"]:
                print(f"  - {error}")
        
        print_subsection("1. Analyst Suggestion")
        if result.get("analyst_suggestion"):
            sugg = result["analyst_suggestion"]
            print(f"  Action:     {sugg.get('action')}")
            print(f"  Symbol:     {sugg.get('symbol')}")
            print(f"  Amount:     ${sugg.get('amount', 0):.2f}")
            print(f"  Confidence: {sugg.get('confidence', 0):.2%}")
            print(f"  Reasoning:  {sugg.get('reasoning', 'N/A')[:80]}...")
        else:
            print("  None")
        
        print_subsection("2. Compiled Intent")
        if result.get("intent"):
            intent = result["intent"]
            print(f"  Action:     {intent.get('action')}")
            print(f"  Symbol:     {intent.get('symbol')}")
            print(f"  Amount:     ${intent.get('amount', 0):.2f}")
            print(f"  Confidence: {intent.get('confidence', 0):.2f}")
        else:
            print("  None")
        
        print_subsection("3. Enforcement Decision")
        print(f"  Decision: {result.get('enforcement_decision')}")
        if result.get("enforcement_details"):
            details = result["enforcement_details"]
            print(f"  Reason:   {details.get('reason')}")
            if details.get('violations'):
                print(f"  Violations:")
                for v in details['violations']:
                    print(f"    - {v}")
        
        print_subsection("4. Trade Execution")
        if result.get("trade_result"):
            trade = result["trade_result"]
            if trade.get("success"):
                print(f"  ✅ Trade Executed")
                print(f"     Order ID: {trade.get('order_id')}")
                print(f"     Symbol:   {trade.get('symbol')}")
                print(f"     Action:   {trade.get('action')}")
                print(f"     Status:   {trade.get('status')}")
            else:
                print(f"  ❌ Trade Failed")
                print(f"     Error: {trade.get('error')}")
        else:
            print("  Trade not executed (blocked or error)")
        
        print_subsection("5. Adversarial Report")
        if result.get("adversarial_report"):
            report = result["adversarial_report"]
            if report.get("status") == "completed":
                print(f"  Status:     {report.get('status')}")
                print(f"  Total:      {report.get('total_attacks')}")
                print(f"  Blocked:    {report.get('blocked')}")
                print(f"  Allowed:    {report.get('allowed')}")
                print(f"  Block Rate: {report.get('block_rate')}")
                
                if report.get('allowed', 0) == 0:
                    print("\n  ✅ All adversarial attacks blocked!")
                else:
                    print(f"\n  ⚠️  {report.get('allowed')} attacks were allowed!")
            else:
                print(f"  Status: {report.get('status')}")
                print(f"  Message: {report.get('message', 'N/A')}")
        else:
            print("  None")
        
        print_section("SUMMARY")
        
        if result.get("enforcement_decision") == "ALLOW":
            print("✅ Trade was ALLOWED and executed")
        else:
            print("🛡️  Trade was BLOCKED by enforcement layer")
        
        if not result.get("errors"):
            print("✅ Pipeline completed without errors")
        else:
            print(f"⚠️  Pipeline completed with {len(result['errors'])} errors")
        
    except Exception as e:
        print(f"\n❌ Test failed: {e}")
        import traceback
        traceback.print_exc()


def test_master_agent_scenarios():
    """Test 2: Multiple market scenarios"""
    print_section("TEST 2: Multiple Market Scenarios")
    
    api_key = os.getenv("GROQ_API_KEY")
    if not api_key:
        try:
            from config.settings import settings
            api_key = settings.GROQ_API_KEY
        except:
            pass
    
    if not api_key:
        print("⚠️  Skipping (requires GROQ_API_KEY)\n")
        return
    
    import importlib.util
    spec = importlib.util.spec_from_file_location('master_agent', 'agents/master_agent.py')
    master_module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(master_module)
    MasterAgent = master_module.MasterAgent
    
    master = MasterAgent()
    
    scenarios = [
        {
            "name": "Bullish Scenario",
            "context": {
                "symbol": "TSLA",
                "current_price": 250.0,
                "trend": "upward",
                "volume": "high",
                "news_sentiment": "positive"
            }
        },
        {
            "name": "Bearish Scenario",
            "context": {
                "symbol": "MSFT",
                "current_price": 420.0,
                "trend": "downward",
                "volume": "high",
                "news_sentiment": "negative"
            }
        },
        {
            "name": "Neutral Scenario",
            "context": {
                "symbol": "GOOGL",
                "current_price": 140.0,
                "trend": "sideways",
                "volume": "low",
                "news_sentiment": "neutral"
            }
        }
    ]
    
    results_summary = []
    
    for scenario in scenarios:
        print_subsection(scenario["name"])
        print(f"Context: {json.dumps(scenario['context'], indent=2)}\n")
        
        try:
            result = master.run(scenario["context"])
            
            summary = {
                "scenario": scenario["name"],
                "decision": result.get("enforcement_decision"),
                "action": result.get("analyst_suggestion", {}).get("action"),
                "confidence": result.get("analyst_suggestion", {}).get("confidence"),
                "executed": result.get("trade_result", {}).get("success", False)
            }
            results_summary.append(summary)
            
            print(f"Analyst Suggestion: {summary['action']} (confidence: {summary.get('confidence', 0):.2%})")
            print(f"Enforcement Decision: {summary['decision']}")
            print(f"Trade Executed: {summary['executed']}")
            
        except Exception as e:
            print(f"❌ Scenario failed: {e}")
    
    print_subsection("Summary Table")
    print(f"{'Scenario':<20} {'Action':<8} {'Decision':<10} {'Executed':<10}")
    print("-" * 50)
    for s in results_summary:
        print(f"{s['scenario']:<20} {s['action']:<8} {s['decision']:<10} {str(s['executed']):<10}")


def main():
    """Main test runner"""
    print()
    print("╔" + "=" * 78 + "╗")
    print("║" + " MASTER AGENT - END-TO-END PIPELINE TEST ".center(78) + "║")
    print("╚" + "=" * 78 + "╝")
    
    # Test 1: Basic orchestration
    test_master_agent_basic()
    
    # Test 2: Multiple scenarios
    test_master_agent_scenarios()
    
    print("\n" + "=" * 80)
    print("ALL TESTS COMPLETE".center(80))
    print("=" * 80)
    print()


if __name__ == "__main__":
    main()
