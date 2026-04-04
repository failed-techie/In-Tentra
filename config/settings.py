"""
Application settings and configuration
Loads configuration from environment variables
"""
from pydantic_settings import BaseSettings
from pydantic import Field
from typing import Optional


class Settings(BaseSettings):
    """
    Application settings loaded from environment variables
    Uses pydantic-settings for validation and type conversion
    """
    
    # Server Configuration
    HOST: str = Field(default="0.0.0.0", description="Server host")
    PORT: int = Field(default=8000, description="Server port")
    DEBUG: bool = Field(default=True, description="Debug mode")
    
    # Groq API Configuration
    GROQ_API_KEY: str = Field(..., description="Groq API key")
    GROQ_MODEL: str = Field(
        default="llama-3.3-70b-versatile",
        description="Groq model to use"
    )
    
    # Alpaca Trading API Configuration
    ALPACA_API_KEY: str = Field(..., description="Alpaca API key")
    ALPACA_SECRET_KEY: str = Field(..., description="Alpaca secret key")
    ALPACA_BASE_URL: str = Field(
        default="https://paper-api.alpaca.markets",
        description="Alpaca API base URL"
    )
    ALPACA_PAPER_TRADING: bool = Field(
        default=True,
        description="Use paper trading"
    )
    
    # Database Configuration
    DATABASE_URL: str = Field(
        default="sqlite:///./logs/intentra.db",
        description="Database connection URL"
    )
    
    # Agent Configuration
    MAX_RETRIES: int = Field(default=3, description="Max retries for agent operations")
    TIMEOUT_SECONDS: int = Field(default=30, description="Timeout for agent operations")
    
    # Policy Configuration
    POLICY_FILE: str = Field(
        default="config/policies.json",
        description="Path to policy configuration file"
    )
    
    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"
        case_sensitive = True


# Create global settings instance
settings = Settings()
