"""Use the usdm4 builder to create codes and USDM objects."""

from banner import header, section, step

# Header first, so something prints while the packages load.
header(5, "Builder", "Create codes and USDM objects with the usdm4 builder")

from simple_error_log.errors import Errors  # noqa: E402
from usdm4 import USDM4  # noqa: E402
from usdm4.api.study_epoch import StudyEpoch  # noqa: E402


def main() -> int:
    errors = Errors()
    builder = USDM4().builder(errors)

    # Codes from CDISC CT, by C-code, or by class and attribute plus a preferred term.
    # The first lookup loads the terminology.
    step("Loading CDISC CT (~10s)")
    title_type = builder.cdisc_code("C207616", "Official Study Title")
    epoch_type = builder.klass_and_attribute_value("StudyEpoch", "type", "Treatment Epoch")
    section("Codes")
    print(f"Title type: {title_type.code} {title_type.decode}")
    print(f"Epoch type: {epoch_type.code} {epoch_type.decode}")

    # ISO 3166 countries and ISO 639 languages.
    country = builder.iso3166_code("DNK")
    language = builder.iso639_code("en")
    print(f"Country:    {country.code} {country.decode}")
    print(f"Language:   {language.code} {language.decode}")

    # Any USDM class. The builder assigns the id and records it for cross-references.
    section("Object")
    epoch = builder.create(
        StudyEpoch,
        {"name": "TREATMENT", "label": "Treatment", "type": epoch_type},
    )
    print(f"Epoch:      {epoch.id} {epoch.name}")
    print(epoch.model_dump_json(indent=2))

    print(f"Errors: {errors.error_count()}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
