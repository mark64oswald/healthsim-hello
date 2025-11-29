# Pytest Guide

A comprehensive guide to testing with pytest as used in HealthSim projects.

## Why Pytest?

Python has a built-in `unittest` module, but pytest is preferred because:

| Feature | unittest | pytest |
|---------|----------|--------|
| Test syntax | Classes required | Simple functions |
| Assertions | `self.assertEqual(a, b)` | `assert a == b` |
| Error messages | Basic | Detailed diff output |
| Fixtures | setUp/tearDown methods | Powerful fixture system |
| Plugins | Limited | Rich ecosystem |

All HealthSim projects use pytest.

## Test File Organization

```
project/
├── src/
│   └── mypackage/
│       ├── __init__.py
│       ├── models.py
│       └── generator.py
└── tests/
    ├── __init__.py           # Makes tests a package
    ├── conftest.py           # Shared fixtures
    ├── test_models.py        # Tests for models.py
    └── test_generator.py     # Tests for generator.py
```

### Naming Conventions

| Element | Convention | Example |
|---------|------------|---------|
| Test files | `test_*.py` or `*_test.py` | `test_models.py` |
| Test functions | `test_*` | `test_create_valid_person` |
| Test classes (optional) | `Test*` | `TestPerson` |

## Basic Test Structure

### Arrange-Act-Assert Pattern

```python
def test_create_valid_person():
    """Test creating a person with valid data."""
    # ARRANGE - Set up the test data
    person = Person(
        person_id="P001",
        first_name="John",
        last_name="Doe",
        birth_date=date(1990, 5, 15),
    )
    
    # ACT - Perform the action being tested
    result = person.full_name
    
    # ASSERT - Verify the result
    assert result == "John Doe"
    assert person.age >= 34
```

### Docstrings Matter

```python
def test_birth_date_not_future():
    """Test that future birth dates are rejected.
    
    A person cannot be born in the future, so the model
    should raise a ValidationError.
    """
```

Good docstrings:
- Describe **what** is being tested
- Explain **why** this test matters
- Help future developers understand failures

## Assertions

Pytest uses plain `assert` statements. When assertions fail, pytest shows detailed output.

### Common Assertions

```python
# Equality
assert result == expected
assert result != unexpected

# Identity
assert result is None
assert result is not None

# Truthiness
assert result  # truthy
assert not result  # falsy

# Membership
assert item in collection
assert item not in collection

# Comparison
assert value > 0
assert value >= minimum
assert value < maximum

# Type checking
assert isinstance(result, Person)

# String operations
assert name.startswith("Dr.")
assert "error" in message.lower()

# Length
assert len(items) == 5
assert len(items) > 0
```

### Assertion Messages

```python
# Add message for context when it fails
assert result == expected, f"Expected {expected}, got {result}"
```

### Floating Point Comparisons

```python
import pytest

# Don't do this (floating point precision issues)
assert 0.1 + 0.2 == 0.3  # Often fails!

# Do this instead
assert 0.1 + 0.2 == pytest.approx(0.3)
assert value == pytest.approx(expected, rel=1e-3)  # relative tolerance
assert value == pytest.approx(expected, abs=0.01)  # absolute tolerance
```

## Testing for Exceptions

Use `pytest.raises` to test that code raises expected exceptions:

```python
import pytest
from pydantic import ValidationError

def test_future_birth_date_rejected():
    """Test that future birth dates raise ValidationError."""
    future_date = date.today() + timedelta(days=1)
    
    with pytest.raises(ValidationError):
        Person(
            person_id="P002",
            first_name="Future",
            last_name="Baby",
            birth_date=future_date,
        )
```

### Inspecting the Exception

```python
def test_future_birth_date_error_message():
    """Test that the error message mentions 'future'."""
    future_date = date.today() + timedelta(days=1)
    
    with pytest.raises(ValidationError) as exc_info:
        Person(
            person_id="P002",
            first_name="Future",
            last_name="Baby",
            birth_date=future_date,
        )
    
    # exc_info.value is the actual exception
    assert "future" in str(exc_info.value).lower()
```

### Testing Specific Exception Types

```python
def test_invalid_age_type():
    """Test that non-integer age raises TypeError."""
    with pytest.raises(ValidationError) as exc_info:
        Person(name="Test", age="not a number")
    
    # Check the error type
    errors = exc_info.value.errors()
    assert errors[0]["type"] == "int_parsing"
```

## Test Classes (Grouping Related Tests)

While not required, classes help organize related tests:

