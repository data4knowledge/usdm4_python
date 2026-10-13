"""Export USDM JSON to Excel with usdm4_excel, then import it again.

Needs output/cdisc_pilot.json, so run 01_excel_to_json.py first.
"""

from pathlib import Path

from simple_error_log.errors import Errors
from usdm4 import USDM4
from usdm4_excel import USDM4Excel

ROOT = Path(__file__).resolve().parent.parent
STUDY = ROOT / "output" / "cdisc_pilot.json"
WORKBOOK = ROOT / "output" / "cdisc_pilot_export.xlsx"


def summary(wrapper) -> dict:
    design = wrapper.study.versions[0].studyDesigns[0]
    return {
        "arms": len(design.arms),
        "epochs": len(design.epochs),
        "encounters": len(design.encounters),
        "activities": len(design.activities),
        "objectives": len(design.objectives),
        "timelines": len(design.scheduleTimelines),
    }


def main() -> int:
    excel = USDM4Excel()
    excel.to_excel(str(STUDY), str(WORKBOOK))
    print(f"Written: {WORKBOOK.relative_to(ROOT)}")

    # Round trip: read the exported workbook back and compare with the original.
    original = USDM4().load(str(STUDY), Errors())
    again = excel.from_excel(str(WORKBOOK))
    print(f"Re-import errors: {excel.errors().error_count()}")
    before, after = summary(original), summary(again)
    for key in before:
        flag = "" if before[key] == after[key] else "  <-- differs"
        print(f"  {key:12} {before[key]:4} {after[key]:4}{flag}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
