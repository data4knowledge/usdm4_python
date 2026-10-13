"""Export USDM JSON to Excel with usdm4_excel, then import it again.

Needs output/cdisc_pilot.json, so run 01_excel_to_json.py first.
"""

from banner import header, section, step

# Header first, so something prints while the packages load.
header(6, "JSON to Excel", "Export the USDM JSON to Excel, then import it again")

from pathlib import Path  # noqa: E402

from simple_error_log.errors import Errors  # noqa: E402
from usdm4 import USDM4  # noqa: E402
from usdm4_excel import USDM4Excel  # noqa: E402

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
    step(f"Exporting {STUDY.name} to {WORKBOOK.name}")
    excel = USDM4Excel()
    excel.to_excel(str(STUDY), str(WORKBOOK))

    # Round trip: read the exported workbook back and compare with the original.
    step(f"Importing {WORKBOOK.name} again (loads CDISC CT first, ~10s)")
    original = USDM4().load(str(STUDY), Errors())
    again = excel.from_excel(str(WORKBOOK))

    section("Round trip")
    print(f"Written: {WORKBOOK.relative_to(ROOT)}")
    print(f"Re-import errors: {excel.errors().error_count()}")
    before, after = summary(original), summary(again)
    print(f"  {'':12} {'JSON':>4} {'xlsx':>4}")
    for key in before:
        flag = "" if before[key] == after[key] else "  <-- differs"
        print(f"  {key:12} {before[key]:4} {after[key]:4}{flag}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
