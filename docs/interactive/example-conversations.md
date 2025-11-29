# Example Conversations

Realistic examples of using HealthSim interactively through Claude.

These conversations demonstrate the "Configuration as Conversation" experience - describing what you need in natural language instead of writing code.

---

## PatientSim Conversations

### Example 1: Simple Patient Generation

A basic interaction to generate a single patient.

```
👤 User: Generate a diabetic patient for testing

🤖 Claude: I'll create a synthetic diabetic patient for you.

Generated Patient:
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
• Patient ID: PAT-58d9a3f2
• Name: Robert Martinez
• Age: 58 (Male)
• MRN: MRN-00847293

Diagnoses:
• E11.9 - Type 2 diabetes mellitus without complications
• I10 - Essential hypertension
• E78.5 - Hyperlipidemia, unspecified

Medications:
• Metformin 1000mg - twice daily
• Lisinopril 10mg - once daily
• Atorvastatin 20mg - once daily at bedtime

Recent Labs (2024-09-15):
• HbA1c: 7.8%
• Fasting Glucose: 142 mg/dL
• Creatinine: 1.1 mg/dL
• eGFR: 72 mL/min
• LDL Cholesterol: 118 mg/dL
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

Would you like me to:
• Add complications or additional conditions?
• Generate more patients like this?
• Export to FHIR or HL7v2 format?
```

---

### Example 2: Generating a Clinical Cohort

Creating multiple patients for a specific use case.

```
👤 User: I need 5 cardiac patients for testing our new cath lab module

🤖 Claude: I'll generate 5 cardiac patients suitable for catheterization lab 
testing. These will include relevant diagnoses, procedures, and cardiac labs.

Generated Cardiac Cohort (5 patients):
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

1. James Wilson, 67M (PAT-001a2b3c)
   • Dx: STEMI (I21.0), s/p PCI with drug-eluting stent
   • Labs: Troponin 4.2 ng/mL (peak), BNP 342 pg/mL
   • Procedure: 92928 (PCI with stent)

2. Patricia Brown, 72F (PAT-002d4e5f)
   • Dx: Unstable angina (I20.0), triple vessel CAD
   • Labs: Troponin 0.08 ng/mL, BNP 198 pg/mL
   • Status: Scheduled for diagnostic cath

3. Michael Chen, 55M (PAT-003g6h7i)
   • Dx: NSTEMI (I21.4), known diabetic
   • Labs: Troponin 1.8 ng/mL, HbA1c 8.2%
   • Procedure: 93458 (L heart cath)

4. Barbara Thompson, 64F (PAT-004j8k9l)
   • Dx: Chest pain (R07.9), abnormal stress test
   • Labs: Troponin <0.01 ng/mL (negative)
   • Status: Cath pending for evaluation

5. William Davis, 71M (PAT-005m0n1o)
   • Dx: Stable angina (I25.1), LAD 80% stenosis
   • Labs: Troponin negative, LDL 142 mg/dL
   • Status: Medical management, possible PCI

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

All patients include:
✓ Cardiac-specific ICD-10 codes
✓ Appropriate CPT procedure codes
✓ Cardiac biomarkers (Troponin, BNP)
✓ ECG findings
✓ Relevant cardiac medications

Would you like me to:
• Add specific complications to any patient?
• Export these to FHIR Bundle?
• Generate HL7v2 ADT messages for admissions?
```

---

### Example 3: Modifying and Exporting

Building on previous generation with modifications and export.

