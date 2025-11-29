# PatientSim Tutorial

Hands-on guide to generating synthetic clinical patient data with PatientSim.

## What is PatientSim?

PatientSim generates realistic synthetic clinical patient data for:

| Use Case | Description |
|----------|-------------|
| **EMR Testing** | Test EHR integrations without real patient data |
| **CDSS Validation** | Validate clinical decision support rules |
| **Training** | Realistic data for educational scenarios |
| **Analytics** | Population health testing and reporting |

### Output Formats

- **FHIR R4** - Modern healthcare interoperability standard
- **HL7v2** - Traditional hospital messaging (ADT, ORM, ORU)
- **MIMIC-III** - Research database format

## Installation

### Step 1: Clone the Repository

```bash
cd ~/Developer/projects
git clone https://github.com/mark64oswald/patientsim.git
cd patientsim
```

### Step 2: Create Virtual Environment

```bash
python3 -m venv .venv
source .venv/bin/activate  # Windows: .venv\Scripts\activate
```

### Step 3: Install PatientSim

```bash
pip install --upgrade pip
pip install -e ".[dev]"
```

### Step 4: Verify Installation

```bash
python -c "from patientsim import PatientGenerator; print('PatientSim installed successfully!')"
```

## Your First Patient

Let's generate a synthetic patient:

```python
from patientsim import PatientGenerator

# Create generator with seed for reproducibility
gen = PatientGenerator(seed=42)

# Generate a single patient
patient = gen.generate_patient()

# Explore the patient
print(f"Patient ID: {patient.patient_id}")
print(f"Name: {patient.full_name}")
print(f"Age: {patient.age}")
print(f"Gender: {patient.gender}")
print(f"MRN: {patient.mrn}")
```

Expected output:
```
Patient ID: PAT-a1b2c3d4
Name: Robert Martinez
Age: 58
Gender: M
MRN: MRN-00847293
```

## Understanding the Patient Model

A generated patient includes:

```
Patient
├── patient_id: str           # Unique identifier
├── mrn: str                  # Medical record number
├── demographics              # From healthsim-core
│   ├── first_name: str
│   ├── last_name: str
│   ├── date_of_birth: date
│   ├── gender: str
│   └── address: Address
├── diagnoses: list[Diagnosis]
│   ├── code: str             # ICD-10 code
│   ├── description: str
│   ├── onset_date: date
│   └── status: str           # active, resolved
├── encounters: list[Encounter]
│   ├── encounter_id: str
│   ├── type: str             # inpatient, outpatient, ED
│   ├── admit_date: datetime
│   ├── discharge_date: datetime
│   └── diagnoses, procedures, observations
├── medications: list[Medication]
│   ├── name: str
│   ├── dose: str
│   ├── frequency: str
│   └── status: str
└── allergies: list[Allergy]
```

### Exploring Patient Data

```python
# List diagnoses
print("\nDiagnoses:")
for dx in patient.diagnoses:
    print(f"  {dx.code}: {dx.description}")

# List encounters
print("\nEncounters:")
for enc in patient.encounters:
    print(f"  {enc.encounter_id}: {enc.type} on {enc.admit_date}")

# List medications
print("\nMedications:")
for med in patient.medications:
    print(f"  {med.name} {med.dose} - {med.frequency}")
```

## Generating with Constraints

### Demographic Constraints

```python
# Specific age range
patient = gen.generate_patient(age_range=(65, 80))

# Specific gender
patient = gen.generate_patient(gender="F")

# Combined
patient = gen.generate_patient(
    age_range=(45, 65),
    gender="M"
)
```

### Clinical Conditions

```python
# Single condition
patient = gen.generate_patient(conditions=["diabetes"])

# Multiple conditions
patient = gen.generate_patient(
    conditions=["diabetes", "hypertension", "copd"]
)
```

### Using Scenarios

Scenarios are pre-configured clinical profiles:

```python
# List available scenarios
scenarios = gen.list_scenarios()
print("Available scenarios:", scenarios)

# Generate using a scenario
cardiac_patient = gen.generate_patient(scenario="cardiac")
diabetic_patient = gen.generate_patient(scenario="diabetes")
emergency_patient = gen.generate_patient(scenario="emergency")
```

Common scenarios:
- `cardiac` - Heart conditions, cath lab procedures
- `diabetes` - Type 2 DM with complications
- `emergency` - ED presentations
- `surgical` - Perioperative patients

## Generating Cohorts

Generate multiple patients at once:

```python
# Simple batch
patients = gen.generate_batch(count=10)
print(f"Generated {len(patients)} patients")

# Batch with constraints
cardiac_cohort = gen.generate_batch(
    count=20,
    scenario="cardiac",
    age_range=(50, 75)
)

# Show summary
for i, p in enumerate(cardiac_cohort[:5], 1):
    print(f"{i}. {p.full_name}, {p.age}y {p.gender}")
    print(f"   Primary Dx: {p.diagnoses[0].code if p.diagnoses else 'None'}")
```

