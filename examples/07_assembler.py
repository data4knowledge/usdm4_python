"""Assemble a complete USDM study from one structured input with the usdm4 assembler.

Written for usdm4 0.30.0, whose SoA input is structured column by column. The
0.29.0 SoA input won't load here.
"""

from banner import header, section, step

# Header first, so something prints while the packages load.
header(7, "Assembler", "Build a complete USDM study from one structured input")

from pathlib import Path  # noqa: E402

from simple_error_log.errors import Errors  # noqa: E402
from usdm4 import USDM4  # noqa: E402

ROOT = Path(__file__).resolve().parent.parent
OUTPUT = ROOT / "output" / "assembled_study.json"

# The assembler input. Plain text in, the way a protocol says it. The assembler
# turns the text into CDISC codes, creates the ids and wires up the references.
# Things refer to each other by name: an arm names its interventions, a cell
# names its arm and epoch, an estimand names its endpoint.

# Titles, identifiers and organisations.
IDENTIFICATION = {
    "titles": {
        "official": "A Phase 2, Randomised, Double-Blind, Placebo-Controlled Study of "
        "Examplinib in Adults with Mild to Moderate Hypertension",
        "brief": "Examplinib in Hypertension",
        "acronym": "EXAMPLE-BP",
    },
    "identifiers": [
        # The sponsor's own number. A role of "sponsor" makes this organisation the sponsor.
        {
            "identifier": "EXP-2026-01",
            "scope": {
                "non_standard": {
                    "type": "pharma",
                    "role": "sponsor",
                    "name": "EXAMPLE PHARMA",
                    "label": "Example Pharma A/S",
                    "identifier": "123456789",
                    "identifierScheme": "DUNS",
                    "legalAddress": {
                        "lines": ["1 Example Street"],
                        "city": "Copenhagen",
                        "postalCode": "2100",
                        "country": "DNK",
                    },
                }
            },
        },
        # Registries and regulators are built in: "nct", "ema", "fda-ind", "jrct", ...
        {"identifier": "NCT09999999", "scope": {"standard": "nct"}},
    ],
    "other": {"sponsor_signatory": "Dr Jane Example, Chief Medical Officer"},
}

# The protocol document and its sections.
DOCUMENT = {
    "document": {
        "label": "EXAMPLE-BP Protocol",
        "version": "1.0",
        "status": "Final",
        "template": "ICH M11",
        "version_date": "2026-09-01",
    },
    "sections": [
        {"section_number": "1", "section_title": "Protocol Summary", "text": ""},
        {
            "section_number": "1.1",
            "section_title": "Synopsis",
            "text": "<p>Adults with hypertension receive examplinib or placebo for 8 weeks.</p>",
        },
        {
            "section_number": "2",
            "section_title": "Introduction",
            "text": "<p>Examplinib is a new oral treatment for hypertension.</p>",
        },
    ],
}

# Who takes part.
POPULATION = {
    "label": "Adults with mild to moderate hypertension",
    "planned_enrollment": 120,
    "demographics": {"age_min": 18, "age_max": 75, "age_unit": "Years", "sex": "ALL"},
    "inclusion_exclusion": {
        # Plain text, or a dict when the protocol's numbering matters.
        "inclusion": [
            {"identifier": "1", "text": "Aged 18 to 75 years at screening."},
            {"identifier": "2", "text": "Seated systolic blood pressure of 140 to 179 mmHg."},
        ],
        "exclusion": [
            {"identifier": "1", "text": "Secondary hypertension."},
            {"identifier": "2", "text": "Pregnant or breastfeeding."},
        ],
    },
}

