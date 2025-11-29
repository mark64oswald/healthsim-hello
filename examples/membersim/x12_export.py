"""
MemberSim X12 EDI Export Examples

This module demonstrates X12 EDI export capabilities:
- Generating X12 834 (Enrollment)
- Generating X12 837P (Professional Claims)
- Generating X12 835 (Remittance)
- Saving to files
"""

from datetime import date
from pathlib import Path


def example_834_enrollment():
    """Generate X12 834 enrollment transaction."""
    from membersim import MemberGenerator
    from membersim.formats import generate_834
    
    gen = MemberGenerator(seed=42)
    
    print("=" * 60)
    print("X12 834 - ENROLLMENT TRANSACTION")
    print("=" * 60)
    
    # Generate members
    members = gen.generate_member_batch(count=5)
    print(f"\nGenerated {len(members)} members for enrollment")
    
    # Generate 834
    edi_834 = generate_834(members)
    
    # Show preview (first 500 chars)
    print("\n834 Preview:")
    print("-" * 40)
    print(edi_834[:500])
    print("...")
    print("-" * 40)
    
    print(f"\nTotal length: {len(edi_834)} characters")
    
    # Count segments
    segments = edi_834.count("~")
    print(f"Segment count: {segments}")
    
    return edi_834, members


def example_837p_claims():
    """Generate X12 837P professional claims."""
    from membersim import MemberGenerator
    from membersim.formats import generate_837p
    
    gen = MemberGenerator(seed=123)
    
    print("\n" + "=" * 60)
    print("X12 837P - PROFESSIONAL CLAIMS")
    print("=" * 60)
    
    # Generate members with claims
    members = gen.generate_population(
        count=3,
        with_claims=True,
        claims_per_member=(2, 5)
    )
    
    # Collect all claims
    all_claims = []
    for member in members:
        all_claims.extend(member.claims)
    
    print(f"\nTotal claims: {len(all_claims)}")
    
    # Generate 837P
    edi_837p = generate_837p(all_claims)
    
    # Show preview
    print("\n837P Preview:")
    print("-" * 40)
    print(edi_837p[:500])
    print("...")
    print("-" * 40)
    
    print(f"\nTotal length: {len(edi_837p)} characters")
    
    return edi_837p, all_claims


def example_835_remittance():
    """Generate X12 835 remittance advice."""
    from membersim import MemberGenerator
    from membersim.formats import generate_835
    
    gen = MemberGenerator(seed=456)
    
    print("\n" + "=" * 60)
    print("X12 835 - REMITTANCE ADVICE")
    print("=" * 60)
    
    # Generate members with claims
    members = gen.generate_population(
        count=5,
        with_claims=True,
        claims_per_member=(1, 3)
    )
    
    # Collect paid claims
    paid_claims = []
    for member in members:
        for claim in member.claims:
            if claim.status == "paid":
                paid_claims.append(claim)
    
    print(f"\nPaid claims: {len(paid_claims)}")
    
    # Generate 835
    edi_835 = generate_835(paid_claims)
    
    # Show preview
    print("\n835 Preview:")
    print("-" * 40)
    print(edi_835[:500])
    print("...")
    print("-" * 40)
    
    # Calculate totals
    total_paid = sum(float(c.total_paid) for c in paid_claims)
    print(f"\nTotal payment amount: ${total_paid:.2f}")
    
    return edi_835, paid_claims


def example_270_271_eligibility():
    """Generate X12 270/271 eligibility inquiry/response."""
    from membersim import MemberGenerator
    from membersim.formats import generate_270, generate_271
    
    gen = MemberGenerator(seed=789)
    
    print("\n" + "=" * 60)
    print("X12 270/271 - ELIGIBILITY")
    print("=" * 60)
    
    # Generate a member
    member = gen.generate_member()
    print(f"\nMember: {member.demographics.full_name}")
    print(f"Plan: {member.plan_code}")
    
    # Generate 270 inquiry
    edi_270 = generate_270(member)
    
    print("\n270 Eligibility Inquiry:")
    print("-" * 40)
    print(edi_270[:300])
    print("...")
    
    # Generate 271 response
    edi_271 = generate_271(member, include_benefits=True)
    
    print("\n271 Eligibility Response:")
    print("-" * 40)
    print(edi_271[:400])
    print("...")
    
    return edi_270, edi_271, member