## Exporting to FHIR

Convert patients to FHIR R4 format:

```python
from patientsim.formats.fhir import FHIRExporter

exporter = FHIRExporter()

# Export single patient to FHIR Bundle
bundle = exporter.to_bundle(patient)

# The bundle contains multiple resource types
print(f"Bundle ID: {bundle.id}")
print(f"Total resources: {len(bundle.entry)}")

# List resources by type
from collections import Counter
types = Counter(e.resource.resource_type for e in bundle.entry)
for rtype, count in types.items():
    print(f"  {rtype}: {count}")
```

Output:
```
Bundle ID: bundle-PAT-a1b2c3d4
Total resources: 15
  Patient: 1
  Condition: 3
  Encounter: 2
  Observation: 6
  MedicationRequest: 3
```

### Save to File

```python
# Save as JSON
with open("patient_bundle.json", "w") as f:
    f.write(bundle.json(indent=2))

# Export multiple patients
cohort_bundle = exporter.to_bundle(patients)
with open("cohort_bundle.json", "w") as f:
    f.write(cohort_bundle.json(indent=2))
```

## Exporting to HL7v2

Generate traditional HL7v2 messages:

```python
from patientsim.formats.hl7v2 import HL7v2Builder

builder = HL7v2Builder()

# Get an encounter
encounter = patient.encounters[0]

# Generate ADT^A01 (Admission)
adt_message = builder.build_adt_a01(patient, encounter)
print(adt_message)
```

Output:
```
MSH|^~\&|PATIENTSIM|FACILITY|RECEIVER|DEST|20241127143000||ADT^A01|MSG001|P|2.5.1
EVN|A01|20241127143000
PID|1||MRN-00847293||Martinez^Robert||19660315|M|||123 Main St^^Boston^MA^02101
PV1|1|I|ICU^101^A|||||||||||||||V001
DG1|1||E11.9^Type 2 diabetes mellitus without complications^ICD10|||A
```

### Message Types

```python
# Discharge
adt_a03 = builder.build_adt_a03(patient, encounter)

# Patient update
adt_a08 = builder.build_adt_a08(patient)

# Order message
orm = builder.build_orm_o01(patient, order)

# Results message
oru = builder.build_oru_r01(patient, observation)
```

## Validation

Check clinical plausibility:

```python
from patientsim.validation import ClinicalValidator

validator = ClinicalValidator()

# Validate single patient
result = validator.validate(patient)
print(f"Valid: {result.is_valid}")

if not result.is_valid:
    for message in result.messages:
        print(f"  {message.severity}: {message.text}")
```

### Validation Rules

The validator checks:
- Age-appropriate diagnoses
- Medication conflicts
- Lab value ranges
- Temporal consistency
- Required fields

## Working with Reference Data

PatientSim includes healthcare reference data:

```python
from patientsim.generation import ReferenceData

ref = ReferenceData()

# ICD-10 codes
icd10_codes = ref.get_icd10_codes(category="E11")  # Diabetes
for code in icd10_codes[:5]:
    print(f"{code.code}: {code.description}")

# CPT codes
cpt_codes = ref.get_cpt_codes(category="9921")  # E&M codes

# LOINC codes
loinc_codes = ref.get_loinc_codes(category="glucose")
```

## Complete Example

Here's a full workflow:

```python
"""Complete PatientSim workflow example."""
from patientsim import PatientGenerator
from patientsim.formats.fhir import FHIRExporter
from patientsim.validation import ClinicalValidator

# Setup
gen = PatientGenerator(seed=42)
exporter = FHIRExporter()
validator = ClinicalValidator()

# Generate a cardiac cohort
patients = gen.generate_batch(
    count=5,
    scenario="cardiac",
    age_range=(55, 75)
)

# Validate all patients
print("Validation Results:")
for patient in patients:
    result = validator.validate(patient)
    status = "✓" if result.is_valid else "✗"
    print(f"  {status} {patient.full_name}")

# Export valid patients to FHIR
valid_patients = [p for p in patients if validator.validate(p).is_valid]
bundle = exporter.to_bundle(valid_patients)

# Save
with open("cardiac_cohort.json", "w") as f:
    f.write(bundle.json(indent=2))

print(f"\nExported {len(valid_patients)} patients to cardiac_cohort.json")
```

## Next Steps

- [MemberSim Tutorial](membersim-tutorial.md) - Generate payer data
- [MCP Setup](../interactive/mcp-setup.md) - Use conversationally
- [Module Inventory](../architecture/module-inventory.md) - Explore the codebase
