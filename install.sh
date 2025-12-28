#!/bin/bash

# UNIVERSAL INSTALLER - Enhanced Intelligent Agent System v2.0
# Works on macOS, Linux, and Windows (WSL)
# FIXED VERSION - Correct user identification and repository URLs

set -e

# Handle execution mode - if script is being piped to bash
if [ -t 0 ]; then
    # Check if we have arguments that don't match our options
    INSTALLER_MODE="install"
    REQUEST=""
    for arg in "$@"; do
        case $arg in
            --skip-deps|--dev|--quiet|--force|--help)
                # Known option - continue with install mode
                ;;
            *)
                # Unknown option - treat as request
                REQUEST="$arg"
                INSTALLER_MODE="run"
                break
                ;;
        esac
    done
else
    # File execution mode
    INSTALLER_MODE="install"
    REQUEST="$@"
fi

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
PURPLE='\033[0;35m'
CYAN='\033[0;36m'
NC='\033[0m' # No Color

# Installation configuration
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
INSTALL_DIR="$HOME/.gemini"
BACKUP_DIR="$HOME/.gemini_backup_$(date +%Y%m%d_%H%M%S)"
GEMINI_REPO_URL="https://github.com/404kidwiz/google-antigravity-intelligent-agent-system.git"

# Get the correct username from the repository
GIT_USER=$(echo "$GEMINI_REPO_URL" | sed -E 's|https://github.com/([^/]+)/.*|\1|')
if [ -z "$GIT_USER" ]; then
    GIT_USER="404kidwiz"  # Fallback username
fi

# Parse command line arguments
SKIP_DEPS=false
DEV_MODE=false
QUIET=false
FORCE=false

# Add a special flag to help with curl execution
INSTALLER_MODE="install"
if [ -n "$1" ] && [ "$1" != "--skip-deps" ] && [ "$1" != "--dev" ] && [ "$1" != "--quiet" ] && [ "$1" != "--force" ] && [ "$1" != "--help" ]; then
    # If first argument doesn't match known options, treat it as install request
    INSTALLER_MODE="run"
    REQUEST="$1"
    shift
fi

for arg in "$@"; do
    case $arg in
        --skip-deps) SKIP_DEPS=true ;;
        --dev) DEV_MODE=true ;;
        --quiet) QUIET=true ;;
        --force) FORCE=true ;;
        --help) 
            echo "Enhanced Intelligent Agent System v2.0 Installer"
            echo ""
            echo "Usage: $0 [options] [request]"
            echo ""
            echo "Options:"
            echo "  --skip-deps    Skip Python dependencies installation"
            echo "  --dev          Install in development mode"
            echo "  --quiet        Silent installation"
            echo "  --force        Force reinstall (overwrite existing)"
            echo "  --help         Show this help message"
            echo ""
            echo "Installation:"
            echo "  $0 'build a react component'  # Install and run"
            echo ""
            echo "Repository: https://github.com/$GIT_USER/google-antigravity-intelligent-agent-system"
            echo "User: $GIT_USER"
            exit 0
            ;;
    esac
done

# Function to print colored output
print_status() {
    if [ "$QUIET" = false ]; then
        echo -e "${BLUE}[INFO]${NC} $1"
    fi
}

print_success() {
    if [ "$QUIET" = false ]; then
        echo -e "${GREEN}[SUCCESS]${NC} $1"
    fi
}

print_warning() {
    if [ "$QUIET" = false ]; then
        echo -e "${YELLOW}[WARNING]${NC} $1"
    fi
}

print_error() {
    echo -e "${RED}[ERROR]${NC} $1"
}

print_header() {
    if [ "$QUIET" = false ]; then
        echo -e "${CYAN}╔════════════════════════════════════════════════════════════╗${NC}"
        echo -e "${CYAN}║     ENHANCED INTELLIGENT AGENT SYSTEM v2.0 INSTALLER       ║${NC}"
        echo -e "${CYAN}║   Hierarchical Orchestration + Memory + Analytics v2.0       ║${NC}"
        echo -e "${CYAN}║     Repository: github.com/$GIT_USER/antigravity-intelligent-agent    ║${NC}"
        echo -e "${CYAN}╚════════════════════════════════════════════════════════════╝${NC}"
        echo ""
    fi
}