```
👤 User: Make patient 4 have a complication - contrast-induced nephropathy 
after her cath

🤖 Claude: I've added contrast-induced nephropathy to Barbara Thompson's 
record, reflecting a post-catheterization complication.

Updated: Barbara Thompson (PAT-004j8k9l)
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

Added Complication:
• N14.1 - Nephropathy induced by other drugs, medicaments and 
          biological substances (Contrast-induced nephropathy)
• Onset: Day 2 post-cardiac catheterization

Clinical Updates:
• Creatinine: 1.1 → 2.4 mg/dL (rise within 48 hours post-cath)
• eGFR: 68 → 32 mL/min
• Urine output: Decreased
• Added IV fluid hydration protocol
• Nephrology consult ordered
• Hold on Metformin (if applicable)
• Extended hospital stay: 3 days → 6 days

New Orders:
• Serial creatinine monitoring q12h
• Strict I/O monitoring
• Hold contrast for future studies

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

This is now a more complex case suitable for testing:
• Complication recognition
• Nephrology integration
• Length of stay calculations
• Medication interaction alerts

Would you like me to export these patients now?

👤 User: Yes, export to FHIR please

🤖 Claude: Exported all 5 cardiac patients to FHIR R4 Bundle.

FHIR Bundle Summary:
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
Bundle ID: bundle-cardiac-cohort-20241127
Type: collection

Resources Included:
• 5 Patient resources
• 12 Condition resources
• 8 Procedure resources
• 23 Observation resources (labs, vitals)
• 5 Encounter resources
• 15 MedicationRequest resources

Total: 68 FHIR resources
File size: 142 KB
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

📎 Download: cardiac-cohort-fhir.json

The bundle is valid FHIR R4 and ready for import into your test system.
```

---

## MemberSim Conversations

### Example 4: Simple Member Generation

Creating a basic health plan member.

```
👤 User: Create a member enrolled in a PPO plan

🤖 Claude: I'll create a synthetic health plan member with PPO coverage.

Generated Member:
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
• Member ID: MEM-00294857
• Name: Jennifer Adams
• Age: 42 (Female)
• SSN: XXX-XX-4521 (masked)

Coverage Details:
• Plan: PPO Gold
• Group: GRP-ACME-001 (ACME Corporation)
• Effective Date: 2024-01-01
• Status: Active
• Relationship: Self (Subscriber)

Benefits Summary:
┌────────────────────────────────────────┐
│ Individual Deductible:    $500        │
│ Family Deductible:        $1,000      │
│ Individual OOP Max:       $3,000      │
│ Family OOP Max:           $6,000      │
│ PCP Copay:               $25         │
│ Specialist Copay:         $50         │
│ ER Copay:                $150        │
│ Coinsurance:             80/20       │
└────────────────────────────────────────┘

Accumulators (Year-to-Date):
• Deductible Met: $325 of $500 (65%)
• Out-of-Pocket: $425 of $3,000 (14%)

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

Would you like me to:
• Add dependents to this subscriber?
• Generate claims history?
• Create enrollment file (X12 834)?
```

---

### Example 5: Member with Claims History

Creating a member with chronic condition management claims.

