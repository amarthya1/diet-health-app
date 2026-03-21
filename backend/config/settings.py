"""
Application Configuration
"""

import os


class Config:
    SECRET_KEY = os.environ.get("SECRET_KEY", "dev-secret-key-change-in-production")
    DEBUG = os.environ.get("DEBUG", "True") == "True"

    # Database (SQLite for development)
    DATABASE_URI = os.environ.get("DATABASE_URI", "sqlite:///diet_health.db")

    # API keys (set in environment for production)
    OPENAI_API_KEY = os.environ.get("OPENAI_API_KEY", "")
    NUTRITION_API_KEY = os.environ.get("NUTRITION_API_KEY", "")

    # CORS settings
    CORS_ORIGINS = os.environ.get("CORS_ORIGINS", "*")


class DevelopmentConfig(Config):
    DEBUG = True


class ProductionConfig(Config):
    DEBUG = False
    SECRET_KEY = os.environ.get("SECRET_KEY")  # Must be set in production


config = {
    "development": DevelopmentConfig,
    "production": ProductionConfig,
    "default": DevelopmentConfig,
}
