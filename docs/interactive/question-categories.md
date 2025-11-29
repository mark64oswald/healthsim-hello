# Question Categories

A comprehensive guide to what you can ask Claude when using HealthSim interactively.

## How to Think About Questions

HealthSim-enabled Claude can help with four main activities:

1. **Generate** - Create new synthetic data
2. **Modify** - Change existing data
3. **Export** - Convert to different formats
4. **Inquire** - Ask about capabilities and data

## PatientSim Questions

### Generation Questions

Create new synthetic patients with various characteristics.

#### Simple Generation
```
"Generate a patient"
"Create a test patient"
"Make me a synthetic patient record"
```

#### With Demographics
```
"Generate a 65-year-old female patient"
"Create a male patient between 40 and 50 years old"
"Generate a pediatric patient (under 18)"
"Create an elderly patient over 80"
```

#### With Clinical Conditions
```
"Generate a diabetic patient"
"Create a patient with heart failure"
"Generate a patient with COPD and hypertension"
"Create a patient with multiple chronic conditions"
```

#### Using Scenarios
```
"Generate a cardiac patient"
"Create a patient using the emergency scenario"
"Generate a patient for diabetes management testing"
"Create a surgical patient"
```

#### Cohort Generation
```
"Generate 5 patients for testing"
"Create 10 cardiac patients"
"Generate a cohort of 20 diabetic patients over 50"
"Create 100 patients for load testing"
```

### Modification Questions

Update existing generated patients.

```
"Add diabetes to patient 3"
"Make the first patient older"
"Add a hospitalization to this patient"
"Give patient PAT-12345 a new diagnosis of pneumonia"
"Add medication allergies to this patient"
"Update the patient's lab values"
```

### Export Questions

Convert patients to different healthcare formats.

#### FHIR Export
```
"Export this patient to FHIR"
"Convert these patients to a FHIR Bundle"
"Generate FHIR resources for the cardiac cohort"
"Export patient PAT-12345 as FHIR JSON"
```

#### HL7v2 Export
```
"Generate an ADT message for this patient"
"Create HL7v2 admission messages"
"Export as HL7v2 ADT^A01"
"Generate discharge messages for these patients"
```

#### MIMIC Format
```
"Export to MIMIC-III format"
"Generate MIMIC tables for these patients"
```

### Inquiry Questions

Learn about capabilities and inspect data.

```
"What scenarios are available?"
"Describe the cardiac scenario"
"What conditions can you generate?"
"Show me the diagnoses for patient 2"
"What medications does this patient have?"
"List the encounters for this patient"
"What FHIR resources do you generate?"
```

---

## MemberSim Questions

### Generation Questions

Create new health plan members.

#### Simple Generation
```
"Generate a health plan member"
"Create a member"
"Make a synthetic member record"
```

#### With Plan Details
```
"Create a member enrolled in PPO Gold"
"Generate a member with HMO Basic coverage"
"Create a member in a high-deductible plan"
```

#### With Demographics
```
"Generate a 45-year-old female member"
"Create a member between 30 and 40"
"Generate a Medicare-aged member (65+)"
```

#### With Status
```
"Create an active member"
"Generate a termed member"
"Create a member with pending enrollment"
```

#### Family Generation
```
"Generate a subscriber with 2 dependents"
"Create a family of 4 members"
"Generate a subscriber with spouse and children"
```

#### Batch Generation
```
"Generate 50 members"
"Create 100 members with various plans"
"Generate a population of 500 members"
```

### Claims Questions

Generate and manage claims data.

#### Claim Generation
```
"Generate claims for this member"
"Create 6 months of claims history"
"Generate professional claims for diabetes management"
"Create a denied claim"
"Generate high-cost claims"
```

#### Claim Types
```
"Generate professional claims (837P)"
"Create institutional claims (837I)"
"Generate pharmacy claims"
```

#### Claim Scenarios
```
"Generate claims for a chronic disease patient"
"Create claims showing ER utilization"
"Generate claims with prior authorization"
```

### Export Questions

Convert to EDI and other formats.

#### X12 834 (Enrollment)
```
"Generate an 834 enrollment file"
"Export these members to X12 834"
"Create an enrollment transaction"
"Generate 834 for new enrollees"
```

#### X12 837 (Claims)
```
"Export claims to 837P format"
"Generate X12 837I for institutional claims"
"Create an 837 claims file"
```

#### X12 835 (Remittance)
```
"Generate an 835 remittance advice"
"Create payment file for these claims"
```

#### X12 270/271 (Eligibility)
```
"Generate an eligibility inquiry (270)"
"Create an eligibility response (271)"
```

### Quality/HEDIS Questions

Work with quality measures and care gaps.

```
"Generate HEDIS care gaps for these members"
"Show members missing A1C tests"
"Create quality measure status report"
"Generate care gap outreach list"
"Which members have open care gaps?"
"Show HEDIS compliance rates"
```

### Inquiry Questions

Learn about capabilities and inspect data.

```
"What plans are available?"
"Describe PPO Gold benefits"
"What X12 formats can you generate?"
"Show me this member's claims"
"What's the deductible status?"
"List the accumulators for this member"
"What HEDIS measures do you support?"
```

---

## Combined Questions

Questions that span both products or require multiple operations.

```
"Generate 5 cardiac patients and export to FHIR"
"Create a diabetic member with claims and export to 837"
"Generate a cohort, validate it, and export to HL7v2"
"Create members with care gaps and generate outreach list"
```

---

## Question Patterns That Work Well

### Be Specific
```
✅ "Generate a 65-year-old female with Type 2 diabetes and hypertension"
❌ "Generate a patient" (works, but less targeted)
```

### Use Numbers for Cohorts
```
✅ "Generate 10 cardiac patients"
✅ "Create 5 members with claims"
```

### Reference by ID
```
✅ "Add pneumonia to patient PAT-12345"
✅ "Export member MEM-67890 to 834"
```

### Combine Steps
```
✅ "Generate 5 patients and export to FHIR"
✅ "Create a member, add claims, and export to 837P"
```

### Ask for What You Need
```
✅ "What scenarios are available for cardiac patients?"
✅ "What's included in a FHIR Patient resource?"
```

---

## Questions Claude Can't Answer (Yet)

Some things are outside current capabilities:

| Question Type | Why Not Available |
|---------------|-------------------|
| "Import this FHIR file" | Import not implemented (generation only) |
| "Connect to my EMR" | No real system connections |
| "Use real patient data" | By design - synthetic only |
| "Generate C-CDA" | Format not yet implemented |
| "Create custom code sets" | Uses standard reference data |

For these requests, Claude will explain what's possible and suggest alternatives.
