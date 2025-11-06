# FAIR metadata annotation reporting tool

We want to create a simple report tool for annotators that have created annotation and are about to upload it to e.g. ENA.

We assume that they have metadata according to the schema that is being worked on in another work track in our project

This tool is aimed at single researchers and small institutions.

## Requirements

-   Tool should be very easy to use for non-technical people. To facilitate this, it should be accessed through a web GUI
    
-   Additionally, should be usable as a command line tool
    
-   Tool should take annotation metadata CSV as primary input
    
-   On top it can accept AGAT output
    
-   On top it can accept Busco output
    
-   Tool should produce a report in PDF format
    
-   Additionally, other output formats should be provided - e.g. JSON
    
-   The tool should not run any significant workflows itself. Instead it should accept the text output from longer running tools (e.g. Omark)

# How to run

Currently, this is supposed to be run as a CLI tool.

Assuming a Linux-like environment, make sure you have perl, duckdb and typst in your
path.

git clone this repo, then from this directory, run:

    reporter.pl -m dtol_metadata.csv

This should produce a report.pdf output file.

# TODO

- Notes on how to run the tools to produce the right output in the right format.
    AGAT, Busco, etc.
