import json
import yaml
from pathlib import Path
from typing import Dict, Any


class ConfigManager:
    """
    Manage pipeline configuration
    """
    
    @staticmethod
    def load_config(config_path: str) -> Dict[str, Any]:
        """
        Load configuration from file
        
        Args:
            config_path: Path to config file (JSON or YAML)
            
        Returns:
            Configuration dictionary
        """
        path = Path(config_path)
        
        if not path.exists():
            raise FileNotFoundError(f"Config file not found: {config_path}")
        
        if path.suffix == '.json':
            with open(path, 'r') as f:
                return json.load(f)
        elif path.suffix in ['.yaml', '.yml']:
            with open(path, 'r') as f:
                return yaml.safe_load(f)
        else:
            raise ValueError(f"Unsupported config format: {path.suffix}")
    
    @staticmethod
    def save_config(config: Dict[str, Any], config_path: str):
        """
        Save configuration to file
        
        Args:
            config: Configuration dictionary
            config_path: Path to save config
        """
        path = Path(config_path)
        
        if path.suffix == '.json':
            with open(path, 'w') as f:
                json.dump(config, f, indent=2)
        elif path.suffix in ['.yaml', '.yml']:
            with open(path, 'w') as f:
                yaml.dump(config, f, default_flow_style=False)
        else:
            raise ValueError(f"Unsupported config format: {path.suffix}")
    
    @staticmethod
    def create_default_config() -> Dict[str, Any]:
        """
        Create default configuration
        
        Returns:
            Default configuration dictionary
        """
        return {
            'pipeline': {
                'use_cache': True,
                'clean_strategy': 'drop',
                'analyze_sentiment': True,
                'extract_entities': True,
                'extract_keywords': True,
                'detect_topics': True,
                'analyze_complexity': True
            },
            'visualization': {
                'create_dashboard': True,
                'dpi': 300,
                'style': 'whitegrid'
            },
            'export': {
                'format': 'csv',
                'include_sentiment': True,
                'include_entities': False
            },
            'output': {
                'directory': 'output',
                'report_name': 'unified_report.txt'
            }
        }


# ============================================
# TESTING CODE
# ============================================

if __name__ == "__main__":
    print("=" * 60)
    print("CONFIG MANAGER - TEST")
    print("=" * 60)
    
    # Create default config
    config = ConfigManager.create_default_config()
    
    print("\n1 Default configuration:")
    print(json.dumps(config, indent=2))
    
    # Save config
    print("\n2 Saving config...")
    ConfigManager.save_config(config, 'config.json')
    print("   Saved to config.json")
    
    # Load config
    print("\n3 Loading config...")
    loaded_config = ConfigManager.load_config('config.json')
    print(f"   Loaded: {len(loaded_config)} sections")
    
    print("\n" + "=" * 60)
    print("✓ TEST COMPLETE")
    print("=" * 60)