# Function to check system requirements
check_requirements() {
    print_status "Checking system requirements..."
    
    # Check Python
    if command -v python3 &> /dev/null; then
        PYTHON_VERSION=$(python3 --version 2>&1)
        PYTHON_MAJOR=$(echo $PYTHON_VERSION | sed 's/Python \([0-9]*\)\.\([0-9]*\).*/\1/')
        PYTHON_MINOR=$(echo $PYTHON_VERSION | sed 's/Python \([0-9]*\)\.\([0-9]*\).*/\2/')
        
        if [ "$PYTHON_MAJOR" -ge 3 ] && [ "$PYTHON_MINOR" -ge 8 ]; then
            print_success "Python $PYTHON_VERSION found ✓"
        else
            print_error "Python 3.8+ required, found $PYTHON_VERSION"
            exit 1
        fi
    else
        print_error "Python 3 not found. Please install Python 3.8+"
        exit 1
    fi
    
    # Check pip
    if command -v pip3 &> /dev/null; then
        print_success "pip3 found ✓"
    else
        print_error "pip3 not found. Please install pip3"
        exit 1
    fi
    
    # Check git
    if command -v git &> /dev/null; then
        print_success "git found ✓"
    else
        print_warning "git not found. Some features may not work"
    fi
    
    # Check available disk space (need at least 2GB)
    if command -v df &> /dev/null; then
        AVAILABLE_SPACE=$(df -h "$HOME" | awk 'NR==2 {print $4}' | sed 's/[^0-9.]//g' | sed 's/G//')
        if [ -n "$AVAILABLE_SPACE" ] && [ "$AVAILABLE_SPACE" -gt 2 ]; then
            print_success "Sufficient disk space ✓"
        else
            print_warning "Low disk space. At least 2GB recommended"
        fi
    fi
    
    print_success "System requirements check completed ✓"
}

