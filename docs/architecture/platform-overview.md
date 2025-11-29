# Platform Architecture Overview

A visual guide to how the HealthSim platform is organized across its four repositories.

## The Layered Architecture

HealthSim follows a layered architecture where shared infrastructure lives in a core library, and domain-specific products extend that foundation.

```
┌──────────────────────────────────────────────────────────────────────────────────────────────────┐
│                                    USER-FACING PRODUCTS                                           │
│                                                                                                  │
│   ┌────────────────────────┐  ┌────────────────────────┐  ┌────────────────────────┐            │
│   │       PatientSim       │  │       MemberSim        │  │      RxMemberSim       │            │
│   │    Clinical Domain     │  │      Payer Domain      │  │    Pharmacy Domain     │            │
│   │                        │  │                        │  │                        │            │
│   │  Models:               │  │  Models:               │  │  Models:               │            │
│   │  • Patient             │  │  • Member              │  │  • RxMember            │            │
│   │  • Encounter           │  │  • Subscriber          │  │  • Drug                │            │
│   │  • Diagnosis           │  │  • Claim, ClaimLine    │  │  • PharmacyClaim       │            │
│   │  • Procedure           │  │  • Plan, Provider      │  │  • Formulary           │            │
│   │  • Medication          │  │  • Authorization       │  │  • DUR Alert           │            │
│   │  • Observation         │  │  • QualityMeasure      │  │  • PriorAuth           │            │
│   │                        │  │                        │  │                        │            │
│   │  Formats:              │  │  Formats:              │  │  Formats:              │            │
│   │  • FHIR R4             │  │  • X12 834 (Enroll)    │  │  • NCPDP Telecom (B1/B2)│           │
│   │  • HL7v2 (ADT,ORM,ORU) │  │  • X12 837 (Claims)    │  │  • NCPDP SCRIPT        │            │
│   │  • MIMIC-III           │  │  • X12 835 (Remit)     │  │  • NCPDP ePA           │            │
│   │                        │  │  • X12 270/271 (Elig)  │  │  • JSON/CSV            │            │
│   └───────────┬────────────┘  └───────────┬────────────┘  └───────────┬────────────┘            │
│               │                           │                           │                          │
│               │              All depend on healthsim-core             │                          │
│               └───────────────────────────┼───────────────────────────┘                          │
│                                           │                                                      │
│   ┌──────────────────────────────▼──────────────────────────────────────┐  │
│   │                        HEALTHSIM-CORE                                │  │
│   │                   Shared Foundation Library                          │  │
│   │                                                                      │  │
│   │   ┌──────────┐ ┌──────────┐ ┌──────────┐ ┌────────────┐             │  │
│   │   │  person  │ │ temporal │ │generation│ │ validation │             │  │
│   │   │          │ │          │ │          │ │            │             │  │
│   │   │Demograph-│ │ Timeline │ │ BaseGen  │ │ ValResult  │             │  │
│   │   │ics      │ │ Event    │ │ Weighted │ │ Validator  │             │  │
│   │   │ Address  │ │ Period   │ │ SeedMgr  │ │ Message    │             │  │
│   │   └──────────┘ └──────────┘ └──────────┘ └────────────┘             │  │
│   │                                                                      │  │
│   │   ┌──────────┐ ┌──────────┐ ┌──────────┐                            │  │
│   │   │ formats  │ │  skills  │ │  config  │                            │  │
│   │   │          │ │          │ │          │                            │  │
│   │   │Transformer│ │ Loader   │ │ Settings │                            │  │
│   │   │ JSON     │ │ Schema   │ │ Logging  │                            │  │
│   │   │ CSV      │ │ Composer │ │          │                            │  │
│   │   └──────────┘ └──────────┘ └──────────┘                            │  │
│   │                                                                      │  │
│   └──────────────────────────────────────────────────────────────────────┘  │
└─────────────────────────────────────────────────────────────────────────────┘
```

## Why This Architecture?