def example_save_to_files():
    """Save X12 files to disk."""
    from membersim import MemberGenerator
    from membersim.formats import generate_834, generate_837p
    
    gen = MemberGenerator(seed=101)
    
    print("\n" + "=" * 60)
    print("SAVE X12 FILES")
    print("=" * 60)
    
    # Create output directory
    output_dir = Path("output")
    output_dir.mkdir(exist_ok=True)
    
    # Generate 834
    members = gen.generate_member_batch(count=10)
    edi_834 = generate_834(members)
    
    file_834 = output_dir / "enrollment.834"
    with open(file_834, "w") as f:
        f.write(edi_834)
    print(f"\nSaved: {file_834} ({file_834.stat().st_size:,} bytes)")
    
    # Generate 837P
    members_with_claims = gen.generate_population(
        count=5,
        with_claims=True,
        claims_per_member=(1, 5)
    )
    all_claims = [c for m in members_with_claims for c in m.claims]
    edi_837 = generate_837p(all_claims)
    
    file_837 = output_dir / "claims.837"
    with open(file_837, "w") as f:
        f.write(edi_837)
    print(f"Saved: {file_837} ({file_837.stat().st_size:,} bytes)")
    
    print("\n✓ Files saved to ./output/")
    
    return file_834, file_837


def example_x12_structure():
    """Explain X12 structure for educational purposes."""
    
    print("\n" + "=" * 60)
    print("X12 EDI STRUCTURE EXPLAINED")
    print("=" * 60)
    
    print("""
X12 transactions have a hierarchical structure:

ISA - Interchange Control Header
  └── GS - Functional Group Header
        └── ST - Transaction Set Header
              └── [Transaction-specific segments]
              └── SE - Transaction Set Trailer
        └── GE - Functional Group Trailer
  └── IEA - Interchange Control Trailer

Key Concepts:
─────────────
• Segment: A line of data ending with ~ (tilde)
• Element: Data within segment, separated by * (asterisk)
• Delimiter: ^ is often used as sub-element separator

Example ISA Segment:
ISA*00*          *00*          *ZZ*SENDER        *ZZ*RECEIVER      *241127*1430*^*00501*000000001*0*P*:~

Breakdown:
• ISA = Segment ID (Interchange Header)
• 00 = Authorization Info Qualifier
• [spaces] = Authorization Info (not used)
• 00 = Security Info Qualifier  
• [spaces] = Security Info (not used)
• ZZ = Sender ID Qualifier
• SENDER = Sender ID
• ZZ = Receiver ID Qualifier
• RECEIVER = Receiver ID
• 241127 = Date (YYMMDD)
• 1430 = Time (HHMM)
• ^ = Component Element Separator
• 00501 = Version
• 000000001 = Control Number
• 0 = Acknowledgment Requested
• P = Usage Indicator (P=Production, T=Test)
• : = Sub-element Separator

Common Transaction Sets:
─────────────────────────
• 834 - Benefit Enrollment and Maintenance
• 837P - Health Care Claim: Professional
• 837I - Health Care Claim: Institutional
• 835 - Health Care Claim Payment/Advice
• 270 - Health Care Eligibility Inquiry
• 271 - Health Care Eligibility Response
• 278 - Health Care Services Review
""")


def main():
    """Run all X12 export examples."""
    print("\n" + "=" * 60)
    print("MEMBERSIM X12 EDI EXPORT EXAMPLES")
    print("=" * 60)
    
    try:
        example_834_enrollment()
        example_837p_claims()
        example_835_remittance()
        example_270_271_eligibility()
        example_save_to_files()
        example_x12_structure()
        
        print("\n" + "=" * 60)
        print("✓ All X12 examples completed successfully!")
        print("=" * 60)
        
    except ImportError as e:
        print(f"\n⚠ MemberSim not installed: {e}")
        print("Run: pip install -e . in the membersim directory")
    except Exception as e:
        print(f"\n✗ Error: {e}")
        raise


if __name__ == "__main__":
    main()
