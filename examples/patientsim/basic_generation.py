"""
Basic PatientSim Generation Examples

This module demonstrates fundamental PatientSim operations:
- Creating a generator with reproducible seed
- Generating single patients
- Generating cohorts with constraints
- Exploring patient data
"""

from datetime import date


def example_basic_generation():
    """Generate a single patient and explore the data."""
    from patientsim import PatientGenerator
    
    # Create generator with seed for reproducibility
    gen = PatientGenerator(seed=42)
    
    # Generate a single patient
    patient = gen.generate_patient()
    
    print("=" * 60)
    print("BASIC PATIENT GENERATION")
    print("=" * 60)
    
    print(f"\nPatient ID: {patient.patient_id}")
    print(f"Name: {patient.full_name}")
    print(f"Age: {patient.age}")
    print(f"Gender: {patient.gender}")
    print(f"MRN: {patient.mrn}")
    
    # Show diagnoses
    print("\nDiagnoses:")
    for dx in patient.diagnoses[:5]:  # First 5
        print(f"  • {dx.code}: {dx.description}")
    
    # Show encounters
    print("\nEncounters:")
    for enc in patient.encounters[:3]:  # First 3
        print(f"  • {enc.encounter_id}: {enc.type} ({enc.admit_date})")
    
    # Show medications
    print("\nMedications:")
    for med in patient.medications[:5]:  # First 5
        print(f"  • {med.name} {med.dose}")
    
    return patient


def example_constrained_generation():
    """Generate patients with specific constraints."""
    from patientsim import PatientGenerator
    
    gen = PatientGenerator(seed=123)
    
    print("\n" + "=" * 60)
    print("CONSTRAINED GENERATION")
    print("=" * 60)
    
    # Age-specific generation
    print("\nElderly patient (65-80):")
    elderly = gen.generate_patient(age_range=(65, 80))
    print(f"  {elderly.full_name}, Age {elderly.age}")
    
    # Gender-specific
    print("\nFemale patient:")
    female = gen.generate_patient(gender="F")
    print(f"  {female.full_name}, Gender {female.gender}")
    
    # With specific conditions
    print("\nDiabetic patient:")
    diabetic = gen.generate_patient(conditions=["diabetes"])
    print(f"  {diabetic.full_name}")
    print(f"  Diagnoses: {[dx.code for dx in diabetic.diagnoses]}")
    
    # Combined constraints
    print("\nMale cardiac patient, 50-70:")
    cardiac = gen.generate_patient(
        scenario="cardiac",
        age_range=(50, 70),
        gender="M"
    )
    print(f"  {cardiac.full_name}, Age {cardiac.age}, {cardiac.gender}")
    
    return elderly, female, diabetic, cardiac


def example_cohort_generation():
    """Generate multiple patients as a cohort."""
    from patientsim import PatientGenerator
    
    gen = PatientGenerator(seed=456)
    
    print("\n" + "=" * 60)
    print("COHORT GENERATION")
    print("=" * 60)
    
    # Simple batch
    patients = gen.generate_batch(count=10)
    print(f"\nGenerated {len(patients)} patients")
    
    # Show summary
    print("\nCohort Summary:")
    for i, p in enumerate(patients[:5], 1):
        primary_dx = p.diagnoses[0].code if p.diagnoses else "None"
        print(f"  {i}. {p.full_name}, {p.age}y {p.gender}, Dx: {primary_dx}")
    print(f"  ... and {len(patients) - 5} more")
    
    # Age distribution
    ages = [p.age for p in patients]
    print(f"\nAge Range: {min(ages)} - {max(ages)}")
    print(f"Average Age: {sum(ages) / len(ages):.1f}")
    
    # Gender distribution
    males = sum(1 for p in patients if p.gender == "M")
    females = sum(1 for p in patients if p.gender == "F")
    print(f"Gender: {males} male, {females} female")
    
    return patients


def example_scenario_generation():
    """Generate patients using clinical scenarios."""
    from patientsim import PatientGenerator
    
    gen = PatientGenerator(seed=789)
    
    print("\n" + "=" * 60)
    print("SCENARIO-BASED GENERATION")
    print("=" * 60)
    
    # List available scenarios
    scenarios = gen.list_scenarios()
    print(f"\nAvailable scenarios: {scenarios}")
    
    # Generate using different scenarios
    print("\nCardiac Scenario Patient:")
    cardiac = gen.generate_patient(scenario="cardiac")
    print(f"  {cardiac.full_name}")
    print(f"  Diagnoses: {[dx.description for dx in cardiac.diagnoses[:3]]}")
    
    print("\nDiabetes Scenario Patient:")
    diabetic = gen.generate_patient(scenario="diabetes")
    print(f"  {diabetic.full_name}")
    print(f"  Diagnoses: {[dx.description for dx in diabetic.diagnoses[:3]]}")
    
    return cardiac, diabetic


def example_reproducibility():
    """Demonstrate reproducible generation with seeds."""
    from patientsim import PatientGenerator
    
    print("\n" + "=" * 60)
    print("REPRODUCIBILITY")
    print("=" * 60)
    
    # Same seed = same results
    gen1 = PatientGenerator(seed=42)
    gen2 = PatientGenerator(seed=42)
    
    p1 = gen1.generate_patient()
    p2 = gen2.generate_patient()
    
    print(f"\nGenerator 1 (seed=42): {p1.full_name}")
    print(f"Generator 2 (seed=42): {p2.full_name}")
    print(f"Same patient? {p1.patient_id == p2.patient_id}")
    
    # Different seed = different results
    gen3 = PatientGenerator(seed=99)
    p3 = gen3.generate_patient()
    
    print(f"\nGenerator 3 (seed=99): {p3.full_name}")
    print(f"Same as seed=42? {p3.patient_id == p1.patient_id}")


def main():
    """Run all examples."""
    print("\n" + "=" * 60)
    print("PATIENTSIM EXAMPLES")
    print("=" * 60)
    
    try:
        example_basic_generation()
        example_constrained_generation()
        example_cohort_generation()
        example_scenario_generation()
        example_reproducibility()
        
        print("\n" + "=" * 60)
        print("✓ All examples completed successfully!")
        print("=" * 60)
        
    except ImportError as e:
        print(f"\n⚠ PatientSim not installed: {e}")
        print("Run: pip install -e . in the patientsim directory")
    except Exception as e:
        print(f"\n✗ Error: {e}")
        raise


if __name__ == "__main__":
    main()
