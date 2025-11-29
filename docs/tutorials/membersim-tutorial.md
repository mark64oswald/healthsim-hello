# MemberSim Tutorial

Hands-on guide to generating synthetic health plan member and claims data with MemberSim.

## What is MemberSim?

MemberSim generates realistic synthetic health plan data for:

| Use Case | Description |
|----------|-------------|
| **Claims Testing** | Test claims processing without real member data |
| **EDI Testing** | Generate X12 transactions for integration testing |
| **HEDIS Validation** | Test quality measure calculations |
| **Analytics** | Population health and risk adjustment testing |

### Output Formats

- **X12 834** - Benefit Enrollment and Maintenance
- **X12 837P** - Professional Claims
- **X12 837I** - Institutional Claims
- **X12 835** - Claims Payment/Remittance
- **X12 270/271** - Eligibility Inquiry/Response
- **FHIR** - Coverage and Claim resources
- **CSV/JSON** - Flat file exports

## Key Concepts

Before diving in, here are essential payer domain concepts:

| Term | Definition |
|------|------------|
| **Member** | Person enrolled in a health plan |
| **Subscriber** | Primary member who holds the policy |
| **Dependent** | Family member covered under subscriber's policy |
| **Plan** | Specific benefit design (PPO Gold, HMO Basic, etc.) |
| **Claim** | Request for payment for healthcare services |
| **Accumulator** | Running total (deductible, out-of-pocket) |
| **HEDIS** | Quality measures for health plans |

## Installation

### Step 1: Clone the Repository

```bash
cd ~/Developer/projects
git clone https://github.com/mark64oswald/membersim.git
cd membersim
```

### Step 2: Create Virtual Environment

```bash
python3 -m venv .venv
source .venv/bin/activate  # Windows: .venv\Scripts\activate
```

### Step 3: Install MemberSim

```bash
pip install --upgrade pip
pip install -e ".[dev]"
```

### Step 4: Verify Installation

```bash
python -c "from membersim import MemberGenerator; print('MemberSim installed successfully!')"
```

## Your First Member

Let's generate a synthetic member:

```python
from membersim import MemberGenerator

# Create generator with seed for reproducibility
gen = MemberGenerator(seed=42)

# Generate a single member
member = gen.generate_member()

# Explore the member
print(f"Member ID: {member.member_id}")
print(f"Name: {member.demographics.full_name}")
print(f"Plan: {member.plan_code}")
print(f"Status: {member.status}")
print(f"Effective: {member.coverage_start}")
```

Expected output:
```
Member ID: MEM-00294857
Name: Jennifer Adams
Plan: PPO-GOLD
Status: active
Effective: 2024-01-01
```

## Understanding the Member Model

A generated member includes:

```
Member
├── member_id: str            # Unique identifier
├── subscriber_id: str        # Link to subscriber (may be self)
├── demographics              # From healthsim-core
│   ├── first_name, last_name
│   ├── date_of_birth
│   ├── gender
│   ├── ssn (masked)
│   └── address
├── plan_code: str           # PPO-GOLD, HMO-BASIC, etc.
├── group_id: str            # Employer group
├── coverage_start: date
├── coverage_end: date       # None if active
├── status: str              # active, termed, pending
├── relationship: str        # self, spouse, child
├── accumulators: dict
│   ├── deductible_individual
│   ├── deductible_family
│   ├── oop_individual
│   └── oop_family
└── claims: list[Claim]
```

### Exploring Member Data

```python
# Check coverage status
print(f"\nCoverage Details:")
print(f"  Plan: {member.plan_code}")
print(f"  Group: {member.group_id}")
print(f"  Status: {member.status}")
print(f"  Relationship: {member.relationship}")

# Check accumulators
print(f"\nAccumulators:")
for name, acc in member.accumulators.items():
    print(f"  {name}: ${acc.used:.2f} of ${acc.limit:.2f}")
```

## Generating with Constraints

### Plan Selection

```python
# Specific plan
member = gen.generate_member(plan_code="PPO-GOLD")

# Random from available plans
plans = gen.list_plans()
print("Available plans:", plans)
```

