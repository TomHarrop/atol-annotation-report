# Annotation Reporting Tool

Generate a standard PDF report for genome annotations from metadata, AGAT
statistics, and results from BUSCO and OMArk assessment of the predicted
proteins.

## Installation

Install the package with pip as follows.

```
VERSION=v0.1.0
python3 -m pip install \
   "git+https://github.com/tomharrop/atol-annotation-report.git@${VERSION}"
```

## Usage

```
atol-annotation-report \
   --metadata_file path/to/metadata.json \
   --agat_file path/to/agat.stats.yaml \
   --busco_file path/to/short_summary.specific.busco.json \
   --omark_file path/to/omark_summary.json
```

To run [atol-annotation-report](/reporting-tool/python_reporter.py) you need:

- a JSON file containing metadata according to the Annotation Metadata Schema
- a YAML file generated as output from an AGAT analysis on your annotation
  file. Generate this by running
  [AnnoOddities](https://github.com/EI-CoreBioinformatics/annooddities).

Optionally, you can include:

- a JSON file generated as output from a BUSCO analysis on your annotation file
- a JSON file generated as output from an OMArk analysis on your annotation
  file. The easiest way to produce is running
  [`atol-qc-annotation`](https://github.com/TomHarrop/atol-qc-annotation)


### Full usage

```
usage: atol-annotation-report [-h] -m METADATA_FILE -a AGAT_FILE -b BUSCO_FILE -om OMARK_FILE
                              [-o OUTPUT_FILE] [--json_atol JSON_ATOL] [--json_full JSON_FULL]

This tool generates a JSON and PDF report of annotation metadata and metric vaules from BUSCO, OMArk, and
AGAT evaulations for the purposes of QA

options:
  -h, --help            show this help message and exit

Input:
  -m METADATA_FILE, --metadata_file METADATA_FILE
                        a JSON file containing metadata according to the Annotation Metadata Schema
                        (default: None)
  -a AGAT_FILE, --agat_file AGAT_FILE
                        a YAML file generated as output from an AGAT analysis on your annotation file
                        (default: None)
  -b BUSCO_FILE, --busco_file BUSCO_FILE
                        a JSON file generated as output from a BUSCO analysis on your annotation file
                        (default: None)
  -om OMARK_FILE, --omark_file OMARK_FILE
                        a JSON file generated as output from an OMArk analysis on your annotation file
                        (default: None)

Output:
  -o OUTPUT_FILE, --output_file OUTPUT_FILE
                        Path to the output PDF report (default: test_out.pdf)
  --json_atol JSON_ATOL
                        Path to the output JSON data for Genome Note lite input (default: json_atol.json)
  --json_full JSON_FULL
                        Path to the output JSON data for all results (default: json_full.json)
```

## Outputs


- a PDF report listing the provided metadata and statistics generated in BUSCO
  and AGAT analyses in human-readable format
- a JSON report with the same key-value pairs used to generate the PDF above
- a JSON report containing a small subset of annotation metrics used in the
  AToL genome-note-lite pipeline

## How it works

`atol-annotation-report` combines values and statistics as a JSON file and uses
that file to populate a typst template.

This tool was originally created at the 2025 Biohackathon as part of Project
23: Streamlining Metadata for Biodiversity Genome Annotation (see
[fairtracks/biohackathon-2025-project-23](https://github.com/fairtracks/biohackathon-2025-project-23)).
Part of the goal of the project was to develop a tool which generates a
report-style output summarising the results from QA a genome annotation, e.g.
BUSCO, OMArk, and AGAT analyses.

This repo holds the reporting tool and simultaneously generates a subset of
metadata and values which can be used as input to the Australian Tree of Life
(AToL) genome-note-lite pipeline.

The [reporter.pl](./extras) script contains the original
reporting tool generated as part of the 2025 Biohackathon.

A prototype [web application](./src/atol_annotation_report/web_interface) is
also included.

[python-reporter.py](./src/atol_annotation_report/python_reporter.py) is an
adaptation of the above script. It generates the same report from the same
typst template file, and simultaneously generates an atol_report JSON file for
use in the AToL genome note lite pipeline.

