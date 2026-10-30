import os
from pathlib import Path
from dotenv import load_dotenv

# Load .env file from project root
BASE_DIR = Path(__file__).resolve().parent
load_dotenv(BASE_DIR / ".env")


class Config:
    """Base application configuration."""
    SECRET_KEY = os.getenv("SECRET_KEY", "travelgo-dev-super-secret-key-change-in-prod-2026")
    
    # Session configuration
    SESSION_COOKIE_NAME = "travelgo_session"
    SESSION_COOKIE_HTTPONLY = True
    SESSION_COOKIE_SAMESITE = "Lax"
    PERMANENT_SESSION_LIFETIME = 86400  # 24 hours
    
    # AWS Settings
    AWS_REGION = os.getenv("AWS_REGION", "us-east-1")
    USE_MOCK_AWS = os.getenv("USE_MOCK_AWS", "true").lower() in ("true", "1", "yes")
    
    # DynamoDB Tables
    DYNAMODB_USERS_TABLE = os.getenv("DYNAMODB_USERS_TABLE", "travelgo_users")
    DYNAMODB_BOOKINGS_TABLE = os.getenv("DYNAMODB_BOOKINGS_TABLE", "travelgo_bookings")
    
    # AWS SNS Topic ARN
    SNS_BOOKING_TOPIC_ARN = os.getenv(
        "SNS_BOOKING_TOPIC_ARN", 
        "arn:aws:sns:us-east-1:123456789012:travelgo-booking-alerts"
    )
    
    # CloudWatch
    CLOUDWATCH_LOG_GROUP = os.getenv("CLOUDWATCH_LOG_GROUP", "/travelgo/application")


class DevelopmentConfig(Config):
    """Development configuration."""
    DEBUG = True
    TESTING = False


class TestingConfig(Config):
    """Testing configuration with mock AWS forced on."""
    DEBUG = False
    TESTING = True
    USE_MOCK_AWS = True
    SECRET_KEY = "test-secret-key-for-pytest"


class ProductionConfig(Config):
    """Production configuration for AWS EC2."""
    DEBUG = False
    TESTING = False
    SESSION_COOKIE_SECURE = True  # Set to true for HTTPS


config_by_name = {
    "development": DevelopmentConfig,
    "testing": TestingConfig,
    "production": ProductionConfig,
    "default": DevelopmentConfig,
}