```
👤 User: Generate a member with diabetes who has 6 months of claims

🤖 Claude: I'll create a diabetic member with a realistic claims pattern 
showing chronic disease management.

Generated Member with Claims:
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
• Member ID: MEM-00384756
• Name: Sarah Mitchell
• Age: 52 (Female)
• Plan: PPO Gold

Primary Diagnosis: E11.65 - Type 2 DM with hyperglycemia

Claims History (January - June 2024):
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

1. CLM-001 | 2024-01-15 | Office Visit - Endocrinology
   • 99214 - Established patient, moderate complexity
   • Provider: Dr. Robert Kim, NPI 1234567890
   ┌─────────────────────────────────────────────────┐
   │ Billed: $185.00  Allowed: $142.00              │
   │ Plan Paid: $113.60  Member Resp: $28.40        │
   └─────────────────────────────────────────────────┘

2. CLM-002 | 2024-01-15 | Lab Work
   • 83036 - Hemoglobin A1c
   • 80053 - Comprehensive metabolic panel
   ┌─────────────────────────────────────────────────┐
   │ Billed: $245.00  Allowed: $89.00               │
   │ Plan Paid: $71.20  Member Resp: $17.80         │
   └─────────────────────────────────────────────────┘

3. CLM-003 | 2024-04-10 | Office Visit - Follow-up
   • 99213 - Established patient, low complexity
   ┌─────────────────────────────────────────────────┐
   │ Billed: $125.00  Allowed: $98.00               │
   │ Plan Paid: $78.40  Member Resp: $19.60         │
   └─────────────────────────────────────────────────┘

4. CLM-004 | 2024-04-10 | Lab Work
   • 83036 - Hemoglobin A1c (quarterly)
   ┌─────────────────────────────────────────────────┐
   │ Billed: $85.00  Allowed: $42.00                │
   │ Plan Paid: $33.60  Member Resp: $8.40          │
   └─────────────────────────────────────────────────┘

5. CLM-005 | 2024-05-20 | Pharmacy
   • Metformin 1000mg #180
   ┌─────────────────────────────────────────────────┐
   │ Billed: $45.00  Copay: $10.00                  │
   └─────────────────────────────────────────────────┘

6. CLM-006 | 2024-06-15 | Eye Exam (Diabetic)
   • 92014 - Ophthalmologic exam, comprehensive
   ┌─────────────────────────────────────────────────┐
   │ Billed: $175.00  Allowed: $125.00              │
   │ Plan Paid: $100.00  Member Resp: $25.00        │
   └─────────────────────────────────────────────────┘

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
Summary:
• Total Claims: 6
• Total Billed: $860.00
• Total Allowed: $496.00
• Total Plan Paid: $396.80
• Total Member Responsibility: $109.20

Accumulator Status:
• Deductible: $500 of $500 ✓ MET
• Out-of-Pocket: $109.20 of $3,000

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

Would you like me to:
• Generate X12 837P for these claims?
• Add more claims or a denied claim?
• Generate care gap analysis?
```

---

### Example 6: X12 EDI Generation

Generating enrollment and claims files.

```
👤 User: Generate an 834 enrollment file for 10 new members

🤖 Claude: I'll generate 10 new members and create an X12 834 enrollment 
transaction file.

Generated Members:
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
1. Thomas Anderson - PPO Gold (Self)
2. Maria Garcia - PPO Gold (Self + Spouse + 2 children)
3. David Kim - HMO Basic (Self)
4. Jennifer Williams - PPO Silver (Self + Spouse)
5. Robert Johnson - PPO Gold (Self)
6. Emily Brown - HMO Basic (Self + 1 child)
7. Michael Lee - PPO Gold (Self)
8. Sarah Davis - PPO Silver (Self)
9. James Wilson - HMO Basic (Self + Spouse)
10. Lisa Chen - PPO Gold (Self)

Total covered lives: 18 (10 subscribers + 8 dependents)

X12 834 Enrollment File:
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

ISA*00*          *00*          *ZZ*MEMBERSIM      *ZZ*RECEIVER       *241127*1430*^*00501*000000001*0*P*:~
GS*BE*MEMBERSIM*RECEIVER*20241127*1430*1*X*005010X220A1~
ST*834*0001*005010X220A1~
BGN*00*ENROLL001*20241127*143000****2~
DTP*007*D8*20241127~
N1*P5*HEALTHSIM INSURANCE*FI*123456789~
N1*IN*MEMBERSIM*94*MEMSIM001~
INS*Y*18*021*XN*A*E**FT~
REF*0F*MEM-00001~
REF*1L*GRP-ACME-001~
NM1*IL*1*ANDERSON*THOMAS****34*123456789~
...

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

File Statistics:
• Transaction Set: 834 (Benefit Enrollment and Maintenance)
• Version: 005010X220A1
• Members: 10 subscribers
• Covered Lives: 18 total
• Maintenance Type: 021 (Addition)
• Segment Count: 312
• File Size: 18.4 KB

📎 Download: enrollment_20241127.834

The file follows HIPAA X12 834 standards and is ready for 
testing enrollment processing.

Would you like me to also generate:
• 820 Premium Payment for these members?
• 837P claims file?
```

