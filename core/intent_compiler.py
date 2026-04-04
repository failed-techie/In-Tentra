"""
Intent Compiler - Parses and structures user trading intents
Converts natural language or structured input into standardized intent format
Uses LangChain + Groq LLM for intelligent parsing
"""
from typing import Dict, Any, Optional
from pydantic import BaseModel, Field, field_validator
from langchain_groq import ChatGroq
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import PydanticOutputParser


class TradingIntent(BaseModel):
    """
    Structured trading intent with validation
    This is the canonical format for all trade requests in INTENTRA
    """
    action: str = Field(
        description="Trading action: BUY or SELL (uppercase)",
        pattern="^(BUY|SELL)$"
    )
    symbol: str = Field(
        description="Stock ticker symbol (uppercase, e.g., AAPL, TSLA)",
        min_length=1
    )
    amount: float = Field(
        default=100.0,
        description="Trade amount in USD",
        ge=0.01
    )
    confidence: float = Field(
        default=0.8,
        description="Confidence score from 0.0 to 1.0",
        ge=0.0,
        le=1.0
    )
    raw_input: str = Field(
        description="Original raw input text"
    )
    
    @field_validator("action")
    @classmethod
    def uppercase_action(cls, v):
        """Ensure action is uppercase"""
        return v.upper() if v else v
    
    @field_validator("symbol")
    @classmethod
    def uppercase_symbol(cls, v):
        """Ensure symbol is uppercase"""
        return v.upper() if v else v


class IntentCompiler:
    """
    Compiles raw user intents into structured trading commands
    Uses LangChain + Groq LLM for intelligent natural language parsing
    """
    
    def __init__(self, model_name: str = "mixtral-8x7b-32768", api_key: Optional[str] = None):
        """
        Initialize intent compiler
        
        Args:
            model_name: Groq model to use (mixtral-8x7b-32768 or llama3-70b-8192)
            api_key: Groq API key (if None, reads from environment)
        """
        # Initialize Groq LLM
        self.llm = ChatGroq(
            model=model_name,
            api_key=api_key,
            temperature=0.1  # Low temperature for consistent parsing
        )
        
        # Create output parser
        self.parser = PydanticOutputParser(pydantic_object=TradingIntent)
        
        # Create prompt template
        self.prompt = ChatPromptTemplate.from_messages([
            ("system", self._get_system_prompt()),
            ("human", "{raw_input}")
        ])
        
        # Create the chain
        self.chain = self.prompt | self.llm | self.parser
    
    def _get_system_prompt(self) -> str:
        """
        Get the system prompt for intent parsing
        
        Returns:
            System prompt string with format instructions
        """
        format_instructions = self.parser.get_format_instructions()
        
        return f"""You are an expert trading intent parser for INTENTRA.

Your job is to extract structured trading information from natural language.

RULES:
1. Extract action: "BUY" or "SELL" (uppercase)
2. Extract symbol: Stock ticker symbol (uppercase, e.g., AAPL, TSLA, MSFT)
3. Extract amount: Dollar amount in USD (default 100.0 if not specified)
4. Set confidence: 0.0-1.0 based on clarity of intent
   - Clear, unambiguous intent: 0.9-1.0
   - Reasonably clear: 0.7-0.8
   - Some ambiguity: 0.4-0.6
   - Very ambiguous or uncertain: 0.1-0.3

HANDLING EDGE CASES:
- If action is unclear or has words like "maybe", "might", "thinking about": Set low confidence (0.2-0.4)
- If amount is missing: Use default 100.0
- If ticker is ambiguous (e.g., "Tesla"): Convert to symbol (TSLA)
- If ticker is unknown: Pass through as-is and set lower confidence
- If multiple actions mentioned: Pick the primary one

EXAMPLES:
"Buy 500 dollars of Tesla stock" → action=BUY, symbol=TSLA, amount=500, confidence=0.95
"Sell some Apple shares" → action=SELL, symbol=AAPL, amount=100.0, confidence=0.75
"Maybe buy something" → action=BUY, symbol=UNKNOWN, amount=100.0, confidence=0.2
"Get me $1000 worth of Microsoft" → action=BUY, symbol=MSFT, amount=1000, confidence=0.9

{format_instructions}

Always return valid JSON matching the schema."""
    
    def compile(self, raw_input: str) -> TradingIntent:
        """
        Compile raw input into structured trading intent
        
        Args:
            raw_input: Raw user input (natural language or partial structure)
            
        Returns:
            TradingIntent: Validated and structured intent
            
        Raises:
            ValueError: If parsing fails completely
        """
        try:
            # Invoke the chain
            result = self.chain.invoke({"raw_input": raw_input})
            
            # Ensure raw_input is preserved
            if not result.raw_input:
                result.raw_input = raw_input
            
            return result
            
        except Exception as e:
            # Fallback: Try to create a low-confidence default
            return TradingIntent(
                action="BUY",
                symbol="UNKNOWN",
                amount=100.0,
                confidence=0.1,
                raw_input=raw_input
            )
    
    def compile_batch(self, raw_inputs: list[str]) -> list[TradingIntent]:
        """
        Compile multiple intents in batch
        
        Args:
            raw_inputs: List of raw input strings
            
        Returns:
            List of TradingIntent objects
        """
        return [self.compile(raw_input) for raw_input in raw_inputs]
    
    def to_dict(self, intent: TradingIntent) -> Dict[str, Any]:
        """
        Convert TradingIntent to dictionary
        
        Args:
            intent: TradingIntent object
            
        Returns:
            Dictionary representation
        """
        return intent.model_dump()


