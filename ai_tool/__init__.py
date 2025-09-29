#!/usr/bin/env python3
"""
Termux AI Tool - Multi-AI API Integration CLI
A powerful command-line tool for Termux that integrates with multiple AI providers.

Supported Providers:
- OpenAI (ChatGPT, GPT-4)
- Anthropic (Claude)
- Google Gemini
- Cohere
- Hugging Face

Author: Subhobhai
License: MIT
"""

__version__ = "1.0.0"
__author__ = "Subhobhai"
__email__ = "subhobhai943@example.com"
__description__ = "Multi-AI API Integration CLI for Termux"

from .cli import main
from .config import ConfigManager
from .api_clients import AIClientManager
from .utils import print_banner, check_termux_environment

__all__ = [
    'main',
    'ConfigManager', 
    'AIClientManager',
    'print_banner',
    'check_termux_environment'
]