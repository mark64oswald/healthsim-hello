"""
PatientSim FHIR Export Examples

This module demonstrates FHIR R4 export capabilities:
- Exporting single patients to FHIR Bundle
- Exporting cohorts
- Saving to files
- Examining FHIR resources
"""

import json
from pathlib import Path


def example_single_patient_export():
    """Export a single patient to FHIR Bundle."""
    from patientsim import PatientGenerator
    from patientsim.formats.fhir import FHIRExporter
    
    gen = PatientGenerator(seed=42)
    exporter = FHIRExporter()
    
    print("=" * 60)
    print("SINGLE PATIENT FHIR EXPORT")
    print("=" * 60)
    
    # Generate patient
    patient = gen.generate_patient(scenario="diabetes")
    print(f"\nPatient: {patient.full_name}")
    
    # Export to FHIR Bundle
    bundle = exporter.to_bundle(patient)
    
    print(f"\nBundle ID: {bundle.id}")
    print(f"Bundle Type: {bundle.type}")
    print(f"Total Resources: {len(bundle.entry)}")
    
    # Count resources by type
    from collections import Counter
    types = Counter(e.resource.resource_type for e in bundle.entry)
    
    print("\nResources by Type:")
    for rtype, count in sorted(types.items()):
        print(f"  {rtype}: {count}")
    
    return bundle


def example_cohort_export():
    """Export multiple patients as a single Bundle."""
    from patientsim import PatientGenerator
    from patientsim.formats.fhir import FHIRExporter
    
    gen = PatientGenerator(seed=123)
    exporter = FHIRExporter()
    
    print("\n" + "=" * 60)
    print("COHORT FHIR EXPORT")
    print("=" * 60)
    
    # Generate cohort
    patients = gen.generate_batch(count=5, scenario="cardiac")
    print(f"\nGenerated {len(patients)} cardiac patients")
    
    # Export all to single bundle
    bundle = exporter.to_bundle(patients)
    
    print(f"\nBundle contains {len(bundle.entry)} resources")
    
    # Summarize
    from collections import Counter
    types = Counter(e.resource.resource_type for e in bundle.entry)
    
    print("\nResources:")
    for rtype, count in sorted(types.items()):
        print(f"  {rtype}: {count}")
    
    return bundle, patients


def example_save_to_file():
    """Save FHIR Bundle to JSON file."""
    from patientsim import PatientGenerator
    from patientsim.formats.fhir import FHIRExporter
    
    gen = PatientGenerator(seed=456)
    exporter = FHIRExporter()
    
    print("\n" + "=" * 60)
    print("SAVE FHIR TO FILE")
    print("=" * 60)
    
    # Generate and export
    patient = gen.generate_patient()
    bundle = exporter.to_bundle(patient)
    
    # Create output directory
    output_dir = Path("output")
    output_dir.mkdir(exist_ok=True)
    
    # Save to file
    output_file = output_dir / "patient_bundle.json"
    with open(output_file, "w") as f:
        f.write(bundle.json(indent=2))
    
    file_size = output_file.stat().st_size
    print(f"\nSaved: {output_file}")
    print(f"Size: {file_size:,} bytes")
    
    # Verify it's valid JSON
    with open(output_file) as f:
        loaded = json.load(f)
    print(f"Resources in file: {len(loaded.get('entry', []))}")
    
    return output_file


def example_examine_resources():
    """Examine individual FHIR resources in detail."""
    from patientsim import PatientGenerator
    from patientsim.formats.fhir import FHIRExporter
    
    gen = PatientGenerator(seed=789)
    exporter = FHIRExporter()
    
    print("\n" + "=" * 60)
    print("EXAMINE FHIR RESOURCES")
    print("=" * 60)
    
    # Generate and export
    patient = gen.generate_patient(conditions=["diabetes", "hypertension"])
    bundle = exporter.to_bundle(patient)
    
    # Find and examine Patient resource
    print("\n--- FHIR Patient Resource ---")
    for entry in bundle.entry:
        if entry.resource.resource_type == "Patient":
            pt = entry.resource
            print(f"ID: {pt.id}")
            if pt.name:
                name = pt.name[0]
                print(f"Name: {name.given[0] if name.given else ''} {name.family}")
            print(f"Gender: {pt.gender}")
            print(f"Birth Date: {pt.birthDate}")
            break
    
    # Find and examine Condition resources
    print("\n--- FHIR Condition Resources ---")
    conditions = [e.resource for e in bundle.entry 
                  if e.resource.resource_type == "Condition"]
    for cond in conditions[:3]:  # First 3
        print(f"  {cond.id}")
        if cond.code and cond.code.coding:
            coding = cond.code.coding[0]
            print(f"    Code: {coding.code}")
            print(f"    Display: {coding.display}")
    
    # Find and examine Observation resources
    print("\n--- FHIR Observation Resources ---")
    observations = [e.resource for e in bundle.entry 
                    if e.resource.resource_type == "Observation"]
    for obs in observations[:3]:  # First 3
        print(f"  {obs.id}")
        if obs.code and obs.code.coding:
            print(f"    Type: {obs.code.coding[0].display}")
        if hasattr(obs, 'valueQuantity') and obs.valueQuantity:
            print(f"    Value: {obs.valueQuantity.value} {obs.valueQuantity.unit}")
    
    return bundle


def example_fhir_validation_ready():
    """Demonstrate FHIR export ready for validation."""
    from patientsim import PatientGenerator
    from patientsim.formats.fhir import FHIRExporter
    
    gen = PatientGenerator(seed=101)
    exporter = FHIRExporter()
    
    print("\n" + "=" * 60)
    print("FHIR VALIDATION-READY EXPORT")
    print("=" * 60)
    
    # Generate multiple patients
    patients = gen.generate_batch(count=3)
    bundle = exporter.to_bundle(patients)
    
    print(f"\nBundle is ready for FHIR validation")
    print(f"Profile: FHIR R4 (4.0.1)")
    
    # Check bundle structure
    bundle_json = json.loads(bundle.json())
    
    print(f"\nBundle Structure:")
    print(f"  resourceType: {bundle_json.get('resourceType')}")
    print(f"  type: {bundle_json.get('type')}")
    print(f"  total entries: {len(bundle_json.get('entry', []))}")
    
    # Verify each entry has required fields
    valid_entries = 0
    for entry in bundle_json.get('entry', []):
        resource = entry.get('resource', {})
        if resource.get('resourceType') and resource.get('id'):
            valid_entries += 1
    
    print(f"  valid entries: {valid_entries}")
    
    print("\n✓ Bundle can be validated with:")
    print("  - HAPI FHIR Validator")
    print("  - HL7 FHIR Validator")
    print("  - Inferno Framework")
    
    return bundle


def main():
    """Run all FHIR export examples."""
    print("\n" + "=" * 60)
    print("PATIENTSIM FHIR EXPORT EXAMPLES")
    print("=" * 60)
    
    try:
        example_single_patient_export()
        example_cohort_export()
        example_save_to_file()
        example_examine_resources()
        example_fhir_validation_ready()
        
        print("\n" + "=" * 60)
        print("✓ All FHIR examples completed successfully!")
        print("=" * 60)
        
    except ImportError as e:
        print(f"\n⚠ PatientSim not installed: {e}")
        print("Run: pip install -e . in the patientsim directory")
    except Exception as e:
        print(f"\n✗ Error: {e}")
        raise


if __name__ == "__main__":
    main()
