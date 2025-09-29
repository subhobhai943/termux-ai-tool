"""
Utility functions for Termux AI Tool
"""

import sys
import os
import json
import time
from typing import Any, Dict, Optional
from datetime import datetime
import re


def print_response(response: str, prefix: str = "AI: "):
    """Print AI response with proper formatting."""
    if not response:
        print("No response received.")
        return
    
    print(f"{prefix}{response}")


def handle_error(error_msg: str, exit_code: int = 1):
    """Handle and display errors."""
    print(f"Error: {error_msg}", file=sys.stderr)
    if exit_code > 0:
        sys.exit(exit_code)


def print_banner():
    """Print the application banner."""
    banner = """
╔═══════════════════════════════════════╗
║          Termux AI Tool               ║
║     Multi-AI API Integration CLI      ║
║                                       ║
║  Supports: OpenAI, Anthropic,        ║
║           Gemini, Cohere, HuggingFace ║
╚═══════════════════════════════════════╝
"""
    print(banner)


def print_colored_text(text: str, color: str = "white"):
    """Print colored text for better UX in terminal."""
    color_codes = {
        "red": "\033[91m",
        "green": "\033[92m",
        "yellow": "\033[93m",
        "blue": "\033[94m",
        "magenta": "\033[95m",
        "cyan": "\033[96m",
        "white": "\033[97m",
        "reset": "\033[0m"
    }
    
    color_code = color_codes.get(color.lower(), color_codes["white"])
    reset_code = color_codes["reset"]
    print(f"{color_code}{text}{reset_code}")


def validate_api_key(api_key: str, provider: str) -> bool:
    """Basic validation for API keys."""
    if not api_key or not isinstance(api_key, str):
        return False
    
    api_key = api_key.strip()
    
    # Basic length and format checks for different providers
    validation_rules = {
        'openai': {'min_length': 20, 'prefix': 'sk-'},
        'anthropic': {'min_length': 20, 'prefix': 'sk-ant-'},
        'gemini': {'min_length': 30, 'prefix': None},
        'cohere': {'min_length': 20, 'prefix': None},
        'huggingface': {'min_length': 20, 'prefix': 'hf_'}
    }
    
    rule = validation_rules.get(provider.lower())
    if not rule:
        return len(api_key) > 10  # Generic validation
    
    if len(api_key) < rule['min_length']:
        return False
    
    if rule['prefix'] and not api_key.startswith(rule['prefix']):
        return False
    
    return True


def format_model_list(models: list, provider: str) -> str:
    """Format model list for display."""
    if not models:
        return f"No models available for {provider}"
    
    formatted = f"Available models for {provider}:\n"
    for i, model in enumerate(models, 1):
        formatted += f"  {i}. {model}\n"
    
    return formatted.rstrip()


def estimate_tokens(text: str) -> int:
    """Rough estimation of token count for text."""
    # Approximate: 4 characters per token on average
    return len(text) // 4


def truncate_text(text: str, max_length: int = 100) -> str:
    """Truncate text for display purposes."""
    if len(text) <= max_length:
        return text
    return text[:max_length] + "..."


def parse_key_value_pairs(pairs: list) -> Dict[str, str]:
    """Parse key-value pairs from command line arguments."""
    result = {}
    for pair in pairs:
        if '=' in pair:
            key, value = pair.split('=', 1)
            result[key.strip()] = value.strip()
        else:
            # Treat as boolean flag
            result[pair.strip()] = True
    return result


def create_config_backup(config_path: str) -> str:
    """Create a backup of the configuration file."""
    if not os.path.exists(config_path):
        return None
    
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    backup_path = f"{config_path}.backup_{timestamp}"
    
    try:
        import shutil
        shutil.copy2(config_path, backup_path)
        return backup_path
    except Exception as e:
        print(f"Warning: Failed to create config backup: {e}")
        return None


def check_termux_environment() -> Dict[str, Any]:
    """Check if running in Termux and get environment info."""
    env_info = {
        'is_termux': False,
        'termux_version': None,
        'android_version': None,
        'architecture': None,
        'storage_available': True
    }
    
    # Check for Termux-specific environment variables
    if os.environ.get('TERMUX_VERSION') or os.path.exists('/data/data/com.termux'):
        env_info['is_termux'] = True
        env_info['termux_version'] = os.environ.get('TERMUX_VERSION', 'Unknown')
    
    # Check Android version
    try:
        with open('/system/build.prop', 'r') as f:
            content = f.read()
            version_match = re.search(r'ro.build.version.release=(.+)', content)
            if version_match:
                env_info['android_version'] = version_match.group(1).strip()
    except (FileNotFoundError, PermissionError):
        pass
    
    # Check architecture
    env_info['architecture'] = os.uname().machine if hasattr(os, 'uname') else 'Unknown'
    
    # Check storage permissions/availability
    try:
        test_file = '/data/data/com.termux/files/home/.test_write'
        with open(test_file, 'w') as f:
            f.write('test')
        os.remove(test_file)
    except (PermissionError, OSError):
        env_info['storage_available'] = False
    
    return env_info


