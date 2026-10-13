"""Load USDM JSON with usdm4 and walk through the study.

Needs output/cdisc_pilot.json, so run 01_excel_to_json.py first.
"""

from pathlib import Path

from simple_error_log.errors import Errors
from usdm4 import USDM4

ROOT = Path(__file__).resolve().parent.parent
STUDY = ROOT / "output" / "cdisc_pilot.json"


def main() -> int:
    errors = Errors()
    wrapper = USDM4().load(str(STUDY), errors)
    if wrapper is None:
        print(f"Failed to load {STUDY}, errors: {errors.error_count()}")
        return 1

    # A study has versions; the content lives in the version.
    version = wrapper.study.versions[0]
    print(f"Study:      {wrapper.study.name}")
    print(f"Title:      {version.official_title_text()}")
    print(f"Acronym:    {version.acronym_text()}")
    print(f"Sponsor:    {version.sponsor_name()} ({version.sponsor_identifier_text()})")
    print(f"Phase:      {version.phases()}")

    # The version holds one or more study designs: arms, epochs, objectives, the SoA.
    for design in version.studyDesigns:
        print(f"\nDesign: {design.name}")
        print(f"  Arms:       {', '.join(arm.name for arm in design.arms)}")
        print(f"  Epochs:     {', '.join(epoch.name for epoch in design.epochs)}")
        print(f"  Encounters: {len(design.encounters)}")
        print(f"  Activities: {len(design.activities)}")
        print(f"  Timelines:  {', '.join(t.name for t in design.scheduleTimelines)}")
        print("  Objectives:")
        for objective in design.objectives:
            print(f"    [{objective.level.decode}] {objective.text}")
            for endpoint in objective.endpoints:
                print(f"      - [{endpoint.level.decode}] {endpoint.text}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
