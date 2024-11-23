from typing import Dict, Any
import ipaddress
import os

def validate_config(config: Dict[str, Any]) -> bool:
    """Validate configuration settings"""
    try:
        # Check network interface
        if not config.get('network_interface'):
            raise ValueError("Network interface not specified")
            
        # Check database connection
        db_config = config.get('database', {})
        if not db_config.get('connection_string'):
            raise ValueError("Database connection string not specified")
            
        # Check logging configuration
        log_config = config.get('logging', {})
        log_dir = os.path.dirname(log_config.get('file', ''))
        if log_dir and not os.path.exists(log_dir):
            os.makedirs(log_dir)
            
        return True
        
    except Exception as e:
        print(f"Configuration validation failed: {str(e)}")
        return False 