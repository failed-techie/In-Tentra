"""
Policy Engine - Evaluates trading intents against defined policies
DETERMINISTIC - No LLM, pure Python logic
"""
import json
from typing import Dict, Any, List
from pathlib import Path


class PolicyEngine:
    """
    Deterministic policy evaluation engine
    Validates trading intents against rules loaded from policies.json
    
    NO LLM INVOLVEMENT - All logic is rule-based
    """
    
    def __init__(self, policy_file: str = "config/policies.json"):
        """
        Initialize policy engine
        
        Args:
            policy_file: Path to policies.json file
        """
        self.policy_file = policy_file
        self.policies = self._load_policies()
    
    def _load_policies(self) -> Dict[str, Any]:
        """
        Load policies from JSON file
        
        Returns:
            dict: Loaded policies
            
        Raises:
            FileNotFoundError: If policy file doesn't exist
            json.JSONDecodeError: If policy file is invalid JSON
        """
        policy_path = Path(self.policy_file)
        
        if not policy_path.exists():
            raise FileNotFoundError(f"Policy file not found: {self.policy_file}")
        
        with open(policy_path, 'r') as f:
            return json.load(f)
    
    def validate(self, intent: Dict[str, Any]) -> Dict[str, Any]:
        """
        Validate trading intent against all policies
        
        Args:
            intent: Trading intent with keys:
                - symbol: str (stock ticker)
                - action: str (BUY, SELL, SHORT, MARGIN, etc.)
                - amount: float (dollar amount)
                - quantity: int (optional, number of shares)
        
        Returns:
            dict: {
                "valid": bool,
                "violations": list[str]
            }
        """
        violations = []
        
        # Extract intent fields
        symbol = intent.get("symbol", "").upper()
        action = intent.get("action", "").upper()
        amount = intent.get("amount", 0)
        
        # Rule 1: Check trade amount limit
        max_amount = self.policies.get("max_trade_amount", float('inf'))
        if amount > max_amount:
            violations.append(
                f"Trade amount ${amount} exceeds maximum ${max_amount}"
            )
        
        # Rule 2: Check minimum trade amount
        min_amount = self.policies.get("additional_rules", {}).get("min_trade_amount", 0)
        if amount < min_amount:
            violations.append(
                f"Trade amount ${amount} below minimum ${min_amount}"
            )
        
        # Rule 3: Check symbol whitelist
        allowed_symbols = self.policies.get("allowed_symbols", [])
        if allowed_symbols and symbol not in allowed_symbols:
            violations.append(
                f"Symbol '{symbol}' not in allowed list: {allowed_symbols}"
            )
        
        # Rule 4: Check blocked actions
        blocked_actions = self.policies.get("blocked_actions", [])
        if action in blocked_actions:
            violations.append(
                f"Action '{action}' is blocked by policy"
            )
        
        # Rule 5: Check allowed actions
        allowed_actions = self.policies.get("additional_rules", {}).get("allowed_actions", [])
        if allowed_actions and action not in allowed_actions:
            violations.append(
                f"Action '{action}' not in allowed actions: {allowed_actions}"
            )
        
        # Rule 6: Validate required fields
        if not symbol:
            violations.append("Symbol is required")
        
        if not action:
            violations.append("Action is required")
        
        return {
            "valid": len(violations) == 0,
            "violations": violations
        }
    
    def get_policy(self, key: str, default: Any = None) -> Any:
        """
        Get a specific policy value
        
        Args:
            key: Policy key
            default: Default value if key not found
            
        Returns:
            Policy value or default
        """
        return self.policies.get(key, default)
    
    def reload_policies(self) -> None:
        """Reload policies from file"""
        self.policies = self._load_policies()
