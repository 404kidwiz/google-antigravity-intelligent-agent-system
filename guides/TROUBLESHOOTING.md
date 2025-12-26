# 🔧 Troubleshooting Guide - Intelligent Agent System

## 🚨 Common Issues and Solutions

### ❌ Issue: Global Rules Not Applied
**Symptoms:**
- "Are global rules applied?" gets no response or default response
- Expert detection not working
- Still responds with original default agent

**🔧 Solutions:**

#### 1. Restart Antigravity
```bash
# Close and restart Antigravity completely
# Check if application restarts correctly
```

#### 2. Check File Locations
```bash
# Verify GEMINI.md exists
ls -la ~/.gemini/GEMINI.md

# Verify content includes intelligent detection
grep -q "Intelligent Expert Detection" ~/.gemini/GEMINI.md && echo "✅ Rules present" || echo "❌ Rules missing"
```

#### 3. File Permissions
```bash
# Set correct permissions
chmod 644 ~/.gemini/GEMINI.md
chmod -R 755 ~/.agent/

# Verify readable
[ -r ~/.gemini/GEMINI.md ] && echo "✅ Readable" || echo "❌ Not readable"
```

#### 4. Manual Installation
If automatic setup failed:
```bash
# Run manual setup
cd /path/to/intelligent-agent-repo
chmod +x setup/install-manual.sh
./setup/install-manual.sh
```

---

### ❌ Issue: Expert Detection Not Working
**Symptoms:**
- Always responds with same expert regardless of topic
- Technology keywords not triggering appropriate experts
- No expert switching during conversation

**🔧 Solutions:**

#### 1. Use Specific Technology Names
**Good Examples:**
```
"Create a React component" (not "component")
"Build a Python FastAPI" (not "API")
"Deploy with Docker" (not "deploy")
```

#### 2. Be Explicit with Domain
**Good Examples:**
```
"I need frontend help with React"
"Backend Python API development"
"DevOps deployment with Kubernetes"
```

#### 3. Test Individual Experts
```
"React expert: How do I use hooks?"
"Python expert: Create a Flask route"
"Docker expert: Write a Dockerfile"
```

#### 4. Check Detection Rules
```bash
# Verify detection rules exist
grep -A2 "React.*react-expert" ~/.gemini/GEMINI.md
grep -A2 "Python.*python-expert" ~/.gemini/GEMINI.md
```

---

### ❌ Issue: Multi-Expert Coordination Not Working
**Symptoms:**
- Only one expert responds to complex requests
- No coordination between different domains
- Doesn't handle full-stack projects well

**🔧 Solutions:**

#### 1. Use Project-Level Language
**Good Examples:**
```
"Build a full-stack application with..."
"Create a complete SaaS platform for..."
"Design an end-to-end solution for..."
```

#### 2. Specify All Domains
**Good Examples:**
```
"React frontend + Node.js backend + PostgreSQL database"
"Vue application with Python API and Redis caching"
"Mobile app with Firebase backend and cloud deployment"
```

#### 3. Request Agency Coordination
**Good Examples:**
```
"I need a complete SaaS solution"
"Coordinate frontend, backend, and deployment"
"Handle this as a full project with multiple experts"
```

---

### ❌ Issue: Backend Architect Expert Not Available
**Symptoms:**
- backend-architect expert not responding
- System architecture questions get generic responses
- No comprehensive system design

**🔧 Solutions:**

#### 1. Verify Expert Installation
```bash
# Check if backend-architect rule exists
ls -la ~/.agent/rules/backend-architect.md

# Check if mentioned in GEMINI.md
grep -q "backend-architect" ~/.gemini/GEMINI.md && echo "✅ Present" || echo "❌ Missing"
```

#### 2. Add Backend Architect Rules
If missing, add to `~/.gemini/GEMINI.md`:
```markdown
- **Backend Architecture**: system design, microservices, architecture → backend-architect
```

