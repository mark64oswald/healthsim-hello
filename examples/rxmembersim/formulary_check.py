"""
RxMemberSim Formulary and DUR Examples

This module demonstrates formulary and DUR operations:
- Checking drug coverage status
- Tier assignments and cost sharing
- PA and step therapy requirements
- Drug utilization review (DUR) screening
- Drug-drug interaction detection
"""

from datetime import date


def example_formulary_coverage():
    """Check coverage status for various drugs."""
    from rxmembersim.formulary.formulary import FormularyGenerator

    formulary = FormularyGenerator().generate_standard_commercial()

    print("=" * 60)
    print("FORMULARY COVERAGE CHECK")
    print("=" * 60)

    # Test drugs across different tiers
    test_drugs = [
        ("00093017101", "Metformin 500mg", "Generic diabetes"),
        ("00071015523", "Atorvastatin 10mg", "Generic statin"),
        ("00003089421", "Eliquis 5mg", "Brand anticoagulant"),
        ("00169413512", "Ozempic 0.5mg", "Specialty GLP-1"),
        ("00074433902", "Humira 40mg", "Specialty biologic"),
        ("99999999999", "Unknown Drug", "Not on formulary"),
    ]

    print("\nCoverage Status by Drug:")
    print("-" * 60)

    for ndc, name, category in test_drugs:
        status = formulary.check_coverage(ndc)

        print(f"\n{name} ({category})")
        print(f"  NDC: {ndc}")
        print(f"  Covered: {status.covered}")

        if status.covered:
            print(f"  Tier: {status.tier}")
            if hasattr(status, 'copay') and status.copay:
                print(f"  Copay: ${status.copay:.2f}")
            if hasattr(status, 'coinsurance') and status.coinsurance:
                print(f"  Coinsurance: {status.coinsurance}%")
            print(f"  Requires PA: {status.requires_pa}")
            print(f"  Step Therapy: {status.step_therapy}")
            if hasattr(status, 'quantity_limit') and status.quantity_limit:
                print(f"  Quantity Limit: {status.quantity_limit}")
        else:
            print(f"  Message: {status.message}")


def example_tier_structure():
    """Display formulary tier structure and cost sharing."""
    from rxmembersim.formulary.formulary import FormularyGenerator

    formulary = FormularyGenerator().generate_standard_commercial()

    print("\n" + "=" * 60)
    print("FORMULARY TIER STRUCTURE")
    print("=" * 60)

    tiers = [
        (1, "Preferred Generic", "$10 copay", "Metformin, Lisinopril, Atorvastatin"),
        (2, "Non-Preferred Generic", "$25 copay", "Gabapentin, Tramadol"),
        (3, "Preferred Brand", "$40 copay", "Eliquis, Jardiance"),
        (4, "Non-Preferred Brand", "$80 copay", "Lipitor, Nexium"),
        (5, "Specialty", "25% coinsurance", "Humira, Ozempic, Enbrel"),
    ]

    print("\nTier Structure:")
    print("-" * 60)
    print(f"{'Tier':<6} {'Category':<22} {'Cost Share':<15} {'Examples'}")
    print("-" * 60)

    for tier_num, category, cost_share, examples in tiers:
        print(f"{tier_num:<6} {category:<22} {cost_share:<15} {examples}")


def example_pa_requirements():
    """Check prior authorization requirements."""
    from rxmembersim.formulary.formulary import FormularyGenerator

    formulary = FormularyGenerator().generate_standard_commercial()

    print("\n" + "=" * 60)
    print("PRIOR AUTHORIZATION REQUIREMENTS")
    print("=" * 60)

    # PA-required drugs
    pa_drugs = [
        ("00169413512", "Ozempic 0.5mg", "GLP-1 agonist"),
        ("00074433902", "Humira 40mg", "Biologic"),
        ("61958060101", "Wegovy 0.25mg", "Weight loss"),
        ("00002141080", "Trulicity 1.5mg", "GLP-1 agonist"),
    ]

    print("\nPA-Required Medications:")
    print("-" * 60)

    for ndc, name, category in pa_drugs:
        status = formulary.check_coverage(ndc)
        print(f"\n{name}")
        print(f"  Category: {category}")
        print(f"  PA Required: {status.requires_pa}")
        print(f"  Step Therapy: {status.step_therapy}")

    print("\nCommon PA Criteria:")
    print("-" * 60)
    print("GLP-1 Agonists:")
    print("  - A1c >= 7.0% documented within 90 days")
    print("  - Failed metformin trial (minimum 3 months)")
    print("  - Type 2 Diabetes diagnosis (E11.*)")
    print("\nBiologics:")
    print("  - Failed conventional therapy")
    print("  - Specialist confirmation")
    print("  - Appropriate diagnosis")


def example_dur_screening():
    """Demonstrate DUR screening for drug interactions."""
    from rxmembersim.dur.validator import DURValidator
    from rxmembersim.core.member import RxMemberGenerator

    validator = DURValidator()
    gen = RxMemberGenerator(seed=42)
    member = gen.generate(bin="610014", pcn="RXTEST", group_number="GRP001")

    print("\n" + "=" * 60)
    print("DUR SCREENING - DRUG INTERACTIONS")
    print("=" * 60)

    # Test Warfarin + NSAID interaction
    print("\nScenario: Warfarin + NSAID (Ibuprofen)")
    print("-" * 60)

    result = validator.validate_simple(
        ndc="00056017270",
        gpi="83300010000330",  # Warfarin
        drug_name="Warfarin 5mg",
        member_id=member.member_id,
        service_date=date.today(),
        current_medications=[
            {
                "ndc": "00904515260",
                "gpi": "66100010000310",
                "name": "Ibuprofen 200mg",
            }
        ],
        patient_age=65,
        patient_gender="F",
    )

    print(f"DUR Passed: {result.passed}")
    print(f"Total Alerts: {result.total_alerts}")

    if not result.passed and result.alerts:
        for alert in result.alerts:
            print(f"\nAlert Details:")
            print(f"  Type: {alert.alert_type}")
            print(f"  Severity: Level {alert.severity}")
            print(f"  Message: {alert.message}")
            if hasattr(alert, 'conflicting_drug'):
                print(f"  Conflicting Drug: {alert.conflicting_drug}")


