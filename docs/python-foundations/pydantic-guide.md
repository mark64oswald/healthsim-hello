# Pydantic 2.x Guide

A comprehensive guide to Pydantic data validation as used in HealthSim projects.

## What Pydantic Does

Pydantic provides **runtime data validation** using Python type hints. Unlike regular type hints (which are just documentation), Pydantic actually enforces types when your code runs.

### Key Capabilities

| Feature | Description |
|---------|-------------|
| **Validation** | Ensures data matches expected types and constraints |
| **Coercion** | Converts compatible types (string "42" → int 42) |
| **Serialization** | Converts models to/from JSON, dictionaries |
| **Documentation** | Self-documenting models with field descriptions |

### Simple Example

```python
from pydantic import BaseModel

class User(BaseModel):
    name: str
    age: int

# This works - types match
user = User(name="Alice", age=30)

# This also works - Pydantic coerces "30" to 30
user = User(name="Bob", age="30")

# This fails - can't convert "thirty" to int
user = User(name="Charlie", age="thirty")
# ValidationError: Input should be a valid integer
```

## Why HealthSim Uses Pydantic

1. **Healthcare data requires strict validation** - A patient's birth date can't be in the future, medication doses must be positive numbers

2. **Clear contracts between components** - When a function expects a `Patient`, the type is enforced

3. **JSON serialization** - FHIR resources, API responses, and configuration files are all JSON

4. **Self-documenting models** - Field descriptions appear in generated schemas

## Basic Model Definition

```python
from pydantic import BaseModel, Field
from datetime import date
from typing import Literal, Optional

class Person(BaseModel):
    """A person with validated demographics."""
    
    # Required field with description
    person_id: str = Field(..., description="Unique identifier")
    
    # Required field with constraint
    first_name: str = Field(..., min_length=1)
    
    # Required field, no extra constraints
    last_name: str
    
    # Required date field
    birth_date: date
    
    # Field with limited valid values
    gender: Literal["M", "F", "U"] = "U"
    
    # Optional field (can be None)
    email: Optional[str] = None
```

### Breaking Down Each Element

#### `BaseModel` Inheritance

```python
class Person(BaseModel):
```

All Pydantic models inherit from `BaseModel`. This gives you:
- Automatic validation on instantiation
- Serialization methods
- Schema generation

#### `Field()` Function

```python
person_id: str = Field(..., description="Unique identifier")
first_name: str = Field(..., min_length=1)
```

`Field()` lets you add:
- **`...`** (Ellipsis) - Marks field as required
- **`description`** - Human-readable description
- **`min_length` / `max_length`** - String length constraints
- **`ge` / `le` / `gt` / `lt`** - Numeric comparisons (greater/less than or equal)
- **`pattern`** - Regex pattern for strings
- **`default`** - Default value

#### `Literal` for Enumerations

```python
gender: Literal["M", "F", "U"] = "U"
```

`Literal` restricts a field to specific values. Any other value raises a validation error.

#### `Optional` for Nullable Fields

```python
email: Optional[str] = None
```

`Optional[str]` means the field can be either `str` or `None`. Always provide a default (usually `None`) for optional fields.

## Properties and Computed Fields

Properties let you compute values from other fields:

```python
from pydantic import BaseModel
from datetime import date

class Person(BaseModel):
    first_name: str
    last_name: str
    birth_date: date
    
    @property
    def full_name(self) -> str:
        """Computed full name."""
        return f"{self.first_name} {self.last_name}"
    
    @property
    def age(self) -> int:
        """Calculate current age in years."""
        today = date.today()
        return today.year - self.birth_date.year - (
            (today.month, today.day) < (self.birth_date.month, self.birth_date.day)
        )

# Usage
person = Person(
    first_name="John",
    last_name="Doe", 
    birth_date=date(1990, 5, 15)
)
print(person.full_name)  # "John Doe"
print(person.age)        # 34 (depending on current date)
```

### Properties vs Stored Fields

