"""
Guardian Agent - Policy validation and risk management
Ensures all trades comply with defined policies and risk parameters
"""
from langchain_groq import ChatGroq
from langchain.schema import HumanMessage, SystemMessage
from typing import Dict, Any

from config.settings import settings
from core.policy_engine import PolicyEngine
from core.enforcement_layer import EnforcementLayer


class GuardianAgent:
    """
    Validates trading intents against policies and risk limits
    Acts as the final gatekeeper before trade execution
    """
    
    def __init__(self):
        self.llm = ChatGroq(
            model=settings.GROQ_MODEL,
            api_key=settings.GROQ_API_KEY,
            temperature=0.1  # Low temperature for consistent policy enforcement
        )
        self.policy_engine = PolicyEngine()
        self.enforcement_layer = EnforcementLayer()
        self.system_prompt = """You are a risk management guardian.
Your role is to validate trading decisions against policies and risk limits.
Be conservative and prioritize capital preservation."""
    
    async def validate(self, intent: Dict[str, Any], analysis: Dict[str, Any]) -> Dict[str, Any]:
        """
        Validate intent against policies and risk parameters
        
        Args:
            intent: Compiled trading intent
            analysis: Market analysis from analyst agent
            
        Returns:
            dict: Validation result with approval status
        """
        # Step 1: Check against hard policy rules
        policy_check = await self.policy_engine.evaluate(intent)
        
        if not policy_check["passed"]:
            return {
                "approved": False,
                "reason": f"Policy violation: {policy_check['violations']}",
                "details": policy_check
            }
        
        # Step 2: Evaluate risk level
        risk_assessment = await self._assess_risk(intent, analysis)
        
        if risk_assessment["risk_level"] == "high":
            return {
                "approved": False,
                "reason": "Risk level exceeds acceptable threshold",
                "risk_assessment": risk_assessment
            }
        
        # Step 3: Enforcement layer check
        enforcement_result = await self.enforcement_layer.enforce(intent, analysis)
        
        return {
            "approved": enforcement_result["approved"],
            "reason": enforcement_result.get("reason", "Approved"),
            "policy_check": policy_check,
            "risk_assessment": risk_assessment,
            "enforcement": enforcement_result
        }
    
    async def _assess_risk(self, intent: Dict[str, Any], analysis: Dict[str, Any]) -> Dict[str, Any]:
        """Assess overall risk of the trade"""
        # TODO: Implement comprehensive risk assessment
        return {
            "risk_level": "medium",
            "risk_score": 0.5,
            "factors": []
        }
    
    async def _check_portfolio_impact(self, intent: Dict[str, Any]) -> bool:
        """Check how this trade impacts overall portfolio"""
        # TODO: Implement portfolio impact analysis
        return True