def example_therapeutic_duplication():
    """Test therapeutic duplication detection."""
    from rxmembersim.dur.validator import DURValidator
    from rxmembersim.core.member import RxMemberGenerator

    validator = DURValidator()
    gen = RxMemberGenerator(seed=42)
    member = gen.generate(bin="610014", pcn="RXTEST", group_number="GRP001")

    print("\n" + "=" * 60)
    print("DUR SCREENING - THERAPEUTIC DUPLICATION")
    print("=" * 60)

    # Test duplicate statin therapy
    print("\nScenario: Two Statins (Atorvastatin + Rosuvastatin)")
    print("-" * 60)

    result = validator.validate_simple(
        ndc="00078057715",
        gpi="39400020000310",  # Rosuvastatin
        drug_name="Rosuvastatin 10mg",
        member_id=member.member_id,
        service_date=date.today(),
        current_medications=[
            {
                "ndc": "00071015523",
                "gpi": "39400010000310",
                "name": "Atorvastatin 10mg",
            }
        ],
        patient_age=55,
        patient_gender="M",
    )

    print(f"DUR Passed: {result.passed}")
    print(f"Total Alerts: {result.total_alerts}")

    if not result.passed and result.alerts:
        for alert in result.alerts:
            print(f"\nAlert Details:")
            print(f"  Type: {alert.alert_type}")
            print(f"  Message: {alert.message}")


def example_age_gender_alerts():
    """Test age and gender-related DUR alerts."""
    from rxmembersim.dur.validator import DURValidator
    from rxmembersim.core.member import RxMemberGenerator

    validator = DURValidator()
    gen = RxMemberGenerator(seed=42)
    member = gen.generate(bin="610014", pcn="RXTEST", group_number="GRP001")

    print("\n" + "=" * 60)
    print("DUR SCREENING - AGE/GENDER ALERTS")
    print("=" * 60)

    # Test NSAID in elderly
    print("\nScenario: NSAID in Elderly Patient (82 years)")
    print("-" * 60)

    result = validator.validate_simple(
        ndc="00904515260",
        gpi="66100010000310",
        drug_name="Ibuprofen 800mg",
        member_id=member.member_id,
        service_date=date.today(),
        current_medications=[],
        patient_age=82,
        patient_gender="F",
    )

    print(f"DUR Passed: {result.passed}")
    print(f"Total Alerts: {result.total_alerts}")

    if not result.passed and result.alerts:
        for alert in result.alerts:
            print(f"\nAlert Details:")
            print(f"  Type: {alert.alert_type}")
            print(f"  Severity: Level {alert.severity}")
            print(f"  Message: {alert.message}")

    # Test gender contraindication
    print("\nScenario: Finasteride in Female Patient")
    print("-" * 60)

    result = validator.validate_simple(
        ndc="00006011731",
        gpi="24100070100310",
        drug_name="Finasteride 5mg",
        member_id=member.member_id,
        service_date=date.today(),
        current_medications=[],
        patient_age=35,
        patient_gender="F",
    )

    print(f"DUR Passed: {result.passed}")
    print(f"Total Alerts: {result.total_alerts}")

    if not result.passed and result.alerts:
        for alert in result.alerts:
            print(f"\nAlert Details:")
            print(f"  Type: {alert.alert_type}")
            print(f"  Severity: Level {alert.severity}")
            print(f"  Message: {alert.message}")


def example_clean_prescription():
    """Show a clean prescription with no DUR alerts."""
    from rxmembersim.dur.validator import DURValidator
    from rxmembersim.core.member import RxMemberGenerator

    validator = DURValidator()
    gen = RxMemberGenerator(seed=42)
    member = gen.generate(bin="610014", pcn="RXTEST", group_number="GRP001")

    print("\n" + "=" * 60)
    print("CLEAN PRESCRIPTION (NO ALERTS)")
    print("=" * 60)

    result = validator.validate_simple(
        ndc="00071015523",
        gpi="39400010000310",
        drug_name="Atorvastatin 10mg",
        member_id=member.member_id,
        service_date=date.today(),
        current_medications=[],  # No other meds
        patient_age=55,
        patient_gender="M",
        quantity=30,
        days_supply=30,
    )

    print(f"\nDrug: Atorvastatin 10mg")
    print(f"Patient: 55-year-old male")
    print(f"Current Meds: None")
    print(f"\nDUR Passed: {result.passed}")
    print(f"Total Alerts: {result.total_alerts}")

    if result.passed:
        print("\nThis is a 'clean' prescription:")
        print("  - No current medications (no interactions)")
        print("  - Appropriate age")
        print("  - Appropriate gender")
        print("  - Standard dose")
        print("  - Not an early refill")


def main():
    """Run all examples."""
    print("\n" + "=" * 60)
    print("RXMEMBERSIM FORMULARY & DUR EXAMPLES")
    print("=" * 60)

    try:
        example_formulary_coverage()
        example_tier_structure()
        example_pa_requirements()
        example_dur_screening()
        example_therapeutic_duplication()
        example_age_gender_alerts()
        example_clean_prescription()

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
