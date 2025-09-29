"""
Configuration Management for Termux AI Tool
Handles storing and retrieving API keys and settings
"""

import os
import json
from typing import Any, Dict, Optional
from pathlib import Path


class ConfigManager:
    """Manages configuration for the AI tool."""
    
    def __init__(self):
        # Use Termux-specific directory structure
        self.config_dir = Path.home() / '.config' / 'termux-ai-tool'
        self.config_file = self.config_dir / 'config.json'
        self.ensure_config_dir()
        self.config = self.load_config()
    
    def ensure_config_dir(self):
        """Ensure configuration directory exists."""
        self.config_dir.mkdir(parents=True, exist_ok=True)
        
        # Set appropriate permissions for Termux
        try:
            os.chmod(self.config_dir, 0o700)
        except OSError:
            pass  # Ignore if we can't set permissions
    
    def load_config(self) -> Dict[str, Any]:
        """Load configuration from file."""
        if self.config_file.exists():
            try:
                with open(self.config_file, 'r') as f:
                    return json.load(f)
            except (json.JSONDecodeError, IOError) as e:
                print(f"Warning: Failed to load config file: {e}")
                return {}
        return {}
    
    def save_config(self):
        """Save configuration to file."""
        try:
            with open(self.config_file, 'w') as f:
                json.dump(self.config, f, indent=2)
            
            # Set appropriate permissions for the config file
            try:
                os.chmod(self.config_file, 0o600)
            except OSError:
                pass  # Ignore if we can't set permissions
                
        except IOError as e:
            raise Exception(f"Failed to save configuration: {e}")
    
    def get(self, key: str, default: Any = None) -> Any:
        """Get configuration value."""
        return self.config.get(key, default)
    
    def set(self, key: str, value: Any):
        """Set configuration value."""
        self.config[key] = value
        self.save_config()
    
    def delete(self, key: str) -> bool:
        """Delete configuration key."""
        if key in self.config:
            del self.config[key]
            self.save_config()
            return True
        return False
    
    def get_all(self) -> Dict[str, Any]:
        """Get all configuration values."""
        return self.config.copy()
    
    def clear(self):
        """Clear all configuration."""
        self.config.clear()
        self.save_config()
    
    def export_config(self, file_path: str):
        """Export configuration to a file."""
        export_config = self.config.copy()
        
        # Mask sensitive values
        for key in export_config:
            if 'api_key' in key.lower() or 'token' in key.lower() or 'secret' in key.lower():
                export_config[key] = '***masked***'
        
        try:
            with open(file_path, 'w') as f:
                json.dump(export_config, f, indent=2)
            print(f"Configuration exported to {file_path} (API keys masked)")
        except IOError as e:
            raise Exception(f"Failed to export configuration: {e}")
    
    def import_config(self, file_path: str):
        """Import configuration from a file."""
        try:
            with open(file_path, 'r') as f:
                imported_config = json.load(f)
            
            # Merge with existing config
            self.config.update(imported_config)
            self.save_config()
            print(f"Configuration imported from {file_path}")
        except (json.JSONDecodeError, IOError) as e:
            raise Exception(f"Failed to import configuration: {e}")
    
    def validate_api_keys(self) -> Dict[str, bool]:
        """Validate that API keys are set for each provider."""
        required_keys = {
            'openai_api_key': 'OpenAI',
            'anthropic_api_key': 'Anthropic',
            'gemini_api_key': 'Google Gemini',
            'cohere_api_key': 'Cohere',
            'huggingface_api_key': 'Hugging Face'
        }
        
        validation_results = {}
        for key, provider in required_keys.items():
            value = self.get(key)
            validation_results[provider] = bool(value and len(value.strip()) > 0)
        
        return validation_results
    
    def get_provider_settings(self, provider: str) -> Dict[str, Any]:
        """Get settings specific to a provider."""
        provider_key = f"{provider}_settings"
        return self.get(provider_key, {})
    
    def set_provider_settings(self, provider: str, settings: Dict[str, Any]):
        """Set settings specific to a provider."""
        provider_key = f"{provider}_settings"
        self.set(provider_key, settings)
    
    def setup_wizard(self):
        """Interactive setup wizard for first-time configuration."""
        print("Welcome to Termux AI Tool Configuration Wizard!")
        print("=" * 50)
        print()
        
        providers = {
            'openai': {
                'name': 'OpenAI (ChatGPT)',
                'key': 'openai_api_key',
                'help': 'Get your API key from https://platform.openai.com/api-keys'
            },
            'anthropic': {
                'name': 'Anthropic (Claude)',
                'key': 'anthropic_api_key',
                'help': 'Get your API key from https://console.anthropic.com/'
            },
            'gemini': {
                'name': 'Google Gemini',
                'key': 'gemini_api_key',
                'help': 'Get your API key from https://ai.google.dev/'
            },
            'cohere': {
                'name': 'Cohere',
                'key': 'cohere_api_key',
                'help': 'Get your API key from https://dashboard.cohere.ai/api-keys'
            },
            'huggingface': {
                'name': 'Hugging Face',
                'key': 'huggingface_api_key',
                'help': 'Get your API key from https://huggingface.co/settings/tokens'
            }
        }
        
        for provider_id, info in providers.items():
            print(f"\n{info['name']}:")
            print(f"  {info['help']}")
            
            current_value = self.get(info['key'])
            if current_value:
                print(f"  Current API key: {'*' * 8}")
                update = input(f"  Update API key? (y/N): ").lower().strip()
                if update != 'y':
                    continue
            
            while True:
                api_key = input(f"  Enter API key (or press Enter to skip): ").strip()
                if not api_key:
                    break
                if len(api_key) > 10:  # Basic validation
                    self.set(info['key'], api_key)
                    print(f"  ✓ API key saved for {info['name']}")
                    break
                else:
                    print("  Invalid API key. Please try again.")
        
        print("\n" + "=" * 50)
        print("Configuration complete!")
        
        # Show validation results
        validation_results = self.validate_api_keys()
        configured_providers = [provider for provider, valid in validation_results.items() if valid]
        
        if configured_providers:
            print(f"\nConfigured providers: {', '.join(configured_providers)}")
        else:
            print("\nNo providers configured. You can add API keys later using:")
            print("  termux-ai --config-set <provider>_api_key <your_api_key>")


def create_example_config() -> Dict[str, Any]:
    """Create an example configuration dictionary."""
    return {
        "openai_api_key": "your_openai_api_key_here",
        "anthropic_api_key": "your_anthropic_api_key_here",
        "gemini_api_key": "your_gemini_api_key_here",
        "cohere_api_key": "your_cohere_api_key_here",
        "huggingface_api_key": "your_huggingface_api_key_here",
        "default_provider": "openai",
        "default_model": {
            "openai": "gpt-3.5-turbo",
            "anthropic": "claude-3-sonnet-20240229",
            "gemini": "gemini-pro",
            "cohere": "command",
            "huggingface": "microsoft/DialoGPT-medium"
        },
        "default_temperature": 0.7,
        "default_max_tokens": 1000,
        "stream_by_default": False,
        "openai_settings": {
            "organization": "your_org_id_here"
        },
        "anthropic_settings": {
            "version": "2023-06-01"
        }
    }