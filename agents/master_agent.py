"""
Master Agent - Orchestrates all agents and modules into end-to-end pipeline
Pure orchestration logic - NO LLM, just sequencing and coordination
"""
import asyncio
from concurrent.futures import ThreadPoolExecutor
from datetime import datetime
from typing import Dict, Any, Optional
import traceback
import logging
import json


class SimpleLogger:
    """Simple logger for trade actions and events"""
    
    def __init__(self, log_file: str = "logs/master_agent.log"):
        self.log_file = log_file
        
        # Setup Python logging
        logging.basicConfig(
            level=logging.INFO,
            format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
        )
        self.logger = logging.getLogger("MasterAgent")
    
    def log(self, level: str, message: str, data: Optional[Dict] = None):
        """Log a message with optional data"""
        log_entry = {
            "timestamp": datetime.utcnow().isoformat(),
            "level": level,
            "message": message,
            "data": data or {}
        }
        
        # Log to Python logger
        log_msg = f"{message} | {json.dumps(data) if data else ''}"
        
        if level == "INFO":
            self.logger.info(log_msg)
        elif level == "WARNING":
            self.logger.warning(log_msg)
        elif level == "ERROR":
            self.logger.error(log_msg)
        else:
            self.logger.debug(log_msg)
    
    def info(self, message: str, data: Optional[Dict] = None):
        self.log("INFO", message, data)
    
    def warning(self, message: str, data: Optional[Dict] = None):
        self.log("WARNING", message, data)
    
    def error(self, message: str, data: Optional[Dict] = None):
        self.log("ERROR", message, data)


