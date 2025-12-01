#!/usr/bin/env python3

# this is a python version of the reporter.pl script.
# it takes a metadata json file, an agat yaml file, and a busco json file.
# this script parses and maps their content to fields in the annotation schema.
# the output is dumped into json_report.json.
# the json is used to populate the atol_report_template.typ during typst rendering.
# this generates a test-output.pdf

# this script simutaneously collects a subset ofdata for atol in atol_report.json.
# atol_report.json contains an object which can be fed straight into the genome-note-lite pipeline.

import json
import yaml
import subprocess
import argparse

argument_parser = argparse.ArgumentParser(description="This tool generates a JSON and PDF report of annotation metadata and metric vaules from BUSCO, OMArk, and AGAT evaulations for the purposes of QA")
argument_parser.add_argument("-m", "--metadata_file", help="a JSON file containing metadata according to the Annotation Metadata Schema")
argument_parser.add_argument("-a", "--agat_file", help="a YAML file generated as output from an AGAT analysis on your annotation file")
argument_parser.add_argument("-b", "--busco_file", help="a JSON file generated as output from a BUSCO analysis on your annotation file")
argument_parser.add_argument("-o", "--output_file", help="your desired report file address for the output PDF report")
args = argument_parser.parse_args()

json_atol_report = "reporting-tool/dev/atol_report.json"
json_full_report = "reporting-tool/dev/json_report.json"
path_to_template = "reporting-tool/atol_report_template.typ"

if args.output_file:
    output_pdf = args.output_file
else:
    output_pdf = "reporting-tool/dev/full_report.pdf"

# this dictionary will contain a json "annotation" object which can be inserted into the atol genome-note-lite input.
stats_for_gnl = {}

# TODO: review metadata.json and update to newer terms

if args.metadata_file:
    path_to_metadata = args.metadata_file
    print("Parsing metadata")

    with open(path_to_metadata, "rt") as f:
        metadata_input = json.load(f)
        all_metadata = {}
        for dict in metadata_input:
            key = dict['meta_key']
            value = dict['meta_value']
            all_metadata[key] = value
else:
    print("No metadata file specified")
    all_metadata = {}

if args.agat_file:
    path_to_agat = args.agat_file

    # define mappings from agat yaml input to annotation schema fields
    key_agat_mappings = {
        'gene_count':'Number of gene',
        'transcript_count':'Number of transcript',
        'mean_transcript_length':'mean transcript length (bp)',
        'mean_transcripts_per_gene':'mean transcripts per gene',
        'mean_exons_per_transcript':'mean exons per transcript'
    }
    additional_agat_mappings = {
        'exon_count':'Number of exon',
        'mean_exon_length':'mean exon length (bp)',
        'mean_gene_length':'mean gene length (bp)',
        'total_gene_length':'Total gene length (bp)',
        'total_transcript_length':'Total transcript length (bp)'
    }
    full_stat_agat_mappings = {
        'cds_count':'Number of cds',
        'intron_count':'Number of intron',
        'single_exon_gene_count':'Number of single exon gene',
        'single_exon_transcript_count':'Number of single exon transcript'
    }
    mean_stat_agat_mappings = {
        'mean_cds_length':'mean cds length (bp)',
        'mean_intron_length':'mean intron length (bp)',
        'mean_cdss_per_transcript':'mean cdss per transcript',
        'mean_exons_per_cds':'mean exons per cds',
        'mean_introns_per_transcript':'mean introns per transcript'
    }
    median_stat_agat_mappings = {
        'median_gene_length':'median gene length (bp)',
        'median_transcript_length':'median transcript length (bp)',
        'median_exon_length':'median exon length (bp)',
        'median_cds_length':'median cds length (bp)',
        'median_intron_length':'median intron length (bp)'
    }
    long_short_agat_mappings = {
        'longest_gene':'Longest gene (bp)',
        'longest_transcript':'Longest transcript (bp)',
        'longest_exon':'Longest exon (bp)',
        'longest_cds':'Longest cds (bp)',
        'longest_intron':'Longest intron (bp)',
        'shortest_gene':'Shortest gene (bp)',
        'shortest_transcript':'Shortest transcript (bp)'
    }
    length_agat_mappings = {
        'total_cds_length':'Total cds length (bp)',
        'total_exon_length':'Total exon length (bp)',
        'total_intron_length':'Total intron length (bp)'
    }

    # TODO: parse and map AGAT software version and add to key_agat_mappings

    # parse AGAT yaml and map to new field names
    print("Parsing AGAT file")

    with open(path_to_agat, "rt") as f:
        key_agat_stats = {}
        all_agat_stats = {}
        full_agat_input = yaml.load(f, Loader=yaml.SafeLoader)
        agat_stats_input = full_agat_input['transcript']['without_isoforms']['value']
        for reporting_field, agat_field in key_agat_mappings.items():
            key_agat_stats[reporting_field] = agat_stats_input[agat_field]
        all_agat_stats.update(key_agat_stats)
        for reporting_field, agat_field in additional_agat_mappings.items():
            all_agat_stats[reporting_field] = agat_stats_input[agat_field]
        for reporting_field, agat_field in full_stat_agat_mappings.items():
            all_agat_stats[reporting_field] = agat_stats_input[agat_field]
        for reporting_field, agat_field in mean_stat_agat_mappings.items():
            all_agat_stats[reporting_field] = agat_stats_input[agat_field]
        for reporting_field, agat_field in median_stat_agat_mappings.items():
            all_agat_stats[reporting_field] = agat_stats_input[agat_field]
        for reporting_field, agat_field in long_short_agat_mappings.items():
            all_agat_stats[reporting_field] = agat_stats_input[agat_field]
        for reporting_field, agat_field in length_agat_mappings.items():
            all_agat_stats[reporting_field] = agat_stats_input[agat_field]

    agat_output = {'agat':all_agat_stats}

    stats_for_gnl.update(key_agat_stats)