# Arms, interventions and products.
STUDY_DESIGN = {
    "label": "Parallel group design",
    "rationale": "A placebo control gives the clearest estimate of the effect on blood pressure.",
    "trial_phase": "Phase 2",
    "intervention_model": "Parallel",
    "products": [
        {
            "name": "Examplinib 10 mg tablet",
            "dose_form": "Tablet",
            "product_designation": "IMP",
            "substances": [{"name": "Examplinib", "strength": "10 mg"}],
        },
        {"name": "Placebo tablet", "dose_form": "Tablet", "product_designation": "IMP"},
    ],
    "interventions": [
        {
            "name": "Examplinib",
            "type": "Drug",
            "role": "Experimental Intervention",
            "administrations": [
                {
                    "dose": "10 mg",
                    "route": "Oral",
                    "frequency": "Once daily",
                    "duration": {"quantity": "8 weeks"},
                    "product_name": "Examplinib 10 mg tablet",
                }
            ],
        },
        {
            "name": "Placebo",
            "type": "Drug",
            "role": "Placebo",
            "administrations": [
                {
                    "dose": "1 tablet",
                    "route": "Oral",
                    "frequency": "Once daily",
                    "duration": {"quantity": "8 weeks"},
                    "product_name": "Placebo tablet",
                }
            ],
        },
    ],
    "arms": [
        {"name": "Examplinib", "type": "Experimental Arm", "intervention_names": ["Examplinib"], "planned_enrollment": 60},
        {"name": "Placebo", "type": "Placebo Comparator Arm", "intervention_names": ["Placebo"], "planned_enrollment": 60},
    ],
    # No "cells" given, so the assembler builds the arm x epoch grid itself.
}

# The schedule of activities: a list of timelines, one entry per printed table.
# Each column carries its own structured header values: epoch, visit, timing
# and window. "text" is the header as printed and becomes the label. Activities
# list the cells they have, by column id. A footnote marker on a cell ("a")
# links the footnote to that activity at that visit.
def column(id, visit, epoch, day, label, window=0):
    return {
        "id": id,
        "epoch": {"text": epoch},
        "visit": {"text": visit},
        "timing": {"text": label, "value": day, "unit": "days"},
        "window": {"before": window, "after": window, "unit": "days"},
    }


def cells(*ids, markers=None):
    return [{"column": c, "text": "X", "markers": (markers or {}).get(c, [])} for c in ids]


SOA = [
    {
        "type": "main",
        "title": "Main schedule",
        "columns": [
            column("V1", "Visit 1", "Screening", -14, "Day -14"),
            column("V2", "Visit 2", "Treatment", 1, "Day 1"),
            column("V3", "Visit 3", "Treatment", 29, "Week 4", window=3),
            column("V4", "Visit 4", "Treatment", 57, "Week 8", window=3),
            column("V5", "Visit 5", "Follow-up", 71, "Week 10", window=3),
        ],
        "activities": [
            {"name": "Informed consent", "cells": cells("V1", markers={"V1": ["a"]})},
            {"name": "Eligibility", "cells": cells("V1", "V2")},
            # Named Biomedical Concepts come from the CDISC library. Anything else becomes a surrogate.
            {
                "name": "Vital signs",
                "cells": cells("V1", "V2", "V3", "V4", "V5"),
                "bcs": ["Systolic Blood Pressure", "Diastolic Blood Pressure", "Heart Rate"],
            },
            {"name": "Body weight", "cells": cells("V1", "V4"), "bcs": ["Body Weight"]},
            {"name": "Home BP diary", "cells": cells("V2", "V3", "V4"), "bcs": ["Home BP diary review"]},
            {"name": "Dispense study drug", "cells": cells("V2", "V3")},
        ],
        "footnotes": [{"marker": "a", "text": "Before any study procedure is done."}],
    }
]

# Objectives, endpoints and an estimand.
OBJECTIVES = {
    "objectives": [
        {
            "text": "To assess the effect of examplinib on systolic blood pressure.",
            "level": "Primary",
            "endpoints": [
                {
                    "name": "SBP change",
                    "text": "Change from baseline in seated systolic blood pressure at Week 8.",
                    "level": "Primary",
                }
            ],
        },
        {
            "text": "To assess the safety and tolerability of examplinib.",
            "level": "Secondary",
            "endpoints": [{"text": "Incidence of adverse events.", "level": "Secondary"}],
        },
    ],
    "estimands": [
        {
            "endpoint_name": "SBP change",
            "treatment_names": ["Examplinib", "Placebo"],
            "summary_measure": "Difference in mean change from baseline",
            "population_text": "All randomised participants",
            "intercurrent_events": [
                {"text": "Rescue medication", "strategy": "Treatment policy"},
            ],
        }
    ],
}