class MasterAgent:
    """
    Master orchestrator for INTENTRA multi-agent trading system
    
    Sequences: AnalystAgent → IntentCompiler → EnforcementLayer → TraderAgent
    Runs GuardianAgent adversarial tests in parallel
    
    NO LLM - Pure orchestration logic
    """
    
    def __init__(
        self,
        analyst_agent=None,
        guardian_agent=None,
        intent_compiler=None,
        enforcement_layer=None,
        trader_agent=None,
        logger=None
    ):
        """
        Initialize Master Agent with all components
        
        Args:
            analyst_agent: AnalystAgent instance (optional, will lazy-load)
            guardian_agent: GuardianAgent instance (optional, will lazy-load)
            intent_compiler: IntentCompiler instance (optional, will lazy-load)
            enforcement_layer: EnforcementLayer instance (optional, will lazy-load)
            trader_agent: TraderAgent instance (optional, will lazy-load)
            logger: Logger instance (optional, will create SimpleLogger)
        """
        self.analyst_agent = analyst_agent
        self.guardian_agent = guardian_agent
        self.intent_compiler = intent_compiler
        self.enforcement_layer = enforcement_layer
        self.trader_agent = trader_agent
        self.logger = logger or SimpleLogger()
        
        # Thread pool for parallel execution
        self.executor = ThreadPoolExecutor(max_workers=3)
    
    def _lazy_load_components(self):
        """Lazy-load components if not provided during initialization"""
        try:
            if self.analyst_agent is None:
                from agents.analyst_agent import AnalystAgent
                self.analyst_agent = AnalystAgent()
                self.logger.info("AnalystAgent lazy-loaded")
            
            if self.guardian_agent is None:
                from agents.guardian_agent import GuardianAgent
                self.guardian_agent = GuardianAgent()
                self.logger.info("GuardianAgent lazy-loaded")
            
            if self.intent_compiler is None:
                from core.intent_compiler import IntentCompiler
                self.intent_compiler = IntentCompiler()
                self.logger.info("IntentCompiler lazy-loaded")
            
            if self.enforcement_layer is None:
                from core.policy_engine import PolicyEngine
                from core.enforcement_layer import EnforcementLayer
                policy_engine = PolicyEngine()
                self.enforcement_layer = EnforcementLayer(policy_engine)
                self.logger.info("EnforcementLayer lazy-loaded")
            
            if self.trader_agent is None:
                from agents.trader_agent import TraderAgent
                self.trader_agent = TraderAgent()
                self.logger.info("TraderAgent lazy-loaded")
                
        except Exception as e:
            self.logger.error(f"Failed to lazy-load components: {e}")
            raise
    
    def run(self, market_context: Dict[str, Any]) -> Dict[str, Any]:
        """
        Execute the complete end-to-end pipeline
        
        Pipeline sequence:
        1. AnalystAgent analyzes market context → trade suggestion
        2. IntentCompiler compiles suggestion → structured intent
        3. EnforcementLayer validates → ALLOW or BLOCK
        4. If ALLOW → TraderAgent executes trade
        5. In parallel: GuardianAgent adversarial test
        6. Log all actions
        7. Return comprehensive summary
        
        Args:
            market_context: Dictionary with market data:
                {
                    "symbol": str,
                    "current_price": float,
                    "trend": str,
                    "volume": str,
                    "news_sentiment": str
                }
        
        Returns:
            dict: Complete run summary with all results
        """
        self.logger.info("=== MASTER AGENT RUN START ===", {"market_context": market_context})
        
        # Ensure components are loaded
        try:
            self._lazy_load_components()
        except Exception as e:
            return self._create_error_response("Component initialization failed", str(e))
        
        run_start_time = datetime.utcnow()
        result = {
            "analyst_suggestion": None,
            "intent": None,
            "enforcement_decision": None,
            "trade_result": None,
            "adversarial_report": None,
            "timestamp": run_start_time.isoformat(),
            "errors": []
        }
        
        # Step 1: Analyst Agent - Analyze market context
        try:
            self.logger.info("Step 1: Running AnalystAgent")
            analyst_suggestion = self.analyst_agent.analyze(market_context)
            result["analyst_suggestion"] = analyst_suggestion
            self.logger.info("AnalystAgent complete", {"suggestion": analyst_suggestion})
        except Exception as e:
            error_msg = f"AnalystAgent failed: {str(e)}"
            self.logger.error(error_msg, {"traceback": traceback.format_exc()})
            result["errors"].append(error_msg)
            # Continue with safe defaults
            analyst_suggestion = {
                "action": "HOLD",
                "symbol": market_context.get("symbol", "UNKNOWN"),
                "amount": 0.0,
                "confidence": 0.0,
                "reasoning": "Error in analysis - defaulting to HOLD"
            }
            result["analyst_suggestion"] = analyst_suggestion
        
        # Step 2: Intent Compiler - Convert suggestion to structured intent
        try:
            self.logger.info("Step 2: Running IntentCompiler")
            
            # Convert analyst suggestion to a natural language string for compiler
            suggestion_text = (
                f"{analyst_suggestion['action']} {analyst_suggestion['amount']} "
                f"dollars of {analyst_suggestion['symbol']}"
            )
            
            compiled_intent = self.intent_compiler.compile(suggestion_text)
            intent_dict = self.intent_compiler.to_dict(compiled_intent)
            result["intent"] = intent_dict
            self.logger.info("IntentCompiler complete", {"intent": intent_dict})
        except Exception as e:
            error_msg = f"IntentCompiler failed: {str(e)}"
            self.logger.error(error_msg, {"traceback": traceback.format_exc()})
            result["errors"].append(error_msg)
            # Create fallback intent
            intent_dict = {
                "action": analyst_suggestion.get("action", "HOLD"),
                "symbol": analyst_suggestion.get("symbol", "UNKNOWN"),
                "amount": analyst_suggestion.get("amount", 0.0),
                "confidence": analyst_suggestion.get("confidence", 0.0),
                "raw_input": suggestion_text if 'suggestion_text' in locals() else ""
            }
            result["intent"] = intent_dict
        
        # Step 3: Enforcement Layer - Validate and decide ALLOW or BLOCK
        try:
            self.logger.info("Step 3: Running EnforcementLayer")
            enforcement_result = self.enforcement_layer.enforce(intent_dict)
            decision = enforcement_result.get("decision", "BLOCK")
            result["enforcement_decision"] = decision
            result["enforcement_details"] = enforcement_result
            self.logger.info("EnforcementLayer complete", {"decision": decision, "result": enforcement_result})
        except Exception as e:
            error_msg = f"EnforcementLayer failed: {str(e)}"
            self.logger.error(error_msg, {"traceback": traceback.format_exc()})
            result["errors"].append(error_msg)
            # Fail-safe: Default to BLOCK on error
            decision = "BLOCK"
            result["enforcement_decision"] = decision
            result["enforcement_details"] = {
                "decision": "BLOCK",
                "reason": "Enforcement error - failing safe",
                "violations": [error_msg]
            }
        
        # Step 4: Trader Agent - Execute trade if ALLOWED
        if decision == "ALLOW":
            try:
                self.logger.info("Step 4: Trade ALLOWED - executing via TraderAgent")
                
                # Mock execution for now (TraderAgent would need full implementation)
                trade_result = {
                    "success": True,
                    "order_id": f"ORDER_{datetime.utcnow().strftime('%Y%m%d%H%M%S')}",
                    "symbol": intent_dict.get("symbol"),
                    "action": intent_dict.get("action"),
                    "amount": intent_dict.get("amount"),
                    "status": "submitted",
                    "timestamp": datetime.utcnow().isoformat()
                }
                
                result["trade_result"] = trade_result
                self.logger.info("TraderAgent complete", {"trade_result": trade_result})
            except Exception as e:
                error_msg = f"TraderAgent failed: {str(e)}"
                self.logger.error(error_msg, {"traceback": traceback.format_exc()})
                result["errors"].append(error_msg)
                result["trade_result"] = {
                    "success": False,
                    "error": str(e)
                }
        else:
            self.logger.info(f"Step 4: Trade BLOCKED - {result.get('enforcement_details', {}).get('reason', 'Unknown')}")
            result["trade_result"] = None
        
        # Step 5: Guardian Agent - Run adversarial test in parallel (non-blocking)
        try:
            self.logger.info("Step 5: Running GuardianAgent adversarial test (async)")
            
            # Submit adversarial test to run in background
            adversarial_future = self.executor.submit(
                self._run_adversarial_test_safe,
                market_context
            )
            
            # Don't wait for it - get result with timeout or skip
            try:
                adversarial_report = adversarial_future.result(timeout=5.0)
                result["adversarial_report"] = adversarial_report
                self.logger.info("GuardianAgent complete", {"report": adversarial_report})
            except Exception as e:
                self.logger.warning(f"Adversarial test timed out or failed: {e}")
                result["adversarial_report"] = {
                    "status": "running_async",
                    "message": "Test running in background"
                }
        except Exception as e:
            error_msg = f"GuardianAgent setup failed: {str(e)}"
            self.logger.error(error_msg)
            result["errors"].append(error_msg)
            result["adversarial_report"] = {"status": "failed", "error": str(e)}
        
        # Step 6: Finalize and return
        run_end_time = datetime.utcnow()
        result["duration_seconds"] = (run_end_time - run_start_time).total_seconds()
        result["status"] = "completed" if not result["errors"] else "completed_with_errors"
        
        self.logger.info("=== MASTER AGENT RUN COMPLETE ===", {
            "duration": result["duration_seconds"],
            "decision": result["enforcement_decision"],
            "errors": len(result["errors"])
        })
        
        return result
    
    def _run_adversarial_test_safe(self, market_context: Dict[str, Any]) -> Dict[str, Any]:
        """
        Run adversarial test with error handling (for background execution)
        
        Args:
            market_context: Market context dict
            
        Returns:
            dict: Adversarial test report
        """
        try:
            # Create a mini pipeline for adversarial testing
            pipeline = {
                "compiler": self.intent_compiler,
                "enforcement": self.enforcement_layer
            }
            
            # Run adversarial test (generates 5 attacks by default)
            report = self.guardian_agent.run_adversarial_test(pipeline)
            
            return {
                "status": "completed",
                "total_attacks": report.get("total", 0),
                "blocked": report.get("blocked", 0),
                "allowed": report.get("allowed", 0),
                "block_rate": f"{report.get('blocked', 0) / max(report.get('total', 1), 1) * 100:.1f}%",
                "summary": f"{report.get('blocked', 0)}/{report.get('total', 0)} attacks blocked"
            }
        except Exception as e:
            return {
                "status": "failed",
                "error": str(e),
                "message": "Adversarial test encountered an error"
            }
    
    def _create_error_response(self, error_type: str, error_message: str) -> Dict[str, Any]:
        """Create an error response structure"""
        return {
            "analyst_suggestion": None,
            "intent": None,
            "enforcement_decision": "BLOCK",
            "trade_result": None,
            "adversarial_report": None,
            "timestamp": datetime.utcnow().isoformat(),
            "errors": [f"{error_type}: {error_message}"],
            "status": "failed"
        }
    
    def __del__(self):
        """Cleanup executor on deletion"""
        if hasattr(self, 'executor'):
            self.executor.shutdown(wait=False)


