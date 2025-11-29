"""
MemberSim Test Examples

Demonstrates how to test MemberSim functionality using pytest.
These tests can be run with: pytest examples/membersim/test_examples.py -v
"""

import pytest
from datetime import date, timedelta


# Skip all tests if membersim is not installed
try:
    from membersim import MemberGenerator
    MEMBERSIM_AVAILABLE = True
except ImportError:
    MEMBERSIM_AVAILABLE = False

pytestmark = pytest.mark.skipif(
    not MEMBERSIM_AVAILABLE, 
    reason="MemberSim not installed"
)


class TestMemberGeneration:
    """Tests for basic member generation."""
    
    def test_generate_member_has_required_fields(self):
        """Test that generated members have all required fields."""
        gen = MemberGenerator(seed=42)
        member = gen.generate_member()
        
        assert member.member_id is not None
        assert member.subscriber_id is not None
        assert member.demographics is not None
        assert member.demographics.first_name is not None
        assert member.demographics.last_name is not None
        assert member.plan_code is not None
        assert member.status is not None
    
    def test_generate_member_plan_constraint(self):
        """Test that plan constraints are respected."""
        gen = MemberGenerator(seed=42)
        
        member = gen.generate_member(plan_code="PPO-GOLD")
        
        assert member.plan_code == "PPO-GOLD"
    
    def test_generate_member_age_constraint(self):
        """Test that age constraints are respected."""
        gen = MemberGenerator(seed=42)
        
        member = gen.generate_member(age_range=(40, 50))
        
        assert 40 <= member.demographics.age <= 50
    
    def test_generate_member_status_constraint(self):
        """Test that status constraints are respected."""
        gen = MemberGenerator(seed=42)
        
        active = gen.generate_member(status="active")
        termed = gen.generate_member(status="termed")
        
        assert active.status == "active"
        assert termed.status == "termed"
    
    def test_termed_member_has_end_date(self):
        """Test that terminated members have coverage end date."""
        gen = MemberGenerator(seed=42)
        
        termed = gen.generate_member(status="termed")
        
        assert termed.coverage_end is not None
        assert termed.coverage_end > termed.coverage_start


class TestReproducibility:
    """Tests for reproducible generation."""
    
    def test_same_seed_same_member(self):
        """Test that same seed produces identical members."""
        gen1 = MemberGenerator(seed=42)
        gen2 = MemberGenerator(seed=42)
        
        m1 = gen1.generate_member()
        m2 = gen2.generate_member()
        
        assert m1.member_id == m2.member_id
        assert m1.demographics.first_name == m2.demographics.first_name
        assert m1.demographics.last_name == m2.demographics.last_name
        assert m1.plan_code == m2.plan_code
    
    def test_different_seed_different_member(self):
        """Test that different seeds produce different members."""
        gen1 = MemberGenerator(seed=42)
        gen2 = MemberGenerator(seed=99)
        
        m1 = gen1.generate_member()
        m2 = gen2.generate_member()
        
        assert m1.member_id != m2.member_id


class TestFamilyGeneration:
    """Tests for family/dependent generation."""
    
    def test_generate_family_subscriber_first(self):
        """Test that subscriber is first in family list."""
        gen = MemberGenerator(seed=42)
        
        family = gen.generate_family(
            plan_code="PPO-GOLD",
            dependent_config={"spouse": True, "children": 1}
        )
        
        assert family[0].relationship == "self"
    
    def test_generate_family_correct_count(self):
        """Test that correct number of dependents generated."""
        gen = MemberGenerator(seed=42)
        
        family = gen.generate_family(
            plan_code="PPO-GOLD",
            dependent_config={"spouse": True, "children": 2}
        )
        
        # 1 subscriber + 1 spouse + 2 children = 4
        assert len(family) == 4
    
    def test_family_same_subscriber_id(self):
        """Test that all family members share subscriber ID."""
        gen = MemberGenerator(seed=42)
        
        family = gen.generate_family(
            plan_code="PPO-GOLD",
            dependent_config={"spouse": True, "children": 1}
        )
        
        subscriber_id = family[0].subscriber_id
        for member in family:
            assert member.subscriber_id == subscriber_id