---

### Example 7: Quality/HEDIS Care Gaps

Working with quality measures and care gaps.

```
👤 User: Generate care gaps for diabetic members

🤖 Claude: I'll create a set of diabetic members with realistic HEDIS care 
gaps for outreach and quality improvement testing.

Generated Members with Care Gaps:
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

Member Population: 25 diabetic members
Gap Rate: ~40% (realistic distribution)

Care Gap Summary by Measure:
┌────────────────────────────────────────────────────────────┐
│ Measure          │ Compliant │ Gap │ Rate │ Star Impact  │
├────────────────────────────────────────────────────────────┤
│ HbA1c Testing    │    18     │  7  │ 72%  │ ⭐⭐⭐       │
│ Eye Exam         │    15     │ 10  │ 60%  │ ⭐⭐⭐       │
│ Kidney Screening │    12     │ 13  │ 48%  │ ⭐⭐         │
│ Statin Therapy   │    20     │  5  │ 80%  │ ⭐⭐⭐⭐     │
│ BP Control       │    16     │  9  │ 64%  │ ⭐⭐⭐       │
└────────────────────────────────────────────────────────────┘

Members with Open Gaps (Sample):
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

1. John Martinez (MEM-001234)
   • Age: 58  Plan: PPO Gold
   • Open Gaps: Eye Exam, Kidney Screening
   • Last HbA1c: 7.8% (2024-03-15)
   • Outreach Priority: HIGH

2. Patricia Williams (MEM-002345)
   • Age: 67  Plan: HMO Basic
   • Open Gaps: HbA1c Testing (overdue 4 months)
   • Last Visit: 2024-02-20
   • Outreach Priority: CRITICAL

3. David Chen (MEM-003456)
   • Age: 52  Plan: PPO Silver
   • Open Gaps: Kidney Screening, Statin Therapy
   • Risk Score: 1.4
   • Outreach Priority: MEDIUM

4. Maria Johnson (MEM-004567)
   • Age: 71  Plan: PPO Gold
   • Open Gaps: Eye Exam
   • Comorbidities: HTN, CKD Stage 3
   • Outreach Priority: HIGH

[... 6 more members with gaps ...]

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

Outreach Recommendations:
• CRITICAL (2 members): Missing HbA1c >3 months
• HIGH (5 members): Missing eye exam or multiple gaps
• MEDIUM (3 members): Single gap, recent activity

📎 Download: care_gaps_report.csv
📎 Download: outreach_list.csv

Would you like me to:
• Generate detailed member profiles?
• Create predicted closure rates?
• Export to specific quality reporting format?
```

---

## RxMemberSim Conversations

### Example 8: Pharmacy Member and Claim Processing

Creating a pharmacy member and processing a basic claim.

```
👤 User: Generate a pharmacy member and process a claim for metformin

🤖 Claude: I'll create a pharmacy benefit member and process a claim for metformin.

Generated Pharmacy Member:
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
• Member ID: MEM-7f8a9b12
• Cardholder ID: CH-7f8a9b12
• Name: John Smith
• Age: 55 (Male)
• DOB: 1969-03-15

Pharmacy Identifiers:
┌────────────────────────────────────────┐
│ BIN:           610014                  │
│ PCN:           RXTEST                  │
│ Group:         GRP001                  │
│ Person Code:   01 (Subscriber)         │
└────────────────────────────────────────┘

Accumulators (Year-to-Date):
• Deductible: $0 of $500 (0%)
• Out-of-Pocket: $0 of $3,000 (0%)

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

Now processing metformin claim...

Formulary Check (NDC 00093017101 - Metformin 500mg):
┌────────────────────────────────────────┐
│ Covered:          Yes                  │
│ Tier:             1 (Preferred Generic)│
│ Copay:            $10.00               │
│ Requires PA:      No                   │
│ Step Therapy:     No                   │
│ Quantity Limit:   180/30 days          │
└────────────────────────────────────────┘

Claim Adjudication Result:
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
• Claim ID: CLM-001
• Status: P (Paid) ✓
• Authorization: AUTH-001234

Financial Summary:
┌────────────────────────────────────────┐
│ Drug Cost:        $10.00               │
│ Dispensing Fee:   $2.00                │
│ Plan Pays:        $2.00                │
│ Patient Pays:     $10.00 (copay)       │
│ Deductible:       $0.00 (waived)       │
└────────────────────────────────────────┘
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

The claim was approved. Generic drugs on Tier 1 bypass the
deductible and apply only the $10 copay.

Would you like me to:
• Process another claim for this member?
• Check coverage for a different drug?
• Test a DUR scenario with drug interactions?
```

