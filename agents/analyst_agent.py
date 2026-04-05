"""
Analyst Agent - Market analysis and trade suggestions
Analyzes market context and generates structured trade recommendations
using LangChain + Groq LLM with Pydantic structured output parsing
"""
from langchain_groq import ChatGroq
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import PydanticOutputParser
from pydantic import BaseModel, Field
from typing import Dict, Any, Literal
import os
import json


class TradeSuggestion(BaseModel):
    """Structured output format for trade suggestions"""
    action: Literal["BUY", "SELL", "HOLD"] = Field(
        description="Trading action recommendation"
    )
    symbol: str = Field(description="Stock symbol")
    amount: float = Field(
        description="Suggested trade amount in USD",
        ge=0.0
    )
    confidence: float = Field(
        description="Confidence level between 0.0 and 1.0",
        ge=0.0,
        le=1.0
    )
    reasoning: str = Field(
        description="Detailed reasoning for the recommendation"
    )


class AnalystAgent:
    """
    LLM-powered analyst that generates trade suggestions from market context
    Uses LangChain + Groq with structured output parsing
    """
    
    def __init__(self, api_key: str = None, model: str = "mixtral-8x7b-32768"):
        """
        Initialize the Analyst Agent
        
        Args:
            api_key: Groq API key (or reads from GROQ_API_KEY env var)
            model: Groq model name to use
        """
        if api_key is None:
            api_key = os.getenv("GROQ_API_KEY")
            if not api_key:
                raise ValueError("GROQ_API_KEY not provided and not found in environment")
        
        self.llm = ChatGroq(
            model=model,
            api_key=api_key,
            temperature=0.3  # Lower temperature for more consistent, cautious analysis
        )
        
        # Set up structured output parser
        self.parser = PydanticOutputParser(pydantic_object=TradeSuggestion)
        
        # Create the prompt template
        self.prompt = ChatPromptTemplate.from_messages([
            ("system", self._get_system_prompt()),
            ("human", self._get_human_prompt())
        ])
    
    def _get_system_prompt(self) -> str:
        """Returns the system prompt for the analyst agent"""
        return """You are a cautious, low-risk trading analyst with expertise in technical analysis and risk management.

Your role is to analyze market conditions and provide conservative trading recommendations that prioritize capital preservation.

Key principles:
- ALWAYS err on the side of caution
- Never recommend trades without strong supporting evidence
- Consider risk before potential reward
- Default to HOLD when signals are unclear or conflicting
- Be transparent about uncertainty in your reasoning
- Avoid emotional or speculative language

When analyzing market context, consider:
1. Price trends and momentum
2. Volume patterns (high volume confirms trends)
3. News sentiment and its reliability
4. Overall market risk factors

Output your recommendation in the exact JSON format specified."""
    
    def _get_human_prompt(self) -> str:
        """Returns the human prompt template"""
        return """Analyze the following market context and provide a trading recommendation:

Market Context:
- Symbol: {symbol}
- Current Price: ${current_price}
- Trend: {trend}
- Volume: {volume}
- News Sentiment: {news_sentiment}

{format_instructions}

Provide your analysis in the specified JSON format only. No additional text."""
    
    def analyze(self, market_context: Dict[str, Any]) -> Dict[str, Any]:
        """
        Analyze market context and generate a trade suggestion
        
        Args:
            market_context: Dictionary with keys:
                - symbol (str): Stock symbol
                - current_price (float): Current price
                - trend (str): Market trend description
                - volume (str): Volume level
                - news_sentiment (str): News sentiment
        
        Returns:
            dict: Trade suggestion with keys:
                - action: "BUY" | "SELL" | "HOLD"
                - symbol: str
                - amount: float
                - confidence: float (0.0 to 1.0)
                - reasoning: str
        """
        try:
            # Format the prompt with market context and parser instructions
            formatted_prompt = self.prompt.format_messages(
                symbol=market_context.get("symbol", "UNKNOWN"),
                current_price=market_context.get("current_price", 0.0),
                trend=market_context.get("trend", "unknown"),
                volume=market_context.get("volume", "unknown"),
                news_sentiment=market_context.get("news_sentiment", "neutral"),
                format_instructions=self.parser.get_format_instructions()
            )
            
            # Invoke the LLM
            response = self.llm.invoke(formatted_prompt)
            
            # Parse the structured output
            suggestion = self.parser.parse(response.content)
            
            # Return as dict
            return suggestion.model_dump()
            
        except Exception as e:
            # Fallback: return safe default if parsing fails
            print(f"Error in analysis: {e}")
            return self._get_safe_default(market_context.get("symbol", "UNKNOWN"))
    
    def _get_safe_default(self, symbol: str) -> Dict[str, Any]:
        """
        Returns a safe default suggestion (HOLD with 0.0 confidence)
        Used as fallback when LLM output cannot be parsed
        """
        return {
            "action": "HOLD",
            "symbol": symbol,
            "amount": 0.0,
            "confidence": 0.0,
            "reasoning": "Unable to generate recommendation due to parsing error. Defaulting to HOLD for safety."
        }


