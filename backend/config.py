"""Configuration settings for the FastAPI backend."""
from pydantic_settings import BaseSettings
from typing import List


class Settings(BaseSettings):
    """Application settings loaded from environment variables."""
    
    # Model Configuration
    model_type: str = "local"  # local, huggingface
    
    # Local Model Configuration
    # Recommended models:
    # - "microsoft/phi-2" (2.7B) - Small, fast, good for education
    # - "google/gemma-2b-it" (2B) - Good instruction following
    # - "mistralai/Mistral-7B-Instruct-v0.2" (7B) - Best quality, needs GPU
    # - "gpt2" - Very fast but lower quality
    local_model_name: str = "microsoft/phi-2"
    
    # Model Settings
    device: str = "auto"  # auto, cpu, cuda
    load_in_8bit: bool = False  # Set to True if you have GPU and want to save memory
    max_length: int = 1024  # Reduced for faster inference
    temperature: float = 0.7
    
    # Server Configuration
    host: str = "0.0.0.0"
    port: int = 8000
    debug: bool = True
    
    # CORS Configuration
    cors_origins: str = "http://localhost:5173,http://localhost:3000"
    
    class Config:
        env_file = ".env"
        case_sensitive = False
    
    @property
    def cors_origins_list(self) -> List[str]:
        """Convert comma-separated CORS origins to list."""
        return [origin.strip() for origin in self.cors_origins.split(",")]


# Global settings instance
settings = Settings()

