# HealthSim Hello 👋

A comprehensive getting-started guide for the HealthSim synthetic healthcare data platform.

## What is HealthSim?

HealthSim is a platform for generating realistic synthetic healthcare data through three complementary products built on a shared foundation:

| Repository | Domain | Key Capabilities |
|------------|--------|------------------|
| **[healthsim-core](https://github.com/mark64oswald/healthsim-core)** | Foundation | Shared models, validation, temporal logic |
| **[PatientSim](https://github.com/mark64oswald/patientsim)** | Clinical | Patient records, encounters, HL7v2, FHIR |
| **[MemberSim](https://github.com/mark64oswald/membersim)** | Payer | Member enrollment, claims, X12 EDI |
| **[RxMemberSim](https://github.com/mark64oswald/rxmembersim)** | Pharmacy | Prescriptions, PBM claims, NCPDP, ePA |

### RxMemberSim - Pharmacy Benefits
Generate synthetic pharmacy data:
- 💊 Prescriptions and e-prescribing (NCPDP SCRIPT)
- 💳 PBM claims and adjudication (NCPDP Telecom)
- 📋 Formulary and DUR rules
- ✅ Prior authorization and ePA
- 🏥 Specialty pharmacy workflows
- 💰 Pricing, rebates, copay assistance

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
- [RxMemberSim Tutorial](docs/tutorials/rxmembersim-tutorial.md) - Generate pharmacy data

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

# RxMemberSim - Generate pharmacy data
from rxmembersim.core.member import RxMemberGenerator

gen = RxMemberGenerator()
member = gen.generate(bin="610014", pcn="RXTEST")
print(f"Member: {member.member_id}, BIN/PCN: {member.bin}/{member.pcn}")
```

### Option 2: Conversational (with Claude)

Once MCP servers are configured, simply ask:

> "Generate 5 cardiac patients for testing our cath lab module"

> "Create a member enrolled in PPO Gold with claims history"

> "Generate a pharmacy claim for 30 tablets of atorvastatin"

See [Interactive Setup](docs/interactive/mcp-setup.md) for configuration details.

## 📦 Related Repositories

| Repository | Description | Status |
|------------|-------------|--------|
| [healthsim-core](https://github.com/mark64oswald/healthsim-core) | Shared foundation library | v0.2.0 |
| [patientsim](https://github.com/mark64oswald/patientsim) | Clinical data generation | Active |
| [membersim](https://github.com/mark64oswald/membersim) | Payer data generation | Active |
| [rxmembersim](https://github.com/mark64oswald/rxmembersim) | Pharmacy data generation | v1.0.0 |

## Prerequisites

- Python 3.11 or higher
- Git
- VS Code (recommended)
- Claude Desktop or Claude Code (for interactive use)

## License

MIT License - See [LICENSE](LICENSE) for details.