"""
Unit tests for EnforcementLayer
Tests deterministic enforcement logic
"""
import unittest
import json
import tempfile
from pathlib import Path
import sys

# Add parent directory to path for imports
sys.path.insert(0, str(Path(__file__).parent.parent))

from core.policy_engine import PolicyEngine
from core.enforcement_layer import EnforcementLayer


class TestEnforcementLayer(unittest.TestCase):
    """Test cases for EnforcementLayer class"""
    
    def setUp(self):
        """Set up test fixtures"""
        # Create temporary policy file
        self.temp_dir = tempfile.mkdtemp()
        self.policy_file = Path(self.temp_dir) / "test_policies.json"
        
        # Test policies
        self.test_policies = {
            "max_trade_amount": 1000,
            "allowed_symbols": ["AAPL", "TSLA", "MSFT", "GOOGL"],
            "max_daily_trades": 5,
            "risk_level": "low",
            "blocked_actions": ["SHORT", "MARGIN"],
            "additional_rules": {
                "min_trade_amount": 1,
                "allowed_actions": ["BUY", "SELL"]
            }
        }
        
        # Write test policies
        with open(self.policy_file, 'w') as f:
            json.dump(self.test_policies, f)
        
        # Create policy engine and enforcement layer
        self.policy_engine = PolicyEngine(policy_file=str(self.policy_file))
        self.enforcement = EnforcementLayer(self.policy_engine)
    
    def tearDown(self):
        """Clean up test fixtures"""
        if self.policy_file.exists():
            self.policy_file.unlink()
        Path(self.temp_dir).rmdir()
    
    def test_valid_trade_allowed(self):
        """Test that a valid trade is ALLOWED"""
        intent = {
            "symbol": "AAPL",
            "action": "BUY",
            "amount": 500
        }
        
        result = self.enforcement.enforce(intent)
        
        self.assertEqual(result["decision"], "ALLOW")
        self.assertEqual(len(result["violations"]), 0)
    
    def test_oversized_trade_blocked(self):
        """Test that oversized trade is BLOCKED"""
        intent = {
            "symbol": "TSLA",
            "action": "BUY",
            "amount": 1500  # Exceeds max of 1000
        }
        
        result = self.enforcement.enforce(intent)
        
        self.assertEqual(result["decision"], "BLOCK")
        self.assertGreater(len(result["violations"]), 0)
    
    def test_disallowed_symbol_blocked(self):
        """Test that non-whitelisted symbol is BLOCKED"""
        intent = {
            "symbol": "AMZN",  # Not in allowed list
            "action": "BUY",
            "amount": 500
        }
        
        result = self.enforcement.enforce(intent)
        
        self.assertEqual(result["decision"], "BLOCK")
    
    def test_blocked_action_rejected(self):
        """Test that SHORT action is BLOCKED"""
        intent = {
            "symbol": "MSFT",
            "action": "SHORT",
            "amount": 500
        }
        
        result = self.enforcement.enforce(intent)
        
        self.assertEqual(result["decision"], "BLOCK")


if __name__ == "__main__":
    unittest.main()