### Demographic Constraints

```python
# Age range
member = gen.generate_member(age_range=(30, 45))

# Gender
member = gen.generate_member(gender="F")

# Combined
member = gen.generate_member(
    plan_code="HMO-BASIC",
    age_range=(25, 35),
    gender="M"
)
```

### Status

```python
# Active member
member = gen.generate_member(status="active")

# Termed member (with termination date)
member = gen.generate_member(status="termed")
```

## Generating Families

Create a subscriber with dependents:

```python
# Subscriber with spouse and 2 children
family = gen.generate_family(
    plan_code="PPO-GOLD",
    dependent_config={
        "spouse": True,
        "children": 2
    }
)

print(f"Family size: {len(family)} members")
for member in family:
    print(f"  {member.demographics.full_name} ({member.relationship})")
```

Output:
```
Family size: 4 members
  John Smith (self)
  Sarah Smith (spouse)
  Emily Smith (child)
  Michael Smith (child)
```

## Generating Claims

### Add Claims to Member

```python
from datetime import date

# Generate member with claims history
member = gen.generate_member_with_claims(
    plan_code="PPO-GOLD",
    claim_count=5,
    date_range=(date(2024, 1, 1), date(2024, 6, 30))
)

print(f"\nClaims for {member.demographics.full_name}:")
for claim in member.claims:
    print(f"  {claim.claim_id}: {claim.service_date}")
    print(f"    Billed: ${claim.total_charge:.2f}")
    print(f"    Paid: ${claim.total_paid:.2f}")
```

### Understanding Claim Structure

```
Claim
├── claim_id: str
├── member_id: str
├── claim_type: str          # professional, institutional
├── service_date: date
├── provider_npi: str
├── provider_name: str
├── diagnosis_codes: list[str]
├── lines: list[ClaimLine]
│   ├── line_number: int
│   ├── procedure_code: str
│   ├── modifier: str
│   ├── units: int
│   ├── charge: Decimal
│   ├── allowed: Decimal
│   ├── paid: Decimal
│   └── member_responsibility: Decimal
├── total_charge: Decimal
├── total_allowed: Decimal
├── total_paid: Decimal
└── status: str              # paid, denied, pending
```

### Claim Scenarios

```python
# High-cost claim
member = gen.generate_member_with_claims(
    claim_count=1,
    claim_type="high_cost"
)

# Denied claim
member = gen.generate_member_with_claims(
    claim_count=1,
    include_denied=True
)

# Chronic care pattern (regular visits)
member = gen.generate_member_with_claims(
    claim_count=12,  # Monthly visits
    scenario="chronic_care"
)
```

## Generating Batches

Generate multiple members at once:

```python
# Simple batch
members = gen.generate_member_batch(count=50)
print(f"Generated {len(members)} members")

# Batch with constraints
ppo_members = gen.generate_member_batch(
    count=100,
    plan_code="PPO-GOLD",
    age_range=(40, 65)
)

# Batch with claims
members_with_claims = gen.generate_population(
    count=200,
    with_claims=True,
    claims_per_member=(1, 10)
)
```

## Exporting to X12 EDI

### X12 834 (Enrollment)

```python
from membersim.formats import generate_834

# Generate enrollment file for members
members = gen.generate_member_batch(10)
edi_834 = generate_834(members)

# Preview
print(edi_834[:500])

# Save to file
with open("enrollment.834", "w") as f:
    f.write(edi_834)
```

The 834 includes:
- ISA/GS envelope segments
- Member demographics (INS, NM1, N3, N4, DMG)
- Coverage information (HD, DTP)
- Subscriber relationships

### X12 837P (Professional Claims)

```python
from membersim.formats import generate_837p

# Collect claims
all_claims = []
for member in members_with_claims:
    all_claims.extend(member.claims)

# Generate 837P
edi_837p = generate_837p(all_claims)

# Save
with open("claims.837", "w") as f:
    f.write(edi_837p)
```

### X12 835 (Remittance)

