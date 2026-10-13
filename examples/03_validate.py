"""Validate USDM JSON against the DDF rules with the usdm4 (d4k) validator.

Needs output/cdisc_pilot.json, so run 01_excel_to_json.py first.
"""

from pathlib import Path

from usdm4 import USDM4
from usdm4.rules.results import RuleStatus

ROOT = Path(__file__).resolve().parent.parent
STUDY = ROOT / "output" / "cdisc_pilot.json"


def main() -> int:
    results = USDM4().validate(str(STUDY))

    print(f"Rules run: {results.count()}")
    for status in RuleStatus:
        print(f"  {status.value}: {len(results.by_status(status))}")

    # Each failed rule carries its own error log, one entry per finding.
    for outcome in results.by_status(RuleStatus.FAILURE):
        findings = outcome.errors.to_dict()
        first = findings[0]["message"].splitlines()[0] if findings else ""
        print(f"{outcome.rule_id} ({outcome.error_count}): {first}")

    print("Passed" if results.passed_or_not_implemented() else "Failed")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
