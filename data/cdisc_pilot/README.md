# CDISC Pilot Study (LZZT)

Xanomeline transdermal therapeutic system in mild to moderate Alzheimer's disease. The CDISC Pilot is a public example protocol.

| File | What it is |
|------|------------|
| `CDISC_Pilot_Study.pdf` | The protocol |
| `CDISC_Pilot_Study.xlsx` | The USDM workbook, in the `usdm4_excel` format |
| `study_design.png` | Trial schema image, pulled into the M11 document by an image macro in the workbook |

All three are copies from the `usdm_data` repository (`source_data/protocols/CDISC_Pilot/`), which is the master. Update them there first, then copy them here.

The workbook imports into `usdm4_excel` 0.10.0 with no errors. The imported study doesn't pass every DDF rule. `examples/03_validate.py` lists what fails.
