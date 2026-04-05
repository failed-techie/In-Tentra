"""
Enforcement Layer - Final gatekeeper before trade execution
DETERMINISTIC - No LLM, pure Python logic
"""
from typing import Dict, Any, List
from datetime import datetime


class EnforcementLayer:
    """
    Final enforcement layer that makes ALLOW/BLOCK decisions
    Uses PolicyEngine for rule validation
    
    NO LLM INVOLVEMENT - All decisions are rule-based
    """
    
    def __init__(self, policy_engine):
        """
        Initialize enforcement layer
        
        Args:
            policy_engine: PolicyEngine instance for validation
        """
        self.policy_engine = policy_engine
        self.daily_trade_count = 0  # In production, load from database
    
    def enforce(self, intent: Dict[str, Any]) -> Dict[str, Any]:
        """
        Make final ALLOW or BLOCK decision on trade intentS
        
        Args:
            intent: Trading intent with keys:
                - symbol: str
                - action: str
                - amount: float
                - quantity: int (optional)
        
        Returns:
            dict: {
                "decision": "ALLOW" | "BLOCK",
                "reason": str,
                "violations": list[str] (if BLOCK)
            }
        """
        # Step 1: Validate against policies
        validation_result = self.policy_engine.validate(intent)
        
        if not validation_result["valid"]:
            return {
                "decision": "BLOCK",
                "reason": "Policy violations detected",
                "violations": validation_result["violations"]
            }
        
        # Step 2: Check daily trade limit
        max_daily = self.policy_engine.get_policy("max_daily_trades", float('inf'))
        if self.daily_trade_count >= max_daily:
            return {
                "decision": "BLOCK",
                "reason": f"Daily trade limit reached ({max_daily} trades)",
                "violations": [f"Current count: {self.daily_trade_count}, Max: {max_daily}"]
            }
        
        # Step 3: Additional runtime checks
        runtime_checks = self._perform_runtime_checks(intent)
        if not runtime_checks["passed"]:
            return {
                "decision": "BLOCK",
                "reason": runtime_checks["reason"],
                "violations": runtime_checks.get("violations", [])
            }
        
        # All checks passed - ALLOW the trade
        return {
            "decision": "ALLOW",
            "reason": "All enforcement checks passed",
            "violations": []
        }
    
    def _perform_runtime_checks(self, intent: Dict[str, Any]) -> Dict[str, Any]:
        """
        Perform additional runtime validation checks
        
        Args:
            intent: Trading intent
            
        Returns:
            dict: Check result
        """
        violations = []
        
        # Check 1: Validate data types
        amount = intent.get("amount")
        if not isinstance(amount, (int, float)):
            violations.append("Amount must be a number")
        elif amount <= 0:
            violations.append("Amount must be greater than 0")
        
        # Check 2: Validate symbol format (basic check)
        symbol = intent.get("symbol", "")
        if not symbol or not symbol.replace(".", "").isalnum():
            violations.append("Invalid symbol format")
        
        # Check 3: Validate action is uppercase
        action = intent.get("action", "")
        if action != action.upper():
            violations.append("Action must be uppercase")
        
        if violations:
            return {
                "passed": False,
                "reason": "Runtime validation failed",
                "violations": violations
            }
        
        return {"passed": True, "reason": "Runtime checks passed"}
    
    def increment_daily_count(self) -> None:
        """
        Increment daily trade counter
        In production, this would update the database
        """
        self.daily_trade_count += 1
    
    def reset_daily_count(self) -> None:
        """
        Reset daily trade counter
        Should be called at market close or start of new trading day
        """
        self.daily_trade_count = 0
    
    def get_daily_count(self) -> int:
        """Get current daily trade count"""
        return self.daily_trade_count