#### 3. Test with Specific Prompts
```
"Backend architect: Design a microservices architecture"
"System design for high-availability application"
"Architecture for scalable user management system"
```

---

### ❌ Issue: Performance Problems
**Symptoms:**
- Slow responses to expert detection
- Lag when switching between experts
- System seems sluggish

**🔧 Solutions:**

#### 1. Optimize Global Rules
```bash
# Check GEMINI.md size
wc -l ~/.gemini/GEMINI.md

# If too large (>1000 lines), consider trimming
# Keep essential detection rules only
```

#### 2. Reduce Expert Categories
- Focus on most-used experts
- Remove rarely used detection rules
- Simplify detection patterns

#### 3. Restart and Clear Cache
```bash
# Clear any potential cache
rm -rf ~/.gemini/cache/
rm -rf ~/.agent/cache/

# Restart Antigravity
```

---

### ❌ Issue: File Corruption
**Symptoms:**
- Parse errors in responses
- Malformed expert behavior
- System not working at all

**🔧 Solutions:**

#### 1. Restore from Backup
```bash
# Find backup files
ls -la ~/.gemini/GEMINI.md.backup.*

# Restore latest backup
cp ~/.gemini/GEMINI.md.backup.LATEST ~/.gemini/GEMINI.md
```

#### 2. Fresh Installation
```bash
# Remove corrupted files
rm ~/.gemini/GEMINI.md
rm -rf ~/.agent/

# Re-run setup
cd /path/to/intelligent-agent-repo
./setup/install.sh
```

#### 3. Verify File Integrity
```bash
# Check for syntax errors
# (Manual review of GEMINI.md content)

# Check encoding
file ~/.gemini/GEMINI.md
```

---

### ❌ Issue: Directory Permissions
**Symptoms:**
- Permission denied errors
- Can't read/write configuration files
- Setup scripts fail

**🔧 Solutions:**

#### 1. Fix Directory Permissions
```bash
# Set correct ownership
sudo chown -R $USER:$USER ~/.gemini/
sudo chown -R $USER:$USER ~/.agent/

# Set correct permissions
chmod -R 755 ~/.gemini/
chmod -R 755 ~/.agent/
chmod 644 ~/.gemini/GEMINI.md
```

#### 2. User Directory Check
```bash
# Verify you're in correct user directory
echo $HOME
whoami

# Should match your username
```

---

### 🔍 Debug Mode

#### Enable Debug Logging
Add to GEMINI.md for troubleshooting:
```markdown
## DEBUG MODE
**Log all expert detection decisions**
**Announce expert switches**
**Show detection confidence scores**
```

#### Test Individual Components
```bash
# Test detection rules individually
echo "React test" | antigravity
echo "Python test" | antigravity
echo "Docker test" | antigravity
```

#### Check System Integration
```bash
# Verify Antigravity reading global rules
# Ask: "What global rules are active?"
# Should list intelligent detection system
```

---

### 📞 Getting Help

#### 1. Run Verification Script
```bash
cd /path/to/intelligent-agent-repo
./setup/verify.sh
```

#### 2. Check Documentation
- `~/.agent/SETUP_GUIDE.md` - Setup instructions
- `~/.agent/USER_GUIDE.md` - Usage guide
- This troubleshooting guide

#### 3. Common Solutions Summary
| Issue | Quick Fix |
|--------|-----------|
| Rules not applied | Restart Antigravity |
| Detection not working | Use specific technology names |
| No coordination | Request full-stack projects |
| Performance issues | Restart and clear cache |
| Permission errors | `chmod 644 ~/.gemini/GEMINI.md` |

---

### ✅ Success Indicators

Your system is working correctly when:
- ✅ Different experts respond to different technologies
- ✅ Expert switching happens seamlessly in conversations
- ✅ Complex projects get multi-expert coordination
- ✅ backend-architect responds to system design questions
- ✅ ULTRATHINK protocol works when triggered
- ✅ All original rules are preserved

**🚀 When everything works, you have a full SaaS development agency!**