| Aspect | Stored Field | Property |
|--------|--------------|----------|
| Stored in model | Yes | No (computed each access) |
| Appears in `.model_dump()` | Yes | No (by default) |
| Can be set directly | Yes | No |
| Use when | Value provided at creation | Value derived from other fields |

## Field Validators

Validators run custom validation logic on field values.

### Single Field Validator

```python
from pydantic import BaseModel, field_validator
from datetime import date

class Person(BaseModel):
    birth_date: date
    
    @field_validator("birth_date")
    @classmethod
    def birth_date_not_future(cls, v: date) -> date:
        """Validate birth date is not in the future."""
        if v > date.today():
            raise ValueError("Birth date cannot be in the future")
        return v
```

Key points:
- **`@field_validator("field_name")`** - Decorator specifying which field
- **`@classmethod`** - Required in Pydantic 2.x
- **`v` parameter** - The value being validated
- **Return the value** - Can return modified value or original
- **Raise `ValueError`** - For validation failures

### Validator for Multiple Fields

```python
@field_validator("first_name", "last_name")
@classmethod
def names_not_empty(cls, v: str) -> str:
    """Ensure names are not just whitespace."""
    if not v.strip():
        raise ValueError("Name cannot be empty or whitespace")
    return v.strip()  # Return cleaned value
```

### Validator Modes

```python
@field_validator("email", mode="before")
@classmethod
def lowercase_email(cls, v: str) -> str:
    """Convert email to lowercase before validation."""
    if isinstance(v, str):
        return v.lower()
    return v
```

| Mode | When It Runs |
|------|--------------|
| `"after"` (default) | After Pydantic's type validation |
| `"before"` | Before type validation (value might not be correct type yet) |
| `"wrap"` | Wraps the validation, can control whether to proceed |

## Model Validators (Cross-Field Validation)

When validation depends on multiple fields:

```python
from pydantic import BaseModel, model_validator
from datetime import date
from typing import Optional

class Member(BaseModel):
    enrollment_date: date
    termination_date: Optional[date] = None
    status: str = "active"
    
    @model_validator(mode='after')
    def check_dates(self) -> 'Member':
        """Validate date relationships across fields."""
        if self.termination_date and self.enrollment_date:
            if self.termination_date < self.enrollment_date:
                raise ValueError("Termination date must be after enrollment date")
        
        if self.status == "termed" and not self.termination_date:
            raise ValueError("Termed members must have termination date")
        
        return self
```

Key points:
- **`mode='after'`** - Run after all fields are validated
- **`self`** - Full access to all model fields
- **Return `self`** - Must return the model instance

## Model Inheritance

Models can inherit from other models:

```python
from pydantic import BaseModel, Field
from datetime import date
from typing import Literal, Optional

class Person(BaseModel):
    """Base person with demographics."""
    person_id: str
    first_name: str
    last_name: str
    birth_date: date
    gender: Literal["M", "F", "U"] = "U"
    
    @property
    def full_name(self) -> str:
        return f"{self.first_name} {self.last_name}"


class Patient(Person):
    """Clinical patient - extends Person."""
    mrn: str = Field(..., description="Medical Record Number")
    diagnoses: list[str] = []
    
    
class Member(Person):
    """Health plan member - extends Person."""
    member_id: str = Field(..., description="Health plan member ID")
    status: Literal["active", "termed", "pending"] = "active"
    enrollment_date: Optional[date] = None
```

Inherited models:
- Get all fields from parent
- Get all validators from parent
- Get all properties from parent
- Can add new fields and validators
- Can override parent fields (use with caution)

## Serialization Methods (Pydantic 2.x)

### Converting to Dictionary

```python
person = Person(
    person_id="P001",
    first_name="John",
    last_name="Doe",
    birth_date=date(1990, 5, 15)
)

# Convert to dictionary
data = person.model_dump()
# {'person_id': 'P001', 'first_name': 'John', 'last_name': 'Doe', 
#  'birth_date': datetime.date(1990, 5, 15), 'gender': 'U'}

# Exclude certain fields
data = person.model_dump(exclude={"person_id"})

# Only include certain fields
data = person.model_dump(include={"first_name", "last_name"})

# Exclude None values
data = person.model_dump(exclude_none=True)
```

