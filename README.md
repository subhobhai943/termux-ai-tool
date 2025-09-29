# Termux AI Tool 🤖

A powerful command-line tool for Termux that integrates with multiple AI providers, allowing you to interact with various AI models directly from your Android device's terminal.

## 🏗️ Architecture

The Termux AI Tool follows a modular, layered architecture designed for extensibility and security:

![System Architecture](docs/architecture_diagram.png)

*For detailed architecture documentation, see [docs/README.md](docs/README.md)*

## ✨ Features

- 🔗 **Multi-AI Provider Support**: OpenAI (ChatGPT), Anthropic (Claude), Google Gemini, Cohere, Hugging Face
- 🎯 **Easy to Use**: Simple command-line interface with intuitive commands
- 🔧 **Highly Configurable**: Flexible configuration management with secure API key storage  
- 💬 **Interactive Mode**: Real-time chat sessions with AI models
- 🌊 **Streaming Support**: Real-time response streaming for better user experience
- 📱 **Termux Optimized**: Designed specifically for Android's Termux environment
- 🛡️ **Secure**: API keys stored securely with proper file permissions
- 📊 **Usage Tracking**: Optional usage statistics and logging

## 🚀 Quick Start

### Prerequisites

1. **Termux**: Install from [F-Droid](https://f-droid.org/packages/com.termux/) (recommended) or Google Play Store
2. **Python 3.7+**: Usually pre-installed in Termux
3. **Internet Connection**: Required for API calls

### Installation

1. **Update Termux packages**:
```bash
pkg update && pkg upgrade
```

2. **Install required packages**:
```bash
pkg install python git
```

3. **Clone the repository**:
```bash
git clone https://github.com/subhobhai943/termux-ai-tool.git
cd termux-ai-tool
```

4. **Install the tool**:
```bash
pip install -e .
```

5. **Verify installation**:
```bash
termux-ai --help
```

6. **Run automated tests** (optional):
```bash
bash test_installation.sh
```

*For detailed installation instructions, see [INSTALLATION.md](INSTALLATION.md)*

## 🔑 API Key Setup

Before using the tool, you need to obtain API keys from your preferred AI providers:

### OpenAI (ChatGPT)
1. Visit [OpenAI Platform](https://platform.openai.com/api-keys)
2. Create an account and generate an API key
3. Set the key: `termux-ai --config-set openai_api_key YOUR_API_KEY`

### Anthropic (Claude)
1. Visit [Anthropic Console](https://console.anthropic.com/)
2. Create an account and generate an API key
3. Set the key: `termux-ai --config-set anthropic_api_key YOUR_API_KEY`

### Google Gemini
1. Visit [Google AI Studio](https://ai.google.dev/)
2. Create an API key
3. Set the key: `termux-ai --config-set gemini_api_key YOUR_API_KEY`

### Cohere
1. Visit [Cohere Dashboard](https://dashboard.cohere.ai/api-keys)
2. Create an account and generate an API key
3. Set the key: `termux-ai --config-set cohere_api_key YOUR_API_KEY`

### Hugging Face
1. Visit [Hugging Face Settings](https://huggingface.co/settings/tokens)
2. Create a token
3. Set the key: `termux-ai --config-set huggingface_api_key YOUR_API_KEY`

### Interactive Setup

Run the setup wizard for guided configuration:
```bash
termux-ai --config-wizard
```

## 📖 Usage Examples

### Basic Usage

```bash
# Ask a question using OpenAI
termux-ai --provider openai --prompt "What is quantum computing?"

# Use a specific model
termux-ai --provider anthropic --model claude-3-opus-20240229 --prompt "Explain machine learning"

# Adjust creativity with temperature
termux-ai --provider gemini --temperature 0.9 --prompt "Write a creative story"

# Stream the response in real-time
termux-ai --provider openai --stream --prompt "Tell me about space exploration"
```

### Interactive Mode

Start a conversation session:
```bash
# Interactive mode with OpenAI
termux-ai --provider openai --interactive

# Interactive mode with streaming
termux-ai --provider anthropic --interactive --stream
```

### Configuration Management

```bash
# List all configuration
termux-ai --config-list

# Get a specific config value
termux-ai --config-get default_provider

# Set default provider
termux-ai --config-set default_provider anthropic

# List available providers
termux-ai --list-providers
```

### Short Alias

For convenience, you can use the short alias `tai`:
```bash
tai --provider openai --prompt "Hello world!"
tai -p gemini -q "Explain Python programming"
tai -i -p anthropic  # Interactive mode
```

## 🛠️ Advanced Usage

### Custom Models

```bash
# Use specific models
termux-ai --provider openai --model gpt-4 --prompt "Complex reasoning task"
termux-ai --provider anthropic --model claude-3-haiku-20240307 --prompt "Quick question"
```

### Response Control

```bash
# Limit response length
termux-ai --provider openai --max-tokens 100 --prompt "Brief explanation of AI"

# Control randomness
termux-ai --provider gemini --temperature 0.1 --prompt "Factual information about Mars"
```

### Batch Processing

```bash
# Process multiple prompts (create a script)
echo "What is AI?" | termux-ai --provider openai
echo "Explain blockchain" | termux-ai --provider anthropic  
echo "Python vs Java" | termux-ai --provider gemini
```

## 📁 Configuration

Configuration files are stored in `~/.config/termux-ai-tool/`:

- `config.json`: Main configuration file
- `logs/usage.log`: Usage statistics (if enabled)

### Configuration Options

```json
{
  "default_provider": "openai",
  "default_temperature": 0.7,
  "default_max_tokens": 1000,
  "stream_by_default": false,
  "openai_settings": {
    "organization": "your_org_id"
  }
}
```

## 🔍 Troubleshooting

### Common Issues

1. **"Command not found"**: 
   - Ensure Python and pip are installed: `pkg install python`
   - Reinstall the tool: `pip install -e .`

2. **API Key Errors**:
   - Verify your API key is correct
   - Check if the key has sufficient credits/quota
   - Ensure no extra spaces in the key

3. **Network Issues**:
   - Check internet connection: `ping google.com`
   - Some regions may need VPN for certain providers

4. **Permission Errors**:
   - Run: `termux-setup-storage` for storage access
   - Check file permissions in config directory

### Debug Mode

Enable verbose output for troubleshooting:
```bash
termux-ai --verbose --provider openai --prompt "test"
```

### System Information

Check your environment:
```bash
termux-ai --system-info
```

*For detailed troubleshooting, see [INSTALLATION.md](INSTALLATION.md)*

## 📊 Usage Statistics

Track your API usage:
```bash
# View usage stats
termux-ai --usage-stats

# Clear usage data
termux-ai --clear-stats
```

## 🔒 Security

- API keys are stored with restricted file permissions (600)
- Configuration directory has limited access (700)
- No API keys are logged or transmitted except to official APIs
- Use environment variables for additional security if needed

## 🤝 Contributing

Contributions are welcome! Here's how to contribute:

1. Fork the repository
2. Create a feature branch: `git checkout -b feature-name`
3. Make your changes and test them
4. Commit your changes: `git commit -am 'Add new feature'`
5. Push to the branch: `git push origin feature-name`
6. Submit a Pull Request

### Development Setup

```bash
# Clone your fork
git clone https://github.com/YOUR_USERNAME/termux-ai-tool.git
cd termux-ai-tool

# Install in development mode
pip install -e .

# Run tests (if available)
python -m pytest
```

## 📋 Available Models

### OpenAI
- `gpt-4` - Most capable model
- `gpt-4-turbo` - Fast and capable
- `gpt-3.5-turbo` - Good balance of capability and cost
- `gpt-3.5-turbo-16k` - Larger context window

### Anthropic
- `claude-3-opus-20240229` - Most capable Claude model
- `claude-3-sonnet-20240229` - Balanced performance
- `claude-3-haiku-20240307` - Fast and efficient
- `claude-2.1` - Previous generation
- `claude-2.0` - Previous generation

### Google Gemini
- `gemini-pro` - Text-based tasks
- `gemini-pro-vision` - Multimodal (text + images)

### Cohere
- `command` - General purpose
- `command-light` - Faster responses
- `command-nightly` - Latest features

### Hugging Face
- `microsoft/DialoGPT-medium` - Conversational
- `microsoft/DialoGPT-large` - Better conversations
- `facebook/blenderbot-400M-distill` - Lightweight
- `gpt2` - Basic text generation

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🙏 Acknowledgments

- Thanks to all AI providers for their APIs
- Termux community for the amazing Android terminal
- OpenAI, Anthropic, Google, Cohere, and Hugging Face for their AI models

## 📞 Support

If you encounter any issues or have questions:

1. Check the [Troubleshooting](#troubleshooting) section
2. Search existing [GitHub Issues](https://github.com/subhobhai943/termux-ai-tool/issues)
3. Create a new issue with detailed information
4. Include system info: `termux-ai --system-info`

## 🔄 Updates

Stay updated with the latest features:
```bash
# Update the tool
git pull origin main
pip install -e .
```

---

**Made with ❤️ for the Termux community**

*Enhance your Android device with the power of AI!*