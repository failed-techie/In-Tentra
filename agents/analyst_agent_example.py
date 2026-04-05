"""
Example usage of the Analyst Agent

This demonstrates how to use the AnalystAgent to analyze market conditions
and get trade suggestions.
"""
from analyst_agent import AnalystAgent
import json


def main():
    # Initialize the agent (will use API key from .env or GROQ_API_KEY env var)
    agent = AnalystAgent()
    
    # Example 1: Bullish market context
    print("=" * 70)
    print("Example 1: Strong Bullish Signals")
    print("=" * 70)
    
    bullish_context = {
        "symbol": "AAPL",
        "current_price": 175.0,
        "trend": "upward",
        "volume": "high",
        "news_sentiment": "positive"
    }
    
    suggestion = agent.analyze(bullish_context)
    
    print(f"\nMarket Context:")
    print(f"  Symbol: {bullish_context['symbol']}")
    print(f"  Price: ${bullish_context['current_price']}")
    print(f"  Trend: {bullish_context['trend']}")
    print(f"  Volume: {bullish_context['volume']}")
    print(f"  News: {bullish_context['news_sentiment']}")
    
    print(f"\nRecommendation:")
    print(f"  Action: {suggestion['action']}")
    print(f"  Amount: ${suggestion['amount']:.2f}")
    print(f"  Confidence: {suggestion['confidence']:.2%}")
    print(f"  Reasoning: {suggestion['reasoning']}")
    
    # Example 2: Bearish market context
    print("\n" + "=" * 70)
    print("Example 2: Bearish Signals")
    print("=" * 70)
    
    bearish_context = {
        "symbol": "TSLA",
        "current_price": 180.0,
        "trend": "downward",
        "volume": "high",
        "news_sentiment": "negative"
    }
    
    suggestion = agent.analyze(bearish_context)
    
    print(f"\nMarket Context:")
    print(f"  Symbol: {bearish_context['symbol']}")
    print(f"  Price: ${bearish_context['current_price']}")
    print(f"  Trend: {bearish_context['trend']}")
    print(f"  Volume: {bearish_context['volume']}")
    print(f"  News: {bearish_context['news_sentiment']}")
    
    print(f"\nRecommendation:")
    print(f"  Action: {suggestion['action']}")
    print(f"  Amount: ${suggestion['amount']:.2f}")
    print(f"  Confidence: {suggestion['confidence']:.2%}")
    print(f"  Reasoning: {suggestion['reasoning']}")
    
    # Example 3: Using with custom model
    print("\n" + "=" * 70)
    print("Example 3: Using Custom Model")
    print("=" * 70)
    
    # You can also specify a different model
    agent_llama = AnalystAgent(model="llama-3.3-70b-versatile")
    
    neutral_context = {
        "symbol": "MSFT",
        "current_price": 420.0,
        "trend": "sideways",
        "volume": "low",
        "news_sentiment": "neutral"
    }
    
    suggestion = agent_llama.analyze(neutral_context)
    
    print(f"\nMarket Context:")
    print(f"  Symbol: {neutral_context['symbol']}")
    print(f"  Price: ${neutral_context['current_price']}")
    print(f"  Trend: {neutral_context['trend']}")
    print(f"  Volume: {neutral_context['volume']}")
    print(f"  News: {neutral_context['news_sentiment']}")
    
    print(f"\nRecommendation:")
    print(f"  Action: {suggestion['action']}")
    print(f"  Amount: ${suggestion['amount']:.2f}")
    print(f"  Confidence: {suggestion['confidence']:.2%}")
    print(f"  Reasoning: {suggestion['reasoning']}")
    
    print("\n" + "=" * 70)


if __name__ == "__main__":
    try:
        main()
    except ValueError as e:
        print(f"\n❌ Error: {e}")
        print("\n💡 Make sure to set up your .env file with GROQ_API_KEY")
        print("   See .env.example for reference")
