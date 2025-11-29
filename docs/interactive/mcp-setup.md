# MCP Server Setup

Complete guide to setting up the Model Context Protocol (MCP) servers for interactive use of HealthSim through Claude.

## What is MCP?

The **Model Context Protocol (MCP)** is a standard that allows Claude to call local tools and functions on your machine. When you ask Claude to "generate a patient," MCP enables Claude to actually run Python code that creates synthetic data.

### Without MCP
```
You: "Generate a patient"
Claude: "I can describe what a synthetic patient might look like..."
       (No actual data generated)
```

### With MCP
```
You: "Generate a patient"
Claude: [Calls PatientSim MCP server]
       "Here's your generated patient:
        - Name: Robert Martinez
        - Age: 58
        - Diagnoses: E11.9 (Type 2 Diabetes)..."
       (Real synthetic data generated)
```

## Architecture Overview

```
┌─────────────────────────────────────────────────────────────────┐
│                 Claude Desktop / Claude Code                     │
│                                                                 │
│    Your conversation with Claude                                │
│    "Generate 5 cardiac patients"                                │
│                          │                                      │
│                          ▼                                      │
│              ┌─────────────────────┐                           │
│              │    MCP Protocol     │                           │
│              │   (JSON-RPC)        │                           │
│              └──────────┬──────────┘                           │
└─────────────────────────┼───────────────────────────────────────┘
                          │
                          │ stdio (standard input/output)
                          │
         ┌────────────────┼────────────────┐
         │                │                │
         ▼                ▼                ▼
┌─────────────────┐ ┌─────────────────┐ ┌─────────────────┐
│   PatientSim    │ │   MemberSim     │ │   Other MCP     │
│   MCP Server    │ │   MCP Server    │ │   Servers       │
│                 │ │                 │ │                 │
│ • generate_     │ │ • generate_     │ │ • Your custom   │
│   patient       │ │   member        │ │   tools         │
│ • export_fhir   │ │ • export_834    │ │                 │
│ • validate      │ │ • care_gaps     │ │                 │
└─────────────────┘ └─────────────────┘ └─────────────────┘
         │                │
         ▼                ▼
┌─────────────────────────────────────────┐
│            Your Local Machine            │
│                                         │
│  ~/Developer/projects/patientsim/       │
│  ~/Developer/projects/membersim/        │
└─────────────────────────────────────────┘
```

## Prerequisites

Before setting up MCP servers:

1. **Python 3.11+** installed
2. **PatientSim and/or MemberSim** installed in virtual environments
3. **Claude Desktop** (macOS/Windows app) OR **Claude Code** (VS Code extension)
4. **MCP Python package** (usually included with HealthSim dependencies)

Verify installations:
```bash
# Check PatientSim
cd ~/Developer/projects/patientsim
source .venv/bin/activate
python -c "from patientsim import PatientGenerator; print('PatientSim OK')"

# Check MemberSim
cd ~/Developer/projects/membersim
source .venv/bin/activate
python -c "from membersim import MemberGenerator; print('MemberSim OK')"
```

## MCP Server Tools

Each HealthSim product exposes tools through its MCP server:

### PatientSim MCP Tools

| Tool | Description | Parameters |
|------|-------------|------------|
| `generate_patient` | Create single patient | scenario, age_range, gender, conditions |
| `generate_cohort` | Create multiple patients | count, scenario, constraints |
| `list_scenarios` | Show available scenarios | (none) |
| `modify_patient` | Add conditions/update | patient_id, modifications |
| `export_fhir` | Export to FHIR R4 | patient_ids |
| `export_hl7v2` | Export to HL7v2 | patient_ids, message_type |
| `validate_patients` | Run clinical validation | patient_ids |

### MemberSim MCP Tools

| Tool | Description | Parameters |
|------|-------------|------------|
| `generate_member` | Create single member | plan_code, age_range, status |
| `generate_family` | Create subscriber + dependents | plan_code, dependent_count |
| `generate_claims` | Generate claims history | member_id, date_range, count |
| `export_834` | Generate X12 834 enrollment | member_ids |
| `export_837` | Generate X12 837 claims | claim_ids, type (P/I) |
| `generate_care_gaps` | Create HEDIS gaps | member_ids, measures |
| `list_plans` | Show available plans | (none) |

## Testing MCP Servers Manually

Before configuring Claude, verify the servers work:

### Test PatientSim Server

```bash
cd ~/Developer/projects/patientsim
source .venv/bin/activate

# Try to start the server (will initialize and wait for input)
python -m patientsim.mcp.server

# You should see MCP protocol initialization
# Press Ctrl+C to stop
```

### Test MemberSim Server

```bash
cd ~/Developer/projects/membersim
source .venv/bin/activate

# Try to start the server
python -m membersim.mcp.server

# Press Ctrl+C to stop
```

If you see errors like "Module not found," the MCP servers may need to be implemented. See the [PatientSim](https://github.com/mark64oswald/patientsim) and [MemberSim](https://github.com/mark64oswald/membersim) repositories for current status.

## Configuration File Location

MCP servers are configured in a JSON file. The location depends on your Claude client:

### Claude Desktop

| OS | Config File Path |
|----|------------------|
| macOS | `~/Library/Application Support/Claude/claude_desktop_config.json` |
| Windows | `%APPDATA%\Claude\claude_desktop_config.json` |

### Claude Code (VS Code Extension)

Config goes in your project directory:
```
your-project/
└── .claude/
    └── mcp-config.json
```

## Next Steps

- [Claude Desktop Configuration](claude-desktop-config.md) - Configure Claude Desktop
- [Question Categories](question-categories.md) - What you can ask
- [Example Conversations](example-conversations.md) - See it in action