def setup_termux_permissions():
    """Setup necessary permissions for Termux."""
    print("Setting up Termux environment...")
    
    env_info = check_termux_environment()
    
    if not env_info['is_termux']:
        print("Warning: This tool is designed for Termux but doesn't appear to be running in Termux.")
        return
    
    if not env_info['storage_available']:
        print("Warning: Storage permissions may be limited. Consider running:")
        print("  termux-setup-storage")
        print("to enable external storage access.")
    
    print(f"Termux Version: {env_info['termux_version']}")
    if env_info['android_version']:
        print(f"Android Version: {env_info['android_version']}")
    print(f"Architecture: {env_info['architecture']}")


def check_internet_connection() -> bool:
    """Check if internet connection is available."""
    try:
        import socket
        socket.create_connection(("8.8.8.8", 53), timeout=3)
        return True
    except OSError:
        return False


def get_system_info() -> Dict[str, str]:
    """Get system information for debugging."""
    info = {}
    
    try:
        info['python_version'] = sys.version
        info['platform'] = sys.platform
        info['executable'] = sys.executable
    except Exception:
        pass
    
    try:
        import platform
        info['system'] = platform.system()
        info['release'] = platform.release()
        info['machine'] = platform.machine()
    except Exception:
        pass
    
    # Add Termux-specific info
    termux_info = check_termux_environment()
    info.update(termux_info)
    
    return info


def log_request(provider: str, model: str, prompt_length: int, response_length: int):
    """Log API requests for usage tracking."""
    log_dir = os.path.expanduser("~/.config/termux-ai-tool/logs")
    os.makedirs(log_dir, exist_ok=True)
    
    log_file = os.path.join(log_dir, "usage.log")
    
    timestamp = datetime.now().isoformat()
    log_entry = {
        'timestamp': timestamp,
        'provider': provider,
        'model': model,
        'prompt_tokens': estimate_tokens(str(prompt_length)),
        'response_tokens': estimate_tokens(str(response_length))
    }
    
    try:
        with open(log_file, 'a') as f:
            f.write(json.dumps(log_entry) + '\n')
    except Exception:
        pass  # Fail silently for logging


def show_usage_stats():
    """Show usage statistics."""
    log_file = os.path.expanduser("~/.config/termux-ai-tool/logs/usage.log")
    
    if not os.path.exists(log_file):
        print("No usage data found.")
        return
    
    try:
        with open(log_file, 'r') as f:
            lines = f.readlines()
        
        print(f"Total API calls: {len(lines)}")
        
        providers = {}
        models = {}
        total_tokens = 0
        
        for line in lines:
            try:
                entry = json.loads(line.strip())
                provider = entry['provider']
                model = entry['model']
                tokens = entry.get('prompt_tokens', 0) + entry.get('response_tokens', 0)
                
                providers[provider] = providers.get(provider, 0) + 1
                models[model] = models.get(model, 0) + 1
                total_tokens += tokens
                
            except json.JSONDecodeError:
                continue
        
        print(f"\nProviders used:")
        for provider, count in sorted(providers.items()):
            print(f"  {provider}: {count} calls")
        
        print(f"\nTop models:")
        for model, count in sorted(models.items(), key=lambda x: x[1], reverse=True)[:5]:
            print(f"  {model}: {count} calls")
        
        print(f"\nApproximate total tokens: {total_tokens}")
        
    except Exception as e:
        print(f"Error reading usage stats: {e}")


def clear_usage_stats():
    """Clear usage statistics."""
    log_file = os.path.expanduser("~/.config/termux-ai-tool/logs/usage.log")
    
    try:
        if os.path.exists(log_file):
            os.remove(log_file)
            print("Usage statistics cleared.")
        else:
            print("No usage data to clear.")
    except Exception as e:
        print(f"Error clearing usage stats: {e}")


def validate_temperature(temperature: float) -> bool:
    """Validate temperature parameter."""
    return 0.0 <= temperature <= 2.0


def validate_max_tokens(max_tokens: int) -> bool:
    """Validate max_tokens parameter."""
    return 1 <= max_tokens <= 100000