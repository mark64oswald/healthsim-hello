# Module Inventory

A complete inventory of modules across all four HealthSim repositories.

## healthsim-core Modules

The foundation library provides generic infrastructure with **no clinical or payer concepts**.

### healthsim.person

**Purpose:** Generic person demographics generation

| Class | Description |
|-------|-------------|
| `Demographics` | Core demographic data (name, DOB, gender) |
| `PersonName` | Name components (first, middle, last, suffix) |
| `Address` | Postal address with validation |
| `IdentifierGenerator` | Generate IDs with configurable patterns |
| `IdentifierConfig` | Configuration for ID formats |

**Used by Products:**
- PatientSim: `Patient.demographics`
- MemberSim: `Member.demographics`
- RxMemberSim: `RxMember.demographics`

---

### healthsim.temporal

**Purpose:** Timeline and date management for event sequencing

| Class | Description |
|-------|-------------|
| `Timeline` | Manages sequence of events |
| `Event` | Timestamped occurrence with type |
| `Period` | Date range with start/end |
| `PeriodCollection` | Manage multiple periods (coverage spans) |
| `TemporalValidator` | Validate date consistency |

**Key Functions:**
- `calculate_age(birth_date)` - Age from DOB
- `is_valid_sequence(events)` - Check event ordering
- `find_overlaps(periods)` - Detect overlapping periods

**Used by Products:**
- PatientSim: Encounter timelines, medication durations
- MemberSim: Coverage periods, claim dates

---

### healthsim.generation

**Purpose:** Base generator patterns for synthetic data

| Class | Description |
|-------|-------------|
| `BaseGenerator` | Abstract base with seed management |
| `SeedManager` | Reproducible random state |
| `WeightedChoice` | Weighted random selection |
| `Distribution` | Statistical distributions |

**Used by Products:**
- PatientSim: `PatientGenerator(BaseGenerator)`
- MemberSim: `MemberGenerator(BaseGenerator)`

---

### healthsim.validation

**Purpose:** Validation framework (not domain-specific rules)

| Class | Description |
|-------|-------------|
| `ValidationResult` | Collection of validation messages |
| `ValidationMessage` | Single validation finding |
| `Severity` | ERROR, WARNING, INFO levels |
| `BaseValidator` | Abstract validator class |

**Used by Products:**
- PatientSim: `ClinicalValidator(BaseValidator)`
- MemberSim: `ClaimsValidator(BaseValidator)`

---

### healthsim.formats

**Purpose:** Base transformer classes for output formats

| Class | Description |
|-------|-------------|
| `Transformer` | Abstract base for format transformers |
| `JSONSerializer` | JSON output utilities |
| `CSVWriter` | CSV/delimited file utilities |
| `DateFormatter` | Consistent date formatting |

**Used by Products:**
- PatientSim: `FHIRTransformer(Transformer)`, `HL7v2Builder`
- MemberSim: `X12Generator(Transformer)`

---

### healthsim.skills

**Purpose:** Skill file loading and composition for Claude

| Class | Description |
|-------|-------------|
| `SkillLoader` | Load .md skill files |
| `SkillSchema` | Skill file format specification |
| `SkillComposer` | Combine multiple skills |

**Used by Products:**
- Both products load domain-specific skills for Claude

---

### healthsim.config

**Purpose:** Configuration and logging management

| Class | Description |
|-------|-------------|
| `Settings` | Configuration management |
| `LogConfig` | Structured logging setup |

---

## PatientSim Modules

Domain-specific modules for clinical patient data.

### patientsim.models

**Purpose:** Clinical data models

| Model | Description |
|-------|-------------|
| `Patient` | Core patient with demographics, clinical data |
| `Encounter` | Hospital visit, ED visit, or outpatient |
| `Diagnosis` | ICD-10 coded condition |
| `Procedure` | CPT coded procedure |
| `Medication` | Prescribed/administered medication |
| `Observation` | Lab result, vital sign, or other observation |
| `Allergy` | Drug or environmental allergy |

**Relationships:**
```
Patient
├── demographics: Demographics (from core)
├── diagnoses: list[Diagnosis]
├── encounters: list[Encounter]
│   └── encounter.diagnoses, procedures, observations
├── medications: list[Medication]
└── allergies: list[Allergy]
```

---

### patientsim.generation

**Purpose:** Clinical data generation

| Class | Description |
|-------|-------------|
| `PatientGenerator` | Generate complete patients |
| `ReferenceData` | ICD-10, CPT, LOINC codes |
| `ScenarioLoader` | Load clinical scenario skills |

