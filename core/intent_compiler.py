"""
Intent Compiler - Parses and structures user trading intents
Converts natural language or structured input into standardized intent format
"""
from typing import Dict, Any
from langchain_groq import ChatGroq
from langchain.schema import HumanMessage, SystemMessage

from config.settings import settings


class IntentCompiler:
    """
    Compiles raw user intents into structured trading commands
    Handles natural language parsing and intent normalization
    """
    
    def __init__(self):
        self.llm = ChatGroq(
            model=settings.GROQ_MODEL,
            api_key=settings.GROQ_API_KEY,
            temperature=0.2
        )
        self.system_prompt = """You are an intent parser for a trading system.
Convert user trading requests into structured JSON format with fields:
- symbol: stock ticker
- action: buy/sell
- quantity: number of shares
- order_type: market/limit/stop
- price: target price (if applicable)
- conditions: any additional conditions"""
    
    async def compile(self, raw_intent: Dict[str, Any]) -> Dict[str, Any]:
        """
        Compile raw intent into structured format
        
        Args:
            raw_intent: Raw user intent (may be natural language or partial structure)
            
        Returns:
            dict: Compiled intent in standard format
        """
        # If already structured, validate and normalize
        if self._is_structured(raw_intent):
            return await self._normalize_intent(raw_intent)
        
        # If natural language, parse using LLM
        if "text" in raw_intent:
            return await self._parse_natural_language(raw_intent["text"])
        
        # Fallback: attempt to extract what we can
        return await self._extract_intent(raw_intent)
    
    def _is_structured(self, intent: Dict[str, Any]) -> bool:
        """Check if intent is already in structured format"""
        required_fields = ["symbol", "action"]
        return all(field in intent for field in required_fields)
    
    async def _normalize_intent(self, intent: Dict[str, Any]) -> Dict[str, Any]:
        """Normalize and validate structured intent"""
        normalized = {
            "symbol": intent.get("symbol", "").upper(),
            "action": intent.get("action", "").lower(),
            "quantity": intent.get("quantity", 1),
            "order_type": intent.get("order_type", "market").lower(),
            "price": intent.get("price"),
            "conditions": intent.get("conditions", [])
        }
        
        # Validate
        if normalized["action"] not in ["buy", "sell"]:
            raise ValueError(f"Invalid action: {normalized['action']}")
        
        if normalized["quantity"] <= 0:
            raise ValueError(f"Invalid quantity: {normalized['quantity']}")
        
        return normalized
    
    async def _parse_natural_language(self, text: str) -> Dict[str, Any]:
        """Parse natural language intent using LLM"""
        messages = [
            SystemMessage(content=self.system_prompt),
            HumanMessage(content=f"Parse this trading intent: {text}")
        ]
        
        # TODO: Implement actual LLM parsing and JSON extraction
        # response = await self.llm.ainvoke(messages)
        # parsed = json.loads(response.content)
        
        # Placeholder
        return {
            "symbol": "AAPL",
            "action": "buy",
            "quantity": 10,
            "order_type": "market",
            "price": None,
            "conditions": []
        }
    
    async def _extract_intent(self, raw_intent: Dict[str, Any]) -> Dict[str, Any]:
        """Extract intent from partial or malformed input"""
        # TODO: Implement extraction logic
        return await self._normalize_intent(raw_intent)