```python
from membersim.formats import generate_835

# Generate payment/remittance for claims
paid_claims = [c for c in all_claims if c.status == "paid"]
edi_835 = generate_835(paid_claims)

with open("remittance.835", "w") as f:
    f.write(edi_835)
```

### X12 270/271 (Eligibility)

```python
from membersim.formats import generate_270, generate_271

# Eligibility inquiry
inquiry_270 = generate_270(member)

# Eligibility response
response_271 = generate_271(member, benefits=True)
```

## Quality Measures (HEDIS)

### Generate Care Gaps

```python
from membersim.quality import generate_care_gaps

# Generate members with care gaps
members = gen.generate_member_batch(100)
gaps = generate_care_gaps(members, gap_rate=0.30)

print(f"Generated {len(gaps)} care gaps")

# Analyze by measure
from collections import Counter
measures = Counter(gap.measure_id for gap in gaps)
for measure, count in measures.most_common():
    print(f"  {measure}: {count} gaps")
```

### HEDIS Measures Supported

| Measure ID | Description |
|------------|-------------|
| CDC-HBD | Diabetes: HbA1c Testing |
| CDC-EYE | Diabetes: Eye Exam |
| CDC-KED | Diabetes: Kidney Screening |
| SPC | Statin Therapy for CVD |
| CBP | Controlling Blood Pressure |
| BCS | Breast Cancer Screening |
| COL | Colorectal Cancer Screening |

### Member Measure Status

```python
from membersim.quality import calculate_measure_status

# Get measure status for a member
status = calculate_measure_status(member, measure_id="CDC-HBD")
print(f"HbA1c Testing: {status}")  # compliant, gap, excluded
```

## Complete Example

Here's a full workflow:

```python
"""Complete MemberSim workflow example."""
from datetime import date
from membersim import MemberGenerator
from membersim.formats import generate_834, generate_837p
from membersim.quality import generate_care_gaps

# Setup
gen = MemberGenerator(seed=42)

# Generate a population with claims
print("Generating member population...")
members = gen.generate_population(
    count=100,
    plan_distribution={
        "PPO-GOLD": 0.40,
        "PPO-SILVER": 0.35,
        "HMO-BASIC": 0.25
    },
    with_claims=True,
    claims_per_member=(0, 12)
)

# Summary
print(f"\nPopulation Summary:")
print(f"  Total members: {len(members)}")
active = sum(1 for m in members if m.status == "active")
print(f"  Active: {active}")

total_claims = sum(len(m.claims) for m in members)
print(f"  Total claims: {total_claims}")

# Generate 834 enrollment file
print("\nGenerating X12 834...")
edi_834 = generate_834([m for m in members if m.status == "active"])
with open("enrollment.834", "w") as f:
    f.write(edi_834)
print(f"  Saved: enrollment.834 ({len(edi_834)} bytes)")

# Generate 837P claims file
print("\nGenerating X12 837P...")
all_claims = [c for m in members for c in m.claims]
edi_837p = generate_837p(all_claims)
with open("claims.837", "w") as f:
    f.write(edi_837p)
print(f"  Saved: claims.837 ({len(edi_837p)} bytes)")

# Generate care gaps
print("\nGenerating care gaps...")
gaps = generate_care_gaps(members, gap_rate=0.25)
print(f"  Generated {len(gaps)} care gaps")

# Export care gaps to CSV
import csv
with open("care_gaps.csv", "w", newline="") as f:
    writer = csv.writer(f)
    writer.writerow(["member_id", "member_name", "measure", "gap_date"])
    for gap in gaps:
        member = next(m for m in members if m.member_id == gap.member_id)
        writer.writerow([
            gap.member_id,
            member.demographics.full_name,
            gap.measure_id,
            gap.gap_date
        ])
print("  Saved: care_gaps.csv")

print("\n✓ Complete!")
```

## Next Steps

- [PatientSim Tutorial](patientsim-tutorial.md) - Generate clinical data
- [MCP Setup](../interactive/mcp-setup.md) - Use conversationally
- [Module Inventory](../architecture/module-inventory.md) - Explore the codebase
