"""
Master Agent - Orchestrates all other agents
Coordinates the flow: Intent -> Analysis -> Policy Check -> Execution
"""
from langchain_groq import ChatGroq
from langchain.schema import HumanMessage, SystemMessage

from config.settings import settings
from core.intent_compiler import IntentCompiler
from .analyst_agent import AnalystAgent
from .guardian_agent import GuardianAgent
from .trader_agent import TraderAgent


class MasterAgent:
    """
    Master orchestrator for the multi-agent trading system
    Manages the workflow between analyst, guardian, and trader agents
    """
    
    def __init__(self):
        self.llm = ChatGroq(
            model=settings.GROQ_MODEL,
            api_key=settings.GROQ_API_KEY,
            temperature=0.3
        )
        self.intent_compiler = IntentCompiler()
        self.analyst = AnalystAgent()
        self.guardian = GuardianAgent()
        self.trader = TraderAgent()
    
    async def process_intent(self, raw_intent: dict) -> dict:
        """
        Main workflow: Process user intent through all agents
        
        Args:
            raw_intent: User's trading intention as dict
            
        Returns:
            dict: Processing result with status and details
        """
        # Step 1: Compile the intent
        compiled_intent = await self.intent_compiler.compile(raw_intent)
        
        # Step 2: Analyst agent analyzes market conditions
        analysis = await self.analyst.analyze(compiled_intent)
        
        # Step 3: Guardian agent validates against policies
        validation = await self.guardian.validate(compiled_intent, analysis)
        
        if not validation["approved"]:
            return {
                "status": "rejected",
                "reason": validation["reason"],
                "intent": compiled_intent
            }
        
        # Step 4: Trader agent executes the trade
        execution_result = await self.trader.execute(compiled_intent, analysis)
        
        return {
            "status": "completed",
            "intent": compiled_intent,
            "analysis": analysis,
            "execution": execution_result
        }
    
    def _coordinate_agents(self, intent: dict) -> dict:
        """Coordinate communication between agents"""
        # TODO: Implement inter-agent communication logic
        pass
