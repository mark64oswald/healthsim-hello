"""
Basic MemberSim Generation Examples

This module demonstrates fundamental MemberSim operations:
- Creating a generator with reproducible seed
- Generating single members
- Generating families
- Generating members with claims
- Exploring member data
"""

from datetime import date


def example_basic_generation():
    """Generate a single member and explore the data."""
    from membersim import MemberGenerator
    
    # Create generator with seed for reproducibility
    gen = MemberGenerator(seed=42)
    
    # Generate a single member
    member = gen.generate_member()
    
    print("=" * 60)
    print("BASIC MEMBER GENERATION")
    print("=" * 60)
    
    print(f"\nMember ID: {member.member_id}")
    print(f"Name: {member.demographics.full_name}")
    print(f"Age: {member.demographics.age}")
    print(f"Gender: {member.demographics.gender}")
    
    print(f"\nCoverage:")
    print(f"  Plan: {member.plan_code}")
    print(f"  Group: {member.group_id}")
    print(f"  Status: {member.status}")
    print(f"  Relationship: {member.relationship}")
    print(f"  Effective: {member.coverage_start}")
    
    # Show accumulators
    print(f"\nAccumulators (YTD):")
    for name, acc in member.accumulators.items():
        pct = (acc.used / acc.limit * 100) if acc.limit > 0 else 0
        print(f"  {name}: ${acc.used:.2f} of ${acc.limit:.2f} ({pct:.0f}%)")
    
    return member


def example_constrained_generation():
    """Generate members with specific constraints."""
    from membersim import MemberGenerator
    
    gen = MemberGenerator(seed=123)
    
    print("\n" + "=" * 60)
    print("CONSTRAINED GENERATION")
    print("=" * 60)
    
    # Specific plan
    print("\nPPO Gold member:")
    ppo_member = gen.generate_member(plan_code="PPO-GOLD")
    print(f"  {ppo_member.demographics.full_name}")
    print(f"  Plan: {ppo_member.plan_code}")
    
    # Age range
    print("\nMedicare-aged member (65+):")
    senior = gen.generate_member(age_range=(65, 80))
    print(f"  {senior.demographics.full_name}, Age {senior.demographics.age}")
    
    # Status
    print("\nTerminated member:")
    termed = gen.generate_member(status="termed")
    print(f"  {termed.demographics.full_name}")
    print(f"  Status: {termed.status}")
    print(f"  Term Date: {termed.coverage_end}")
    
    return ppo_member, senior, termed


def example_family_generation():
    """Generate a subscriber with dependents."""
    from membersim import MemberGenerator
    
    gen = MemberGenerator(seed=456)
    
    print("\n" + "=" * 60)
    print("FAMILY GENERATION")
    print("=" * 60)
    
    # Generate family
    family = gen.generate_family(
        plan_code="PPO-GOLD",
        dependent_config={
            "spouse": True,
            "children": 2
        }
    )
    
    print(f"\nFamily size: {len(family)} members")
    print(f"Subscriber: {family[0].subscriber_id}")
    
    print("\nFamily Members:")
    for member in family:
        print(f"  {member.demographics.full_name}")
        print(f"    Relationship: {member.relationship}")
        print(f"    Member ID: {member.member_id}")
        print(f"    Age: {member.demographics.age}")
    
    return family


def example_claims_generation():
    """Generate a member with claims history."""
    from membersim import MemberGenerator
    
    gen = MemberGenerator(seed=789)
    
    print("\n" + "=" * 60)
    print("MEMBER WITH CLAIMS")
    print("=" * 60)
    
    # Generate member with claims
    member = gen.generate_member_with_claims(
        plan_code="PPO-GOLD",
        claim_count=5,
        date_range=(date(2024, 1, 1), date(2024, 6, 30))
    )
    
    print(f"\nMember: {member.demographics.full_name}")
    print(f"Claims: {len(member.claims)}")
    
    print("\nClaims Summary:")
    total_billed = 0
    total_paid = 0
    for claim in member.claims:
        print(f"\n  {claim.claim_id} ({claim.service_date})")
        print(f"    Provider: {claim.provider_name}")
        print(f"    Billed: ${claim.total_charge:.2f}")
        print(f"    Paid: ${claim.total_paid:.2f}")
        print(f"    Status: {claim.status}")
        total_billed += float(claim.total_charge)
        total_paid += float(claim.total_paid)
    
    print(f"\nTotals:")
    print(f"  Total Billed: ${total_billed:.2f}")
    print(f"  Total Paid: ${total_paid:.2f}")
    
    return member


