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

## RxMemberSim Questions

### Generation Questions

Create pharmacy benefit members and test data.

#### Simple Generation
```
"Generate a pharmacy member"
"Create an RxMemberSim member"
"Make a synthetic pharmacy benefit member"
```

#### With BIN/PCN/Group
```
"Generate a member with BIN 610014"
"Create a member with PCN RXTEST and Group GRP001"
"Generate a member for pharmacy network testing"
```

#### With Accumulators
```
"Create a member with $500 deductible"
"Generate a member who has met their deductible"
"Create a member near their OOP max"
```

#### Batch Generation
```
"Generate 50 pharmacy members"
"Create 100 members for PBM testing"
"Generate a population for pharmacy utilization testing"
```

### Formulary Questions

Check drug coverage and tier assignments.

#### Coverage Checks
```
"Is metformin covered?"
"Check coverage for NDC 00169413512"
"What tier is Ozempic on?"
"Is Humira on the formulary?"
```

#### PA Requirements
```
"Which drugs require prior authorization?"
"Does Ozempic need PA?"
"List PA-required GLP-1 medications"
"What step therapy drugs are there?"
```

#### Tier Information
```
"Show me Tier 1 drugs"
"What's the copay for Tier 3?"
"List specialty tier drugs"
"Show formulary tier structure"
```

### DUR Questions

Drug utilization review and interaction checking.

#### Drug Interactions
```
"Check interactions between warfarin and ibuprofen"
"Are there interactions for this medication list?"
"Test drug-drug interaction detection"
"Check DUR for this claim"
```

#### Therapeutic Duplication
```
"Check for duplicate statins"
"Is there therapeutic duplication?"
"Test duplicate therapy detection"
```

#### Other DUR Checks
```
"Check early refill eligibility"
"Test high dose detection"
"Check age-related precautions for elderly patient"
"Test gender contraindication detection"
```

### Prior Authorization Questions

PA workflow testing.

#### PA Requirements
```
"Why was this claim rejected for PA?"
"What are the PA criteria for Ozempic?"
"Submit a PA request for this member"
```

#### PA Decisions
```
"Show me PA approval scenario"
"Test PA denial workflow"
"What information is needed for PA?"
"Test emergency PA auto-approval"
```

#### Appeals
```
"How do PA appeals work?"
"Test the appeals process"
"What's the IRO review process?"
```

### Export Questions

Convert to NCPDP and other formats.

#### NCPDP Formats
```
"Generate an NCPDP B1 claim request"
"Export to NCPDP Telecommunication format"
"Create a claim response message"
```

#### SCRIPT Standard
```
"Generate an NCPDP SCRIPT message"
"Create an electronic prescription"
"Export Rx to SCRIPT format"
```

### Inquiry Questions

Learn about pharmacy benefit capabilities.

```
"What DUR alert types are available?"
"Explain the formulary tier structure"
"What NCPDP transaction codes exist?"
"Show me this member's pharmacy history"
"What reject codes can occur?"
"List common PA rejection reasons"
"What specialty pharmacy features exist?"
```

---

## Combined Questions

Questions that span multiple products or require multiple operations.

```
"Generate 5 cardiac patients and export to FHIR"
"Create a diabetic member with claims and export to 837"
"Generate a cohort, validate it, and export to HL7v2"
"Create members with care gaps and generate outreach list"
"Generate a pharmacy member and process a metformin claim"
"Create a member with claims history and check DUR for new Rx"
"Submit a claim for Ozempic and walk through the PA process"
"Generate 10 pharmacy members and batch test formulary coverage"
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
