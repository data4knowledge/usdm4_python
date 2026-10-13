"""Use the usdm4 builder to create codes and USDM objects."""

from simple_error_log.errors import Errors
from usdm4 import USDM4
from usdm4.api.study_epoch import StudyEpoch


def main() -> int:
    errors = Errors()
    builder = USDM4().builder(errors)

    # Codes from CDISC CT, by C-code, or by class and attribute plus a preferred term.
    title_type = builder.cdisc_code("C207616", "Official Study Title")
    epoch_type = builder.klass_and_attribute_value("StudyEpoch", "type", "Treatment Epoch")
    print(f"Title type: {title_type.code} {title_type.decode}")
    print(f"Epoch type: {epoch_type.code} {epoch_type.decode}")

    # ISO 3166 countries and ISO 639 languages.
    country = builder.iso3166_code("DNK")
    language = builder.iso639_code("en")
    print(f"Country:    {country.code} {country.decode}")
    print(f"Language:   {language.code} {language.decode}")

    # Any USDM class. The builder assigns the id and records it for cross-references.
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
