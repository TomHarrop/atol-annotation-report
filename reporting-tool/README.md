# FAIR metadata annotation reporting tool

We created a simple reporting tool for annotators that have created annotation and are about to upload it to e.g. ENA.

We assume that they have metadata according to the schema that is being worked on in another work track in our project.

This tool is aimed at single researchers and small institutions.

## Requirements

-   Tool should be very easy to use for non-technical people. To facilitate this, it should be accessed through a web GUI
    
-   Additionally, should be usable as a command line tool
    
-   Tool should take annotation metadata CSV / JSON as primary input
    
-   On top it can accept AGAT output
    
-   On top it can accept Busco output
    
-   Tool should produce a report in PDF format
    
-   Additionally, other output formats should be provided - e.g. JSON
    
-   The tool should not run any significant workflows itself. Instead it should accept the text output from longer running tools (e.g. Omark)

# How to run

Currently, this is supposed to be run as a CLI tool.

Assuming a Linux-like environment, make sure you have perl and typst in your
path.

git clone this repo, then from this directory, run:

    reporter.pl -m metadata.json -a agat.yaml -b  busco_short_summary.json

This should produce a report_main.json and a report.pdf output file.

# How to run with Docker

Build the Docker file like this:

    docker build --tag=reporter .

Then you run it like this. It will pick up files from the current directory and
also write output to the current directory.

    docker run --rm --volume "$(pwd):/data" --user $(id -u):$(id -g) reporter -m metadata.json -a agat.yaml -b busco_short_summary.json

You can make this nicer to run like this:

    alias reporter='docker run --rm --volume "$(pwd):/data" --user $(id -u):$(id -g) reporter'

Now you would run it like this:

    reporter -m metadata.json -a agat.yaml -b busco_short_summary.json


# TODO

- We should add notes on how to run the tools (AGAT, Busco etc.) to produce the
    right output in the right format.
    We assume that this repo will have a pipeline (e.g. nextflow) in the future
    to provide this.