```python
class TestPerson:
    """Tests for the Person model."""
    
    def test_create_valid(self):
        """Test creating a valid person."""
        person = Person(
            person_id="P001",
            first_name="John",
            last_name="Doe",
            birth_date=date(1990, 5, 15),
        )
        assert person.full_name == "John Doe"
    
    def test_default_gender(self):
        """Test that gender defaults to 'U'."""
        person = Person(
            person_id="P002",
            first_name="Pat",
            last_name="Smith",
            birth_date=date(2000, 1, 1),
        )
        assert person.gender == "U"
    
    def test_computed_age(self):
        """Test age calculation."""
        person = Person(
            person_id="P003",
            first_name="Test",
            last_name="User",
            birth_date=date(1990, 1, 1),
        )
        assert person.age >= 34


class TestPersonValidation:
    """Tests for Person validation rules."""
    
    def test_empty_first_name_rejected(self):
        """Test that empty first name is rejected."""
        with pytest.raises(ValidationError):
            Person(
                person_id="P004",
                first_name="",  # Empty!
                last_name="User",
                birth_date=date(1990, 1, 1),
            )
```

## Fixtures - Reusable Test Data

Fixtures provide reusable test data and setup logic.

### Basic Fixture

```python
import pytest
from datetime import date

@pytest.fixture
def sample_person():
    """Create a sample person for testing."""
    return Person(
        person_id="P001",
        first_name="Test",
        last_name="User",
        birth_date=date(1990, 1, 1),
    )

# Using the fixture - just add it as a parameter
def test_person_has_full_name(sample_person):
    assert sample_person.full_name == "Test User"

def test_person_has_id(sample_person):
    assert sample_person.person_id == "P001"
```

### Fixture with Cleanup

```python
@pytest.fixture
def temp_file():
    """Create a temporary file, clean up after test."""
    import tempfile
    import os
    
    # Setup
    fd, path = tempfile.mkstemp()
    os.close(fd)
    
    yield path  # This is what the test receives
    
    # Cleanup (runs after test completes)
    os.unlink(path)

def test_write_to_file(temp_file):
    with open(temp_file, 'w') as f:
        f.write("test data")
    
    with open(temp_file, 'r') as f:
        assert f.read() == "test data"
    # File is automatically cleaned up after test
```

### Fixture Scopes

```python
@pytest.fixture(scope="function")  # Default - runs for each test
def fresh_generator():
    return PersonGenerator(seed=42)

@pytest.fixture(scope="class")  # Shared within a test class
def shared_generator():
    return PersonGenerator(seed=42)

@pytest.fixture(scope="module")  # Shared within a test file
def module_generator():
    return PersonGenerator(seed=42)

@pytest.fixture(scope="session")  # Shared across all tests
def session_generator():
    return PersonGenerator(seed=42)
```

### conftest.py - Shared Fixtures

Put fixtures in `conftest.py` to share across test files:

```python
# tests/conftest.py
import pytest
from mypackage import PersonGenerator, MemberGenerator

@pytest.fixture
def person_generator():
    """Seeded person generator for reproducible tests."""
    return PersonGenerator(seed=42)

@pytest.fixture
def member_generator():
    """Seeded member generator for reproducible tests."""
    return MemberGenerator(seed=42)

@pytest.fixture
def sample_patient(person_generator):
    """Generate a sample patient."""
    return person_generator.generate_patient()
```

Fixtures in `conftest.py` are automatically available to all tests in that directory and subdirectories.

## Parametrized Tests

Run the same test with different inputs:

```python
@pytest.mark.parametrize("gender,expected", [
    ("M", "Male"),
    ("F", "Female"),
    ("U", "Unknown"),
])
def test_gender_display(gender, expected):
    person = Person(
        person_id="P001",
        first_name="Test",
        last_name="User",
        birth_date=date(1990, 1, 1),
        gender=gender,
    )
    assert person.gender_display == expected
```

### Multiple Parameters

```python
@pytest.mark.parametrize("age,status", [
    (17, "minor"),
    (18, "adult"),
    (65, "senior"),
])
def test_age_status(age, status):
    birth_year = date.today().year - age
    person = Person(
        person_id="P001",
        first_name="Test",
        last_name="User",
        birth_date=date(birth_year, 1, 1),
    )
    assert person.age_status == status
```

### IDs for Clarity

```python
@pytest.mark.parametrize("code,valid", [
    pytest.param("E11.9", True, id="valid_icd10"),
    pytest.param("E11", True, id="valid_icd10_short"),
    pytest.param("", False, id="empty_code"),
    pytest.param("INVALID", False, id="invalid_format"),
])
def test_diagnosis_code_validation(code, valid):
    if valid:
        dx = Diagnosis(code=code)
        assert dx.code == code
    else:
        with pytest.raises(ValidationError):
            Diagnosis(code=code)
```

## Running Tests

### Basic Commands

```bash
# Run all tests
pytest

# Verbose output (show test names)
pytest -v

# Very verbose (show print statements too)
pytest -vv -s

# Run specific file
pytest tests/test_models.py

# Run specific test class
pytest tests/test_models.py::TestPerson

# Run specific test
pytest tests/test_models.py::TestPerson::test_create_valid

# Run tests matching a pattern
pytest -k "person"
pytest -k "person and not validation"
```

### Useful Flags