# The study and this version of it.
STUDY = {
    "name": {"acronym": "EXAMPLE-BP"},
    "version": "1",
    "rationale": "Original protocol.",
    "sponsor_approval_date": "2026-09-01",
    "confidentiality": "Confidential",
    "original_protocol": "Yes",
}

INPUT = {
    "identification": IDENTIFICATION,
    "document": DOCUMENT,
    "population": POPULATION,
    "study_design": STUDY_DESIGN,
    "soa": SOA,
    "objectives": OBJECTIVES,
    "study": STUDY,
    # "amendments" is the one block left out. An original protocol has none.
}


def main() -> int:
    errors = Errors()
    assembler = USDM4().assembler(errors)

    step("Assembling the study (loads CDISC CT first, ~10s)")
    assembler.execute(INPUT)
    wrapper = assembler.wrapper("usdm4_python example", "1.0")
    if wrapper is None or assembler.study is None:
        print(f"Failed, errors: {errors.error_count()}")
        print(errors.dump())
        return 1

    version = wrapper.study.versions[0]
    design = version.studyDesigns[0]
    timeline = design.scheduleTimelines[0]

    section("Study")
    print(f"Title:      {version.official_title_text()}")
    print(f"Sponsor:    {version.sponsor_name()} ({version.sponsor_identifier_text()})")
    print(f"Phase:      {design.studyPhase.standardCode.decode}")
    print(f"Model:      {design.model.decode}")
    for identifier in version.studyIdentifiers:
        print(f"Identifier: {identifier.text}")

    section("Design")
    print(f"Arms:          {', '.join(f'{a.label} ({a.type.decode})' for a in design.arms)}")
    print(f"Epochs:        {', '.join(e.label for e in design.epochs)}")
    print(f"Cells:         {len(design.studyCells)} (arm x epoch, built by the assembler)")
    for intervention in version.studyInterventions:
        for admin in intervention.administrations:
            print(f"Intervention:  {intervention.label}, {admin.dose.value:g} {admin.dose.unit.standardCode.decode if admin.dose.unit else ''}, "
                  f"{admin.route.standardCode.decode}, {admin.frequency.standardCode.decode}")
    print(f"Products:      {', '.join(p.name for p in version.administrableProducts)}")
    print(f"Population:    {design.population.label}, {len(design.eligibilityCriteria)} criteria")

    section("Schedule")
    print(f"Timeline:      {timeline.label}, {len(timeline.instances)} timepoints")
    for timing in timeline.timings:
        window = f" window {timing.windowLabel}" if timing.windowLabel else ""
        print(f"  {timing.label:<8} {timing.type.decode:<16} {timing.value}{window}")
    print(f"Activities:    {', '.join(a.label for a in design.activities)}")
    print(f"BCs:           {', '.join(bc.name for bc in version.biomedicalConcepts)}")
    print(f"BC surrogates: {', '.join(bc.name for bc in version.bcSurrogates)}")
    print(f"Conditions:    {', '.join(c.text for c in version.conditions)}")

    section("Objectives")
    for objective in design.objectives:
        print(f"{objective.level.decode}: {objective.text}")
        for endpoint in objective.endpoints:
            print(f"  {endpoint.level.decode}: {endpoint.text}")
    for estimand in design.estimands:
        print(f"Estimand: {estimand.populationSummary}, {len(estimand.intercurrentEvents)} intercurrent event")

    section("Document")
    document = wrapper.study.documentedBy[0]
    print(f"Document:   {document.label}, version {document.versions[0].version}")
    print(f"Sections:   {len(version.narrativeContentItems)}")

    OUTPUT.parent.mkdir(exist_ok=True)
    OUTPUT.write_text(wrapper.model_dump_json(indent=2))
    print(f"\nWritten: {OUTPUT.relative_to(ROOT)}")
    print(f"Errors: {errors.error_count()}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
