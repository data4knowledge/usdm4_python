"""Extract USDM from a legacy PDF protocol with usdm4_protocol and Claude, then export it to Excel.

Needs an Anthropic API key, in ANTHROPIC_API_KEY or in a .development_env file
in the repository root. A Gemini key, GEMINI_API_KEY, is optional: with it the
inclusion and exclusion criteria are voted on by Claude and Gemini together.
The extraction calls the AI many times, so it takes a few minutes and costs a
little.
"""

from banner import header, section, step

# Header first, so something prints while the packages load.
header(
    8,
    "PDF to USDM",
    "Extract USDM from the CDISC Pilot PDF with Claude, then export it to Excel",
    packages=["usdm4", "usdm4_excel", "usdm4_protocol"],
)

import json  # noqa: E402
from pathlib import Path  # noqa: E402

from d4k_ms_base.service_environment import ServiceEnvironment  # noqa: E402
from simple_error_log.errors import Errors  # noqa: E402
from usdm4_excel import USDM4Excel  # noqa: E402
from usdm4_protocol import USDM4Protocol  # noqa: E402

ROOT = Path(__file__).resolve().parent.parent
PROTOCOL = ROOT / "data" / "cdisc_pilot" / "CDISC_Pilot_Study.pdf"
OUTPUT = ROOT / "output" / "cdisc_pilot_pdf.json"
WORKBOOK = ROOT / "output" / "cdisc_pilot_pdf.xlsx"
ERRORS = ROOT / "output" / "cdisc_pilot_pdf_errors.json"


def main() -> int:
    # The AI extraction reads the key from the environment, or from .development_env.
    if not ServiceEnvironment().get("ANTHROPIC_API_KEY"):
        print("No ANTHROPIC_API_KEY set. Put it in the environment or in .development_env")
        return 1

    gemini = "with Gemini for the criteria" if ServiceEnvironment().get("GEMINI_API_KEY") else "no Gemini key"
    step(f"Extracting {PROTOCOL.name} with Claude, {gemini} (a few minutes)")
    protocol = USDM4Protocol()
    wrapper = protocol.from_pdf(str(PROTOCOL), pdf_converter="pymupdf")

    # The error log is as useful as the study. Keep everything, warnings and info too.
    errors = protocol.errors
    OUTPUT.parent.mkdir(exist_ok=True)
    ERRORS.write_text(json.dumps(errors.to_dict(level=Errors.INFO), indent=2))

    section("Extraction")
    print(f"Errors: {errors.error_count()}  ·  log entries: {errors.count()}")
    for item in errors.to_dict(level=Errors.ERROR):
        print(f"  {item['message'].splitlines()[0]}")
    print(f"Written: {ERRORS.relative_to(ROOT)}")

    if wrapper is None:
        print("No study could be extracted")
        return 1

    OUTPUT.write_text(wrapper.model_dump_json(indent=2))
    print(f"Written: {OUTPUT.relative_to(ROOT)}")

    version = wrapper.study.versions[0]
    design = version.studyDesigns[0]

    section("Study")
    print(f"Title:       {version.official_title_text()}")
    print(f"Sponsor:     {version.sponsor_name()} ({version.sponsor_identifier_text()})")
    print(f"Arms:        {len(design.arms)}")
    print(f"Epochs:      {', '.join(e.label for e in design.epochs)}")
    print(f"Encounters:  {len(design.encounters)}")
    print(f"Activities:  {len(design.activities)}")
    print(f"Timelines:   {len(design.scheduleTimelines)}")
    print(f"Criteria:    {len(design.eligibilityCriteria)}")
    print(f"Objectives:  {len(design.objectives)}")
    print(f"Sections:    {len(version.narrativeContentItems)}")

    # The same study as a usdm4_excel workbook, so it can be read and corrected by hand.
    step(f"Exporting {OUTPUT.name} to {WORKBOOK.name}")
    USDM4Excel().to_excel(str(OUTPUT), str(WORKBOOK))
    print(f"Written: {WORKBOOK.relative_to(ROOT)}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
