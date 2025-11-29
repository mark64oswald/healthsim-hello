# Claude Desktop Configuration

Step-by-step guide to configuring Claude Desktop to use HealthSim MCP servers.

## Step 1: Locate the Config File

### macOS

```bash
# The config directory
ls ~/Library/Application\ Support/Claude/

# If it doesn't exist, create it
mkdir -p ~/Library/Application\ Support/Claude/

# Create or edit the config file
nano ~/Library/Application\ Support/Claude/claude_desktop_config.json
```

### Windows

```powershell
# The config directory (in PowerShell)
dir $env:APPDATA\Claude\

# Create directory if needed
mkdir $env:APPDATA\Claude

# Edit the config file
notepad $env:APPDATA\Claude\claude_desktop_config.json
```

## Step 2: Create the Configuration

Replace `YOUR_USERNAME` with your actual username in the paths below.

### macOS Configuration

```json
{
  "mcpServers": {
    "patientsim": {
      "command": "/Users/YOUR_USERNAME/Developer/projects/patientsim/.venv/bin/python",
      "args": ["-m", "patientsim.mcp.server"],
      "env": {
        "PYTHONPATH": "/Users/YOUR_USERNAME/Developer/projects/patientsim/src"
      }
    },
    "membersim": {
      "command": "/Users/YOUR_USERNAME/Developer/projects/membersim/.venv/bin/python",
      "args": ["-m", "membersim.mcp.server"],
      "env": {
        "PYTHONPATH": "/Users/YOUR_USERNAME/Developer/projects/membersim/src"
      }
    }
  }
}
```

### Windows Configuration

```json
{
  "mcpServers": {
    "patientsim": {
      "command": "C:\\Users\\YOUR_USERNAME\\Developer\\projects\\patientsim\\.venv\\Scripts\\python.exe",
      "args": ["-m", "patientsim.mcp.server"],
      "env": {
        "PYTHONPATH": "C:\\Users\\YOUR_USERNAME\\Developer\\projects\\patientsim\\src"
      }
    },
    "membersim": {
      "command": "C:\\Users\\YOUR_USERNAME\\Developer\\projects\\membersim\\.venv\\Scripts\\python.exe",
      "args": ["-m", "membersim.mcp.server"],
      "env": {
        "PYTHONPATH": "C:\\Users\\YOUR_USERNAME\\Developer\\projects\\membersim\\src"
      }
    }
  }
}
```

## Step 3: Find Your Actual Paths

To get the exact paths for your system:

```bash
# Get your username
whoami

# Get full path to PatientSim Python
cd ~/Developer/projects/patientsim
source .venv/bin/activate
which python
# Output example: /Users/markoswald/Developer/projects/patientsim/.venv/bin/python

# Get full path to MemberSim Python
cd ~/Developer/projects/membersim
source .venv/bin/activate
which python
```

## Configuration Details

### Understanding Each Field

```json
{
  "mcpServers": {
    "patientsim": {                    // Server name (shown in Claude)
      "command": "/full/path/.venv/bin/python",  // Python executable
      "args": ["-m", "patientsim.mcp.server"],   // Module to run
      "env": {                         // Environment variables
        "PYTHONPATH": "/full/path/src" // Where to find source code
      }
    }
  }
}
```

### Important Notes

| Requirement | Why |
|-------------|-----|
| **Use full paths** | No `~` or `$HOME` - must be absolute paths |
| **Point to venv Python** | Use `.venv/bin/python`, not system Python |
| **Include PYTHONPATH** | Required if project uses `src/` layout |
| **Each product is separate** | PatientSim and MemberSim are independent servers |

## Step 4: Restart Claude Desktop

After saving the configuration:

1. **Quit Claude Desktop completely**
   - macOS: Cmd+Q (not just close window)
   - Windows: Right-click system tray icon → Quit

2. **Reopen Claude Desktop**

3. **Start a new conversation**

## Step 5: Verify Tools Are Available

In a new Claude conversation, ask:

> "What tools do you have available?"

Claude should list the HealthSim tools:
- `generate_patient`
- `generate_member`
- `export_fhir`
- etc.

