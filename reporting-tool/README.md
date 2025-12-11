# FAIR metadata annotation reporting tool

The [reporter.pl](/reporting-tool/reporter.pl) script contains the original reporting tool generated as part of the 2025 Biohackathon.

This script takes an annotation metadata file, an AGAT report file, and a BUSCO report file, combines values and statistics as a JSON file and uses that file to populate a typst template to generate a PDF report.

The [python-reporter.py](/reporting-tool/python_reporter.py) script is an adaptation of the above script. It generates the same report from the same typst template file, and simultaneously generates an atol_report JSON file for use in the AToL genome note lite pipeline.

## Input arguments

[python-reporter.py](/reporting-tool/python_reporter.py) takes as input:
 - 3 mandatory arguments:
    - `-m`: path to a JSON metadata file with metadata specified according to the Annotation Metadata Schema (link pending)
    - `-a`: path to a YAML AGAT output report file
    - `-b`: path to a JSON BUSCO output report file
    - `-om`: path to a JSON OMArk output report file
 - 1 optional argument:
    - `-o`: path to PDF report output (if not provided, the default is `"reporting-tool/dev/full_report.pdf"`)

## Outputs

[python-reporter.py](/reporting-tool/python_reporter.py) generates:
 - a PDF report listing the provided metadata and statistics generated in BUSCO and AGAT analyses in human-readable format
 - a JSON report with the same key-value pairs used to generate the PDF above
 - a JSON report containing a small subset of annotation metrics used in the AToL genome-note-lite pipeline