| Flag | Purpose |
|------|---------|
| `-v` | Verbose - show test names |
| `-vv` | Very verbose - more detail |
| `-s` | Show print statements (don't capture stdout) |
| `-x` | Stop on first failure |
| `--lf` | Run only last failed tests |
| `-k EXPR` | Run tests matching expression |
| `--tb=short` | Shorter tracebacks |
| `--tb=no` | No tracebacks |
| `--collect-only` | List tests without running |

### With Coverage

```bash
# Install pytest-cov
pip install pytest-cov

# Run with coverage report
pytest --cov=mypackage

# Coverage with missing lines
pytest --cov=mypackage --cov-report=term-missing

# Generate HTML report
pytest --cov=mypackage --cov-report=html
# Open htmlcov/index.html in browser
```

## Configuration in pyproject.toml

```toml
[tool.pytest.ini_options]
testpaths = ["tests"]
pythonpath = ["src"]
addopts = "-v --tb=short"
filterwarnings = [
    "ignore::DeprecationWarning",
]
markers = [
    "slow: marks tests as slow (deselect with '-m \"not slow\"')",
    "integration: marks tests as integration tests",
]
```

### Using Markers

```python
@pytest.mark.slow
def test_generate_large_batch():
    """Test generating 10000 patients (slow)."""
    gen = PatientGenerator(seed=42)
    patients = gen.generate_batch(10000)
    assert len(patients) == 10000

@pytest.mark.integration
def test_fhir_export_roundtrip():
    """Test exporting to FHIR and importing back."""
    # ...
```

```bash
# Skip slow tests
pytest -m "not slow"

# Run only integration tests
pytest -m integration
```

## HealthSim Testing Patterns

### Pattern 1: Seed for Reproducibility

```python
def test_generator_reproducible():
    """Test that same seed produces same results."""
    gen1 = PersonGenerator(seed=42)
    gen2 = PersonGenerator(seed=42)
    
    p1 = gen1.generate_person()
    p2 = gen2.generate_person()
    
    assert p1.first_name == p2.first_name
    assert p1.last_name == p2.last_name
    assert p1.birth_date == p2.birth_date
```

### Pattern 2: Test Validation (Positive and Negative)

```python
class TestMemberValidation:
    """Test Member model validation."""
    
    def test_valid_member_accepted(self):
        """Test that valid data creates a member."""
        member = Member(
            member_id="MEM001",
            person_id="P001",
            first_name="Jane",
            last_name="Doe",
            birth_date=date(1985, 3, 20),
            enrollment_date=date(2024, 1, 1),
        )
        assert member.status == "active"
    
    def test_termination_before_enrollment_rejected(self):
        """Test that termination before enrollment fails."""
        with pytest.raises(ValidationError) as exc_info:
            Member(
                member_id="MEM002",
                person_id="P002",
                first_name="Bad",
                last_name="Dates",
                birth_date=date(1990, 1, 1),
                enrollment_date=date(2024, 6, 1),
                termination_date=date(2024, 1, 1),  # Before enrollment!
            )
        assert "enrollment" in str(exc_info.value).lower()
```

### Pattern 3: Test Serialization Round-Trip

```python
def test_person_serialization_roundtrip():
    """Test that person survives JSON round-trip."""
    original = Person(
        person_id="P001",
        first_name="John",
        last_name="Doe",
        birth_date=date(1990, 5, 15),
    )
    
    # Serialize to JSON
    json_str = original.model_dump_json()
    
    # Deserialize back
    restored = Person.model_validate_json(json_str)
    
    # Verify all fields match
    assert restored.person_id == original.person_id
    assert restored.first_name == original.first_name
    assert restored.last_name == original.last_name
    assert restored.birth_date == original.birth_date
```

### Pattern 4: Test Edge Cases

```python
class TestEdgeCases:
    """Test edge cases and boundary conditions."""
    
    def test_empty_diagnoses_list(self):
        """Test patient with no diagnoses."""
        patient = Patient(
            patient_id="P001",
            first_name="Healthy",
            last_name="Person",
            birth_date=date(1990, 1, 1),
            diagnoses=[],  # Empty list
        )
        assert len(patient.diagnoses) == 0
    
    def test_none_optional_fields(self):
        """Test that optional fields can be None."""
        member = Member(
            member_id="MEM001",
            person_id="P001",
            first_name="Test",
            last_name="User",
            birth_date=date(1990, 1, 1),
            email=None,
            termination_date=None,
        )
        assert member.email is None
        assert member.termination_date is None
```

## Summary

| Concept | Purpose |
|---------|---------|
| `pytest` | Test runner and framework |
| `assert` | Simple assertions |
| `pytest.raises` | Test for expected exceptions |
| `@pytest.fixture` | Reusable test data/setup |
| `conftest.py` | Shared fixtures across files |
| `@pytest.mark.parametrize` | Run test with multiple inputs |
| `-v`, `-x`, `-k` | Common command-line flags |
| `--cov` | Coverage reporting |

Pytest makes testing straightforward. Write functions that start with `test_`, use plain `assert` statements, and let pytest handle the rest.
