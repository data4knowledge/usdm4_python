"""Create the minimum valid USDM study with usdm4 and save it as JSON."""

from pathlib import Path

from simple_error_log.errors import Errors
from usdm4 import USDM4

ROOT = Path(__file__).resolve().parent.parent
OUTPUT = ROOT / "output" / "minimum.json"


def main() -> int:
    errors = Errors()
    wrapper = USDM4().minimum("Example Study", "EX-001", "1", errors)
    if wrapper is None:
        print(f"Failed, errors: {errors.error_count()}")
        return 1

    version = wrapper.study.versions[0]
    print(f"Title:   {version.official_title_text()}")
    print(f"Sponsor: {version.sponsor_name()} ({version.sponsor_identifier_text()})")
    print(f"Designs: {len(version.studyDesigns)}")

    OUTPUT.parent.mkdir(exist_ok=True)
    OUTPUT.write_text(wrapper.model_dump_json(indent=2))
    print(f"Written: {OUTPUT.relative_to(ROOT)}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
