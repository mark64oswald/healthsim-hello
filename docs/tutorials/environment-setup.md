# Environment Setup

Complete guide to setting up your development environment for HealthSim.

## Prerequisites Checklist

Before starting, ensure you have:

- [ ] **Operating System**: macOS, Linux, or Windows with WSL
- [ ] **Python 3.11+**: Required for all HealthSim projects
- [ ] **Git**: For cloning repositories
- [ ] **VS Code** (recommended): With Python extension
- [ ] **Claude Desktop or Claude Code**: For interactive use (optional)

## Step 1: Verify Python Version

```bash
python3 --version
# Should output: Python 3.11.x or higher
```

### If Python 3.11+ is not installed:

**macOS (with Homebrew):**
```bash
brew install python@3.11
```

**Ubuntu/Debian:**
```bash
sudo apt update
sudo apt install python3.11 python3.11-venv
```

**Windows:**
Download from [python.org](https://www.python.org/downloads/) and install.

## Step 2: Create Project Directory

```bash
# Create the projects directory
mkdir -p ~/Developer/projects
cd ~/Developer/projects
```

## Step 3: Clone Repositories

Clone all four HealthSim repositories:

```bash
# Core library (required)
git clone https://github.com/mark64oswald/healthsim-core.git

# Clinical data generation
git clone https://github.com/mark64oswald/patientsim.git

# Payer data generation
git clone https://github.com/mark64oswald/membersim.git

# This tutorial (optional)
git clone https://github.com/mark64oswald/healthsim-hello.git
```

Your directory should now look like:
```
~/Developer/projects/
├── healthsim-core/
├── patientsim/
├── membersim/
└── healthsim-hello/
```

## Step 4: Set Up Each Project

Each project needs its own virtual environment. Here's how to set up each one:

### 4.1 healthsim-core

```bash
cd ~/Developer/projects/healthsim-core

# Create virtual environment
python3 -m venv .venv

# Activate it
source .venv/bin/activate  # On Windows: .venv\Scripts\activate

# Upgrade pip
pip install --upgrade pip

# Install with dev dependencies
pip install -e ".[dev]"

# Verify installation
python -c "from healthsim import person; print('healthsim-core: OK')"

# Run tests
pytest

# Deactivate when done
deactivate
```

### 4.2 PatientSim

```bash
cd ~/Developer/projects/patientsim

# Create virtual environment
python3 -m venv .venv

# Activate it
source .venv/bin/activate

# Upgrade pip
pip install --upgrade pip

# Install with dev dependencies
pip install -e ".[dev]"

# Verify installation
python -c "from patientsim import PatientGenerator; print('patientsim: OK')"

# Run tests
pytest

# Deactivate
deactivate
```

### 4.3 MemberSim

```bash
cd ~/Developer/projects/membersim

# Create virtual environment
python3 -m venv .venv

# Activate it
source .venv/bin/activate

# Upgrade pip
pip install --upgrade pip

# Install with dev dependencies
pip install -e ".[dev]"

# Verify installation
python -c "from membersim import MemberGenerator; print('membersim: OK')"

# Run tests
pytest

# Deactivate
deactivate
```

## Step 5: VS Code Setup

### 5.1 Open the Workspace

If you cloned healthsim-hello, there's a workspace file:

```bash
code ~/Developer/projects/healthsim.code-workspace
```

Or create one manually:

1. Open VS Code
2. File → Add Folder to Workspace...
3. Add all four project folders
4. File → Save Workspace As... → `healthsim.code-workspace`

### 5.2 Install Recommended Extensions

When you open the workspace, VS Code may prompt you to install recommended extensions. Accept, or manually install:

- **Python** (ms-python.python)
- **Pylance** (ms-python.vscode-pylance)
- **Ruff** (charliermarsh.ruff)
- **Markdown All in One** (yzhang.markdown-all-in-one)

### 5.3 Select Python Interpreter

For each project folder:

1. Open a Python file in that project
2. Click the Python version in the bottom status bar
3. Select the `.venv` interpreter for that project

Or press `Cmd+Shift+P` (Mac) / `Ctrl+Shift+P` (Windows/Linux) and type "Python: Select Interpreter".

## Step 6: Verification Script

Create this script to verify everything is set up correctly:

```bash
#!/bin/bash
# save as: ~/Developer/projects/verify-healthsim.sh

echo "🔍 Checking HealthSim Environment..."
echo ""

# Check Python version
echo -n "Python version: "
python3 --version

echo ""

# Check healthsim-core
echo -n "healthsim-core: "
cd ~/Developer/projects/healthsim-core
source .venv/bin/activate 2>/dev/null
if python -c "from healthsim import person; print('✅ OK')" 2>/dev/null; then
    :
else
    echo "❌ Failed"
fi
deactivate 2>/dev/null

# Check patientsim
echo -n "patientsim: "
cd ~/Developer/projects/patientsim
source .venv/bin/activate 2>/dev/null
if python -c "from patientsim import PatientGenerator; print('✅ OK')" 2>/dev/null; then
    :
else
    echo "❌ Failed"
fi
deactivate 2>/dev/null

# Check membersim
echo -n "membersim: "
cd ~/Developer/projects/membersim
source .venv/bin/activate 2>/dev/null
if python -c "from membersim import MemberGenerator; print('✅ OK')" 2>/dev/null; then
    :
else
    echo "❌ Failed"
fi
deactivate 2>/dev/null

echo ""
echo "✨ Verification complete!"
```

Run it:
```bash
chmod +x ~/Developer/projects/verify-healthsim.sh
~/Developer/projects/verify-healthsim.sh
```

Expected output:
```
🔍 Checking HealthSim Environment...

Python version: Python 3.11.5

healthsim-core: ✅ OK
patientsim: ✅ OK
membersim: ✅ OK

✨ Verification complete!
```

## Troubleshooting

### "Module not found" errors

1. Make sure you're in the right virtual environment:
   ```bash
   which python
   # Should show: /path/to/project/.venv/bin/python
   ```

2. Reinstall the package:
   ```bash
   pip install -e ".[dev]"
   ```

### "python3: command not found"

Python isn't in your PATH. Try:
```bash
# Find where Python is installed
which python3.11

# Add to your shell profile (~/.zshrc or ~/.bashrc)
export PATH="/usr/local/bin:$PATH"
```

### Tests failing with import errors

Make sure healthsim-core is installed first, as other packages depend on it:
```bash
cd ~/Developer/projects/healthsim-core
source .venv/bin/activate
pip install -e ".[dev]"
```

### VS Code not finding the right Python

1. Close and reopen VS Code
2. Open the Command Palette (Cmd+Shift+P / Ctrl+Shift+P)
3. Type "Python: Clear Cache and Reload Window"

## Next Steps

Once your environment is set up:

1. **Try the tutorials:**
   - [PatientSim Tutorial](patientsim-tutorial.md)
   - [MemberSim Tutorial](membersim-tutorial.md)

2. **Set up interactive use:**
   - [MCP Setup](../interactive/mcp-setup.md)
   - [Claude Desktop Configuration](../interactive/claude-desktop-config.md)

3. **Explore the architecture:**
   - [Platform Overview](../architecture/platform-overview.md)
   - [Module Inventory](../architecture/module-inventory.md)
