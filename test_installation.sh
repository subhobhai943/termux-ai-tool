#!/bin/bash

# Termux AI Tool - Automated Testing Script
# This script performs comprehensive tests on the Termux AI Tool installation

echo "🚀 Termux AI Tool - Automated Testing Script"
echo "==============================================="
echo

# Color codes for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Test counter
TESTS_PASSED=0
TESTS_FAILED=0

# Function to print test results
print_result() {
    if [ $1 -eq 0 ]; then
        echo -e "${GREEN}✓ PASS${NC}: $2"
        ((TESTS_PASSED++))
    else
        echo -e "${RED}✗ FAIL${NC}: $2"
        ((TESTS_FAILED++))
    fi
}

# Function to run a test
run_test() {
    echo -e "${BLUE}Running:${NC} $1"
    if eval "$2" &> /dev/null; then
        print_result 0 "$1"
    else
        print_result 1 "$1"
        if [ ! -z "$3" ]; then
            echo -e "${YELLOW}  Suggestion: $3${NC}"
        fi
    fi
    echo
}

echo "🔍 Testing Prerequisites..."
echo "------------------------------"

# Test Python installation
run_test "Python installation" "python3 --version" "Install Python: pkg install python"

# Test pip installation
run_test "pip installation" "pip --version" "Upgrade pip: python3 -m pip install --upgrade pip"

# Test git installation
run_test "git installation" "git --version" "Install git: pkg install git"

# Test internet connection
run_test "Internet connection" "ping -c 1 google.com" "Check your internet connection"

echo "🔧 Testing Package Installation..."
echo "-----------------------------------"

# Test if termux-ai is installed
run_test "termux-ai command availability" "termux-ai --help"

# Test if tai alias works
run_test "tai alias availability" "tai --help"

# Test package import
run_test "Python package import" "python3 -c 'import ai_tool; print(ai_tool.__version__)'"

echo "⚙️ Testing Configuration..."
echo "-------------------------"

# Test config directory
run_test "Configuration directory exists" "[ -d ~/.config/termux-ai-tool ]"

# Test config file creation
run_test "Config file can be created" "termux-ai --config-set test_key test_value && termux-ai --config-get test_key"

# Clean up test config
termux-ai --config-set test_key "" &> /dev/null

echo "🤖 Testing AI Provider Support..."
echo "--------------------------------"

# Test provider listing
run_test "List available providers" "termux-ai --list-providers | grep -E 'openai|anthropic|gemini|cohere|huggingface'"

# Test configuration listing
run_test "Configuration listing" "termux-ai --config-list"

echo "🔐 Testing Security Features..."
echo "---------------------------"

# Test config directory permissions
if [ -d ~/.config/termux-ai-tool ]; then
    PERMS=$(stat -c "%a" ~/.config/termux-ai-tool)
    if [ "$PERMS" = "700" ]; then
        print_result 0 "Config directory permissions (700)"
    else
        print_result 1 "Config directory permissions (got $PERMS, expected 700)"
        echo -e "${YELLOW}  Fix: chmod 700 ~/.config/termux-ai-tool${NC}"
    fi
fi

# Test if API keys are masked in config list
run_test "API keys are masked in output" "termux-ai --config-set test_api_key sk-1234567890 && termux-ai --config-list | grep -q '\\*\\*\\*\\*\\*\\*\\*\\*'"

# Clean up test API key
termux-ai --config-set test_api_key "" &> /dev/null

echo "📊 Testing Advanced Features..."
echo "----------------------------"

# Test usage stats (should not fail even if empty)
run_test "Usage statistics access" "termux-ai --usage-stats"

# Test system info
run_test "System information access" "termux-ai --system-info"

# Test environment detection
run_test "Termux environment detection" "python3 -c 'from ai_tool.utils import check_termux_environment; info = check_termux_environment(); print(info)'"

echo "🎯 Testing Error Handling..."
echo "--------------------------"

# Test invalid provider
run_test "Invalid provider handling" "! termux-ai --provider invalid_provider --prompt 'test'"

# Test missing prompt
run_test "Missing prompt handling" "! termux-ai --provider openai"

# Test invalid temperature
run_test "Invalid temperature handling" "! termux-ai --provider openai --temperature 5.0 --prompt 'test'"

echo "📈 Test Summary"
echo "==============="

TOTAL_TESTS=$((TESTS_PASSED + TESTS_FAILED))
PASS_RATE=$((TESTS_PASSED * 100 / TOTAL_TESTS))

echo -e "${GREEN}Tests Passed: $TESTS_PASSED${NC}"
echo -e "${RED}Tests Failed: $TESTS_FAILED${NC}"
echo "Total Tests: $TOTAL_TESTS"
echo -e "Pass Rate: ${GREEN}$PASS_RATE%${NC}"

echo
echo "📋 Next Steps:"
echo "------------"

if [ $TESTS_FAILED -eq 0 ]; then
    echo -e "${GREEN}🎉 All tests passed! Your Termux AI Tool installation is ready.${NC}"
    echo
    echo "To get started:"
    echo "1. Set up your API keys: termux-ai --setup-wizard"
    echo "2. Try a simple query: termux-ai --provider openai --prompt 'Hello!'"
    echo "3. Start interactive mode: termux-ai --provider openai --interactive"
else
    echo -e "${YELLOW}⚠️ Some tests failed. Please address the issues above.${NC}"
    echo
    echo "Common fixes:"
    echo "1. Reinstall package: pip install -e ."
    echo "2. Update packages: pkg update && pkg upgrade"
    echo "3. Check permissions: ls -la ~/.config/termux-ai-tool/"
fi

echo
echo "For help and support, visit:"
echo "https://github.com/subhobhai943/termux-ai-tool"

# Exit with appropriate code
if [ $TESTS_FAILED -eq 0 ]; then
    exit 0
else
    exit 1
fi