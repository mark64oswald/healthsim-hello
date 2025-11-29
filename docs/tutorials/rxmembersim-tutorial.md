# RxMemberSim Tutorial

Generate synthetic pharmacy benefit data for PBM system testing.

## Installation

```bash
pip install rxmembersim
```

Or from source:

```bash
git clone https://github.com/mark64oswald/rxmembersim.git
cd rxmembersim
pip install -e ".[dev]"
```

## Your First Pharmacy Member

```python
from rxmembersim.core.member import RxMemberGenerator

generator = RxMemberGenerator()
member = generator.generate(
    bin="610014",
    pcn="RXTEST",
    group_number="DEMO001",
)

print(f"Member ID: {member.member_id}")
print(f"BIN/PCN/Group: {member.bin}/{member.pcn}/{member.group_number}")
print(f"Name: {member.demographics.first_name} {member.demographics.last_name}")
print(f"Deductible Remaining: ${member.accumulators.deductible_remaining}")
```

Output:
```
Member ID: RXM-12345678
BIN/PCN/Group: 610014/RXTEST/DEMO001
Name: John Smith
Deductible Remaining: $250
```

## Check Formulary Coverage

```python
from rxmembersim.formulary.formulary import FormularyGenerator

# Generate a standard commercial formulary
formulary = FormularyGenerator().generate_standard_commercial()

# Check drug coverage
drugs_to_check = [
    ("00071015523", "Atorvastatin 10mg"),
    ("00169413512", "Ozempic 0.5mg"),
    ("99999999999", "Unknown Drug"),
]

for ndc, name in drugs_to_check:
    status = formulary.check_coverage(ndc)
    print(f"\n{name} ({ndc}):")
    print(f"  Covered: {status.covered}")
    if status.covered:
        print(f"  Tier: {status.tier} - {status.tier_name}")
        print(f"  Copay: ${status.copay}")
        print(f"  Requires PA: {status.requires_pa}")
```

Output:
```
Atorvastatin 10mg (00071015523):
  Covered: True
  Tier: 1 - Preferred Generic
  Copay: $10
  Requires PA: False

Ozempic 0.5mg (00169413512):
  Covered: True
  Tier: 5 - Specialty
  Copay: None (25% coinsurance)
  Requires PA: True

Unknown Drug (99999999999):
  Covered: False
```

## Process a Pharmacy Claim

```python
from datetime import date
from decimal import Decimal

from rxmembersim.core.member import RxMemberGenerator
from rxmembersim.claims.claim import PharmacyClaim, TransactionCode
from rxmembersim.claims.adjudication import AdjudicationEngine
from rxmembersim.formulary.formulary import FormularyGenerator

# Generate member
member = RxMemberGenerator().generate(bin="610014", pcn="RXTEST", group_number="GRP001")

# Create claim
claim = PharmacyClaim(
    claim_id="CLM001",
    transaction_code=TransactionCode.BILLING,
    service_date=date.today(),
    pharmacy_npi="9876543210",
    member_id=member.member_id,
    cardholder_id=member.cardholder_id,
    person_code=member.person_code,
    bin=member.bin,
    pcn=member.pcn,
    group_number=member.group_number,
    prescription_number="RX123456",
    fill_number=1,
    ndc="00071015523",  # Atorvastatin
    quantity_dispensed=Decimal("30"),
    days_supply=30,
    daw_code="0",
    prescriber_npi="1234567890",
    ingredient_cost_submitted=Decimal("15.00"),
    dispensing_fee_submitted=Decimal("2.00"),
    patient_paid_submitted=Decimal("0.00"),
    usual_customary_charge=Decimal("25.00"),
    gross_amount_due=Decimal("17.00"),
)

# Adjudicate
formulary = FormularyGenerator().generate_standard_commercial()
engine = AdjudicationEngine(formulary=formulary)
response = engine.adjudicate(claim, member)

print(f"Status: {response.response_status}")
print(f"Plan Pays: ${response.total_amount_paid}")
print(f"Patient Pays: ${response.patient_pay_amount}")
```

## Drug Utilization Review (DUR)

