# RxMemberSim Conversation Examples

Examples of using RxMemberSim through Claude Desktop or Claude Code.

## Basic Data Generation

**You:** Create a pharmacy member for testing

**Claude:** I'll generate a pharmacy benefit member:
```
Member ID: RXM-2025-001234
BIN: 610014 | PCN: RXTEST | Group: GRP001
Name: Sarah Johnson
DOB: 1985-03-15 | Gender: F
Effective: 2025-01-01

Accumulators:
  Deductible: $250 ($175 remaining)
  OOP Max: $3,000 ($2,450 remaining)
```

---

## Formulary and Coverage

**You:** Is Jardiance covered on the formulary?

**Claude:** Let me check formulary status for Jardiance (empagliflozin):
```
Drug: Jardiance (empagliflozin) 10mg
NDC: 00597-0151-30
Coverage Status: COVERED

Tier: 3 (Non-Preferred Brand)
Copay: $65

Requirements:
  ⚠️ Prior Authorization: REQUIRED
  ⚠️ Step Therapy: Must try metformin first

Preferred Alternatives (Tier 1-2):
  - Metformin 500mg (Tier 1) - $10 copay
  - Farxiga (dapagliflozin) (Tier 2) - $40 copay
```

---

**You:** What tier is atorvastatin?

**Claude:** Checking formulary for atorvastatin:
```
Drug: Atorvastatin 10mg (generic Lipitor)
NDC: 00071015523
Coverage Status: COVERED

Tier: 1 (Preferred Generic)
Copay: $10

No restrictions - covered without prior auth
```

---

## DUR Alerts

**You:** Check for drug interactions if we add warfarin to a patient taking ibuprofen

**Claude:** Running DUR check for warfarin with current medication ibuprofen:
```
🚨 DUR ALERTS DETECTED

ALERT 1: Drug-Drug Interaction
  Severity: ⚠️ HIGH (Level 1)

  Warfarin + Ibuprofen (NSAID)
  Risk: Increased bleeding risk

  Clinical Details:
  - NSAIDs inhibit platelet function
  - May increase warfarin anticoagulant effect
  - GI bleeding risk significantly elevated

  Recommendation:
  - Consider acetaminophen for pain
  - Monitor INR closely if NSAID required
  - Avoid concurrent use if possible

Override Required: Yes, with clinical justification
```

---

**You:** What about adding metformin to that same patient?

**Claude:** Running DUR check for metformin:
```
✅ DUR CHECK PASSED

No drug interactions detected between:
  - Metformin
  - Warfarin
  - Ibuprofen

Additional checks:
  - Therapeutic duplication: None
  - Age restriction: Pass
  - Gender restriction: Pass

Claim can proceed.
```

---

## Prior Authorization

**You:** Submit a prior auth for Ozempic

**Claude:** Initiating prior authorization for Ozempic:
```
PA REQUEST SUBMITTED

PA Request ID: PA-2025-11-29-0001
Drug: Ozempic (semaglutide) 0.5mg/dose
NDC: 00169413512
Member: RXM-2025-001234
Status: PENDING - Questions Required

Clinical Questions:
1. Primary diagnosis?
   [ ] Type 2 Diabetes (E11.x)
   [ ] Obesity (E66.x)
   [ ] Other: _____

2. Has patient tried metformin ≥90 days?
   [ ] Yes  [ ] No
   If no, reason: _____

3. Current HbA1c value: _____%
   (Must be ≥7.0% for approval)

4. Current BMI: _____

Turnaround Time: 24-72 hours (standard)
Expedited Available: Yes (24 hours for urgent)
```

---

**You:** The patient has type 2 diabetes, tried metformin for 6 months, and HbA1c is 8.2%

**Claude:** Evaluating PA criteria:
```
PA CRITERIA EVALUATION

✅ Diagnosis: Type 2 Diabetes (E11.x) - MET
✅ Step Therapy: Metformin trial >90 days - MET
✅ Lab Result: HbA1c 8.2% (≥7.0% required) - MET

DECISION: AUTO-APPROVED

PA Number: PA-AUTH-2025-567890
Effective: 2025-11-29
Expires: 2026-05-29 (6 months)

Approved Quantity: 1 pen per 28 days
Refills: 5

The pharmacy can now process the claim with this PA number.
```

