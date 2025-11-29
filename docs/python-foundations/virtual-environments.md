# Python Virtual Environments

A comprehensive guide to understanding and using Python virtual environments in HealthSim projects.

## The Problem They Solve

Imagine you have two projects on your machine:

- **Project A** requires `pydantic==1.10.0` (the v1 API)
- **Project B** requires `pydantic==2.5.0` (the v2 API with breaking changes)

Without virtual environments, Python installs packages **globally**—meaning you can only have *one* version of pydantic installed at a time. Switching between projects would require uninstalling and reinstalling different versions constantly.

**Virtual environments solve this** by giving each project its own isolated Python installation with its own packages.

## What a Virtual Environment Actually Is

A virtual environment is simply a **directory** containing:

1. A copy of (or symlink to) the Python interpreter
2. Its own `site-packages` folder for installed packages
3. Activation scripts that modify your shell's PATH

### Directory Structure

When you create a virtual environment with `python3 -m venv .venv`, here's what gets created:

```
.venv/
├── bin/                          # (Scripts/ on Windows)
│   ├── activate                  # Activation script for bash/zsh
│   ├── activate.csh              # Activation script for csh
│   ├── activate.fish             # Activation script for fish
│   ├── pip                       # Package installer
│   ├── pip3
│   ├── python -> python3         # Symlink to Python
│   ├── python3 -> /usr/bin/python3.11
│   └── python3.11 -> python3
├── include/                      # Header files for C extensions
├── lib/
│   └── python3.11/
│       └── site-packages/        # WHERE PACKAGES GET INSTALLED
│           ├── pip/
│           ├── pydantic/
│           ├── faker/
│           └── ...
└── pyvenv.cfg                    # Configuration file
```

### The pyvenv.cfg File

This small file tells Python about the virtual environment:

```ini
home = /usr/bin
include-system-site-packages = false
version = 3.11.5
executable = /usr/bin/python3.11
command = /usr/bin/python3 -m venv /path/to/project/.venv
```

Key settings:
- `home` - Where the base Python lives
- `include-system-site-packages` - If `false`, completely isolated from global packages
- `version` - Python version

## How Activation Works

When you run `source .venv/bin/activate`, the script does two simple things:

```bash
# 1. Set the VIRTUAL_ENV environment variable
VIRTUAL_ENV="/path/to/project/.venv"
export VIRTUAL_ENV

# 2. Prepend .venv/bin to your PATH
_OLD_VIRTUAL_PATH="$PATH"
PATH="$VIRTUAL_ENV/bin:$PATH"
export PATH
```

**That's it.** When you type `python` or `pip`, your shell finds the one in `.venv/bin/` first because it's at the front of your PATH.

### Before and After Activation

```bash
# BEFORE activation
$ which python3
/usr/bin/python3

$ python3 -c "import sys; print(sys.prefix)"
/usr

# AFTER activation
$ source .venv/bin/activate
(.venv) $ which python3
/path/to/project/.venv/bin/python3

(.venv) $ python3 -c "import sys; print(sys.prefix)"
/path/to/project/.venv
```

Notice:
- The prompt shows `(.venv)` to remind you the environment is active
- `which python3` now points to the venv
- `sys.prefix` shows the venv path instead of system path

### What Deactivate Does

The `deactivate` command simply restores your original PATH:

```bash
PATH="$_OLD_VIRTUAL_PATH"
unset VIRTUAL_ENV
```

## The Mental Model

Think of virtual environments as isolated bubbles:

```
Your Machine
├── System Python (/usr/bin/python3)
│   └── site-packages/  ← System packages (avoid installing here)
│
├── healthsim-core/.venv/
│   └── site-packages/  ← pydantic 2.x, faker, pytest
│
├── patientsim/.venv/
│   └── site-packages/  ← healthsim-core, pydantic 2.x, hl7
│
└── membersim/.venv/
    └── site-packages/  ← healthsim-core, pydantic 2.x, x12
```

Each project gets its own isolated bubble. They can have:
- Different versions of the same package
- Different sets of packages entirely
- No interference with each other

## Common Commands Reference

| Task | Command |
|------|---------|
| **Create** virtual environment | `python3 -m venv .venv` |
| **Activate** (macOS/Linux) | `source .venv/bin/activate` |
| **Activate** (Windows cmd) | `.venv\Scripts\activate.bat` |
| **Activate** (Windows PowerShell) | `.venv\Scripts\Activate.ps1` |
| **Verify** active environment | `which python` (should show .venv path) |
| **Install** package | `pip install package-name` |
| **Install** from pyproject.toml | `pip install -e ".[dev]"` |
| **List** installed packages | `pip list` |
| **Show** package details | `pip show package-name` |
| **Freeze** requirements | `pip freeze > requirements.txt` |
| **Deactivate** | `deactivate` |
| **Delete** venv (recreate if needed) | `rm -rf .venv` |

