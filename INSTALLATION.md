# Termux AI Tool - Complete Setup Guide

## Overview

The Termux AI Tool is a powerful command-line interface that allows you to interact with multiple AI providers directly from your Android device using Termux. This guide will walk you through the complete setup process, from installation to testing.

## Prerequisites

### 1. Install Termux
- **F-Droid (Recommended)**: Download from [https://f-droid.org/packages/com.termux/](https://f-droid.org/packages/com.termux/)
- **Google Play Store**: Available but may have limitations

### 2. Update System
```bash
pkg update && pkg upgrade
```

### 3. Install Required Packages
```bash
pkg install python git curl wget
```

### 4. Enable Storage Access (Optional but Recommended)
```bash
termux-setup-storage
```

## Installation

### Method 1: Direct Installation from GitHub

```bash
# Clone the repository
git clone https://github.com/subhobhai943/termux-ai-tool.git

# Navigate to the directory
cd termux-ai-tool

# Install the package
pip install -e .
```

### Method 2: Install from PyPI (When Available)

```bash
pip install termux-ai-tool
```

## Verification

Check if the installation was successful:

```bash
# Test main command
termux-ai --help

# Test short alias
tai --help

# Check version
python -c "import ai_tool; print(ai_tool.__version__)"
```

## Configuration

### Interactive Setup (Recommended)

```bash
termux-ai --setup-wizard
```

### Manual Configuration

Set API keys for your preferred providers:

```bash
# OpenAI (ChatGPT)
termux-ai --config-set openai_api_key YOUR_OPENAI_API_KEY

# Anthropic (Claude)
termux-ai --config-set anthropic_api_key YOUR_ANTHROPIC_API_KEY

# Google Gemini
termux-ai --config-set gemini_api_key YOUR_GEMINI_API_KEY

# Cohere
termux-ai --config-set cohere_api_key YOUR_COHERE_API_KEY

# Hugging Face
termux-ai --config-set huggingface_api_key YOUR_HUGGINGFACE_API_KEY
```

### View Configuration

```bash
# List all configuration
termux-ai --config-list

# Check specific setting
termux-ai --config-get openai_api_key
```

## Getting API Keys

### OpenAI
1. Visit [https://platform.openai.com/api-keys](https://platform.openai.com/api-keys)
2. Sign in or create an account
3. Click "Create new secret key"
4. Copy the key (starts with `sk-`)

### Anthropic
1. Visit [https://console.anthropic.com/](https://console.anthropic.com/)
2. Sign in or create an account
3. Go to API Keys section
4. Generate new key (starts with `sk-ant-`)

### Google Gemini
1. Visit [https://ai.google.dev/](https://ai.google.dev/)
2. Click "Get API key in Google AI Studio"
3. Create new API key
4. Copy the key

### Cohere
1. Visit [https://dashboard.cohere.ai/api-keys](https://dashboard.cohere.ai/api-keys)
2. Sign in or create an account
3. Generate new API key
4. Copy the key

### Hugging Face
1. Visit [https://huggingface.co/settings/tokens](https://huggingface.co/settings/tokens)
2. Sign in or create an account
3. Create new token
4. Select appropriate permissions
5. Copy the token (starts with `hf_`)

## Usage Examples

### Basic Commands

```bash
# Simple query with OpenAI
termux-ai --provider openai --prompt "What is artificial intelligence?"

# Use specific model
termux-ai --provider anthropic --model claude-3-opus-20240229 --prompt "Explain quantum computing"

# Stream response in real-time
termux-ai --provider gemini --stream --prompt "Write a Python function to sort a list"

# Adjust creativity/temperature
termux-ai --provider openai --temperature 0.9 --prompt "Write a creative story about robots"
```

### Interactive Mode

```bash
# Start interactive chat with OpenAI
termux-ai --provider openai --interactive

# Interactive mode with streaming
termux-ai --provider anthropic --interactive --stream
```

### Short Commands (Using 'tai' alias)

```bash
# Quick query
tai -p openai -q "Hello, world!"

# Interactive mode
tai -i -p gemini

# Stream response
tai -p anthropic --stream -q "Explain machine learning"
```

## Testing Your Setup

### Basic Functionality Test

```bash
# Test configuration
termux-ai --list-providers

# Test simple query (replace with your configured provider)
termux-ai --provider openai --prompt "Say hello and confirm you're working!"

# Test streaming
termux-ai --provider openai --stream --prompt "Count from 1 to 5 slowly"
```

### Advanced Testing

```bash
# Test temperature variations
termux-ai --provider openai --temperature 0.1 --prompt "What is 2+2?"
termux-ai --provider openai --temperature 1.5 --prompt "What is 2+2?"

# Test token limits
termux-ai --provider openai --max-tokens 50 --prompt "Write a long essay about AI"

# Test different models
termux-ai --provider openai --model gpt-4 --prompt "Complex reasoning task"
termux-ai --provider anthropic --model claude-3-haiku-20240307 --prompt "Quick question"
```

## Troubleshooting

### Common Issues

#### 1. "Command not found" Error

**Problem**: `termux-ai` command not found after installation.

**Solutions**:
```bash
# Reinstall the package
pip install -e .

# Check if pip installed correctly
pip list | grep termux-ai

# Try using full path
~/.local/bin/termux-ai --help

# Add to PATH (add to ~/.bashrc or ~/.zshrc)
export PATH=$PATH:~/.local/bin
```

#### 2. API Key Errors

**Problem**: "Invalid API key" or "Authentication failed" errors.

**Solutions**:
```bash
# Verify key is set correctly
termux-ai --config-get openai_api_key

# Check for extra spaces or quotes
termux-ai --config-set openai_api_key "$(echo $YOUR_API_KEY | tr -d ' ')"

# Test with a simple request
curl -H "Authorization: Bearer $YOUR_API_KEY" https://api.openai.com/v1/models
```

#### 3. Network/Connection Issues

**Problem**: Connection timeouts or network errors.

**Solutions**:
```bash
# Test internet connection
ping google.com

# Check DNS resolution
nslookup api.openai.com

# Try with verbose output
termux-ai --verbose --provider openai --prompt "test"

# Use VPN if certain APIs are blocked in your region
```

#### 4. Permission Errors

**Problem**: File permission or storage access issues.

**Solutions**:
```bash
# Enable storage access
termux-setup-storage

# Check config directory permissions
ls -la ~/.config/termux-ai-tool/

# Fix permissions if needed
chmod 700 ~/.config/termux-ai-tool/
chmod 600 ~/.config/termux-ai-tool/config.json
```

#### 5. Package Installation Issues

**Problem**: pip install fails with compilation errors.

**Solutions**:
```bash
# Install build tools
pkg install build-essential

# Update pip and setuptools
pip install --upgrade pip setuptools wheel

# Install with no-cache to force fresh download
pip install --no-cache-dir -e .
```

### Debug Mode

Enable verbose logging for detailed troubleshooting:

```bash
termux-ai --verbose --provider openai --prompt "debug test"
```

### System Information

Get detailed system information for bug reports:

```bash
# Check Python version
python --version

# Check pip version
pip --version

# Check installed packages
pip list | grep -E "(termux-ai|requests|click)"

# Check Termux environment
echo $TERMUX_VERSION
uname -a
```

## Usage Statistics

Track your API usage:

```bash
# View usage statistics
termux-ai --usage-stats

# Clear usage data
termux-ai --clear-stats
```

## Configuration Files

The tool stores configuration in:
- **Config Directory**: `~/.config/termux-ai-tool/`
- **Main Config**: `~/.config/termux-ai-tool/config.json`
- **Usage Logs**: `~/.config/termux-ai-tool/logs/usage.log`

### Example Configuration

```json
{
  "openai_api_key": "sk-your-key-here",
  "anthropic_api_key": "sk-ant-your-key-here",
  "gemini_api_key": "your-gemini-key-here",
  "default_provider": "openai",
  "default_temperature": 0.7,
  "stream_by_default": false
}
```

## Performance Tips

1. **Use Streaming**: For long responses, use `--stream` to see output in real-time
2. **Optimize Temperature**: Lower values (0.1-0.3) for factual queries, higher (0.7-1.0) for creative tasks
3. **Choose Right Model**: Use faster models like `gpt-3.5-turbo` or `claude-3-haiku` for simple tasks
4. **Limit Tokens**: Use `--max-tokens` to control response length and costs

## Security Best Practices

1. **Protect API Keys**: Never share your API keys publicly
2. **Use Environment Variables**: For additional security, use environment variables
3. **Regular Key Rotation**: Rotate API keys periodically
4. **Monitor Usage**: Keep track of your API usage and costs

## Contributing

Found a bug or want to contribute? Visit our GitHub repository:
[https://github.com/subhobhai943/termux-ai-tool](https://github.com/subhobhai943/termux-ai-tool)

## Support

For help and support:
1. Check this troubleshooting guide
2. Search existing GitHub Issues
3. Create a new issue with system information
4. Include output from: `termux-ai --system-info`

## Updates

Keep your tool updated:

```bash
# Update from Git
cd termux-ai-tool
git pull origin main
pip install -e .

# Or if installed from PyPI
pip install --upgrade termux-ai-tool
```

---

**Happy AI chatting from your Android device! 🤖📱**