# Test examples
if __name__ == "__main__":
    import os
    from dotenv import load_dotenv
    
    # Load environment variables
    load_dotenv()
    
    # Check for API key
    api_key = os.getenv("GROQ_API_KEY")
    if not api_key:
        print("=" * 70)
        print("⚠️  GROQ_API_KEY not found - Running with mock examples")
        print("=" * 70)
        print()
        print("To test with real LLM:")
        print("1. Set GROQ_API_KEY in your .env file")
        print("2. Get your key from https://console.groq.com")
        print()
        print("Showing structure without LLM calls...")
        print()
        
        # Show mock examples without API call
        mock_intents = [
            TradingIntent(
                action="BUY",
                symbol="TSLA",
                amount=500.0,
                confidence=0.95,
                raw_input="Buy 500 dollars of Tesla stock"
            ),
            TradingIntent(
                action="SELL",
                symbol="AAPL",
                amount=100.0,
                confidence=0.75,
                raw_input="Sell some Apple shares"
            ),
            TradingIntent(
                action="BUY",
                symbol="MSFT",
                amount=100.0,
                confidence=0.3,
                raw_input="Maybe buy something with Microsoft"
            )
        ]
        
        for i, intent in enumerate(mock_intents, 1):
            print(f"Example {i}: {intent.raw_input}")
            print("-" * 70)
            print(f"  Action:     {intent.action}")
            print(f"  Symbol:     {intent.symbol}")
            print(f"  Amount:     ${intent.amount:.2f}")
            print(f"  Confidence: {intent.confidence:.2f}")
            print()
        
        exit(0)
    
    print("=" * 70)
    print("INTENTRA Intent Compiler - Test Examples")
    print("=" * 70)
    print()
    
    # Initialize compiler
    compiler = IntentCompiler(model_name="mixtral-8x7b-32768", api_key=api_key)
    
    # Test examples
    test_inputs = [
        "Buy 500 dollars of Tesla stock",
        "Sell some Apple shares",
        "Maybe buy something with Microsoft"
    ]
    
    for i, raw_input in enumerate(test_inputs, 1):
        print(f"Example {i}: {raw_input}")
        print("-" * 70)
        
        try:
            intent = compiler.compile(raw_input)
            
            print(f"  Action:     {intent.action}")
            print(f"  Symbol:     {intent.symbol}")
            print(f"  Amount:     ${intent.amount:.2f}")
            print(f"  Confidence: {intent.confidence:.2f}")
            print(f"  Raw Input:  {intent.raw_input}")
            
            # Show as dict
            print(f"\n  As Dictionary:")
            result_dict = compiler.to_dict(intent)
            for key, value in result_dict.items():
                print(f"    {key}: {value}")
            
        except Exception as e:
            print(f"  ❌ Error: {str(e)}")
        
        print()
    
    print("=" * 70)
    print("✅ Test completed!")
    print("=" * 70)

