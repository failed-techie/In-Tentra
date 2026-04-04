"""
Application settings and configuration
Loads configuration from environment variables with validation
"""
import os
import sys
from pathlib import Path
from typing import Optional
from pydantic import Field, field_validator, ValidationError
from pydantic_settings import BaseSettings
from dotenv import load_dotenv

# Load .env file before anything else
env_path = Path(__file__).parent.parent / ".env"
load_dotenv(dotenv_path=env_path)


class Settings(BaseSettings):
    """
    Application settings loaded from environment variables
    Uses pydantic-settings for validation and type conversion
    
    Required environment variables will raise ValidationError if missing.
    """
    
    # ============ REQUIRED API KEYS ============
    GROQ_API_KEY: str = Field(
        ...,
        description="Groq API key (required)",
        min_length=10
    )
    
    ALPACA_API_KEY: str = Field(
        ...,
        description="Alpaca API key (required)",
        min_length=10
    )
    
    ALPACA_SECRET_KEY: str = Field(
        ...,
        description="Alpaca secret key (required)",
        min_length=10
    )
    
    ALPACA_BASE_URL: str = Field(
        default="https://paper-api.alpaca.markets",
        description="Alpaca API base URL"
    )
    
    # ============ OPTIONAL SETTINGS ============
    # Server Configuration
    HOST: str = Field(default="0.0.0.0", description="Server host")
    PORT: int = Field(default=8000, ge=1024, le=65535, description="Server port")
    DEBUG: bool = Field(default=True, description="Debug mode")
    
    # Groq Model Configuration
    GROQ_MODEL: str = Field(
        default="llama-3.3-70b-versatile",
        description="Groq model to use"
    )
    
    # Database Configuration
    DATABASE_URL: str = Field(
        default="sqlite:///./logs/intentra.db",
        description="Database connection URL"
    )
    
    # Agent Configuration
    MAX_RETRIES: int = Field(default=3, ge=1, le=10, description="Max retries for agent operations")
    TIMEOUT_SECONDS: int = Field(default=30, ge=5, le=300, description="Timeout for agent operations")
    
    # Policy Configuration
    POLICY_FILE: str = Field(
        default="config/policies.json",
        description="Path to policy configuration file"
    )
    
    @field_validator("ALPACA_BASE_URL")
    @classmethod
    def validate_alpaca_url(cls, v: str) -> str:
        """Ensure Alpaca URL is valid"""
        if not v.startswith("https://"):
            raise ValueError("ALPACA_BASE_URL must start with https://")
        return v
    
    @field_validator("DATABASE_URL")
    @classmethod
    def validate_database_url(cls, v: str) -> str:
        """Ensure database directory exists for SQLite"""
        if v.startswith("sqlite:///"):
            db_path = v.replace("sqlite:///", "")
            if db_path.startswith("./"):
                db_path = db_path[2:]
            db_dir = Path(db_path).parent
            db_dir.mkdir(parents=True, exist_ok=True)
        return v
    
    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"
        case_sensitive = True
        extra = "ignore"  # Ignore extra env vars


def get_settings() -> Settings:
    """
    Factory function to get settings with proper error handling
    
    Returns:
        Settings: Validated settings instance
        
    Raises:
        SystemExit: If required environment variables are missing
    """
    try:
        return Settings()
    except ValidationError as e:
        print("❌ Configuration Error - Missing or invalid environment variables:\n", file=sys.stderr)
        
        for error in e.errors():
            field = error["loc"][0]
            msg = error["msg"]
            
            if error["type"] == "missing":
                print(f"  ❌ {field}: REQUIRED but not set", file=sys.stderr)
            else:
                print(f"  ❌ {field}: {msg}", file=sys.stderr)
        
        print("\n💡 Setup instructions:", file=sys.stderr)
        print("  1. Copy .env.example to .env", file=sys.stderr)
        print("  2. Fill in your API keys in the .env file", file=sys.stderr)
        print("  3. Get Groq API key from: https://console.groq.com", file=sys.stderr)
        print("  4. Get Alpaca API keys from: https://alpaca.markets\n", file=sys.stderr)
        
        sys.exit(1)


# Create global settings instance with error handling
settings = get_settings()
