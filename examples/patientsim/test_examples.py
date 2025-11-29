"""
PatientSim Test Examples

Demonstrates how to test PatientSim functionality using pytest.
These tests can be run with: pytest examples/patientsim/test_examples.py -v
"""

import pytest
from datetime import date, timedelta


# Skip all tests if patientsim is not installed
try:
    from patientsim import PatientGenerator
    PATIENTSIM_AVAILABLE = True
except ImportError:
    PATIENTSIM_AVAILABLE = False

pytestmark = pytest.mark.skipif(
    not PATIENTSIM_AVAILABLE, 
    reason="PatientSim not installed"
)


class TestPatientGeneration:
    """Tests for basic patient generation."""
    
    def test_generate_patient_has_required_fields(self):
        """Test that generated patients have all required fields."""
        gen = PatientGenerator(seed=42)
        patient = gen.generate_patient()
        
        assert patient.patient_id is not None
        assert patient.mrn is not None
        assert patient.demographics is not None
        assert patient.demographics.first_name is not None
        assert patient.demographics.last_name is not None
        assert patient.demographics.date_of_birth is not None
    
    def test_generate_patient_age_constraint(self):
        """Test that age constraints are respected."""
        gen = PatientGenerator(seed=42)
        
        patient = gen.generate_patient(age_range=(65, 75))
        
        assert 65 <= patient.age <= 75
    
    def test_generate_patient_gender_constraint(self):
        """Test that gender constraints are respected."""
        gen = PatientGenerator(seed=42)
        
        male = gen.generate_patient(gender="M")
        female = gen.generate_patient(gender="F")
        
        assert male.gender == "M"
        assert female.gender == "F"
    
    def test_generate_patient_with_conditions(self):
        """Test that specified conditions are included."""
        gen = PatientGenerator(seed=42)
        
        patient = gen.generate_patient(conditions=["diabetes"])
        
        # Check that at least one diagnosis contains diabetes-related code
        diagnosis_codes = [dx.code for dx in patient.diagnoses]
        has_diabetes = any(code.startswith("E11") for code in diagnosis_codes)
        
        assert has_diabetes, f"Expected diabetes code, got: {diagnosis_codes}"


class TestReproducibility:
    """Tests for reproducible generation."""
    
    def test_same_seed_same_patient(self):
        """Test that same seed produces identical patients."""
        gen1 = PatientGenerator(seed=42)
        gen2 = PatientGenerator(seed=42)
        
        p1 = gen1.generate_patient()
        p2 = gen2.generate_patient()
        
        assert p1.patient_id == p2.patient_id
        assert p1.demographics.first_name == p2.demographics.first_name
        assert p1.demographics.last_name == p2.demographics.last_name
        assert p1.demographics.date_of_birth == p2.demographics.date_of_birth
    
    def test_different_seed_different_patient(self):
        """Test that different seeds produce different patients."""
        gen1 = PatientGenerator(seed=42)
        gen2 = PatientGenerator(seed=99)
        
        p1 = gen1.generate_patient()
        p2 = gen2.generate_patient()
        
        # Very unlikely to be the same
        assert p1.patient_id != p2.patient_id


class TestCohortGeneration:
    """Tests for batch/cohort generation."""
    
    def test_generate_batch_count(self):
        """Test that batch generates correct number of patients."""
        gen = PatientGenerator(seed=42)
        
        patients = gen.generate_batch(count=10)
        
        assert len(patients) == 10
    
    def test_generate_batch_unique_ids(self):
        """Test that all patients in batch have unique IDs."""
        gen = PatientGenerator(seed=42)
        
        patients = gen.generate_batch(count=20)
        ids = [p.patient_id for p in patients]
        
        assert len(ids) == len(set(ids)), "Duplicate patient IDs found"
    
    def test_generate_batch_with_constraints(self):
        """Test that batch respects constraints."""
        gen = PatientGenerator(seed=42)
        
        patients = gen.generate_batch(
            count=10,
            age_range=(50, 60)
        )
        
        for patient in patients:
            assert 50 <= patient.age <= 60


class TestPatientData:
    """Tests for patient data structure."""
    
    def test_patient_has_diagnoses(self):
        """Test that patients have diagnoses."""
        gen = PatientGenerator(seed=42)
        patient = gen.generate_patient(scenario="diabetes")
        
        assert len(patient.diagnoses) > 0
        
        # Each diagnosis should have code and description
        for dx in patient.diagnoses:
            assert dx.code is not None
            assert dx.description is not None
    
    def test_patient_has_encounters(self):
        """Test that patients have encounters."""
        gen = PatientGenerator(seed=42)
        patient = gen.generate_patient()
        
        # Most patients should have at least one encounter
        # (this may vary based on generation logic)
        assert patient.encounters is not None
    
    def test_patient_computed_properties(self):
        """Test computed properties like full_name and age."""
        gen = PatientGenerator(seed=42)
        patient = gen.generate_patient()
        
        # Full name should combine first and last
        expected_name = f"{patient.demographics.first_name} {patient.demographics.last_name}"
        assert patient.full_name == expected_name
        
        # Age should be positive
        assert patient.age > 0
        assert patient.age < 120  # Reasonable upper bound


class TestScenarios:
    """Tests for clinical scenarios."""
    
    def test_list_scenarios(self):
        """Test that scenarios can be listed."""
        gen = PatientGenerator(seed=42)
        
        scenarios = gen.list_scenarios()
        
        assert isinstance(scenarios, list)
        assert len(scenarios) > 0
    
    def test_cardiac_scenario(self):
        """Test cardiac scenario generates appropriate data."""
        gen = PatientGenerator(seed=42)
        
        patient = gen.generate_patient(scenario="cardiac")
        
        # Should have cardiac-related diagnoses (I-codes in ICD-10)
        diagnosis_codes = [dx.code for dx in patient.diagnoses]
        has_cardiac = any(
            code.startswith("I") for code in diagnosis_codes
        )
        
        assert has_cardiac, f"Expected cardiac codes, got: {diagnosis_codes}"


# Fixtures for reuse

@pytest.fixture
def patient_generator():
    """Provide a seeded patient generator."""
    return PatientGenerator(seed=42)


@pytest.fixture
def sample_patient(patient_generator):
    """Provide a sample patient."""
    return patient_generator.generate_patient()


@pytest.fixture
def cardiac_cohort(patient_generator):
    """Provide a cohort of cardiac patients."""
    return patient_generator.generate_batch(count=5, scenario="cardiac")


# Example using fixtures

def test_with_fixture(sample_patient):
    """Example test using fixture."""
    assert sample_patient.patient_id is not None
    assert sample_patient.full_name is not None


def test_cohort_fixture(cardiac_cohort):
    """Example test using cohort fixture."""
    assert len(cardiac_cohort) == 5
