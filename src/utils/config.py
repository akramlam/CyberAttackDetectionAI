import yaml
from typing import Dict, Any

class Config:
    def __init__(self, config_path: str):
        self.config_path = config_path
        self.config = self.load_config()
        
    def load_config(self) -> Dict[str, Any]:
        """Load configuration from YAML file."""
        with open(self.config_path, 'r') as f:
            return yaml.safe_load(f)
    
    def get(self, key: str) -> Any:
        """Get configuration value by key."""
        return self.config.get(key) 