else:
    print("No AGAT file specified")
    agat_output = {'agat':{}}

if args.busco_file:
    path_to_busco = args.busco_file

    # define mappings from BUSCO json input to annotation schema fields
    parameter_busco_mappings = {
        'mode':'mode',
        'gene_predictor':'gene_predictor'
    }
    lineage_busco_mappings = {
        'lineage_name':'name'
    }
    version_busco_mappings = {
        'version_busco':'busco',
        'version_hmmsearch':'hmmsearch',
        'version_metaeuk':'metaeuk'
    }
    result_busco_mappings = {
        'one_line_summary':'one_line_summary',
        'complete_percent':'Complete',
        'single_copy_percent':'Single copy',
        'duplicated_percent':'Multi copy',
        'fragmented_percent':'Fragmented',
        'missing_percent':'Missing',
        'n_markers':'n_markers',
        'domain':'domain'
    }
    # these are mappings from the annotation schema to the atol schema
    key_busco_mappings = {
        'annot_busco_mode':'mode',
        'annot_busco_lineage':'lineage_name',
        'annot_busco_summary':'one_line_summary'
    }

    # parse BUSCO json and map to new field names
    print("Parsing BUSCO file")

    with open(path_to_busco, "rt") as f:
        key_busco_stats = {}
        all_busco_stats = {}
        all_busco_input = json.load(f)
        busco_param_info = all_busco_input['parameters']
        busco_lineage_info = all_busco_input['lineage_dataset']
        busco_version_info = all_busco_input['versions']
        busco_result_info = all_busco_input['results']
        for reporting_field, busco_field in parameter_busco_mappings.items():
            all_busco_stats[reporting_field] = busco_param_info[busco_field]
        for reporting_field, busco_field in lineage_busco_mappings.items():
            all_busco_stats[reporting_field] = busco_lineage_info[busco_field]
        for reporting_field, busco_field in version_busco_mappings.items():
            all_busco_stats[reporting_field] = busco_version_info[busco_field]
        for reporting_field, busco_field in result_busco_mappings.items():
            all_busco_stats[reporting_field] = busco_result_info[busco_field]
        for atol_field, reporting_field in key_busco_mappings.items():
            key_busco_stats[atol_field] = all_busco_stats[reporting_field]

    busco_output = {'busco':all_busco_stats}

    stats_for_gnl.update(key_busco_stats)
else:
    print("No BUSCO file specified")
    busco_output = {'busco':{}}

with open(json_atol_report,'w', encoding="utf-8") as f:
    output_for_gnl = {'annotation':stats_for_gnl}
    json.dump(output_for_gnl, f)

print("Combining statistics and writing to JSON")

combined_stats = all_metadata | agat_output | busco_output

with open(json_full_report, 'w', encoding="utf-8") as f:
    json.dump(combined_stats, f)

# populate typst template with json dataa
print("Rendering typst template")

subprocess.run([
    "typst", "compile",
    str(path_to_template),
    str(output_pdf),
    "--input", "file=dev/json_report.json"
], check=True)

print("Script completed. Report available as PDF (" + str(output_pdf) + ") and JSON (" + str(json_full_report) + ")")