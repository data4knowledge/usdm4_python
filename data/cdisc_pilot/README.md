# CDISC Pilot Study (LZZT)

Xanomeline transdermal therapeutic system in mild to moderate Alzheimer's disease. The CDISC Pilot is a public example protocol.

| File | What it is |
|------|------------|
| `CDISC_Pilot_Study.pdf` | The protocol |
| `CDISC_Pilot_Study.xlsx` | The USDM workbook, in the `usdm4_excel` format |
| `study_design.png` | Trial schema image, pulled into the M11 document by an image macro in the workbook |

## Where the workbook came from

It started as the 2024 workbook in `usdm_data` (`source_data/protocols/CDISC_Pilot/`), written for the older `usdm` package. That version imports into `usdm4_excel` 0.10.0 with 311 errors, so this copy has been brought up to date. It now imports with no errors. The changes:

- **Document template sheets** (`lillyFormat`, `m11Format`). The section text moved to a new `documentContent` sheet. The template rows reference it by name in a `content` column and gain `displaySectionNumber` / `displaySectionTitle`. Every section gets a unique name.
- **Organisations.** `studyIdentifiers` used to carry the organisation details. They now sit on a new `studyOrganizations` sheet, and the identifiers reference the organisation by name. Organisation types use the v4 terms: `Pharmaceutical Company`, `Clinical Study Registry`, `Healthcare Facility`.
- **Sponsor.** In v4 the sponsor is a role. A new `roles` sheet makes Eli Lilly the Sponsor. The sponsor masking text moved there from the `studyDesign` sheet.
- **Sites.** `studyDesignSites` now names a site and references its managing organisation, which moved to `studyOrganizations`.
- **Study type and phase.** They moved from the `study` sheet to the `studyDesign` sheet. `trialTypes` is renamed `trialSubTypes`. The deprecated `studyTitle` row is gone.
- **CT terms.** Objective levels are `Trial Primary Objective` / `Trial Secondary Objective`. Governance date types are `Approval Date` / `Effective Date`.
- **Amendments.** The amendment row has a `name`.
- **Timelines.** A stray `-` in the Parent Activity column turned the ADAS-Cog row into a parent activity, which left every activity above it without a parent. It's been cleared.

The imported study doesn't pass every DDF rule. `examples/03_validate.py` lists what fails.