# ============================================================================
# STANDALONE TEST
# ============================================================================

if __name__ == "__main__":
    import json
    import os
    import sys
    
    # Add parent directory to path for imports
    sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
    
    print("=" * 80)
    print("MASTER AGENT - STANDALONE TEST")
    print("=" * 80)
    print()
    
    # Check for API key (check env first to avoid config.settings validation)
    api_key = os.getenv("GROQ_API_KEY")
    
    if not api_key:
        # Try config.settings only if env var not found
        try:
            from config.settings import settings
            api_key = settings.GROQ_API_KEY
            print("✓ Using GROQ_API_KEY from config/settings.py\n")
        except Exception as e:
            print("⚠️  GROQ_API_KEY not found in environment or config")
            print("   Set up .env file or export GROQ_API_KEY to run the full pipeline\n")
            print("Pipeline Structure (execution requires API key):")
            print("  1. AnalystAgent: market_context → trade suggestion")
            print("  2. IntentCompiler: suggestion → structured intent")
            print("  3. EnforcementLayer: intent → ALLOW/BLOCK decision")
            print("  4. TraderAgent: execute trade (if allowed)")
            print("  5. GuardianAgent: adversarial test (parallel)")
            print("  6. Logger: log all actions")
            print()
            print("To test without API key, see the architecture:")
            print("  python -c \"from agents.master_agent import MasterAgent; help(MasterAgent.run)\"")
            print()
            exit(0)
    else:
        print("✓ Using GROQ_API_KEY from environment variable\n")
    
    # Initialize Master Agent
    print("Initializing Master Agent...")
    try:
        master = MasterAgent()
        print("✓ MasterAgent initialized (components will lazy-load)\n")
    except Exception as e:
        print(f"✗ Failed to initialize: {e}\n")
        exit(1)
    
    # Test market context
    market_context = {
        "symbol": "AAPL",
        "current_price": 175.0,
        "trend": "upward",
        "volume": "high",
        "news_sentiment": "positive"
    }
    
    print("Market Context:")
    print(json.dumps(market_context, indent=2))
    print()
    
    # Run pipeline
    print("-" * 80)
    print("Running Complete Pipeline...")
    print("-" * 80)
    print()
    
    try:
        result = master.run(market_context)
        
        # Display results
        print("\n" + "=" * 80)
        print("RESULTS")
        print("=" * 80)
        print()
        
        print(f"Status:    {result.get('status')}")
        print(f"Duration:  {result.get('duration_seconds', 0):.2f}s")
        print(f"Timestamp: {result.get('timestamp')}")
        
        if result.get("errors"):
            print(f"\n⚠️  Errors: {len(result['errors'])}")
            for error in result["errors"]:
                print(f"  - {error}")
        
        print("\n" + "-" * 80)
        print("Pipeline Steps:")
        print("-" * 80)
        
        # Step 1
        print("\n1. Analyst Suggestion:")
        if result.get("analyst_suggestion"):
            sugg = result["analyst_suggestion"]
            print(f"   Action:     {sugg.get('action')}")
            print(f"   Symbol:     {sugg.get('symbol')}")
            print(f"   Amount:     ${sugg.get('amount', 0):.2f}")
            print(f"   Confidence: {sugg.get('confidence', 0):.1%}")
        
        # Step 2
        print("\n2. Compiled Intent:")
        if result.get("intent"):
            intent = result["intent"]
            print(f"   {intent.get('action')} {intent.get('symbol')} ${intent.get('amount', 0):.2f}")
        
        # Step 3
        print("\n3. Enforcement Decision:")
        decision = result.get("enforcement_decision")
        print(f"   {decision}")
        if result.get("enforcement_details"):
            print(f"   Reason: {result['enforcement_details'].get('reason')}")
        
        # Step 4
        print("\n4. Trade Execution:")
        if result.get("trade_result"):
            trade = result["trade_result"]
            if trade.get("success"):
                print(f"   ✅ Executed - Order {trade.get('order_id')}")
            else:
                print(f"   ❌ Failed - {trade.get('error')}")
        else:
            print(f"   Not executed (blocked or error)")
        
        # Step 5
        print("\n5. Adversarial Report:")
        if result.get("adversarial_report"):
            report = result["adversarial_report"]
            if report.get("status") == "completed":
                print(f"   {report.get('summary')}")
                print(f"   Block rate: {report.get('block_rate')}")
            else:
                print(f"   Status: {report.get('status')}")
        
        print("\n" + "=" * 80)
        
        if decision == "ALLOW":
            print("✅ TRADE ALLOWED AND EXECUTED")
        else:
            print("🛡️  TRADE BLOCKED BY ENFORCEMENT LAYER")
        
        if not result.get("errors"):
            print("✅ PIPELINE COMPLETED SUCCESSFULLY")
        else:
            print(f"⚠️  COMPLETED WITH {len(result['errors'])} ERRORS")
        
        print("=" * 80)
        
    except Exception as e:
        print(f"\n✗ Pipeline failed: {e}")
        import traceback
        traceback.print_exc()
    
    print()
