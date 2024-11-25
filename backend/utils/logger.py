import logging
import os
from logging.handlers import RotatingFileHandler

def setup_logger(name: str) -> logging.Logger:
    """Set up and return a logger instance."""
    if not os.path.exists('logs'):
        os.makedirs('logs')
        
    logger = logging.getLogger(name)
    
    if not logger.handlers:
        logger.setLevel(logging.INFO)
        
        # File handler with rotation
        fh = RotatingFileHandler(
            'logs/ids.log',
            maxBytes=10*1024*1024,  # 10MB
            backupCount=5
        )
        
        # Console handler
        ch = logging.StreamHandler()
        
        # Formatter
        formatter = logging.Formatter(
            '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
        )
        
        fh.setFormatter(formatter)
        ch.setFormatter(formatter)
        
        logger.addHandler(fh)
        logger.addHandler(ch)
    
    return logger 