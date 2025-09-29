# Documentation

This directory contains visual documentation for the Termux AI Tool project.

## Architecture Diagram

![System Architecture](architecture_diagram.png)

The architecture diagram shows the complete system structure including:
- CLI Interface Layer
- Configuration Management Layer  
- AI Client Management Layer
- API Communication Layer
- Utility Functions Layer

## Project Dashboard

![Project Dashboard](project_dashboard.png)

The project dashboard provides an overview of:
- All implemented components
- Supported AI providers
- Key features
- Documentation status
- Deployment completion

## Usage Flow

1. **User Input** → CLI Interface processes commands
2. **Configuration** → Loads API keys and settings securely
3. **Client Selection** → Chooses appropriate AI provider client
4. **API Communication** → Sends requests to AI provider
5. **Response Processing** → Formats and displays responses
6. **Logging** → Tracks usage statistics (optional)

## Component Details

### CLI Interface (`cli.py`)
- Argument parsing with argparse
- Interactive mode support
- Streaming response handling
- Configuration management commands

### API Clients (`api_clients.py`)
- Abstract base class for consistency
- Provider-specific implementations
- Unified response interface
- Error handling and retry logic

### Configuration (`config.py`)
- Secure JSON-based storage
- API key validation
- Interactive setup wizard
- Termux-optimized file permissions

### Utilities (`utils.py`)
- Response formatting utilities
- System environment detection
- Usage tracking and statistics
- Error handling helpers

For more details, see the main [README.md](../README.md) file.