If tools aren't showing:
- Check the [Troubleshooting](#troubleshooting) section below
- Verify the config file syntax (valid JSON)
- Ensure paths are correct

## Step 6: Test with a Simple Request

Try generating a patient:

> "Generate a single patient for testing"

Claude should call the MCP server and return actual synthetic data.

## Claude Code Configuration

For the VS Code extension, configuration is per-project:

### Step 1: Create Config Directory

```bash
cd ~/Developer/projects/your-project
mkdir -p .claude
```

### Step 2: Create mcp-config.json

```bash
cat > .claude/mcp-config.json << 'EOF'
{
  "mcpServers": {
    "patientsim": {
      "command": "/Users/YOUR_USERNAME/Developer/projects/patientsim/.venv/bin/python",
      "args": ["-m", "patientsim.mcp.server"],
      "env": {
        "PYTHONPATH": "/Users/YOUR_USERNAME/Developer/projects/patientsim/src"
      }
    }
  }
}
EOF
```

### Step 3: Reload VS Code

The Claude Code extension will detect the config on reload.

## Troubleshooting

### Tools Not Appearing

1. **Check config file location**
   ```bash
   # macOS
   cat ~/Library/Application\ Support/Claude/claude_desktop_config.json
   ```

2. **Validate JSON syntax**
   ```bash
   python -m json.tool < ~/Library/Application\ Support/Claude/claude_desktop_config.json
   ```

3. **Verify paths exist**
   ```bash
   ls -la /Users/YOUR_USERNAME/Developer/projects/patientsim/.venv/bin/python
   ```

### "Module not found" Errors

The MCP server can't find the Python module.

1. **Check PYTHONPATH is correct**
   ```bash
   # Test manually
   cd ~/Developer/projects/patientsim
   source .venv/bin/activate
   PYTHONPATH=src python -m patientsim.mcp.server
   ```

2. **Verify package is installed**
   ```bash
   pip list | grep patientsim
   ```

### Server Crashes Immediately

1. **Test server manually**
   ```bash
   cd ~/Developer/projects/patientsim
   source .venv/bin/activate
   python -m patientsim.mcp.server
   # Look for error messages
   ```

2. **Check Python version**
   ```bash
   /path/to/.venv/bin/python --version
   # Should be 3.11+
   ```

### Permission Denied

1. **Check file permissions**
   ```bash
   ls -la ~/Developer/projects/patientsim/.venv/bin/python
   # Should be executable (-rwxr-xr-x)
   ```

2. **Fix if needed**
   ```bash
   chmod +x ~/Developer/projects/patientsim/.venv/bin/python
   ```

### Still Not Working?

Try this diagnostic approach:

```bash
# 1. Can you run Python from the venv?
/Users/YOUR_USERNAME/Developer/projects/patientsim/.venv/bin/python --version

# 2. Can you import the module?
/Users/YOUR_USERNAME/Developer/projects/patientsim/.venv/bin/python -c "import patientsim; print('OK')"

# 3. Can you run the server module?
cd ~/Developer/projects/patientsim
/Users/YOUR_USERNAME/Developer/projects/patientsim/.venv/bin/python -m patientsim.mcp.server

# 4. Is the config file valid JSON?
python -m json.tool < ~/Library/Application\ Support/Claude/claude_desktop_config.json
```

## Example: Complete Working Configuration

Here's a real example configuration (macOS):

```json
{
  "mcpServers": {
    "patientsim": {
      "command": "/Users/markoswald/Developer/projects/patientsim/.venv/bin/python",
      "args": ["-m", "patientsim.mcp.server"],
      "env": {
        "PYTHONPATH": "/Users/markoswald/Developer/projects/patientsim/src",
        "LOG_LEVEL": "INFO"
      }
    },
    "membersim": {
      "command": "/Users/markoswald/Developer/projects/membersim/.venv/bin/python",
      "args": ["-m", "membersim.mcp.server"],
      "env": {
        "PYTHONPATH": "/Users/markoswald/Developer/projects/membersim/src",
        "LOG_LEVEL": "INFO"
      }
    }
  }
}
```

## Next Steps

Once configured:
- [Question Categories](question-categories.md) - What you can ask
- [Example Conversations](example-conversations.md) - See realistic interactions
