# Annotation Reporting Tool

Generate a standard PDF report for genome annotations from metadata, AGAT
statistics, and results from BUSCO and OMArk assessment of the predicted
proteins.

## Installation

```
VERSION=v0.0.1
python3 -m pip install \
   "git+https://github.com/tomharrop/atol-annotation-report.git@${VERSION}"
```

## Usage

[python-reporter.py](/reporting-tool/python_reporter.py) takes as input:
 - 3 mandatory arguments:
    - `-m`: path to a JSON metadata file with metadata specified according to the Annotation Metadata Schema (link pending)
    - `-a`: path to a YAML AGAT output report file
    - `-b`: path to a JSON BUSCO output report file
    - `-om`: path to a JSON OMArk output report file
 - 1 optional argument:
    - `-o`: path to PDF report output (if not provided, the default is `"reporting-tool/dev/full_report.pdf"`)


### Full usage

```


```

## Outputs

[python-reporter.py](/reporting-tool/python_reporter.py) generates:
 - a PDF report listing the provided metadata and statistics generated in BUSCO and AGAT analyses in human-readable format
 - a JSON report with the same key-value pairs used to generate the PDF above
 - a JSON report containing a small subset of annotation metrics used in the AToL genome-note-lite pipeline



, combines values and statistics as a JSON file and uses that file to populate a typst template to 

This tool was originally created at the 2025 Biohackathon as part of Project 23: Streamlining Metadata for Biodiversity Genome Annotation (see [fairtracks/biohackathon-2025-project-23](https://github.com/fairtracks/biohackathon-2025-project-23)). Part of the goal of the project was to develop a tool which generates a report-style output summarising the results from QA a genome annotation, e.g. BUSCO, OMArk, and AGAT analyses.

This repo holds the original reporting tool as a Perl script, as well as an adapted reporting tool in Python which is being developed to simultaneously generate a subset of metadata and values which can be used as input to the Australian Tree of Life (AToL) genome-note-lite pipeline.

See the README [here](/reporting-tool)# FAIR metadata annotation reporting tool

The [reporter.pl](/reporting-tool/reporter.pl) script contains the original reporting tool generated as part of the 2025 Biohackathon.


The [python-reporter.py](/reporting-tool/python_reporter.py) script is an adaptation of the above script. It generates the same report from the same typst template file, and simultaneously generates an atol_report JSON file for use in the AToL genome note lite pipeline.
