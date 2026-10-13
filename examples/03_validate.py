"""Validate USDM JSON against the DDF rules with the usdm4 (d4k) validator.

Needs output/cdisc_pilot.json, so run 01_excel_to_json.py first.
"""

from banner import header, section, step

# Header first, so something prints while the packages load.
header(3, "Validate", "Check the USDM JSON against the DDF rules (d4k validator)")

from pathlib import Path  # noqa: E402

from usdm4 import USDM4  # noqa: E402
from usdm4.rules.results import RuleStatus  # noqa: E402

ROOT = Path(__file__).resolve().parent.parent
STUDY = ROOT / "output" / "cdisc_pilot.json"


def main() -> int:
    step(f"Validating {STUDY.name}")
    results = USDM4().validate(str(STUDY))

    section("Summary")
    print(f"Rules run: {results.count()}")
    for status in RuleStatus:
        print(f"  {status.value}: {len(results.by_status(status))}")

    # Each failed rule carries its own error log, one entry per finding.
    section("Failed rules")
    for outcome in results.by_status(RuleStatus.FAILURE):
        findings = outcome.errors.to_dict()
        first = findings[0]["message"].splitlines()[0] if findings else ""
        print(f"{outcome.rule_id} ({outcome.error_count}): {first}")

    print("\nPassed" if results.passed_or_not_implemented() else "\nFailed")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
