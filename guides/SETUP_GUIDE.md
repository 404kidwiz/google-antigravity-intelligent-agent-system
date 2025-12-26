# 📋 Setup Guide - Intelligent Agent System

## 🎯 Overview

Transform your Antigravity into a full SaaS development agency with:
- 🧠 **Automatic expert detection** for 138+ specialists
- 🏢 **End-to-end SaaS capabilities**
- 🔄 **Seamless multi-expert coordination**
- ✨ **Preserved excellence** (your original rules + ULTRATHINK)

## 📁 Installation Methods

### Method 1: Automatic Setup (Recommended)
```bash
curl -sSL https://raw.githubusercontent.com/your-username/intelligent-agent-system/main/setup/install.sh | bash
```

### Method 2: Manual Setup
```bash
# Clone repository
git clone https://github.com/your-username/intelligent-agent-system.git
cd intelligent-agent-system

# Run manual setup
chmod +x setup/install-manual.sh
./setup/install-manual.sh
```

### Method 3: Quick Install (Already Done)
If you already have the files:
```bash
# Just run verification
chmod +x setup/verify.sh
./setup/verify.sh
```

## 🔧 What Gets Installed

### Core Files
- **`~/.gemini/GEMINI.md`** - Enhanced global rules with intelligent detection
- **`~/.agent/SETUP_GUIDE.md`** - Complete setup documentation
- **`~/.agent/USER_GUIDE.md`** - Usage instructions
- **`~/.agent/TROUBLESHOOTING.md`** - Common issues and solutions

### Intelligent Detection Rules
Automatic expert selection for:
- **Frontend**: React, Vue, Angular, TypeScript, CSS, HTML
- **Backend**: Python, Node.js, Go, Java, PHP, Rust + Backend Architecture
- **Database**: PostgreSQL, MongoDB, Redis, SQL, Prisma
- **DevOps**: Docker, Kubernetes, Terraform, CI/CD
- **Mobile**: React Native, Flutter, iOS, Android
- **Testing**: Jest, Cypress, Playwright, Selenium
- **AI/ML**: TensorFlow, PyTorch, OpenAI API
- **Business**: Product Management, UX Design, Architecture

## ✅ Verification

### After Installation
1. **Restart Antigravity** (if running)
2. **Test with**:
   ```
   "Are global rules applied?"
   "What experts are available?"
   "How do I create a React form with validation?"
   ```
3. **Expect responses** from appropriate experts automatically

### Success Indicators
- ✅ **Perfect expert appears** without manual selection
- ✅ **Seamless switching** between domains
- ✅ **Multi-expert coordination** for complex tasks
- ✅ **Agency-level solutions** for SaaS projects

## 🎯 Usage Examples

### Single Expert Request
```
You: "How do I create a Python API endpoint?"
System: [Auto-detects python-expert] 
"I'll create a FastAPI endpoint with proper validation..."
```

### Multi-Domain Request
```
You: "Build a SaaS platform with React frontend and Python backend"
System: [Coordinates react-expert + python-expert + backend-architect]
"I'll design this as a complete SaaS solution:
- Frontend: React application with user authentication
- Backend: Scalable Python API with microservices
- Architecture: Multi-tenant design with proper separation..."
```

### Conversation Evolution
```
You: "I need to add real-time collaboration features"
System: [Switches to websocket-expert + database-expert]
"For real-time features, I'll implement WebSocket communication..."
```

## 🔍 Troubleshooting

### Common Issues

#### Rules Not Applied
**Problem**: "Are global rules applied?" gets no response
**Solution**:
1. Restart Antigravity
2. Check `~/.gemini/GEMINI.md` exists
3. Verify file permissions: `chmod 644 ~/.gemini/GEMINI.md`

#### Expert Detection Not Working
**Problem**: Always responds with default expert
**Solution**:
1. Be specific with technology keywords
2. Use full technology names: "React" not just "component"
3. Test with clear requests: "Create a Python API endpoint"

#### File Permission Issues
**Problem**: Can't read/write files
**Solution**:
```bash
chmod 644 ~/.gemini/GEMINI.md
chmod -R 755 ~/.agent/
```

## 📚 Advanced Usage

### ULTRATHINK Protocol
Your original ULTRATHINK protocol is preserved! Trigger with:
```
ULTRATHINK: Design a complex e-commerce system
```

### Agency Coordination
For complex SaaS projects, the system automatically:
1. **Decomposes** requirements into expert domains
2. **Assigns** primary expert for coordination
3. **Integrates** multiple expert perspectives
4. **Delivers** unified solution

### Custom Expert Integration
Add your own experts by:
1. Creating `.agent/rules/your-expert.md`
2. Adding detection rules to `GEMINI.md`
3. Testing with specific requests

## 🚀 You're Ready!

After successful installation, you have:
- 🧠 **Intelligent agent system** with 138+ experts
- 🏢 **SaaS development agency** capabilities
- 🔄 **Automatic expert switching** and coordination
- ✨ **Preserved excellence** and standards

**Start any development task - perfect expert appears automatically!** 🎯