**Key Methods:**
```python
gen = PatientGenerator(seed=42)
patient = gen.generate_patient()
patient = gen.generate_patient(scenario="cardiac", age_range=(45, 75))
patients = gen.generate_batch(count=10)
```

---

### patientsim.formats.fhir

**Purpose:** FHIR R4 export

| Class | Description |
|-------|-------------|
| `FHIRExporter` | Main exporter class |
| `PatientTransformer` | Patient → FHIR Patient |
| `ConditionTransformer` | Diagnosis → FHIR Condition |
| `EncounterTransformer` | Encounter → FHIR Encounter |
| `ObservationTransformer` | Observation → FHIR Observation |
| `MedicationRequestTransformer` | Medication → FHIR MedicationRequest |

**Output:** FHIR R4 Bundle (JSON)

---

### patientsim.formats.hl7v2

**Purpose:** HL7v2 message generation

| Class | Description |
|-------|-------------|
| `HL7v2Builder` | Main message builder |
| `SegmentBuilder` | Build individual segments |

**Message Types:**
- `ADT^A01` - Admission
- `ADT^A03` - Discharge
- `ADT^A08` - Patient update
- `ORM^O01` - Order message
- `ORU^R01` - Observation result

---

### patientsim.formats.mimic

**Purpose:** MIMIC-III format export for research

| Class | Description |
|-------|-------------|
| `MIMICExporter` | Export to MIMIC table structure |

**Output Tables:**
- PATIENTS
- ADMISSIONS
- DIAGNOSES_ICD
- PROCEDURES_ICD
- LABEVENTS
- PRESCRIPTIONS

---

### patientsim.validation

**Purpose:** Clinical validation rules

| Class | Description |
|-------|-------------|
| `ClinicalValidator` | Validate clinical plausibility |

**Validation Rules:**
- Age-appropriate diagnoses
- Medication conflict detection
- Lab value ranges
- Temporal consistency

---

### patientsim.mcp

**Purpose:** MCP servers for Claude integration

| Server | Tools |
|--------|-------|
| `generation_server` | generate_patient, generate_cohort, list_scenarios |
| `export_server` | export_fhir, export_hl7v2, export_mimic |
| `validation_server` | validate_patients, validate_for_export |

---

## MemberSim Modules

Domain-specific modules for payer/claims data.

### membersim.core

**Purpose:** Core member and plan models

| Model | Description |
|-------|-------------|
| `Member` | Health plan member |
| `Subscriber` | Primary subscriber (member may be dependent) |
| `Dependent` | Family member on subscriber's plan |
| `Plan` | Health plan configuration |
| `Provider` | Healthcare provider (NPI, taxonomy) |
| `Accumulator` | Deductible/OOP tracking |

**Relationships:**
```
Subscriber
├── demographics: Demographics (from core)
├── plan: Plan
├── dependents: list[Member]
└── accumulators: dict[str, Accumulator]

Member
├── demographics: Demographics (from core)
├── subscriber_id: str (reference to subscriber)
├── plan_code: str
└── claims: list[Claim]
```

---

### membersim.claims

**Purpose:** Claims processing models

| Model | Description |
|-------|-------------|
| `Claim` | Healthcare claim header |
| `ClaimLine` | Individual service line |
| `Payment` | Claim payment/adjudication |
| `ClaimStatus` | PENDING, PAID, DENIED, etc. |

**Claim Types:**
- Professional (837P) - Physician services
- Institutional (837I) - Hospital services

---

### membersim.quality

**Purpose:** Quality measures and care gaps

| Model | Description |
|-------|-------------|
| `QualityMeasure` | HEDIS measure definition |
| `MeasureStatus` | Member's status for a measure |
| `CareGap` | Open care gap for outreach |

**HEDIS Measures Supported:**
- Diabetes: A1C testing, eye exams, kidney screening
- Cardiovascular: Statin therapy, blood pressure
- Preventive: Cancer screenings, immunizations

---

### membersim.authorization

**Purpose:** Prior authorization workflows

| Model | Description |
|-------|-------------|
| `Authorization` | Prior auth request |
| `AuthStatus` | PENDING, APPROVED, DENIED, MODIFIED |
| `AuthDecision` | Authorization decision details |

---

### membersim.network

**Purpose:** Provider network management

