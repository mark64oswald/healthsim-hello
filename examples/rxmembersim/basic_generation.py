"""
Basic RxMemberSim Generation Examples

This module demonstrates fundamental RxMemberSim operations:
- Creating a generator with reproducible seed
- Generating pharmacy members with BIN/PCN/Group
- Processing pharmacy claims
- Checking formulary coverage
- Exploring member accumulators
"""

from datetime import date
from decimal import Decimal


def example_basic_member():
    """Generate a single pharmacy member and explore the data."""
    from rxmembersim.core.member import RxMemberGenerator

    # Create generator with seed for reproducibility
    gen = RxMemberGenerator(seed=42)

    # Generate a pharmacy member
    member = gen.generate(
        bin="610014",
        pcn="RXTEST",
        group_number="GRP001"
    )

    print("=" * 60)
    print("BASIC PHARMACY MEMBER GENERATION")
    print("=" * 60)

    print(f"\nMember ID: {member.member_id}")
    print(f"Cardholder ID: {member.cardholder_id}")
    print(f"Person Code: {member.person_code}")

    print(f"\nPharmacy Identifiers:")
    print(f"  BIN: {member.bin}")
    print(f"  PCN: {member.pcn}")
    print(f"  Group: {member.group_number}")

    print(f"\nDemographics:")
    print(f"  Name: {member.first_name} {member.last_name}")
    print(f"  DOB: {member.date_of_birth}")
    print(f"  Gender: {member.gender}")

    # Show accumulators
    print(f"\nAccumulators (YTD):")
    print(f"  Deductible: ${member.deductible_met:.2f} of ${member.deductible_limit:.2f}")
    print(f"  Out-of-Pocket: ${member.oop_met:.2f} of ${member.oop_limit:.2f}")

    return member


def example_process_claim():
    """Generate a member and process a pharmacy claim."""
    from rxmembersim.core.member import RxMemberGenerator
    from rxmembersim.claims.claim import PharmacyClaim, TransactionCode
    from rxmembersim.claims.adjudication import AdjudicationEngine
    from rxmembersim.formulary.formulary import FormularyGenerator

    # Setup
    gen = RxMemberGenerator(seed=42)
    member = gen.generate(bin="610014", pcn="RXTEST", group_number="GRP001")
    formulary = FormularyGenerator().generate_standard_commercial()
    engine = AdjudicationEngine(formulary=formulary)

    print("\n" + "=" * 60)
    print("PHARMACY CLAIM PROCESSING")
    print("=" * 60)

    # Create claim for metformin
    claim = PharmacyClaim(
        claim_id="CLM001",
        transaction_code=TransactionCode.BILLING,
        service_date=date.today(),
        pharmacy_npi="9876543210",
        member_id=member.member_id,
        cardholder_id=member.cardholder_id,
        person_code=member.person_code,
        bin=member.bin,
        pcn=member.pcn,
        group_number=member.group_number,
        prescription_number="RX123456",
        fill_number=1,
        ndc="00093017101",  # Metformin 500mg
        quantity_dispensed=Decimal("30"),
        days_supply=30,
        daw_code="0",
        prescriber_npi="1234567890",
        ingredient_cost_submitted=Decimal("8.00"),
        dispensing_fee_submitted=Decimal("2.00"),
        patient_paid_submitted=Decimal("0.00"),
        usual_customary_charge=Decimal("15.00"),
        gross_amount_due=Decimal("10.00"),
    )

    print(f"\nSubmitting claim:")
    print(f"  Drug: Metformin 500mg (NDC 00093017101)")
    print(f"  Quantity: {claim.quantity_dispensed}")
    print(f"  Days Supply: {claim.days_supply}")

    # Adjudicate
    response = engine.adjudicate(claim, member)

    print(f"\nAdjudication Result:")
    print(f"  Status: {response.status}")
    print(f"  Authorization: {response.authorization_number}")

    if response.status == "P":
        print(f"  Plan Pays: ${response.plan_paid:.2f}")
        print(f"  Patient Pays: ${response.patient_pay:.2f}")
        print(f"  Copay: ${response.copay:.2f}")
    else:
        print(f"  Reject Code: {response.reject_code}")
        print(f"  Message: {response.reject_message}")

    return response


