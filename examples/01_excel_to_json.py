"""Import the CDISC Pilot workbook with usdm4_excel and save it as USDM JSON.

Run from the repository root:  python examples/01_excel_to_json.py
"""

from banner import header, section, step

# Header first, so something prints while the packages load.
header(1, "Excel to JSON", "Import the CDISC Pilot workbook and save it as USDM JSON")

from pathlib import Path  # noqa: E402

from usdm4_excel import USDM4Excel  # noqa: E402

ROOT = Path(__file__).resolve().parent.parent
WORKBOOK = ROOT / "data" / "cdisc_pilot" / "CDISC_Pilot_Study.xlsx"
OUTPUT = ROOT / "output" / "cdisc_pilot.json"


def main() -> int:
    step(f"Importing {WORKBOOK.name} (loads CDISC CT first, ~10s)")
    excel = USDM4Excel()
    wrapper = excel.from_excel(str(WORKBOOK))

    # Every problem is logged, with the sheet, row and column where it was found.
    section("Import")
    errors = excel.errors()
    print(f"Errors: {errors.error_count()}")
    for item in errors.to_dict(level=errors.ERROR):
        print(f"  {item['location']}: {item['message'].splitlines()[0]}")

    if wrapper is None:
        print("No study could be built")
        return 1

    OUTPUT.parent.mkdir(exist_ok=True)
    OUTPUT.write_text(wrapper.model_dump_json(indent=2))
    print(f"Written: {OUTPUT.relative_to(ROOT)}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
