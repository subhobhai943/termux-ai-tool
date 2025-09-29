# Documentation

This directory contains comprehensive documentation for the Termux AI Tool project.

## 📋 Documentation Index

### 🏗️ Architecture & Design
- **[System Architecture](architecture.md)** - Complete system design with ASCII diagrams
- **[Project Status Dashboard](project_status.md)** - Project completion status and statistics

### 📚 User Guides
- **[Main README](../README.md)** - Project overview and quick start
- **[Installation Guide](../INSTALLATION.md)** - Complete setup and troubleshooting
- **[Testing Script](../test_installation.sh)** - Automated validation tool

### 🔧 Developer Resources
- **[Package Configuration](../setup.py)** - Python package setup
- **[Dependencies](../requirements.txt)** - Required packages
- **[Configuration Example](../config.json.example)** - Sample configuration

## 🏗️ System Architecture

The Termux AI Tool follows a clean, layered architecture:

```
┌─────────────────────────────────────────────┐
│              TERMUX AI TOOL ARCHITECTURE              │
├─────────────────────────────────────────────┤
│ 🖥️  User Interface Layer (CLI)                    │
│ ⚙️  Configuration Management                       │
│ 🤖  AI Client Management (5 Providers)            │
│ 🌐  API Communication Layer                        │
│ 🛠️  Utility Functions                               │
└─────────────────────────────────────────────┘
```

*For detailed architecture, see [architecture.md](architecture.md)*

## 📊 Project Dashboard

**Status**: ✅ **COMPLETE**  
**Components**: 4 core modules, 5 AI providers, 6+ features  
**Documentation**: Comprehensive guides and examples  
**Testing**: Automated validation script  
**Deployment**: GitHub repository with all files  

*For full dashboard, see [project_status.md](project_status.md)*

## 📝 Usage Flow Documentation

### 1. Installation Process
1. **Prerequisites**: Termux, Python, Git
2. **Clone Repository**: `git clone https://github.com/subhobhai943/termux-ai-tool.git`
3. **Install Package**: `pip install -e .`
4. **Run Tests**: `bash test_installation.sh`
5. **Configure**: `termux-ai --config-wizard`

### 2. Component Interaction
```
User Input → CLI Parser → Config Manager → Client Manager → AI Provider
                                                            │
Formatted Output ← Response Handler ← API Response ←─────┘
```

### 3. Supported Operations
- **Simple Queries**: Single prompt to any provider
- **Interactive Chat**: Real-time conversation mode
- **Configuration**: API key management and settings
- **Provider Management**: Switch between AI services
- **Usage Tracking**: Optional statistics logging

## 🔍 Component Details

### CLI Interface (`cli.py`)
- **Primary Function**: Command-line argument parsing and user interaction
- **Key Features**: Interactive mode, streaming support, configuration commands
- **Entry Points**: `termux-ai` and `tai` (short alias)
- **Lines of Code**: 259

### API Clients (`api_clients.py`)
- **Primary Function**: Interface with multiple AI providers
- **Supported Providers**: OpenAI, Anthropic, Gemini, Cohere, HuggingFace
- **Key Features**: Abstract base class, streaming responses, error handling
- **Lines of Code**: 444

### Configuration (`config.py`)
- **Primary Function**: Secure configuration and API key management
- **Key Features**: JSON storage, permission handling, validation
- **Security**: File permissions (600/700), masked sensitive data
- **Lines of Code**: 236

### Utilities (`utils.py`)
- **Primary Function**: Support functions and system validation
- **Key Features**: Termux detection, response formatting, usage tracking
- **Platform Support**: Android/Termux optimizations
- **Lines of Code**: 334

## 🤝 Contributing Guidelines

### Development Setup
1. Fork the repository
2. Create a feature branch
3. Make changes and add tests
4. Update documentation if needed
5. Submit a pull request

### Code Standards
- **Python Style**: PEP 8 compliance
- **Documentation**: Comprehensive docstrings
- **Error Handling**: Graceful failure modes
- **Security**: No hardcoded secrets

### Testing
- Run `bash test_installation.sh` for validation
- Test with multiple AI providers
- Verify Termux-specific functionality
- Check security measures

## 🔗 External Resources

### AI Provider Documentation
- **OpenAI**: https://platform.openai.com/docs
- **Anthropic**: https://docs.anthropic.com
- **Google Gemini**: https://ai.google.dev/docs
- **Cohere**: https://docs.cohere.com
- **HuggingFace**: https://huggingface.co/docs

### Termux Resources
- **Official Wiki**: https://wiki.termux.com
- **F-Droid**: https://f-droid.org/packages/com.termux
- **GitHub**: https://github.com/termux/termux-app

### Python Packaging
- **setuptools**: https://setuptools.pypa.io
- **pip**: https://pip.pypa.io
- **PyPI**: https://pypi.org

## ❓ Support & Help

### Getting Help
1. **Check Documentation**: Start with README.md and INSTALLATION.md
2. **Run Diagnostics**: Use `termux-ai --system-info`
3. **Search Issues**: Check existing GitHub issues
4. **Create Issue**: Report bugs with full details

### Common Issues
- **Installation Problems**: See INSTALLATION.md troubleshooting section
- **API Key Errors**: Verify keys and check provider status
- **Network Issues**: Test internet connection and provider access
- **Permission Errors**: Run `termux-setup-storage`

---

**Documentation Version**: 1.0.0  
**Last Updated**: September 30, 2025  
**Repository**: https://github.com/subhobhai943/termux-ai-tool  

*For the most up-to-date information, always refer to the main repository.*