class TestClaimsGeneration:
    """Tests for claims generation."""
    
    def test_generate_member_with_claims(self):
        """Test that claims are generated correctly."""
        gen = MemberGenerator(seed=42)
        
        member = gen.generate_member_with_claims(
            claim_count=5,
            date_range=(date(2024, 1, 1), date(2024, 6, 30))
        )
        
        assert len(member.claims) == 5
    
    def test_claims_have_required_fields(self):
        """Test that claims have all required fields."""
        gen = MemberGenerator(seed=42)
        
        member = gen.generate_member_with_claims(claim_count=1)
        claim = member.claims[0]
        
        assert claim.claim_id is not None
        assert claim.member_id == member.member_id
        assert claim.service_date is not None
        assert claim.total_charge is not None
        assert claim.status is not None
    
    def test_claims_within_date_range(self):
        """Test that claims are within specified date range."""
        gen = MemberGenerator(seed=42)
        
        start_date = date(2024, 1, 1)
        end_date = date(2024, 6, 30)
        
        member = gen.generate_member_with_claims(
            claim_count=5,
            date_range=(start_date, end_date)
        )
        
        for claim in member.claims:
            assert start_date <= claim.service_date <= end_date


class TestBatchGeneration:
    """Tests for batch/population generation."""
    
    def test_generate_batch_count(self):
        """Test that batch generates correct number of members."""
        gen = MemberGenerator(seed=42)
        
        members = gen.generate_member_batch(count=20)
        
        assert len(members) == 20
    
    def test_generate_batch_unique_ids(self):
        """Test that all members in batch have unique IDs."""
        gen = MemberGenerator(seed=42)
        
        members = gen.generate_member_batch(count=50)
        ids = [m.member_id for m in members]
        
        assert len(ids) == len(set(ids)), "Duplicate member IDs found"


class TestAccumulators:
    """Tests for accumulator tracking."""
    
    def test_member_has_accumulators(self):
        """Test that members have accumulators."""
        gen = MemberGenerator(seed=42)
        member = gen.generate_member()
        
        assert member.accumulators is not None
        assert len(member.accumulators) > 0
    
    def test_accumulator_within_limits(self):
        """Test that accumulator used is within limit."""
        gen = MemberGenerator(seed=42)
        member = gen.generate_member()
        
        for name, acc in member.accumulators.items():
            assert acc.used >= 0
            assert acc.used <= acc.limit


class TestAvailablePlans:
    """Tests for plan configuration."""
    
    def test_list_plans_not_empty(self):
        """Test that plans list is not empty."""
        gen = MemberGenerator(seed=42)
        
        plans = gen.list_plans()
        
        assert len(plans) > 0
    
    def test_plans_have_required_fields(self):
        """Test that plans have required configuration."""
        gen = MemberGenerator(seed=42)
        
        plans = gen.list_plans()
        plan = plans[0]
        
        assert plan.code is not None
        assert plan.name is not None
        assert plan.deductible_individual is not None
        assert plan.oop_max_individual is not None


# Fixtures for reuse

@pytest.fixture
def member_generator():
    """Provide a seeded member generator."""
    return MemberGenerator(seed=42)


@pytest.fixture
def sample_member(member_generator):
    """Provide a sample member."""
    return member_generator.generate_member()


@pytest.fixture
def member_with_claims(member_generator):
    """Provide a member with claims."""
    return member_generator.generate_member_with_claims(claim_count=5)


@pytest.fixture
def sample_family(member_generator):
    """Provide a sample family."""
    return member_generator.generate_family(
        plan_code="PPO-GOLD",
        dependent_config={"spouse": True, "children": 2}
    )


# Example using fixtures

def test_with_fixture(sample_member):
    """Example test using fixture."""
    assert sample_member.member_id is not None
    assert sample_member.demographics.full_name is not None


def test_family_fixture(sample_family):
    """Example test using family fixture."""
    assert len(sample_family) == 4  # subscriber + spouse + 2 children


def test_claims_fixture(member_with_claims):
    """Example test using claims fixture."""
    assert len(member_with_claims.claims) == 5