---

### Example 9: Formulary Check and DUR Screening

Checking coverage and testing drug interactions.

```
👤 User: Check if Ozempic is covered, then test what happens with a
warfarin and ibuprofen interaction

🤖 Claude: I'll check Ozempic coverage and then demonstrate DUR
screening for the warfarin/ibuprofen interaction.

Formulary Check (NDC 00169413512 - Ozempic 0.5mg):
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

Coverage Status:
┌────────────────────────────────────────┐
│ Covered:          Yes                  │
│ Tier:             5 (Specialty)        │
│ Cost Share:       25% coinsurance      │
│ Requires PA:      Yes ⚠️               │
│ Step Therapy:     Yes ⚠️               │
│ Specialty Rx:     Required             │
└────────────────────────────────────────┘

PA Criteria for GLP-1 Agonists:
• Diagnosis: Type 2 Diabetes (E11.*)
• A1c >= 7.0% documented within 90 days
• Failed metformin trial (minimum 3 months)
• No history of pancreatitis

⚠️ Claims for Ozempic will reject with code 75 (PA Required)
until prior authorization is obtained.

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

Now testing DUR for Warfarin + Ibuprofen...

DUR Screening Result:
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

Current Medications:
• Ibuprofen 200mg (NSAID)

Proposed Drug:
• Warfarin 5mg (Anticoagulant)

⚠️ DRUG-DRUG INTERACTION DETECTED

┌────────────────────────────────────────────────────┐
│ Alert Type:    DD (Drug-Drug Interaction)          │
│ Severity:      Level 2 (Serious)                   │
│ Override:      Allowed with intervention code      │
│                                                    │
│ Clinical Message:                                  │
│ Concurrent use of warfarin and NSAIDs increases    │
│ risk of GI bleeding. Consider alternative for      │
│ pain management (e.g., acetaminophen).             │
│                                                    │
│ Recommendations:                                   │
│ • Monitor for signs of bleeding                    │
│ • Consider GI prophylaxis (PPI)                    │
│ • Use lowest effective NSAID dose                  │
│ • Alternative: Acetaminophen for pain              │
└────────────────────────────────────────────────────┘

DUR Response Codes:
• DUR Passed: No
• Alert Count: 1
• Reject Code: 88 (DUR Reject)

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

The claim would soft-reject pending pharmacist review. The
pharmacist can override with an intervention code documenting
they counseled the patient.

Would you like me to:
• Test other drug interactions?
• Show how to override with intervention code?
• Test therapeutic duplication (e.g., two statins)?
```

---

### Example 10: Prior Authorization Workflow

Walking through the PA request and approval process.