### 1. Shared Foundation Prevents Code Duplication

All three products (PatientSim, MemberSim, RxMemberSim) need:
- Person demographics (names, addresses, dates of birth)
- Timeline management (events in sequence)
- Data validation (structural and temporal)
- Output formatting utilities

Without healthsim-core, each product would implement these independently, leading to divergent code and bugs fixed in one place but not the other.

### 2. Consistent Patterns Across Products

When you learn how PatientSim works, you already understand MemberSim because they share the same:
- Model patterns (Pydantic models extending core classes)
- Generator patterns (extending BaseGenerator)
- Validation patterns (extending BaseValidator)
- Export patterns (extending Transformer)

### 3. Easy to Add New Products

RxMemberSim for pharmacy benefits was built quickly by:
1. Depending on healthsim-core
2. Adding domain-specific models (Drug, PharmacyClaim, Formulary)
3. Adding domain-specific formats (NCPDP Telecom, SCRIPT, ePA)
4. Reusing all the infrastructure

### 4. Clear Separation of Concerns

| Layer | Responsibility |
|-------|----------------|
| **healthsim-core** | Generic infrastructure (no healthcare domain concepts) |
| **PatientSim** | Clinical domain (patients, encounters, diagnoses) |
| **MemberSim** | Payer domain (members, claims, eligibility) |
| **RxMemberSim** | Pharmacy domain (prescriptions, PBM claims, formulary) |

## Repository Relationships

### Dependency Direction

```
┌─────────────┐  ┌─────────────┐  ┌──────────────┐
│ PatientSim  │  │  MemberSim  │  │ RxMemberSim  │
└──────┬──────┘  └──────┬──────┘  └──────┬───────┘
       │                │                │
       │        All depend on            │
       └────────────────┼────────────────┘
                        │
                        ▼
              ┌─────────────────┐
              │  healthsim-core │
              └────────┬────────┘
                       │
                       │  depends on
                       ▼
              ┌─────────────────┐
              │ pydantic, faker │
              │   (minimal)     │
              └─────────────────┘
```

### Key Principles

1. **Core has no clinical, payer, or pharmacy concepts**
   - No `Patient`, `Member`, `Diagnosis`, `Claim`, `Drug`
   - Only generic: `Demographics`, `Timeline`, `Period`

2. **Products extend, don't copy**
   - `Patient` uses `Demographics` from core
   - `Member` uses `Demographics` from core
   - `RxMember` uses `Demographics` from core
   - All get identical demographic handling

3. **Products add domain knowledge**
   - PatientSim knows about ICD-10, FHIR, HL7v2
   - MemberSim knows about X12, HIPAA, HEDIS
   - RxMemberSim knows about NCPDP, NDC, DUR rules

## How Products Extend Core

### Example: Person → Patient / Member

```python
# In healthsim-core
class Demographics(BaseModel):
    """Generic person demographics."""
    first_name: str
    last_name: str
    date_of_birth: date
    gender: Literal["M", "F", "U"]
    address: Address

# In PatientSim
class Patient(BaseModel):
    """Clinical patient."""
    patient_id: str
    demographics: Demographics  # Uses core!
    mrn: str
    diagnoses: list[Diagnosis]
    encounters: list[Encounter]

# In MemberSim
class Member(BaseModel):
    """Health plan member."""
    member_id: str
    demographics: Demographics  # Same core class!
    subscriber_id: str
    plan_code: str
    claims: list[Claim]
```

### Example: BaseGenerator → Product Generators

```python
# In healthsim-core
class BaseGenerator:
    """Base for all generators with seed management."""
    def __init__(self, seed: Optional[int] = None):
        self.seed_manager = SeedManager(seed)
        self.fake = Faker()
        if seed:
            self.fake.seed_instance(seed)

# In PatientSim
class PatientGenerator(BaseGenerator):
    """Generate synthetic patients."""
    def generate_patient(self, **params) -> Patient:
        demographics = self._generate_demographics()
        diagnoses = self._generate_diagnoses()
        return Patient(demographics=demographics, ...)

# In MemberSim
class MemberGenerator(BaseGenerator):
    """Generate synthetic members."""
    def generate_member(self, **params) -> Member:
        demographics = self._generate_demographics()
        plan = self._select_plan()
        return Member(demographics=demographics, ...)
```