def example_batch_members():
    """Generate multiple pharmacy members."""
    from rxmembersim.core.member import RxMemberGenerator

    gen = RxMemberGenerator(seed=101)

    print("\n" + "=" * 60)
    print("BATCH MEMBER GENERATION")
    print("=" * 60)

    # Generate multiple members
    members = []
    for i in range(10):
        member = gen.generate(
            bin="610014",
            pcn="RXTEST",
            group_number=f"GRP{i % 3 + 1:03d}"
        )
        members.append(member)

    print(f"\nGenerated {len(members)} pharmacy members")

    # Analyze population
    from collections import Counter

    groups = Counter(m.group_number for m in members)
    print("\nGroup Distribution:")
    for group, count in groups.most_common():
        print(f"  {group}: {count}")

    # Show sample members
    print("\nSample Members:")
    for member in members[:3]:
        print(f"  {member.member_id}: {member.first_name} {member.last_name}")
        print(f"    BIN/PCN/Group: {member.bin}/{member.pcn}/{member.group_number}")

    return members


def example_accumulators():
    """Demonstrate accumulator tracking."""
    from rxmembersim.core.member import RxMemberGenerator
    from rxmembersim.claims.claim import PharmacyClaim, TransactionCode
    from rxmembersim.claims.adjudication import AdjudicationEngine
    from rxmembersim.formulary.formulary import FormularyGenerator

    print("\n" + "=" * 60)
    print("ACCUMULATOR TRACKING")
    print("=" * 60)

    # Setup
    gen = RxMemberGenerator(seed=42)
    member = gen.generate(bin="610014", pcn="RXTEST", group_number="GRP001")
    formulary = FormularyGenerator().generate_standard_commercial()
    engine = AdjudicationEngine(formulary=formulary)

    print(f"\nInitial Accumulators:")
    print(f"  Deductible: ${member.deductible_met:.2f} of ${member.deductible_limit:.2f}")
    print(f"  OOP: ${member.oop_met:.2f} of ${member.oop_limit:.2f}")

    # Process a claim
    claim = PharmacyClaim(
        claim_id="CLM001",
        transaction_code=TransactionCode.BILLING,
        service_date=date.today(),
        pharmacy_npi="9876543210",
        member_id=member.member_id,
        cardholder_id=member.cardholder_id,
        person_code=member.person_code,
        bin=member.bin,
        pcn=member.pcn,
        group_number=member.group_number,
        prescription_number="RX123456",
        fill_number=1,
        ndc="00093017101",  # Metformin 500mg
        quantity_dispensed=Decimal("30"),
        days_supply=30,
        daw_code="0",
        prescriber_npi="1234567890",
        ingredient_cost_submitted=Decimal("8.00"),
        dispensing_fee_submitted=Decimal("2.00"),
        patient_paid_submitted=Decimal("0.00"),
        usual_customary_charge=Decimal("15.00"),
        gross_amount_due=Decimal("10.00"),
    )

    response = engine.adjudicate(claim, member)

    print(f"\nAfter metformin claim:")
    print(f"  Patient paid: ${response.patient_pay:.2f}")

    # Note: In production, accumulators would be updated on the member
    # This example shows the concept
    print(f"\nNote: Accumulators updated based on patient responsibility")
    print(f"  - Copays apply to OOP max")
    print(f"  - Generic drugs may bypass deductible")


def example_reproducibility():
    """Demonstrate reproducible generation with seeds."""
    from rxmembersim.core.member import RxMemberGenerator

    print("\n" + "=" * 60)
    print("REPRODUCIBILITY")
    print("=" * 60)

    # Same seed = same results
    gen1 = RxMemberGenerator(seed=42)
    gen2 = RxMemberGenerator(seed=42)

    m1 = gen1.generate(bin="610014", pcn="RXTEST", group_number="GRP001")
    m2 = gen2.generate(bin="610014", pcn="RXTEST", group_number="GRP001")

    print(f"\nGenerator 1 (seed=42): {m1.first_name} {m1.last_name}")
    print(f"Generator 2 (seed=42): {m2.first_name} {m2.last_name}")
    print(f"Same member? {m1.member_id == m2.member_id}")

    # Different seed = different results
    gen3 = RxMemberGenerator(seed=99)
    m3 = gen3.generate(bin="610014", pcn="RXTEST", group_number="GRP001")

    print(f"\nGenerator 3 (seed=99): {m3.first_name} {m3.last_name}")
    print(f"Same as seed=42? {m3.member_id == m1.member_id}")


def main():
    """Run all examples."""
    print("\n" + "=" * 60)
    print("RXMEMBERSIM EXAMPLES")
    print("=" * 60)

    try:
        example_basic_member()
        example_process_claim()
        example_batch_members()
        example_accumulators()
        example_reproducibility()

        print("\n" + "=" * 60)
        print("All examples completed successfully!")
        print("=" * 60)

    except ImportError as e:
        print(f"\n RxMemberSim not installed: {e}")
        print("Run: pip install -e . in the rxmembersim directory")
    except Exception as e:
        print(f"\n Error: {e}")
        raise


if __name__ == "__main__":
    main()
