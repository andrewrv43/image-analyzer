import os


class Config:
    APP_ENV: str = os.getenv("APP_ENV", "dev")
    MAX_CONTENT_LENGTH: int = int(os.getenv("MAX_CONTENT_LENGTH", 5 * 1024 * 1024))  # 5MB default
    
    MAX_CONTENT_LENGTH = MAX_CONTENT_LENGTH