# Function to backup existing installation
backup_existing() {
    if [ -d "$INSTALL_DIR" ] && [ "$FORCE" = false ]; then
        print_status "Backing up existing installation..."
        mkdir -p "$BACKUP_DIR"
        cp -r "$INSTALL_DIR"/* "$BACKUP_DIR/" 2>/dev/null || true
        print_success "Backup created at $BACKUP_DIR"
    elif [ "$FORCE" = true ]; then
        print_status "Force mode: Removing existing installation..."
        rm -rf "$INSTALL_DIR"
        print_success "Existing installation removed"
    fi
}

# Function to create directory structure
create_directories() {
    print_status "Creating directory structure..."
    
    # Create main directories
    mkdir -p "$INSTALL_DIR"
    mkdir -p "$INSTALL_DIR/memory"
    mkdir -p "$INSTALL_DIR/analytics"
    mkdir -p "$INSTALL_DIR/experts"
    mkdir -p "$INSTALL_DIR/logs"
    mkdir -p "$INSTALL_DIR/config"
    mkdir -p "$INSTALL_DIR/cache"
    
    # Create subdirectories
    mkdir -p "$INSTALL_DIR/memory/sessions"
    mkdir -p "$INSTALL_DIR/analytics/alerts"
    mkdir -p "$INSTALL_DIR/experts/custom"
    mkdir -p "$INSTALL_DIR/experts/cache"
    mkdir -p "$INSTALL_DIR/config/expert_profiles"
    
    print_success "Directory structure created ✓"
}

# Function to install Python dependencies
install_dependencies() {
    if [ "$SKIP_DEPS" = true ]; then
        print_status "Skipping Python dependencies installation..."
        return 0
    fi
    
    print_status "Installing Python dependencies..."
    
    # Check if we're in the repository directory
    if [ -f "$SCRIPT_DIR/requirements.txt" ]; then
        pip3 install -r "$SCRIPT_DIR/requirements.txt" --user --quiet
    else
        # Install core dependencies
        pip3 install --user --quiet \
            sqlite3 \
            asyncio \
            statistics \
            pathlib \
            threading \
            dataclasses \
            enum \
            typing \
            collections \
            datetime \
            json \
            time \
            uuid \
            hashlib \
            os \
            re \
            random
    fi
    
    print_success "Python dependencies installed ✓"
}

# Function to install core system files
install_core_files() {
    print_status "Installing core system files..."
    
    # Copy Python modules
    cp "$SCRIPT_DIR/meta_orchestrator.py" "$INSTALL_DIR/"
    cp "$SCRIPT_DIR/expert_memory_system.py" "$INSTALL_DIR/"
    cp "$SCRIPT_DIR/performance_analytics.py" "$INSTALL_DIR/"
    cp "$SCRIPT_DIR/multi_agent_conversation.py" "$INSTALL_DIR/"
    
    # Copy rules
    mkdir -p "$INSTALL_DIR/rules"
    cp "$SCRIPT_DIR/rules/GEMINI.md" "$INSTALL_DIR/rules/"
    
    # Copy scripts
    cp "$SCRIPT_DIR/verify_system.sh" "$INSTALL_DIR/"
    cp "$SCRIPT_DIR/install.sh" "$INSTALL_DIR/"
    
    # Copy documentation
    if [ -f "$SCRIPT_DIR/README.md" ]; then
        cp "$SCRIPT_DIR/README.md" "$INSTALL_DIR/"
    fi
    
    # Make scripts executable
    chmod +x "$INSTALL_DIR/verify_system.sh"
    chmod +x "$INSTALL_DIR/install.sh"
    
    print_success "Core system files installed ✓"
}

# Function to create configuration files
create_config() {
    print_status "Creating configuration files..."
    
    # Create main configuration
    cat > "$INSTALL_DIR/config/gemini.conf" << 'EOF'
[system]
max_concurrent_experts = 5
memory_retention_days = 30
analytics_collection = true
verbose_default = false

[performance]
response_time_threshold = 3.0
memory_usage_limit = 0.8
circuit_breaker_threshold = 3

[expert_selection]
semantic_matching = true
context_weight = 0.3
performance_weight = 0.4
learning_weight = 0.3

[memory]
session_persistence = true
cross_session_learning = true
max_memory_entries = 10000
EOF

    # Create expert library reference
    cat > "$INSTALL_DIR/experts/library.json" << EOF
{
  "version": "2.0",
  "total_experts": 138,
  "domains": {
    "frontend": 17,
    "backend": 33,
    "database": 18,
    "devops": 8,
    "testing": 9,
    "mobile": 6,
    "ai_ml": 7,
    "product": 15
  },
  "last_updated": "$(date -Iseconds)",
  "repository": "https://github.com/$GIT_USER/google-antigravity-intelligent-agent-system",
  "git_user": "$GIT_USER"
}
EOF

    # Create log rotation config
    cat > "$INSTALL_DIR/config/logrotate.conf" << 'EOF'
~/.gemini/logs/*.log {
    daily
    rotate 30
    compress
    delaycompress
    missingok
    notifempty
}
EOF

    print_success "Configuration files created ✓"
}

# Function to create command-line interface
create_cli() {
    print_status "Creating command-line interface..."
    
    # Create main CLI script
    cat > "$INSTALL_DIR/gemini" << 'EOF'
#!/bin/bash

# Enhanced Intelligent Agent System CLI v2.0
# Repository: https://github.com/$GIT_USER/google-antigravity-intelligent-agent-system

SCRIPT_DIR="\$(cd "\$(dirname "\${BASH_SOURCE[0]}")" && pwd)"
PYTHON_SCRIPT="\$SCRIPT_DIR/meta_orchestrator.py"

# Check if system is installed
if [ ! -f "\$PYTHON_SCRIPT" ]; then
    echo "Error: Enhanced Intelligent Agent System v2.0 not found"
    echo "Repository: https://github.com/$GIT_USER/google-antigravity-intelligent-agent-system"
    echo "Please run installation script first"
    exit 1
fi

# Handle CLI arguments
VERBOSE=false
ULTRATHINK=false
SESSION_ID=""

while [[ \$# -gt 0 ]]; do
    case \$1 in
        --verbose|-v)
            VERBOSE=true
            shift
            ;;
        --ultrathink|-u)
            ULTRATHINK=true
            shift
            ;;
        --session|-s)
            SESSION_ID="\$2"
            shift 2
            ;;
        --help|-h)
            echo "Enhanced Intelligent Agent System CLI v2.0"
            echo "Repository: https://github.com/$GIT_USER/google-antigravity-intelligent-agent-system"
            echo ""
            echo "Usage: gemini [options] [request]"
            echo ""
            echo "Options:"
            echo "  --verbose, -v        Enable verbose mode with transparency"
            echo "  --ultrathink, -u    Enable ULTRATHINK mode for deep analysis"
            echo "  --session, -s <id>   Use specific session ID"
            echo "  --help, -h          Show this help message"
            echo ""
            echo "Examples:"
            echo "  gemini build a react component"
            echo "  gemini --verbose build a full-stack application"
            echo "  gemini --ultrathink design a scalable architecture"
            echo ""
            exit 0
            ;;
        *)
            REQUEST="\$*"
            break
            ;;
    esac
done

# Read request from stdin if not provided
if [ -z "\$REQUEST" ]; then
    if [ -t 0 ]; then
        echo "Enter your request (Ctrl+D to finish):"
    fi
    REQUEST=\$(cat)
fi

# Prepare Python command
PYTHON_CMD="python3 \"\$PYTHON_SCRIPT\""

# Add flags
if [ "\$VERBOSE" = true ]; then
    PYTHON_CMD="\$PYTHON_CMD --verbose"
fi

if [ "\$ULTRATHINK" = true ]; then
    PYTHON_CMD="\$PYTHON_CMD --ultrathink"
fi

if [ -n "\$SESSION_ID" ]; then
    PYTHON_CMD="\$PYTHON_CMD --session-id \"\$SESSION_ID\""
fi

# Execute
if [ "$INSTALLER_MODE" = "run" ] && [ -n "$REQUEST" ]; then
    echo "$REQUEST" | eval $PYTHON_CMD
elif [ "$INSTALLER_MODE" = "install" ]; then
    # Run full installation
    check_requirements
    backup_existing
    create_directories
    if [ "$DEV_MODE" = false ]; then
        install_dependencies
    fi
    install_core_files
    create_config
    create_cli
    setup_shell_integration
    run_verification
    print_completion
    
    # Create marker file for successful installation
    touch "$INSTALL_DIR/.installation_complete"
    
    print_success "Installation completed successfully! ✓"
else
    echo "$REQUEST" | eval $PYTHON_CMD
fi
EOF

    # Make CLI executable
    chmod +x "$INSTALL_DIR/gemini"
    
    print_success "Command-line interface created ✓"
}

# Function to setup shell integration
setup_shell_integration() {
    print_status "Setting up shell integration..."
    
    # Create shell profile update
    PROFILE_UPDATE="$HOME/.gemini_shell_profile.sh"
    
    cat > "$PROFILE_UPDATE" << EOF
# Enhanced Intelligent Agent System v2.0 Shell Integration
# Repository: https://github.com/$GIT_USER/google-antigravity-intelligent-agent-system

# Add to PATH
export PATH="\$HOME/.gemini:\$PATH"

# Aliases for convenience
alias gemini="~/.gemini/gemini"
alias gemini-verbose="~/.gemini/gemini --verbose"
alias gemini-ultrathink="~/.gemini/gemini --ultrathink"
alias gemini-status="~/.gemini/verify_system.sh"
alias gemini-performance="~/.gemini/gemini 'show performance dashboard'"
alias gemini-memory="~/.gemini/gemini 'what have we worked on before?'"
alias gemini-help="~/.gemini/gemini --help"

# Environment variables
export GEMINI_HOME="\$HOME/.gemini"
export GEMINI_LOG_LEVEL="INFO"
export GEMINI_DEBUG=false
export GEMINI_REPO_USER="$GIT_USER"

# Auto-completion (optional)
if [ -n "\$BASH_VERSION" ]; then
    _gemini_completion() {
        local cur prev
        cur="\${COMP_WORDS[COMP_CWORD]}"
        prev="\${COMP_WORDS[COMP_CWORD-1]}"
        
        case "\$prev" in
            gemini)
                COMPREPLY=\$(compgen -W "--verbose --ultrathink --session --help" -- "\$cur")
                ;;
            *)
                COMPREPLY=()
                ;;
        esac
    }
    complete -F _gemini_completion gemini
fi
EOF

    # Add to shell profile if not already there
    if ! grep -q "Enhanced Intelligent Agent System v2.0" "$HOME/.bashrc" 2>/dev/null; then
        if [ -f "$HOME/.bashrc" ]; then
            echo "" >> "$HOME/.bashrc"
            echo "# Enhanced Intelligent Agent System v2.0" >> "$HOME/.bashrc"
            echo "source ~/.gemini_shell_profile.sh" >> "$HOME/.bashrc"
        fi
        
        if [ -f "$HOME/.zshrc" ] && ! grep -q "Enhanced Intelligent Agent System v2.0" "$HOME/.zshrc" 2>/dev/null; then
            echo "" >> "$HOME/.zshrc"
            echo "# Enhanced Intelligent Agent System v2.0" >> "$HOME/.zshrc"
            echo "source ~/.gemini_shell_profile.sh" >> "$HOME/.zshrc"
        fi
    fi
    
    print_success "Shell integration setup completed ✓"
}

# Function to run verification
run_verification() {
    print_status "Running system verification..."
    
    if [ -f "$INSTALL_DIR/verify_system.sh" ]; then
        cd "$INSTALL_DIR"
        if ./verify_system.sh; then
            print_success "System verification passed ✓"
        else
            print_warning "System verification had some issues"
            print_status "Run '$INSTALL_DIR/verify_system.sh' to see details"
        fi
    else
        print_warning "Verification script not found"
    fi
}

# Function to print completion message
print_completion() {
    if [ "$QUIET" = false ]; then
        echo ""
        echo -e "${GREEN}╔════════════════════════════════════════════════════════════╗${NC}"
        echo -e "${GREEN}║           INSTALLATION COMPLETED SUCCESSFULLY!            ║${NC}"
        echo -e "${GREEN}╚════════════════════════════════════════════════════════════╝${NC}"
        echo ""
        echo -e "${CYAN}🚀 Enhanced Intelligent Agent System v2.0 is now installed!${NC}"
        echo -e "${CYAN}🌐 Repository: https://github.com/$GIT_USER/google-antigravity-intelligent-agent-system${NC}"
        echo ""
        echo -e "${YELLOW}Quick Start:${NC}"
        echo -e "  ${BLUE}source ~/.gemini_shell_profile.sh${NC}  # Load environment"
        echo -e "  ${BLUE}gemini 'build a react component'${NC}     # Basic usage"
        echo -e "  ${BLUE}gemini --verbose 'complex request'${NC} # Verbose mode"
        echo -e "  ${BLUE}gemini --ultrathink 'deep analysis'${NC} # Deep analysis"
        echo ""
        echo -e "${YELLOW}Available Commands:${NC}"
        echo -e "  ${BLUE}gemini${NC}                    - Main CLI interface"
        echo -e "  ${BLUE}gemini --verbose${NC}           - Verbose mode with transparency"
        echo -e "  ${BLUE}gemini --ultrathink${NC}       - Deep analysis mode"
        echo -e "  ${BLUE}gemini-status${NC}             - System verification"
        echo -e "  ${BLUE}gemini-performance${NC}        - Performance dashboard"
        echo -e "  ${BLUE}gemini-memory${NC}             - Memory and learning status"
        echo -e "  ${BLUE}gemini-help${NC}               - Show help"
        echo ""
        echo -e "${YELLOW}System Features:${NC}"
        echo -e "  ✓ 138+ Expert Personas"
        echo -e "  ✓ Hierarchical Orchestration"
        echo -e "  ✓ Persistent Memory System"
        echo -e "  ✓ Real-Time Performance Analytics"
        echo -e "  ✓ Multi-Agent Conversations"
        echo -e "  ✓ Custom Expert Creation"
        echo -e "  ✓ Production Resilience"
        echo -e "  ✓ Learning & Adaptation"
        echo ""
        echo -e "${YELLOW}Configuration:${NC}"
        echo -e "  ${BLUE}Config File:${NC} $INSTALL_DIR/config/gemini.conf"
        echo -e "  ${BLUE}Memory Store:${NC} $INSTALL_DIR/memory/"
        echo -e "  ${BLUE}Analytics:${NC} $INSTALL_DIR/analytics/"
        echo -e "  ${BLUE}Logs:${NC} $INSTALL_DIR/logs/"
        echo ""
        echo -e "${GREEN}🎉 Start building with your AI development agency!${NC}"
    fi
}

# Main installation function
main() {
    print_header
    
    # Show repository info
    if [ "$QUIET" = false ]; then
        echo -e "${CYAN}Repository Information:${NC}"
        echo -e "  ${BLUE}User:${NC} $GIT_USER"
        echo -e "  ${BLUE}URL:${NC} https://github.com/$GIT_USER/google-antigravity-intelligent-agent-system"
        echo ""
    fi
    
    # Check if running as root (not recommended)
    if [ "$EUID" -eq 0 ]; then
        print_error "Please do not run this installer as root"
        exit 1
    fi
    
    # Run installation steps
    check_requirements
    backup_existing
    create_directories
    
    if [ "$DEV_MODE" = false ]; then
        install_dependencies
    fi
    
    install_core_files
    create_config
    create_cli
    setup_shell_integration
    run_verification
    print_completion
    
    # Create marker file for successful installation
    touch "$INSTALL_DIR/.installation_complete"
    
    print_success "Installation completed successfully! ✓"
}

# Error handling
trap 'print_error "Installation failed. Check to error messages above."' ERR

# Run main function
main "$@"