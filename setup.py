"""
Setup script for Termux AI Tool
"""

from setuptools import setup, find_packages
import os

# Read the README file
def read_readme():
    with open("README.md", "r", encoding="utf-8") as fh:
        return fh.read()

# Read requirements
def read_requirements():
    with open("requirements.txt", "r", encoding="utf-8") as fh:
        return [line.strip() for line in fh if line.strip() and not line.startswith("#")]

setup(
    name="termux-ai-tool",
    version="1.0.0",
    author="Subhobhai",
    author_email="subhobhai943@example.com",
    description="Multi-AI API Integration CLI for Termux",
    long_description=read_readme(),
    long_description_content_type="text/markdown",
    url="https://github.com/subhobhai943/termux-ai-tool",
    packages=find_packages(),
    classifiers=[
        "Development Status :: 4 - Beta",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: MIT License",
        "Operating System :: POSIX :: Linux",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "Topic :: Scientific/Engineering :: Artificial Intelligence",
        "Topic :: Software Development :: Libraries :: Python Modules",
        "Topic :: Terminals",
        "Environment :: Console",
    ],
    python_requires=">=3.7",
    install_requires=read_requirements(),
    entry_points={
        "console_scripts": [
            "termux-ai=ai_tool.cli:main",
            "tai=ai_tool.cli:main",  # Short alias
        ],
    },
    keywords="ai, termux, cli, openai, anthropic, gemini, api, chatgpt, claude",
    project_urls={
        "Bug Reports": "https://github.com/subhobhai943/termux-ai-tool/issues",
        "Source": "https://github.com/subhobhai943/termux-ai-tool",
        "Documentation": "https://github.com/subhobhai943/termux-ai-tool#readme",
    },
)