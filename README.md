# HealthSim Hello 👋

A comprehensive getting-started guide for the HealthSim synthetic healthcare data platform.

## What is HealthSim?

HealthSim is a platform for generating realistic synthetic healthcare data through two complementary products built on a shared foundation:

| Repository | Purpose | Output Formats |
|------------|---------|----------------|
| **[healthsim-core](https://github.com/mark64oswald/healthsim-core)** | Shared foundation library | - |
| **[PatientSim](https://github.com/mark64oswald/patientsim)** | Clinical patient data generation | FHIR R4, HL7v2, MIMIC-III |
| **[MemberSim](https://github.com/mark64oswald/membersim)** | Health plan member/claims data | X12 EDI (834, 837, 835, etc.) |

## 📚 Tutorial Contents

### Python Foundations
Deep dives into the Python tools used across all HealthSim projects:
- [Virtual Environments](docs/python-foundations/virtual-environments.md) - Isolation and dependency management
- [Pydantic Guide](docs/python-foundations/pydantic-guide.md) - Data validation and models
- [Pytest Guide](docs/python-foundations/pytest-guide.md) - Testing your code

### Architecture
Understanding how the platform is organized:
- [Platform Overview](docs/architecture/platform-overview.md) - How the pieces fit together
- [Module Inventory](docs/architecture/module-inventory.md) - What's in each package

### Hands-On Tutorials
Step-by-step guides with working code:
- [Environment Setup](docs/tutorials/environment-setup.md) - Get everything installed
- [PatientSim Tutorial](docs/tutorials/patientsim-tutorial.md) - Generate clinical data
- [MemberSim Tutorial](docs/tutorials/membersim-tutorial.md) - Generate payer data

### Interactive (Conversational) Use
Using HealthSim through Claude Desktop or Claude Code:
- [MCP Setup](docs/interactive/mcp-setup.md) - Configure the MCP servers
- [Claude Desktop Config](docs/interactive/claude-desktop-config.md) - Connect to Claude
- [Question Categories](docs/interactive/question-categories.md) - What you can ask
- [Example Conversations](docs/interactive/example-conversations.md) - See it in action

## 🚀 Quick Start

### Option 1: Python API

```python
# PatientSim - Generate clinical data
from patientsim import PatientGenerator

gen = PatientGenerator(seed=42)
patient = gen.generate_patient()
print(f"Generated: {patient.full_name}, Age {patient.age}")

# MemberSim - Generate payer data
from membersim import MemberGenerator

gen = MemberGenerator(seed=42)
member = gen.generate_member()
print(f"Member: {member.member_id}, Plan: {member.plan_code}")
```

### Option 2: Conversational (with Claude)

Once MCP servers are configured, simply ask:

> "Generate 5 cardiac patients for testing our cath lab module"

> "Create a member enrolled in PPO Gold with claims history"

See [Interactive Setup](docs/interactive/mcp-setup.md) for configuration details.

## 📦 Related Repositories

| Repository | Description | Status |
|------------|-------------|--------|
| [healthsim-core](https://github.com/mark64oswald/healthsim-core) | Shared foundation library | Foundation |
| [patientsim](https://github.com/mark64oswald/patientsim) | Clinical data generation | Active |
| [membersim](https://github.com/mark64oswald/membersim) | Payer data generation | Active |

## Prerequisites

- Python 3.11 or higher
- Git
- VS Code (recommended)
- Claude Desktop or Claude Code (for interactive use)

## License

MIT License - See [LICENSE](LICENSE) for details.
