import logging
import os

def setup_logger(name: str) -> logging.Logger:
    """Set up and return a logger instance."""
    # Create logs directory if it doesn't exist
    if not os.path.exists('logs'):
        os.makedirs('logs')
        
    logger = logging.getLogger(name)
    
    # Only add handlers if the logger doesn't have any
    if not logger.handlers:
        logger.setLevel(logging.INFO)
        
        # Create file handler
        fh = logging.FileHandler('logs/ids.log')
        fh.setLevel(logging.INFO)
        
        # Create console handler
        ch = logging.StreamHandler()
        ch.setLevel(logging.INFO)
        
        # Create formatter
        formatter = logging.Formatter(
            '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
        )
        
        # Add formatter to handlers
        fh.setFormatter(formatter)
        ch.setFormatter(formatter)
        
        # Add handlers to logger
        logger.addHandler(fh)
        logger.addHandler(ch)
    
    return logger 