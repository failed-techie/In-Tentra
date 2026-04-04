"""
Unit tests for PolicyEngine
Tests deterministic policy validation logic
"""
import unittest
import json
import tempfile
from pathlib import Path
import sys

# Add parent directory to path for imports
sys.path.insert(0, str(Path(__file__).parent.parent))

from core.policy_engine import PolicyEngine


class TestPolicyEngine(unittest.TestCase):
    """Test cases for PolicyEngine class"""
    
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
        
        # Create policy engine
        self.engine = PolicyEngine(policy_file=str(self.policy_file))
    
    def tearDown(self):
        """Clean up test fixtures"""
        if self.policy_file.exists():
            self.policy_file.unlink()
        Path(self.temp_dir).rmdir()
    
    def test_valid_trade_passes(self):
        """Test that a valid trade passes all policy checks"""
        intent = {
            "symbol": "AAPL",
            "action": "BUY",
            "amount": 500
        }
        
        result = self.engine.validate(intent)
        
        self.assertTrue(result["valid"])
        self.assertEqual(len(result["violations"]), 0)
    
    def test_oversized_trade_blocked(self):
        """Test that trade exceeding max amount is blocked"""
        intent = {
            "symbol": "AAPL",
            "action": "BUY",
            "amount": 1500  # Exceeds max_trade_amount of 1000
        }
        
        result = self.engine.validate(intent)
        
        self.assertFalse(result["valid"])
        self.assertGreater(len(result["violations"]), 0)
        self.assertTrue(
            any("exceeds maximum" in v for v in result["violations"])
        )
    
    def test_disallowed_symbol_blocked(self):
        """Test that non-whitelisted symbol is blocked"""
        intent = {
            "symbol": "AMZN",  # Not in allowed_symbols
            "action": "BUY",
            "amount": 500
        }
        
        result = self.engine.validate(intent)
        
        self.assertFalse(result["valid"])
        self.assertGreater(len(result["violations"]), 0)
        self.assertTrue(
            any("not in allowed list" in v for v in result["violations"])
        )
    
    def test_blocked_action_rejected(self):
        """Test that blocked action type is rejected"""
        intent = {
            "symbol": "AAPL",
            "action": "SHORT",  # Blocked action
            "amount": 500
        }
        
        result = self.engine.validate(intent)
        
        self.assertFalse(result["valid"])
        self.assertGreater(len(result["violations"]), 0)
        self.assertTrue(
            any("is blocked by policy" in v for v in result["violations"])
        )


if __name__ == "__main__":
    unittest.main()