| Model | Description |
|-------|-------------|
| `ProviderContract` | Provider participation agreement |
| `FeeSchedule` | Contracted fee schedule |
| `NetworkStatus` | IN_NETWORK, OUT_OF_NETWORK |

---

### membersim.formats.x12

**Purpose:** X12 EDI transaction generation

| Generator | Transaction | Description |
|-----------|-------------|-------------|
| `Generate834` | 834 | Benefit Enrollment |
| `Generate837P` | 837P | Professional Claims |
| `Generate837I` | 837I | Institutional Claims |
| `Generate835` | 835 | Claim Payment/Remittance |
| `Generate270` | 270 | Eligibility Inquiry |
| `Generate271` | 271 | Eligibility Response |
| `Generate278` | 278 | Prior Authorization |

---

### membersim.mcp

**Purpose:** MCP servers for Claude integration

| Server | Tools |
|--------|-------|
| `member_server` | generate_member, generate_batch, list_plans |
| `claims_server` | generate_claims, adjudicate_claim |
| `export_server` | export_834, export_837, export_835 |
| `quality_server` | generate_care_gaps, measure_status |

---

## RxMemberSim Modules

Domain-specific modules for pharmacy benefit management (PBM) data.

### rxmembersim.core

**Purpose:** Core pharmacy member and drug models

| Model | Description |
|-------|-------------|
| `RxMember` | Pharmacy benefit member with BIN/PCN/Group |
| `Drug` | Drug information with NDC, GPI |
| `Accumulator` | Deductible/OOP/MOOP tracking |

**Relationships:**
```
RxMember
├── demographics: Demographics (from core)
├── member_id: str
├── bin: str (BIN number)
├── pcn: str (Processor Control Number)
├── group_number: str
├── cardholder_id: str
├── person_code: str
└── accumulators: dict[str, Accumulator]
```

---

### rxmembersim.claims

**Purpose:** Pharmacy claims processing

| Model | Description |
|-------|-------------|
| `PharmacyClaim` | NCPDP B1/B2 claim transaction |
| `ClaimResponse` | Adjudication response with pricing |
| `TransactionCode` | BILLING, REVERSAL, REBILL |
| `ResponseStatus` | PAID, REJECTED, DUPLICATE |

**Key Methods:**
```python
from rxmembersim.claims.claim import PharmacyClaim, TransactionCode
from rxmembersim.claims.adjudication import AdjudicationEngine

claim = PharmacyClaim(
    ndc="00071015523",
    quantity_dispensed=Decimal("30"),
    days_supply=30,
    ...
)
engine = AdjudicationEngine(formulary=formulary)
response = engine.adjudicate(claim, member)
```

---

### rxmembersim.formulary

**Purpose:** Formulary management and drug coverage

| Model | Description |
|-------|-------------|
| `Formulary` | Complete formulary with tier structure |
| `FormularyEntry` | Drug coverage details |
| `CoverageStatus` | Coverage check result |
| `TierDefinition` | Tier cost-sharing rules |
| `StepTherapy` | Step therapy requirements |
| `QuantityLimit` | Quantity/days supply limits |

**Tier Structures:**
- Tier 1: Preferred generics (lowest copay)
- Tier 2: Non-preferred generics
- Tier 3: Preferred brands
- Tier 4: Non-preferred brands
- Tier 5: Specialty drugs (highest copay)

---

### rxmembersim.dur

**Purpose:** Drug Utilization Review (DUR) screening

| Model | Description |
|-------|-------------|
| `DURValidator` | Execute DUR checks |
| `DURAlert` | Alert with severity and message |
| `DURAlertType` | INTERACTION, DUPLICATE, EARLY_REFILL, etc. |
| `DURResult` | Collection of alerts |

**DUR Alert Types:**
- Drug-drug interactions
- Therapeutic duplication
- Early refill detection
- Maximum dose exceeded
- Age/gender appropriateness
- Allergy contraindications

---

### rxmembersim.authorization

**Purpose:** Prior authorization and ePA workflows

| Model | Description |
|-------|-------------|
| `PARequest` | Prior authorization request |
| `PAResponse` | Authorization decision |
| `PAStatus` | PENDING, APPROVED, DENIED, PARTIAL |
| `PAWorkflow` | End-to-end PA processing |

**ePA Support:**
- NCPDP ePA transaction generation
- Question set handling
- Auto-approval for emergencies
- Appeal processing

---

### rxmembersim.specialty

**Purpose:** Specialty pharmacy workflows

