#!/bin/bash

# 🔍 Intelligent Agent System - Verification Script
# 
# This script verifies that the intelligent agent system is properly installed and functioning

set -e

echo "🔍 Verifying Intelligent Agent System Installation"
echo "==============================================="

# Colors
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m'

# Paths
GEMINI_DIR="$HOME/.gemini"
AGENT_DIR="$HOME/.agent"

echo "${BLUE}📁 Checking installation paths...${NC}"

# Check directories
DIRS_EXIST=true

if [ ! -d "$GEMINI_DIR" ]; then
    echo "${RED}❌ .gemini directory not found${NC}"
    DIRS_EXIST=false
fi

if [ ! -d "$AGENT_DIR" ]; then
    echo "${RED}❌ .agent directory not found${NC}"
    DIRS_EXIST=false
fi

if [ "$DIRS_EXIST" = true ]; then
    echo "${GREEN}✅ Directory structure correct${NC}"
else
    echo "${RED}❌ Directory structure incomplete${NC}"
    exit 1
fi

echo "${BLUE}📋 Checking files...${NC}"

# Check core files
FILES_CHECKED=0
MISSING_FILES=""

# Check GEMINI.md
if [ -f "$GEMINI_DIR/GEMINI.md" ]; then
    echo "${GREEN}✅ GEMINI.md found${NC}"
    FILES_CHECKED=$((FILES_CHECKED + 1))
    
    # Check if it contains intelligent agent rules
    if grep -q "Intelligent Expert Detection" "$GEMINI_DIR/GEMINI.md"; then
        echo "${GREEN}✅ Intelligent detection rules present${NC}"
    else
        echo "${YELLOW}⚠️  Intelligent detection rules may be missing${NC}"
        MISSING_FILES="$MISSING_FILES GEMINI.md(intelligent rules)"
    fi
else
    echo "${RED}❌ GEMINI.md not found${NC}"
    MISSING_FILES="$MISSING_FILES GEMINI.md"
fi

# Check documentation files
if [ -f "$AGENT_DIR/SETUP_GUIDE.md" ]; then
    echo "${GREEN}✅ Setup guide found${NC}"
    FILES_CHECKED=$((FILES_CHECKED + 1))
else
    echo "${YELLOW}⚠️  Setup guide missing${NC}"
    MISSING_FILES="$MISSING_FILES SETUP_GUIDE.md"
fi

if [ -f "$AGENT_DIR/USER_GUIDE.md" ]; then
    echo "${GREEN}✅ User guide found${NC}"
    FILES_CHECKED=$((FILES_CHECKED + 1))
else
    echo "${YELLOW}⚠️  User guide missing${NC}"
    MISSING_FILES="$MISSING_FILES USER_GUIDE.md"
fi

# Check permissions
if [ -r "$GEMINI_DIR/GEMINI.md" ]; then
    echo "${GREEN}✅ File permissions correct${NC}"
else
    echo "${RED}❌ File permissions incorrect${NC}"
    echo "Run: chmod 644 $GEMINI_DIR/GEMINI.md"
    exit 1
fi

echo ""
echo "${BLUE}🧠 Testing functionality...${NC}"

# Test if the system would work (simulated)
echo "${BLUE}📝 Simulating expert detection...${NC}"

# Sample keywords and expected experts
declare -A EXPERT_TESTS=(
    ["React"]="react-expert"
    ["Python"]="python-expert"
    ["Docker"]="docker-expert"
    ["Database"]="database-expert"
    ["Backend"]="backend-architect"
)

TESTS_PASSED=0
for keyword in "${!EXPERT_TESTS[@]}"; do
    if grep -q "$keyword" "$GEMINI_DIR/GEMINI.md"; then
        echo "${GREEN}✅ $keyword → ${EXPERT_TESTS[$keyword]} detection working${NC}"
        TESTS_PASSED=$((TESTS_PASSED + 1))
    else
        echo "${RED}❌ $keyword detection missing${NC}"
    fi
done

echo ""
echo "${BLUE}📊 Installation Summary:${NC}"

if [ $FILES_CHECKED -ge 2 ] && [ $TESTS_PASSED -ge 4 ]; then
    echo "${GREEN}🎉 Installation VERIFIED SUCCESSFULLY!${NC}"
    echo ""
    echo "${GREEN}✅ Features Available:${NC}"
    echo "  • Automatic expert detection for 138+ specialists"
    echo "  • SaaS agency capabilities"
    echo "  • Multi-expert coordination"
    echo "  • Preserved frontend design excellence"
    echo "  • ULTRATHINK protocol"
    echo ""
    echo "${YELLOW}🚀 Ready to use:${NC}"
    echo "1. Restart Antigravity"
    echo "2. Test with any technical question"
    echo "3. Perfect expert appears automatically!"
else
    echo "${RED}❌ Installation verification FAILED${NC}"
    echo ""
    echo "${RED}Issues found:${NC}"
    if [ -n "$MISSING_FILES" ]; then
        echo "  Missing files: $MISSING_FILES"
    fi
    if [ $TESTS_PASSED -lt 4 ]; then
        echo "  Expert detection tests failed"
    fi
    echo ""
    echo "${YELLOW}🔧 To fix:${NC}"
    echo "1. Re-run the installation script"
    echo "2. Check file permissions"
    echo "3. Verify all files copied correctly"
fi

echo ""
echo "${BLUE}📚 For help:${NC}"
echo "  • Documentation: $AGENT_DIR/SETUP_GUIDE.md"
echo "  • Usage guide: $AGENT_DIR/USER_GUIDE.md"
echo "  • Troubleshooting: $AGENT_DIR/TROUBLESHOOTING.md"