```
👤 User: Submit a claim for Ozempic and show me the PA workflow

🤖 Claude: I'll submit an Ozempic claim and walk through the
complete prior authorization workflow.

Step 1: Initial Claim Submission (No PA)
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

Submitting claim for Ozempic 0.5mg...

Adjudication Result:
┌────────────────────────────────────────────────────┐
│ Status:          R (Rejected) ❌                   │
│ Reject Code:     75                                │
│ Message:         Prior Authorization Required      │
│ Additional:      GLP-1 agonist requires PA         │
└────────────────────────────────────────────────────┘

Pharmacy must now initiate PA request.

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

Step 2: PA Request Submission
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

Creating PA request with clinical documentation...

PA Request Details:
┌────────────────────────────────────────────────────┐
│ PA Request ID:   PA-2024-001234                    │
│ Member ID:       MEM-7f8a9b12                      │
│ Drug:            Ozempic 0.5mg (00169413512)       │
│ Prescriber:      Dr. Sarah Johnson                 │
│ NPI:             1234567890                        │
│ Urgency:         Standard (72-hour review)         │
└────────────────────────────────────────────────────┘

Clinical Documentation Submitted:
• Diagnosis: E11.9 (Type 2 Diabetes)
• A1c: 8.2% (documented 2024-01-10)
• Metformin trial: 2000mg/day for 6 months
• Notes: Failed to achieve glycemic control on
  metformin monotherapy

Criteria Assessment:
┌────────────────────────────────────────────────────┐
│ Criteria              │ Required │ Met │ Status   │
├────────────────────────────────────────────────────┤
│ T2DM Diagnosis        │    ✓     │  ✓  │ PASS    │
│ A1c >= 7%             │    ✓     │  ✓  │ PASS    │
│ Metformin Trial       │    ✓     │  ✓  │ PASS    │
│ No Exclusions         │    ✓     │  ✓  │ PASS    │
└────────────────────────────────────────────────────┘

All criteria met - recommending approval.

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

Step 3: PA Decision
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

PA Decision: APPROVED ✓

┌────────────────────────────────────────────────────┐
│ PA Number:       AUTH-2024-56789                   │
│ Effective:       2024-01-15                        │
│ Expires:         2024-07-15 (6 months)             │
│ Approved Qty:    1 pen per 28 days                 │
│ Refills:         5                                 │
│ Renewal Note:    Updated A1c required for renewal  │
└────────────────────────────────────────────────────┘

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

Step 4: Resubmit Claim with PA
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

Resubmitting claim with PA number...

Adjudication Result:
┌────────────────────────────────────────────────────┐
│ Status:          P (Paid) ✓                        │
│ Authorization:   AUTH-2024-56789                   │
│ Drug Cost:       $850.00                           │
│ Plan Pays:       $637.50                           │
│ Patient Pays:    $212.50 (25% coinsurance)         │
└────────────────────────────────────────────────────┘

Claim approved with PA authorization. The member pays 25%
coinsurance ($212.50) for this specialty medication.

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

💡 Tip: Many specialty drugs have copay assistance programs.
Humira Complete, for example, can reduce patient cost to $5/month
for commercial insurance members.

Would you like me to:
• Show a PA denial scenario?
• Test the appeals process?
• Generate batch PA requests?
```

---

## Tips for Effective Conversations

### 1. Be Specific When You Can

```
❌ "Generate a patient"
✅ "Generate a 65-year-old female with COPD and heart failure"
```

### 2. Build Iteratively

Start simple, then refine:
```
"Generate a cardiac patient"
→ "Add diabetes as a comorbidity"
→ "Add a recent hospitalization"
→ "Export to FHIR"
```

### 3. Use IDs for Follow-up

Reference patient/member IDs when modifying:
```
"Add pneumonia to PAT-58d9a3f2"
"Generate claims for MEM-00294857"
```

### 4. Combine Operations

```
"Generate 5 diabetic patients and export to FHIR"
"Create a member, add 6 months of claims, and export to 837P"
```

### 5. Ask Questions

```
"What scenarios are available?"
"What's included in the cardiac scenario?"
"Can you generate denied claims?"
```

---

## What Claude Will Tell You

Claude will explain:
- What data was generated
- IDs you can use for follow-up
- Available next steps
- Any limitations or caveats

Claude will ask for clarification when:
- The request is ambiguous
- Multiple interpretations are possible
- Required information is missing