---

## Scenario Execution

**You:** Run a step therapy scenario for a brand drug

**Claude:** Executing step therapy scenario:
```
SCENARIO: Step Therapy Required

Member: DEMO-001
Target Drug: Nexium (esomeprazole) - Tier 4
Step 1 Required: Omeprazole (generic PPI) - Tier 1

TIMELINE:

Day 0: New Prescription for Nexium
       └─ Claim submitted
       └─ ❌ REJECTED - Code 76 (Plan Limitations)
       └─ Message: Step therapy required - try omeprazole first

Day 1: Prescriber changes to Omeprazole
       └─ Claim submitted
       └─ ✅ APPROVED
       └─ Patient pays: $10 copay

Day 30: Refill Omeprazole
        └─ ✅ APPROVED

Day 60: Refill Omeprazole
        └─ ✅ APPROVED
        └─ Note: Step therapy satisfied after 90 days

Day 90: Prescriber resubmits Nexium
        └─ Step therapy override applied
        └─ ✅ APPROVED
        └─ Patient pays: $80 copay

SCENARIO COMPLETE ✓
Total Events: 5
Duration: 90 days
```

---

## Specialty Pharmacy

**You:** What's involved in starting a patient on Humira?

**Claude:** Specialty onboarding workflow for Humira:
```
SPECIALTY DRUG ONBOARDING

Drug: Humira (adalimumab) 40mg
Category: TNF Inhibitor (Biologic)
Distribution: Specialty Pharmacy Only

STEP 1: Prior Authorization
  Status: REQUIRED
  Criteria:
    - Diagnosis: RA, Psoriasis, or Crohn's
    - Failed methotrexate trial (≥90 days)
    - Prescribed by specialist
  Turnaround: 48-72 hours

STEP 2: Benefits Verification
  - Confirm specialty tier coverage
  - Calculate patient cost share
  - Check copay card eligibility

STEP 3: Hub Enrollment
  Provider: AbbVie Patient Support
  Services:
    - Injection training
    - Nurse educator calls
    - Refill reminders
    - Financial assistance

STEP 4: Copay Assistance
  Manufacturer Card: Up to $6,000/year
  Patient cost after card: ~$5/month

STEP 5: Dispensing
  - Cold chain shipping required
  - Signature required
  - 28-day supply maximum

Estimated Time to First Fill: 5-10 business days
```

---

## Claim Adjudication

**You:** Process a claim for 30 tablets of lisinopril

**Claude:** Processing pharmacy claim:
```
CLAIM ADJUDICATION

Claim ID: CLM-2025-11-29-001
Drug: Lisinopril 10mg (NDC: 00378-0850-01)
Quantity: 30 tablets
Days Supply: 30

ELIGIBILITY CHECK
  ✅ Member active
  ✅ BIN/PCN/Group verified
  ✅ Coverage effective

FORMULARY CHECK
  ✅ Drug covered - Tier 1
  ✅ No PA required
  ✅ No quantity limits exceeded

DUR CHECK
  ✅ No interactions
  ✅ No duplications

PRICING
  Ingredient Cost:    $4.50
  Dispensing Fee:     $2.00
  Total Cost:         $6.50

  Copay (Tier 1):     $10.00
  Deductible Applied: $0.00

  Patient Pays:       $6.50 (cost < copay)
  Plan Pays:          $0.00

RESULT: ✅ APPROVED
Authorization #: AUTH-987654321
```

---

## Tips for Effective Prompts

### Be Specific About Drug Details
- Include drug name, strength, and quantity
- Specify NDC if you have it
- Mention brand vs generic preference

### Include Patient Context
- Current medications for DUR checks
- Diagnosis codes for PA evaluation
- Age and gender for clinical alerts

### Specify Output Format
- "Show me the NCPDP response codes"
- "Format as a claim submission"
- "Generate an ePA transaction"