```python
from datetime import date
from rxmembersim.dur.validator import DURValidator

validator = DURValidator()

# Check for drug interactions
result = validator.validate_simple(
    ndc="00056017270",
    gpi="83300010000330",  # Warfarin
    drug_name="Warfarin 5mg",
    member_id="MEM001",
    service_date=date.today(),
    current_medications=[
        {"ndc": "00904515260", "gpi": "66100010000310", "name": "Ibuprofen 200mg"}
    ],
    patient_age=65,
    patient_gender="F",
)

print(f"DUR Passed: {result.passed}")
print(f"Total Alerts: {result.total_alerts}")
for alert in result.alerts:
    print(f"  [{alert.alert_type.value}] {alert.message}")
```

Output:
```
DUR Passed: False
Total Alerts: 1
  [DD] Increased bleeding risk
```

## Prior Authorization

```python
from decimal import Decimal
from rxmembersim.authorization.prior_auth import PAWorkflow

pa_workflow = PAWorkflow()

# Create PA request for specialty drug
request = pa_workflow.create_request(
    member_id="MEM001",
    cardholder_id="CH001",
    ndc="00169413512",  # Ozempic
    drug_name="Ozempic 0.5mg",
    quantity=Decimal("1"),
    days_supply=28,
    prescriber_npi="1234567890",
    prescriber_name="Dr. Smith",
)

print(f"PA Request ID: {request.pa_request_id}")
print(f"Status: {request.status}")

# Emergency auto-approval
urgent_request = pa_workflow.create_request(
    member_id="MEM001",
    cardholder_id="CH001",
    ndc="00169413512",
    drug_name="Ozempic 0.5mg",
    quantity=Decimal("1"),
    days_supply=28,
    prescriber_npi="1234567890",
    prescriber_name="Dr. Smith",
    urgency="emergency",
)
response = pa_workflow.check_auto_approval(urgent_request)
print(f"Auto-Approved: {response.auto_approved if response else False}")
```

## Run Scenarios

```python
from rxmembersim.scenarios.engine import RxScenarioEngine

engine = RxScenarioEngine()

# List available scenarios
print("Available scenarios:")
for scenario in engine.list_scenarios():
    print(f"  {scenario.scenario_id}: {scenario.scenario_name}")

# Run a scenario
scenario = engine.new_therapy_pa_required()
timeline = engine.execute_scenario(scenario, "MEM001")

print(f"\nTimeline ({len(timeline.events)} events):")
for event in timeline.events:
    print(f"  {event.event_date}: {event.event_type.value}")
```

Output:
```
Available scenarios:
  NEW_THERAPY_01: New Therapy - Approved
  NEW_THERAPY_PA: New Therapy - PA Required
  NEW_THERAPY_ST: New Therapy - Step Therapy
  SPECIALTY_ONBOARD: Specialty Drug Onboarding
  ADHERENCE_GAP: Adherence Gap

Timeline (5 events):
  2025-01-15: new_prescription
  2025-01-15: claim_submitted
  2025-01-15: pa_required
  2025-01-16: pa_submitted
  2025-01-18: pa_approved
```

## Key Concepts

### BIN/PCN/Group
These identifiers route pharmacy claims to the correct PBM:

| Field | Description | Example |
|-------|-------------|---------|
| **BIN** | Bank Identification Number - identifies the PBM | 610014 |
| **PCN** | Processor Control Number - identifies the plan | RXTEST |
| **Group** | Employer or sponsor group number | GRP001 |

### Formulary Tiers

| Tier | Description | Typical Copay |
|------|-------------|---------------|
| 1 | Preferred Generic | $5-15 |
| 2 | Non-Preferred Generic | $20-30 |
| 3 | Preferred Brand | $35-50 |
| 4 | Non-Preferred Brand | $75-100 |
| 5 | Specialty | 20-33% coinsurance |

### Common Reject Codes

| Code | Description |
|------|-------------|
| 70 | Product/Service Not Covered |
| 75 | Prior Authorization Required |
| 76 | Plan Limitations Exceeded |
| 79 | Refill Too Soon |
| 88 | DUR Reject |

### DUR Alert Types

| Code | Type | Description |
|------|------|-------------|
| DD | Drug-Drug | Interaction between medications |
| TD | Therapeutic Duplication | Multiple drugs in same class |
| DA | Drug-Age | Age-inappropriate medication |
| ER | Early Refill | Refill requested too soon |
| HD | High Dose | Exceeds maximum recommended dose |

## Next Steps

- Explore the [RxMemberSim README](https://github.com/mark64oswald/rxmembersim) for full API documentation
- Check out the `skills/` directory for pharmacy domain knowledge
- Run the interactive demo: `python demos/interactive_demo.py`