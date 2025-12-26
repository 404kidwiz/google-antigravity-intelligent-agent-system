#!/bin/bash

# 🚀 Intelligent Agent System - Automatic Setup Script
# 
# This script installs the complete intelligent agent system with automatic expert detection
# for Google Antigravity, transforming it into a full SaaS development agency.

set -e

echo "🧠 Installing Intelligent Agent System..."
echo "=================================="

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Check if Antigravity directory exists
ANTIGRAVITY_DIR="$HOME/.antigravity"
GEMINI_DIR="$HOME/.gemini"
AGENT_DIR="$HOME/.agent"

echo "${BLUE}📁 Checking directory structure...${NC}"

# Create necessary directories
mkdir -p "$AGENT_DIR/rules"
mkdir -p "$AGENT_DIR/workflows"
mkdir -p "$GEMINI_DIR"

echo "${GREEN}✅ Directories created/verified${NC}"

# Backup existing GEMINI.md if it exists
if [ -f "$GEMINI_DIR/GEMINI.md" ]; then
    cp "$GEMINI_DIR/GEMINI.md" "$GEMINI_DIR/GEMINI.md.backup.$(date +%Y%m%d_%H%M%S)"
    echo "${YELLOW}📦 Backed up existing GEMINI.md${NC}"
fi

# Get script directory
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"

# Copy global rules
echo "${BLUE}📋 Installing global rules...${NC}"
cp "$SCRIPT_DIR/../rules/GEMINI.md" "$GEMINI_DIR/GEMINI.md"
echo "${GREEN}✅ Global rules installed${NC}"

# Copy additional rule files
cp "$SCRIPT_DIR/../rules/INTELLIGENT_GLOBAL_RULES.md" "$AGENT_DIR/"
cp "$SCRIPT_DIR/../rules/backend-architect.md" "$AGENT_DIR/rules/"

# Copy guides
echo "${BLUE}📚 Installing documentation...${NC}"
cp "$SCRIPT_DIR/../guides/"*.md "$AGENT_DIR/"

# Set permissions
chmod 644 "$GEMINI_DIR/GEMINI.md"
chmod -R 644 "$AGENT_DIR/"*.md
chmod -R 755 "$AGENT_DIR/rules"
chmod -R 755 "$AGENT_DIR/workflows"

echo "${GREEN}✅ Documentation installed${NC}"

# Verify installation
echo "${BLUE}🔍 Verifying installation...${NC}"
if [ -f "$GEMINI_DIR/GEMINI.md" ] && [ -f "$AGENT_DIR/SETUP_GUIDE.md" ]; then
    echo "${GREEN}✅ Installation successful!${NC}"
else
    echo "${RED}❌ Installation failed. Please check file permissions.${NC}"
    exit 1
fi

echo ""
echo "${GREEN}🎉 Intelligent Agent System Installation Complete!${NC}"
echo ""
echo "${BLUE}📋 What's been installed:${NC}"
echo "  • Enhanced GEMINI.md with intelligent expert detection"
echo "  • 138+ expert personas available automatically"
echo "  • SaaS agency capabilities"
echo "  • Complete documentation and guides"
echo "  • Backend architect expert integration"
echo ""
echo "${YELLOW}🚀 Next Steps:${NC}"
echo "  1. Restart Antigravity"
echo "  2. Test with: 'Are global rules applied?'"
echo "  3. Start using - perfect expert appears automatically!"
echo ""
echo "${BLUE}📚 For detailed usage, see:${NC}"
echo "  • $AGENT_DIR/SETUP_GUIDE.md"
echo "  • $AGENT_DIR/USER_GUIDE.md"
echo ""
echo "${GREEN}🎯 Your Antigravity is now a full SaaS development agency!${NC}"