### Converting to JSON

```python
# Convert to JSON string
json_str = person.model_dump_json()
# '{"person_id":"P001","first_name":"John",...}'

# Pretty-printed
json_str = person.model_dump_json(indent=2)
```

### Creating from Dictionary

```python
data = {
    "person_id": "P002",
    "first_name": "Jane",
    "last_name": "Smith",
    "birth_date": "1985-03-20"  # String gets parsed to date
}

person = Person.model_validate(data)
```

### Creating from JSON

```python
json_str = '{"person_id": "P003", "first_name": "Bob", ...}'
person = Person.model_validate_json(json_str)
```

### Getting JSON Schema

```python
schema = Person.model_json_schema()
# Returns dict with JSON Schema representation
```

## Pydantic 1.x vs 2.x Changes

If you see older code or documentation:

| Pydantic 1.x | Pydantic 2.x |
|--------------|--------------|
| `.dict()` | `.model_dump()` |
| `.json()` | `.model_dump_json()` |
| `.parse_obj(data)` | `.model_validate(data)` |
| `.parse_raw(json)` | `.model_validate_json(json)` |
| `.schema()` | `.model_json_schema()` |
| `@validator` | `@field_validator` |
| `@root_validator` | `@model_validator` |

## Common Patterns in HealthSim

### Pattern 1: Literal for Code Values

```python
class Diagnosis(BaseModel):
    code: str  # ICD-10 code like "E11.9"
    code_system: Literal["ICD-10", "ICD-9", "SNOMED"] = "ICD-10"
    status: Literal["active", "resolved", "inactive"] = "active"
```

### Pattern 2: Optional with None Default

```python
class Encounter(BaseModel):
    encounter_id: str
    admit_date: date
    discharge_date: Optional[date] = None  # Still in hospital if None
    discharge_disposition: Optional[str] = None
```

### Pattern 3: Nested Models

```python
class Address(BaseModel):
    street: str
    city: str
    state: str
    zip_code: str

class Person(BaseModel):
    name: str
    address: Address  # Nested model
    
# Usage
person = Person(
    name="John Doe",
    address=Address(
        street="123 Main St",
        city="Boston",
        state="MA",
        zip_code="02101"
    )
)

# Or from nested dict
person = Person(
    name="John Doe",
    address={
        "street": "123 Main St",
        "city": "Boston",
        "state": "MA",
        "zip_code": "02101"
    }
)
```

### Pattern 4: Lists of Models

```python
class Patient(BaseModel):
    patient_id: str
    diagnoses: list[Diagnosis] = []
    encounters: list[Encounter] = []
    
# Append to lists
patient.diagnoses.append(Diagnosis(code="E11.9", ...))
```

## Handling Validation Errors

When validation fails, Pydantic raises `ValidationError`:

```python
from pydantic import BaseModel, ValidationError

class Person(BaseModel):
    name: str
    age: int

try:
    person = Person(name="Alice", age="not a number")
except ValidationError as e:
    print(e)
    # 1 validation error for Person
    # age
    #   Input should be a valid integer, unable to parse string as an integer
    
    # Programmatic access to errors
    for error in e.errors():
        print(f"Field: {error['loc']}")
        print(f"Message: {error['msg']}")
        print(f"Type: {error['type']}")
```

## Summary

| Concept | Purpose |
|---------|---------|
| `BaseModel` | Base class for all Pydantic models |
| `Field()` | Add constraints and metadata to fields |
| `Literal` | Restrict to specific values |
| `Optional` | Allow None as a value |
| `@field_validator` | Custom validation for single field |
| `@model_validator` | Cross-field validation |
| `.model_dump()` | Convert to dictionary |
| `.model_dump_json()` | Convert to JSON string |
| `.model_validate()` | Create from dictionary |
| `ValidationError` | Raised when validation fails |

Pydantic is the backbone of all HealthSim models, ensuring that generated data is always valid and properly structured.
