# usdm4_python

Small example programs for the USDM4 Python packages, `usdm4`, `usdm4_excel` and `usdm4_protocol`. They go with the *USDM and Python* training course.

## Setup

Python 3.12 or later.

```bash
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

## Examples

Run them from the repository root, in order. Examples 2, 3 and 6 read the JSON that example 1 writes. Examples 7 and 8 stand alone. Everything they write goes in `output/`, which git ignores.

| Program | Package | What it does |
|---------|---------|--------------|
| `examples/01_excel_to_json.py` | usdm4_excel | Imports the CDISC Pilot workbook and saves it as USDM JSON. Prints the error log. |
| `examples/02_explore_study.py` | usdm4 | Loads the JSON and walks the study: titles, sponsor, arms, epochs, objectives and endpoints. |
| `examples/03_validate.py` | usdm4 | Runs the d4k validator (the DDF rules in Python) and lists the rules that fail. |
| `examples/04_minimum_study.py` | usdm4 | Creates the minimum valid study and saves it as JSON. |
| `examples/05_builder.py` | usdm4 | Uses the builder for CDISC CT, ISO 3166 and ISO 639 codes and to create a USDM object. |
| `examples/06_json_to_excel.py` | usdm4_excel | Exports the JSON back to Excel, re-imports it and compares the two. |
| `examples/07_assembler.py` | usdm4 | Builds a complete study from one structured input with the assembler and saves it as JSON. |
| `examples/08_pdf_to_usdm.py` | usdm4_protocol | Extracts USDM from the CDISC Pilot PDF with Claude. Saves the JSON, the same study as Excel, and the error log. |

```bash
python examples/01_excel_to_json.py
```

`examples/banner.py` isn't an example. It prints the header and progress lines the examples share.

Programs that build or import a study take 10 to 15 seconds, most of it loading the controlled terminology. Loading and validating JSON takes a second or two.

Example 8 calls Claude, so it needs an Anthropic API key, in `ANTHROPIC_API_KEY` or in a `.development_env` file in the repository root (git ignores it). A Gemini key, `GEMINI_API_KEY`, is optional. With it, Claude and Gemini vote on the inclusion and exclusion criteria. It takes a few minutes.

## Data

`data/cdisc_pilot/` holds the CDISC Pilot study (LZZT): the protocol PDF, the USDM workbook and the trial schema image the workbook's document references. See [data/cdisc_pilot/README.md](data/cdisc_pilot/README.md) for where the workbook came from.
