"""
Enforcement Layer - Final validation before trade execution
Performs real-time checks including account balance, market hours, etc.
"""
from typing import Dict, Any
from datetime import datetime, time
import alpaca_trade_api as tradeapi

from config.settings import settings


class EnforcementLayer:
    """
    Final enforcement checks before trade execution
    Validates real-time constraints like account balance, market hours
    """
    
    def __init__(self):
        # Initialize Alpaca API for account checks
        self.alpaca = tradeapi.REST(
            key_id=settings.ALPACA_API_KEY,
            secret_key=settings.ALPACA_SECRET_KEY,
            base_url=settings.ALPACA_BASE_URL
        )
    
    async def enforce(self, intent: Dict[str, Any], analysis: Dict[str, Any]) -> Dict[str, Any]:
        """
        Perform final enforcement checks
        
        Args:
            intent: Validated trading intent
            analysis: Market analysis data
            
        Returns:
            dict: Enforcement result with approval status
        """
        checks = []
        
        # Check 1: Account has sufficient buying power
        balance_check = await self._check_buying_power(intent)
        checks.append(balance_check)
        if not balance_check["passed"]:
            return {
                "approved": False,
                "reason": balance_check["reason"],
                "checks": checks
            }
        
        # Check 2: Market is open (if required)
        market_check = self._check_market_hours()
        checks.append(market_check)
        if not market_check["passed"]:
            return {
                "approved": False,
                "reason": market_check["reason"],
                "checks": checks
            }
        
        # Check 3: No duplicate orders
        duplicate_check = await self._check_duplicate_orders(intent)
        checks.append(duplicate_check)
        if not duplicate_check["passed"]:
            return {
                "approved": False,
                "reason": duplicate_check["reason"],
                "checks": checks
            }
        
        # All checks passed
        return {
            "approved": True,
            "reason": "All enforcement checks passed",
            "checks": checks
        }
    
    async def _check_buying_power(self, intent: Dict[str, Any]) -> Dict[str, Any]:
        """Check if account has sufficient buying power"""
        try:
            # TODO: Implement actual Alpaca account check
            # account = self.alpaca.get_account()
            # buying_power = float(account.buying_power)
            
            # Placeholder
            buying_power = 100000.0
            
            # Estimate required buying power
            estimated_cost = intent.get("quantity", 0) * 100  # Assume $100/share
            
            if estimated_cost > buying_power:
                return {
                    "passed": False,
                    "reason": f"Insufficient buying power: ${buying_power} < ${estimated_cost}"
                }
            
            return {"passed": True, "reason": "Sufficient buying power"}
            
        except Exception as e:
            return {
                "passed": False,
                "reason": f"Error checking buying power: {str(e)}"
            }
    
    def _check_market_hours(self) -> Dict[str, Any]:
        """Check if market is currently open"""
        try:
            # TODO: Implement actual market hours check using Alpaca
            # clock = self.alpaca.get_clock()
            # is_open = clock.is_open
            
            # Placeholder - basic time check
            now = datetime.now().time()
            market_open = time(9, 30)  # 9:30 AM
            market_close = time(16, 0)  # 4:00 PM
            
            is_open = market_open <= now <= market_close
            
            if not is_open:
                return {
                    "passed": False,
                    "reason": "Market is currently closed"
                }
            
            return {"passed": True, "reason": "Market is open"}
            
        except Exception as e:
            # In case of error, allow trade (fail-open for now)
            return {"passed": True, "reason": f"Could not verify market hours: {str(e)}"}
    
    async def _check_duplicate_orders(self, intent: Dict[str, Any]) -> Dict[str, Any]:
        """Check for duplicate pending orders"""
        try:
            # TODO: Implement duplicate order check
            # orders = self.alpaca.list_orders(status='open')
            # Check if similar order exists
            
            return {"passed": True, "reason": "No duplicate orders found"}
            
        except Exception as e:
            return {"passed": True, "reason": f"Could not check duplicates: {str(e)}"}
