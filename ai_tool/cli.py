#!/usr/bin/env python3
"""
Termux AI Tool - Multi-AI API Integration CLI
A command-line tool for Termux that supports multiple AI APIs including OpenAI, Anthropic, Google Gemini, and more.
"""

import argparse
import sys
import os
import json
from typing import Optional, Dict, Any

from .config import ConfigManager
from .api_clients import AIClientManager
from .utils import print_response, handle_error


def create_parser() -> argparse.ArgumentParser:
    """Create and configure the argument parser."""
    parser = argparse.ArgumentParser(
        description="Termux AI Tool - Multi-AI API Integration",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  %(prog)s --provider openai --prompt "Hello, world!"
  %(prog)s --provider anthropic --prompt "Explain quantum computing"
  %(prog)s --provider gemini --prompt "Write a Python script"
  %(prog)s --config-set openai_api_key YOUR_API_KEY
  %(prog)s --list-providers
        """
    )
    
    # Main arguments
    parser.add_argument(
        "--provider", "-p",
        choices=["openai", "anthropic", "gemini", "cohere", "huggingface"],
        help="AI provider to use"
    )
    
    parser.add_argument(
        "--prompt", "-q",
        type=str,
        help="Prompt to send to the AI"
    )
    
    parser.add_argument(
        "--model", "-m",
        type=str,
        help="Model to use (e.g., gpt-4, claude-3, gemini-pro)"
    )
    
    parser.add_argument(
        "--temperature", "-t",
        type=float,
        default=0.7,
        help="Temperature for response generation (0.0-2.0)"
    )
    
    parser.add_argument(
        "--max-tokens",
        type=int,
        help="Maximum tokens in response"
    )
    
    parser.add_argument(
        "--stream",
        action="store_true",
        help="Stream the response in real-time"
    )
    
    # Configuration commands
    parser.add_argument(
        "--config-set",
        nargs=2,
        metavar=("KEY", "VALUE"),
        help="Set configuration value"
    )
    
    parser.add_argument(
        "--config-get",
        metavar="KEY",
        help="Get configuration value"
    )
    
    parser.add_argument(
        "--config-list",
        action="store_true",
        help="List all configuration"
    )
    
    parser.add_argument(
        "--list-providers",
        action="store_true",
        help="List all available providers"
    )
    
    # Interactive mode
    parser.add_argument(
        "--interactive", "-i",
        action="store_true",
        help="Start interactive chat mode"
    )
    
    # Verbose output
    parser.add_argument(
        "--verbose", "-v",
        action="store_true",
        help="Enable verbose output"
    )
    
    return parser


def interactive_mode(client_manager: AIClientManager, provider: str, model: Optional[str] = None):
    """Start interactive chat mode."""
    print(f"Starting interactive mode with {provider}")
    print("Type 'quit', 'exit', or Ctrl+C to stop")
    print("-" * 50)
    
    conversation_history = []
    
    try:
        while True:
            try:
                user_input = input("You: ").strip()
                
                if user_input.lower() in ['quit', 'exit']:
                    break
                
                if not user_input:
                    continue
                
                # Add user message to history
                conversation_history.append({"role": "user", "content": user_input})
                
                # Get AI response
                response = client_manager.get_response(
                    provider=provider,
                    messages=conversation_history,
                    model=model,
                    stream=True
                )
                
                print("AI: ", end="")
                full_response = ""
                for chunk in response:
                    if chunk:
                        print(chunk, end="", flush=True)
                        full_response += chunk
                print()  # New line after response
                
                # Add AI response to history
                conversation_history.append({"role": "assistant", "content": full_response})
                
            except KeyboardInterrupt:
                print("\n\nGoodbye!")
                break
            except Exception as e:
                print(f"\nError: {e}")
                
    except KeyboardInterrupt:
        print("\n\nGoodbye!")


def main():
    """Main entry point for the CLI."""
    parser = create_parser()
    args = parser.parse_args()
    
    # Initialize configuration manager
    config_manager = ConfigManager()
    
    # Handle configuration commands
    if args.config_set:
        key, value = args.config_set
        config_manager.set(key, value)
        print(f"Configuration set: {key}")
        return
    
    if args.config_get:
        value = config_manager.get(args.config_get)
        if value:
            print(f"{args.config_get}: {value}")
        else:
            print(f"Configuration key '{args.config_get}' not found")
        return
    
    if args.config_list:
        config = config_manager.get_all()
        print("Configuration:")
        for key, value in config.items():
            # Hide API keys for security
            if 'api_key' in key.lower() or 'token' in key.lower():
                value = '*' * 8 if value else 'Not set'
            print(f"  {key}: {value}")
        return
    
    if args.list_providers:
        providers = ["openai", "anthropic", "gemini", "cohere", "huggingface"]
        print("Available providers:")
        for provider in providers:
            print(f"  - {provider}")
        return
    
    # Validate required arguments for AI requests
    if not args.provider and not args.interactive:
        parser.error("--provider is required for AI requests")
    
    if not args.prompt and not args.interactive:
        parser.error("--prompt is required for AI requests")
    
    # Initialize AI client manager
    try:
        client_manager = AIClientManager(config_manager)
    except Exception as e:
        handle_error(f"Failed to initialize AI clients: {e}")
        sys.exit(1)
    
    try:
        # Interactive mode
        if args.interactive:
            provider = args.provider or input("Choose provider (openai/anthropic/gemini/cohere/huggingface): ").strip()
            if provider not in ["openai", "anthropic", "gemini", "cohere", "huggingface"]:
                print("Invalid provider selected")
                sys.exit(1)
            interactive_mode(client_manager, provider, args.model)
            return
        
        # Single prompt mode
        messages = [{"role": "user", "content": args.prompt}]
        
        response = client_manager.get_response(
            provider=args.provider,
            messages=messages,
            model=args.model,
            temperature=args.temperature,
            max_tokens=args.max_tokens,
            stream=args.stream
        )
        
        if args.stream:
            for chunk in response:
                if chunk:
                    print(chunk, end="", flush=True)
            print()  # New line after response
        else:
            print_response(response)
            
    except KeyboardInterrupt:
        print("\n\nOperation cancelled by user")
        sys.exit(1)
    except Exception as e:
        handle_error(f"Error processing request: {e}")
        sys.exit(1)


if __name__ == "__main__":
    main()