| Model | Description |
|-------|-------------|
| `HubEnrollment` | Specialty hub enrollment |
| `REMSProgram` | REMS compliance tracking |
| `CopayAssistance` | Copay card/assistance programs |
| `ColdChain` | Temperature-sensitive handling |

---

### rxmembersim.pricing

**Purpose:** Pharmacy pricing and rebates

| Model | Description |
|-------|-------------|
| `DrugPricing` | AWP, WAC, MAC pricing |
| `RebateCalculation` | Manufacturer rebate logic |
| `SpreadPricing` | Plan/PBM spread calculations |
| `CopayCard` | Manufacturer copay assistance |

---

### rxmembersim.scenarios

**Purpose:** Pre-built test scenarios

| Scenario | Description |
|----------|-------------|
| `new_therapy_approved` | New Rx fills successfully |
| `step_therapy_required` | Step therapy enforcement |
| `prior_auth_flow` | PA request to approval |
| `specialty_onboarding` | Specialty hub enrollment |
| `early_refill_reject` | Refill too soon rejection |
| `drug_interaction_alert` | DUR interaction warning |

---

### rxmembersim.formats.ncpdp

**Purpose:** NCPDP standard format generation

| Generator | Format | Description |
|-----------|--------|-------------|
| `TelecomBuilder` | B1/B2 | Pharmacy claim transactions |
| `SCRIPTBuilder` | SCRIPT | NewRx, RxChange, CancelRx |
| `ePABuilder` | ePA | Electronic prior authorization |

**NCPDP Versions:**
- Telecommunication D.0 (B1/B2)
- SCRIPT 2017071
- ePA 2019

---

### rxmembersim.mcp

**Purpose:** MCP server for Claude integration

| Tool | Description |
|------|-------------|
| `generate_rx_member` | Create pharmacy member with BIN/PCN |
| `check_formulary` | Look up drug coverage and tier |
| `check_dur` | Execute DUR screening |
| `submit_prior_auth` | Submit PA request |
| `run_rx_scenario` | Execute pre-built scenario |
| `list_scenarios` | List available scenarios |

---

## Cross-Reference: How Products Use Core

| Core Module | PatientSim Usage | MemberSim Usage | RxMemberSim Usage |
|-------------|------------------|-----------------|-------------------|
| `person.Demographics` | `Patient.demographics` | `Member.demographics` | `RxMember.demographics` |
| `person.Address` | Patient address | Member address | Member address |
| `person.IdentifierGenerator` | MRN generation | Member ID generation | Cardholder ID generation |
| `temporal.Timeline` | Encounter timelines | Claim timelines | Prescription timelines |
| `temporal.Period` | Admission periods | Coverage periods | Benefit periods |
| `generation.BaseGenerator` | `PatientGenerator` | `MemberGenerator` | `RxMemberGenerator` |
| `generation.WeightedChoice` | Diagnosis selection | Plan selection | Drug selection |
| `generation.SeedManager` | Reproducible patients | Reproducible members | Reproducible Rx members |
| `validation.ValidationResult` | Clinical validation | Claims validation | DUR validation |
| `validation.BaseValidator` | `ClinicalValidator` | `ClaimsValidator` | `DURValidator` |
| `formats.Transformer` | `FHIRTransformer` | `X12Generator` | `NCPDPBuilder` |
| `formats.JSONSerializer` | FHIR Bundle output | JSON exports | JSON exports |
| `skills.SkillLoader` | Clinical scenarios | Payer scenarios | Pharmacy scenarios |
| `config.Settings` | Configuration | Configuration | Configuration |

---

## Quick Reference: Finding Things

| If you need... | Look in... |
|----------------|------------|
| Demographics, addresses | `healthsim.person` |
| Date/time handling | `healthsim.temporal` |
| Random generation utilities | `healthsim.generation` |
| Validation framework | `healthsim.validation` |
| Patient models | `patientsim.models` |
| FHIR export | `patientsim.formats.fhir` |
| HL7v2 messages | `patientsim.formats.hl7v2` |
| Member models | `membersim.core` |
| Medical claims | `membersim.claims` |
| X12 EDI | `membersim.formats.x12` |
| HEDIS/quality | `membersim.quality` |
| Rx member models | `rxmembersim.core` |
| Pharmacy claims | `rxmembersim.claims` |
| Formulary/tiers | `rxmembersim.formulary` |
| DUR screening | `rxmembersim.dur` |
| NCPDP formats | `rxmembersim.formats.ncpdp` |
| Pharmacy scenarios | `rxmembersim.scenarios` |