## The -e Flag (Editable Installs)

When you run `pip install -e ".[dev]"`, the `-e` flag means **editable** mode.

### Without -e (Regular Install)

```bash
pip install .
```

Pip copies your package code into `site-packages/`. If you change your source files, you need to reinstall to see the changes.

### With -e (Editable Install)

```bash
pip install -e .
```

Pip creates a **link** to your source directory. Changes to your source files take effect immediately without reinstalling.

### How It Works

Editable installs create a `.pth` file in site-packages:

```bash
$ cat .venv/lib/python3.11/site-packages/_healthsim_hello.pth
/path/to/project/healthsim-hello/src
```

This file tells Python: "When looking for `healthsim_hello`, also check this path."

### When to Use Each

| Situation | Use |
|-----------|-----|
| **Development** (you're editing the code) | `pip install -e .` |
| **Production** (deploying the code) | `pip install .` |
| **Installing someone else's package** | `pip install package-name` |

## Convention: .venv vs venv

Both work fine. The leading dot (`.venv`) makes it a **hidden directory** on Unix systems:

- Keeps it out of regular `ls` listings
- Makes it clear this is a tooling artifact, not source code
- Most `.gitignore` templates already exclude `.venv`

The HealthSim projects use `.venv` by convention.

## Troubleshooting Common Issues

### "command not found: python"

**Cause:** Virtual environment not activated

**Solution:**
```bash
source .venv/bin/activate
```

### Wrong packages showing up

**Cause:** Using system pip instead of venv pip

**Solution:** Check which pip you're using:
```bash
which pip
# Should show: /path/to/project/.venv/bin/pip
# NOT: /usr/bin/pip or /usr/local/bin/pip
```

If wrong, activate the venv first.

### "Permission denied" errors

**Cause:** Trying to use `sudo` with pip in a venv

**Solution:** Never use `sudo` with a virtual environment. If you get permission errors:
```bash
# Make sure you own the venv directory
ls -la .venv/

# If needed, fix ownership
chown -R $(whoami) .venv/
```

### "No module named X" after installing

**Cause:** Installed in wrong environment

**Solution:**
1. Check you're in the right venv: `which python`
2. Verify package is installed: `pip list | grep package-name`
3. If missing, install it: `pip install package-name`

### Venv seems corrupted

**Solution:** Delete and recreate:
```bash
deactivate
rm -rf .venv
python3 -m venv .venv
source .venv/bin/activate
pip install -e ".[dev]"
```

## HealthSim-Specific Notes

### Each Project Has Its Own Venv

```
~/Developer/projects/
├── healthsim-core/
│   └── .venv/          ← Independent environment
├── patientsim/
│   └── .venv/          ← Has healthsim-core as dependency
├── membersim/
│   └── .venv/          ← Has healthsim-core as dependency
└── healthsim-hello/
    └── .venv/          ← Tutorial project
```

### Dependency Chain

When you install PatientSim or MemberSim, they automatically install healthsim-core as a dependency:

```toml
# In patientsim/pyproject.toml
dependencies = [
    "healthsim-core @ git+https://github.com/mark64oswald/healthsim-core.git",
    # ... other deps
]
```

### VS Code Workspace Configuration

The HealthSim workspace is configured to use the correct venv for each project:

```json
{
    "python.defaultInterpreterPath": "${workspaceFolder}/.venv/bin/python"
}
```

When you open a file from a specific project folder, VS Code uses that project's `.venv`.

## Quick Setup Script

Here's a script to set up any HealthSim project:

```bash
#!/bin/bash
# setup-venv.sh

# Create virtual environment
python3 -m venv .venv

# Activate it
source .venv/bin/activate

# Upgrade pip
pip install --upgrade pip

# Install project with dev dependencies
pip install -e ".[dev]"

# Verify installation
python -c "import sys; print(f'Python: {sys.executable}')"
pip list

echo "✅ Virtual environment ready!"
echo "Run 'source .venv/bin/activate' to activate in new shells"
```

## Summary

| Concept | What It Means |
|---------|---------------|
| **Virtual environment** | A directory with its own Python + packages |
| **Activation** | Modifies PATH so `.venv/bin/python` is found first |
| **site-packages** | Where pip installs packages (inside each venv) |
| **Editable install** (`-e`) | Links to source code instead of copying |
| **Why use them** | Project isolation—different projects can have different dependencies |

The key insight: **virtual environments aren't magic**. They're just directories with a Python symlink and an activation script that puts that directory first in your PATH. Everything else flows from that simple mechanism.