# ============================================================================
# STANDALONE TEST
# ============================================================================

if __name__ == "__main__":
    print("=" * 70)
    print("ANALYST AGENT - STANDALONE TEST")
    print("=" * 70)
    
    # Try to load from config/settings first, fallback to env var
    api_key = None
    try:
        # Attempt to import settings if available
        from config.settings import settings
        api_key = settings.GROQ_API_KEY
        print("\n✓ Using GROQ_API_KEY from config/settings.py")
    except Exception:
        # Fall back to environment variable
        api_key = os.getenv("GROQ_API_KEY")
        if api_key:
            print("\n✓ Using GROQ_API_KEY from environment variable")
        else:
            print("\n⚠️  GROQ_API_KEY not found in config or environment")
            print("Options:")
            print("  1. Set up .env file (see SETUP_GUIDE.md)")
            print("  2. Export: export GROQ_API_KEY='your-key-here'")
            print("\nRunning test with fallback mode (will test error handling)...\n")
    
    # Create agent
    try:
        agent = AnalystAgent(api_key=api_key) if api_key else None
        if agent:
            print("✓ AnalystAgent initialized successfully\n")
        else:
            print("⚠️  Testing fallback behavior without API key\n")
            # Create a mock agent for testing fallback
            class MockAgent:
                def analyze(self, context):
                    return {
                        "action": "HOLD",
                        "symbol": context.get("symbol", "UNKNOWN"),
                        "amount": 0.0,
                        "confidence": 0.0,
                        "reasoning": "Unable to generate recommendation due to parsing error. Defaulting to HOLD for safety."
                    }
            agent = MockAgent()
    except Exception as e:
        print(f"✗ Failed to initialize agent: {e}\n")
        exit(1)
    
    # Test case 1: Strong bullish signals
    print("\n" + "-" * 70)
    print("TEST 1: Strong Bullish Signals (AAPL)")
    print("-" * 70)
    market_context_1 = {
        "symbol": "AAPL",
        "current_price": 175.0,
        "trend": "upward",
        "volume": "high",
        "news_sentiment": "positive"
    }
    print(f"Input: {json.dumps(market_context_1, indent=2)}")
    suggestion_1 = agent.analyze(market_context_1)
    print(f"\nOutput:\n{json.dumps(suggestion_1, indent=2)}")
    
    # Test case 2: Bearish signals
    print("\n" + "-" * 70)
    print("TEST 2: Bearish Signals (TSLA)")
    print("-" * 70)
    market_context_2 = {
        "symbol": "TSLA",
        "current_price": 180.0,
        "trend": "downward",
        "volume": "high",
        "news_sentiment": "negative"
    }
    print(f"Input: {json.dumps(market_context_2, indent=2)}")
    suggestion_2 = agent.analyze(market_context_2)
    print(f"\nOutput:\n{json.dumps(suggestion_2, indent=2)}")
    
    # Test case 3: Unclear signals
    print("\n" + "-" * 70)
    print("TEST 3: Unclear/Mixed Signals (MSFT)")
    print("-" * 70)
    market_context_3 = {
        "symbol": "MSFT",
        "current_price": 420.0,
        "trend": "sideways",
        "volume": "low",
        "news_sentiment": "neutral"
    }
    print(f"Input: {json.dumps(market_context_3, indent=2)}")
    suggestion_3 = agent.analyze(market_context_3)
    print(f"\nOutput:\n{json.dumps(suggestion_3, indent=2)}")
    
    print("\n" + "=" * 70)
    print("TEST COMPLETE")
    print("=" * 70)
