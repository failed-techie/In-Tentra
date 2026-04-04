"""
Policy Engine - Evaluates trading intents against defined policies
Loads and enforces trading policies from configuration
"""
import json
from typing import Dict, Any, List
from pathlib import Path

from config.settings import settings


class PolicyEngine:
    """
    Evaluates trading intents against policy rules
    Loads policies from JSON configuration and validates trades
    """
    
    def __init__(self):
        self.policies = self._load_policies()
    
    def _load_policies(self) -> Dict[str, Any]:
        """Load policies from configuration file"""
        policy_path = Path(settings.POLICY_FILE)
        
        if not policy_path.exists():
            # Return default policies if file doesn't exist
            return self._get_default_policies()
        
        with open(policy_path, 'r') as f:
            return json.load(f)
    
    def _get_default_policies(self) -> Dict[str, Any]:
        """Get default policies if config file doesn't exist"""
        return {
            "max_position_size": 10000,
            "max_order_value": 50000,
            "allowed_symbols": [],  # Empty means all allowed
            "blocked_symbols": [],
            "max_daily_trades": 50,
            "max_loss_per_trade": 1000,
            "require_stop_loss": False,
            "trading_hours_only": True
        }
    
    async def evaluate(self, intent: Dict[str, Any]) -> Dict[str, Any]:
        """
        Evaluate intent against all policies
        
        Args:
            intent: Trading intent to evaluate
            
        Returns:
            dict: Evaluation result with pass/fail and violations
        """
        violations = []
        
        # Check symbol restrictions
        symbol_check = self._check_symbol_restrictions(intent["symbol"])
        if not symbol_check["passed"]:
            violations.append(symbol_check["reason"])
        
        # Check position size limits
        size_check = self._check_position_size(intent)
        if not size_check["passed"]:
            violations.append(size_check["reason"])
        
        # Check order value limits
        value_check = self._check_order_value(intent)
        if not value_check["passed"]:
            violations.append(value_check["reason"])
        
        # Check daily trade limit
        daily_limit_check = await self._check_daily_limit()
        if not daily_limit_check["passed"]:
            violations.append(daily_limit_check["reason"])
        
        return {
            "passed": len(violations) == 0,
            "violations": violations,
            "policies_checked": ["symbol", "position_size", "order_value", "daily_limit"]
        }
    
    def _check_symbol_restrictions(self, symbol: str) -> Dict[str, Any]:
        """Check if symbol is allowed"""
        if symbol in self.policies.get("blocked_symbols", []):
            return {"passed": False, "reason": f"Symbol {symbol} is blocked"}
        
        allowed = self.policies.get("allowed_symbols", [])
        if allowed and symbol not in allowed:
            return {"passed": False, "reason": f"Symbol {symbol} not in allowed list"}
        
        return {"passed": True, "reason": ""}
    
    def _check_position_size(self, intent: Dict[str, Any]) -> Dict[str, Any]:
        """Check if position size is within limits"""
        max_size = self.policies.get("max_position_size", float('inf'))
        quantity = intent.get("quantity", 0)
        
        if quantity > max_size:
            return {
                "passed": False,
                "reason": f"Position size {quantity} exceeds limit {max_size}"
            }
        
        return {"passed": True, "reason": ""}
    
    def _check_order_value(self, intent: Dict[str, Any]) -> Dict[str, Any]:
        """Check if order value is within limits"""
        # TODO: Calculate actual order value using current price
        max_value = self.policies.get("max_order_value", float('inf'))
        
        # Placeholder - would need current price
        estimated_value = intent.get("quantity", 0) * 100  # Assume $100/share
        
        if estimated_value > max_value:
            return {
                "passed": False,
                "reason": f"Order value ${estimated_value} exceeds limit ${max_value}"
            }
        
        return {"passed": True, "reason": ""}
    
    async def _check_daily_limit(self) -> Dict[str, Any]:
        """Check if daily trade limit has been reached"""
        # TODO: Query database for today's trade count
        max_daily = self.policies.get("max_daily_trades", float('inf'))
        current_count = 0  # Placeholder
        
        if current_count >= max_daily:
            return {
                "passed": False,
                "reason": f"Daily trade limit ({max_daily}) reached"
            }
        
        return {"passed": True, "reason": ""}