## Data Flow Example

Here's how data flows through the system when generating a patient:

```
User Request: "Generate a cardiac patient"
                    │
                    ▼
┌─────────────────────────────────────────────────────────────┐
│                      PatientSim                              │
│  ┌─────────────────────────────────────────────────────────┐│
│  │              PatientGenerator                           ││
│  │  1. Load cardiac scenario skill                         ││
│  │  2. Generate demographics (using healthsim-core)        ││
│  │  3. Generate cardiac diagnoses (ICD-10)                 ││
│  │  4. Generate procedures (CPT)                           ││
│  │  5. Generate timeline of events                         ││
│  │  6. Validate clinical plausibility                      ││
│  └───────────────────────────────┬─────────────────────────┘│
│                                  │                          │
│                                  ▼                          │
│  ┌─────────────────────────────────────────────────────────┐│
│  │                    Patient Model                        ││
│  │  • patient_id: "PAT-12345"                             ││
│  │  • demographics: Demographics(...)  ← from core         ││
│  │  • diagnoses: [Diagnosis(code="I21.0", ...)]           ││
│  │  • encounters: [Encounter(...)]                         ││
│  │  • medications: [Medication(...)]                       ││
│  └───────────────────────────────┬─────────────────────────┘│
│                                  │                          │
│                                  ▼                          │
│  ┌─────────────────────────────────────────────────────────┐│
│  │                  FHIRTransformer                        ││
│  │  • Patient → FHIR Patient resource                     ││
│  │  • Diagnosis → FHIR Condition resource                 ││
│  │  • Encounter → FHIR Encounter resource                 ││
│  │  • Bundle everything together                           ││
│  └───────────────────────────────┬─────────────────────────┘│
└──────────────────────────────────┼──────────────────────────┘
                                   │
                                   ▼
                         FHIR R4 Bundle (JSON)
```

## Interactive (MCP) Architecture

When using HealthSim conversationally through Claude:

```
┌─────────────────────────────────────────────────────────────┐
│              Claude Desktop / Claude Code                    │
│                                                             │
│   User: "Generate 5 cardiac patients and export to FHIR"   │
│                          │                                  │
│                          ▼                                  │
│              ┌─────────────────────┐                       │
│              │   MCP Protocol      │                       │
│              └──────────┬──────────┘                       │
└─────────────────────────┼───────────────────────────────────┘
                          │ JSON-RPC over stdio
                          ▼
┌─────────────────────────────────────────────────────────────┐
│                PatientSim MCP Server                         │
│                                                             │
│   Tools:                                                    │
│   • generate_patient(scenario, constraints)                 │
│   • generate_cohort(count, scenario)                        │
│   • export_fhir(patients)                                   │
│   • export_hl7v2(patients, message_type)                   │
│   • validate_patients(patients)                             │
│   • list_scenarios()                                        │
│                                                             │
└─────────────────────────────────────────────────────────────┘
```

## Summary

| Repository | Role | Key Contents |
|------------|------|--------------|
| **healthsim-core** | Foundation | Demographics, Timeline, BaseGenerator, Validation framework |
| **PatientSim** | Clinical Product | Patient, Encounter, Diagnosis; FHIR, HL7v2 exports |
| **MemberSim** | Payer Product | Member, Claim, Plan; X12 EDI exports |
| **RxMemberSim** | Pharmacy Product | RxMember, PharmacyClaim, Formulary, DUR; NCPDP exports |

The architecture ensures:
- **Consistency** - Same patterns across products
- **Efficiency** - Shared code, single maintenance point
- **Extensibility** - Easy to add new products
- **Clarity** - Clear boundaries between domains
