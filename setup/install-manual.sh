#!/bin/bash

# 🔧 Manual Setup Script for Intelligent Agent System
# Use this if automatic setup doesn't work

set -e

echo "🔧 Manual Setup: Intelligent Agent System"
echo "======================================"

# Colors
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m'

# Directory paths
GEMINI_DIR="$HOME/.gemini"
AGENT_DIR="$HOME/.agent"
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"

echo "${BLUE}📁 Step 1: Creating directories...${NC}"

# Create directories
mkdir -p "$AGENT_DIR/rules"
mkdir -p "$AGENT_DIR/workflows"
mkdir -p "$GEMINI_DIR"

echo "${GREEN}✅ Directories created${NC}"

echo "${BLUE}📋 Step 2: Installing global rules...${NC}"

# Backup existing GEMINI.md
if [ -f "$GEMINI_DIR/GEMINI.md" ]; then
    cp "$GEMINI_DIR/GEMINI.md" "$GEMINI_DIR/GEMINI.md.backup.$(date +%Y%m%d_%H%M%S)"
    echo "${YELLOW}📦 Backed up existing GEMINI.md${NC}"
fi

# Copy main global rules
if [ -f "$SCRIPT_DIR/../rules/GEMINI.md" ]; then
    cp "$SCRIPT_DIR/../rules/GEMINI.md" "$GEMINI_DIR/GEMINI.md"
    echo "${GREEN}✅ GEMINI.md installed${NC}"
else
    echo "${RED}❌ GEMINI.md not found in source directory${NC}"
    echo "Please ensure you're running this script from the repository"
    exit 1
fi

echo "${BLUE}📚 Step 3: Installing additional resources...${NC}"

# Copy additional files
if [ -d "$SCRIPT_DIR/../rules" ]; then
    cp "$SCRIPT_DIR/../rules/"*.md "$AGENT_DIR/rules/"
    echo "${GREEN}✅ Additional rule files installed${NC}"
fi

if [ -d "$SCRIPT_DIR/../guides" ]; then
    cp "$SCRIPT_DIR/../guides/"*.md "$AGENT_DIR/"
    echo "${GREEN}✅ Documentation installed${NC}"
fi

echo "${BLUE}🔧 Step 4: Setting permissions...${NC}"

# Set proper permissions
chmod 644 "$GEMINI_DIR/GEMINI.md"
find "$AGENT_DIR" -name "*.md" -exec chmod 644 {} \;
find "$AGENT_DIR" -type d -exec chmod 755 {} \;

echo "${GREEN}✅ Permissions set${NC}"

echo "${BLUE}🔍 Step 5: Verification...${NC}"

# Verify installation
FILES_CHECKED=0

if [ -f "$GEMINI_DIR/GEMINI.md" ]; then
    echo "${GREEN}✅ GEMINI.md is in place${NC}"
    FILES_CHECKED=$((FILES_CHECKED + 1))
fi

if [ -f "$AGENT_DIR/SETUP_GUIDE.md" ]; then
    echo "${GREEN}✅ Setup guide installed${NC}"
    FILES_CHECKED=$((FILES_CHECKED + 1))
fi

if [ -f "$AGENT_DIR/USER_GUIDE.md" ]; then
    echo "${GREEN}✅ User guide installed${NC}"
    FILES_CHECKED=$((FILES_CHECKED + 1))
fi

if [ $FILES_CHECKED -eq 3 ]; then
    echo ""
    echo "${GREEN}🎉 Manual setup completed successfully!${NC}"
else
    echo ""
    echo "${RED}❌ Setup incomplete. Please check the errors above.${NC}"
    exit 1
fi

echo ""
echo "${YELLOW}📋 Manual Steps to Complete Setup:${NC}"
echo "1. Open Antigravity"
echo "2. Restart the application (if running)"
echo "3. Test installation with: 'Are global rules applied?'"
echo ""

echo "${GREEN}🎯 Your Intelligent Agent System is ready!${NC}"
echo "${BLUE}📚 Documentation available at:${NC}"
echo "   • $AGENT_DIR/SETUP_GUIDE.md"
echo "   • $AGENT_DIR/USER_GUIDE.md"

echo ""
echo "${GREEN}🚀 You now have a full SaaS development agency!${NC}"