def example_batch_generation():
    """Generate multiple members as a population."""
    from membersim import MemberGenerator
    
    gen = MemberGenerator(seed=101)
    
    print("\n" + "=" * 60)
    print("POPULATION GENERATION")
    print("=" * 60)
    
    # Simple batch
    members = gen.generate_member_batch(count=20)
    print(f"\nGenerated {len(members)} members")
    
    # Analyze population
    from collections import Counter
    
    plans = Counter(m.plan_code for m in members)
    print("\nPlan Distribution:")
    for plan, count in plans.most_common():
        print(f"  {plan}: {count} ({count/len(members)*100:.0f}%)")
    
    statuses = Counter(m.status for m in members)
    print("\nStatus Distribution:")
    for status, count in statuses.items():
        print(f"  {status}: {count}")
    
    ages = [m.demographics.age for m in members]
    print(f"\nAge Range: {min(ages)} - {max(ages)}")
    print(f"Average Age: {sum(ages)/len(ages):.1f}")
    
    return members


def example_available_plans():
    """Show available plan configurations."""
    from membersim import MemberGenerator
    
    gen = MemberGenerator(seed=42)
    
    print("\n" + "=" * 60)
    print("AVAILABLE PLANS")
    print("=" * 60)
    
    plans = gen.list_plans()
    print(f"\nAvailable plans: {len(plans)}")
    
    for plan in plans:
        print(f"\n  {plan.code}: {plan.name}")
        print(f"    Type: {plan.plan_type}")
        print(f"    Deductible: ${plan.deductible_individual}")
        print(f"    OOP Max: ${plan.oop_max_individual}")
        print(f"    PCP Copay: ${plan.copay_pcp}")
    
    return plans


def example_reproducibility():
    """Demonstrate reproducible generation with seeds."""
    from membersim import MemberGenerator
    
    print("\n" + "=" * 60)
    print("REPRODUCIBILITY")
    print("=" * 60)
    
    # Same seed = same results
    gen1 = MemberGenerator(seed=42)
    gen2 = MemberGenerator(seed=42)
    
    m1 = gen1.generate_member()
    m2 = gen2.generate_member()
    
    print(f"\nGenerator 1 (seed=42): {m1.demographics.full_name}")
    print(f"Generator 2 (seed=42): {m2.demographics.full_name}")
    print(f"Same member? {m1.member_id == m2.member_id}")
    
    # Different seed = different results
    gen3 = MemberGenerator(seed=99)
    m3 = gen3.generate_member()
    
    print(f"\nGenerator 3 (seed=99): {m3.demographics.full_name}")
    print(f"Same as seed=42? {m3.member_id == m1.member_id}")


def main():
    """Run all examples."""
    print("\n" + "=" * 60)
    print("MEMBERSIM EXAMPLES")
    print("=" * 60)
    
    try:
        example_basic_generation()
        example_constrained_generation()
        example_family_generation()
        example_claims_generation()
        example_batch_generation()
        example_available_plans()
        example_reproducibility()
        
        print("\n" + "=" * 60)
        print("✓ All examples completed successfully!")
        print("=" * 60)
        
    except ImportError as e:
        print(f"\n⚠ MemberSim not installed: {e}")
        print("Run: pip install -e . in the membersim directory")
    except Exception as e:
        print(f"\n✗ Error: {e}")
        raise


if __name__ == "__main__":
    main()
