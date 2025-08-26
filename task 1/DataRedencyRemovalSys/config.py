import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

class Config:
    """Configuration settings for the Data Redundancy Removal System"""
    
    # Database Configuration
    DATABASE_URL = os.getenv('DATABASE_URL', 'sqlite:///data_redundancy.db')
    DATABASE_POOL_SIZE = int(os.getenv('DATABASE_POOL_SIZE', 5))
    DATABASE_MAX_OVERFLOW = int(os.getenv('DATABASE_MAX_OVERFLOW', 10))
    
    # Redundancy Detection Settings
    SIMILARITY_THRESHOLD = float(os.getenv('SIMILARITY_THRESHOLD', 0.8))
    EXACT_MATCH_THRESHOLD = float(os.getenv('EXACT_MATCH_THRESHOLD', 1.0))
    MIN_SIMILARITY_SCORE = float(os.getenv('MIN_SIMILARITY_SCORE', 0.6))
    
    # Batch Processing Settings
    BATCH_SIZE = int(os.getenv('BATCH_SIZE', 1000))
    MAX_BATCH_RETRIES = int(os.getenv('MAX_BATCH_RETRIES', 3))
    
    # Validation Settings
    MAX_STRING_LENGTH = int(os.getenv('MAX_STRING_LENGTH', 1000))
    REQUIRED_FIELDS = ['data_content', 'data_type']
    
    # Logging Settings
    LOG_LEVEL = os.getenv('LOG_LEVEL', 'INFO')
    LOG_FILE = os.getenv('LOG_FILE', 'data_redundancy.log')
    
    # Performance Settings
    CACHE_SIZE = int(os.getenv('CACHE_SIZE', 10000))
    HASH_ALGORITHM = os.getenv('HASH_ALGORITHM', 'md5')
    
    @classmethod
    def validate(cls):
        """Validate configuration values"""
        if not 0 <= cls.SIMILARITY_THRESHOLD <= 1:
            raise ValueError("SIMILARITY_THRESHOLD must be between 0 and 1")
        if not 0 <= cls.EXACT_MATCH_THRESHOLD <= 1:
            raise ValueError("EXACT_MATCH_THRESHOLD must be between 0 and 1")
        if cls.BATCH_SIZE <= 0:
            raise ValueError("BATCH_SIZE must be positive")
        
        return True

# Validate configuration on import
Config.validate()
