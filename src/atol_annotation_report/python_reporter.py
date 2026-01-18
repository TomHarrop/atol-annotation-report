#!/usr/bin/env python3

# this is a python version of the reporter.pl script.
# it takes a metadata json file, an agat yaml file, and a busco json file.
# this script parses and maps their content to fields in the annotation schema.
# the output is dumped into json_report.json.
# the json is used to populate the full_report_template.typ during typst rendering.
# this generates a test-output.pdf

# this script simutaneously collects a subset of data for atol in atol_report.json.
# atol_report.json contains an object which can be fed straight into the genome-note-lite pipeline.


from importlib.resources import files
from pathlib import Path
import argparse
import json
import typst
import yaml
import csv
import logging
import sys
from atol_annotation_report import mapping_configs

logging.basicConfig(
    stream=sys.stderr,
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s"
)
logger = logging.getLogger()

def parse_arguments():

    argument_parser = argparse.ArgumentParser(
        description="This tool generates a JSON and PDF report of annotation metadata and metric vaules from BUSCO, OMArk, and AGAT evaulations for the purposes of QA",
        formatter_class=argparse.ArgumentDefaultsHelpFormatter,
    )

    input_group = argument_parser.add_argument_group("Input")
    output_group = argument_parser.add_argument_group("Output")

    input_group.add_argument(
        "-m",
        "--metadata_file",
        nargs="?",
        type=Path,
        help="a JSON file containing metadata according to the Annotation Metadata Schema",
    )
    input_group.add_argument(
        "-a",
        "--agat_file",
        nargs="?",
        type=Path,
        help="a YAML file generated as output from an AGAT analysis on your annotation file",
    )
    input_group.add_argument(
        "-b",
        "--busco_file",
        nargs="?",
        type=Path,
        help="a JSON file generated as output from a BUSCO analysis on your annotation file",
    )
    input_group.add_argument(
        "-om",
        "--omark_file",
        nargs="?",
        type=Path,
        help="a JSON file generated as output from an OMArk analysis on your annotation file",
    )
    input_group.add_argument(
        "-ao",
        "--annooddities_file",
        nargs="?",
        type=Path,
        help="a TXT file summarising any oddities found in the AnnoOddity analysis of your annotation file",
    )
    input_group.add_argument(
        "-t",
        "--template_file",
        default=Path(files(), "resources", "full_report_template.typ"),
        type=Path,
        help="Path to the .typ document used as the base template populated with metadata and metrics from QA tools"
    )

    output_group.add_argument(
        "-o",
        "--output_file",
        default=Path("test_out.pdf"),
        type=Path,
        help="Path to the output PDF report",
    )
    output_group.add_argument(
        "--json_atol",
        default=Path("json_atol.json"),
        type=Path,
        help="Path to the output JSON data for Genome Note lite input",
    )
    output_group.add_argument(
        "--json_full",
        default=Path("json_full.json"),
        type=Path,
        help="Path to the output JSON data for all results",
    )

    args = argument_parser.parse_args()

    return args

# new functions for mapping
def map_stat_to_report(mapping_section, stat_input, report_output):
    for report_field, stat_field in mapping_section.items():
        if stat_field in stat_input:
            report_output[report_field] = stat_input[stat_field]
        else:
            report_output[report_field] = None

def map_one_to_many(stat_input, report_output, mapping_section):
    for report_field, mapped_vals in mapping_section.items():
        for stat_field, stat_value in stat_input.items():
            if stat_field in mapped_vals:
                report_output[report_field] = stat_value
            elif report_field in report_output.keys():
                pass
            else:
                report_output[report_field] = None

# function to write stats to json
def write_data(json_stats_input, file_path):
    with open(file_path, "w",  encoding="utf-8") as f:
        json.dump(json_stats_input, f)

# functions to convert None values to string for rendering by typst
def convert_null_values(full_report):
    report_in_prep = full_report.copy()
    converted_report = replace_nulls(report_in_prep)
    return converted_report

def replace_nulls(report_in_prep):
    for key, value in report_in_prep.items():
        if isinstance(value, dict):
            replace_nulls(value)
        elif value is None:
            report_in_prep[key] = "N/A"
        elif isinstance(value, list) and None in value:
            report_in_prep[key] = ["N/A"]
        else:
            report_in_prep[key] = value
    return report_in_prep

# function to populate template
def populate_template(template, input_data, output_path):
    try: 
        typst.compile(
            input=template,
            output=output_path,
            sys_inputs=input_data
        )
    except typst.TypstError as e:
        logger.critical("typst compilation failed")
        raise e

# Possibly break main up into sub-functions, e.g. one for the BUSCO file, one
# for the OMArk, etc. If you repeat code, it should be a function. (not always
# possible!)
def main():
    args = parse_arguments()

    # this dictionary will contain a json "annotation" object which can be inserted into the atol genome-note-lite input.
    stats_for_gnl = {}

    all_metadata = {}
    if args.metadata_file is not None:
        all_metadata["metadata_input_provided"] = True
        logger.info("Parsing metadata")
        with open(args.metadata_file, "rt") as f:
            metadata_input = json.load(f)
            for dictionary in metadata_input:
                key = dictionary["meta_key"]
                value = dictionary["meta_value"]
                all_metadata[key] = value
    else:
        logger.info("No metadata file specified")
        all_metadata["metadata_input_provided"] = False

    all_agat_stats = {}
    if args.agat_file is not None:
        # TODO: parse and map AGAT software version and add to key_agat_mappings
        # parse AGAT yaml and map to new field names
        all_agat_stats["agat_input_provided"] = True
        logger.info("Parsing AGAT file")
        with open(args.agat_file, "rt") as f:
            key_agat_stats = {}
            full_agat_input = yaml.load(f, Loader=yaml.SafeLoader)
            if "transcript" in full_agat_input:
                transcript_stats = full_agat_input["transcript"]
                key_agat_stats["feature_stats_calculated_for"] = (
                    "transcripts (without isoforms)"
                )
                if "without_isoforms" in transcript_stats:
                    agat_stats_input = transcript_stats["without_isoforms"]["value"]
                elif "without_isoform" in transcript_stats:
                    agat_stats_input = transcript_stats["without_isoform"]["value"]
                else:
                    logger.info(
                        "AGAT stats for transcripts without isoform not found, looking for stats for mRNAs"
                    )
            elif "mrna" in full_agat_input:
                mrna_stats = full_agat_input["mrna"]
                key_agat_stats["feature_stats_calculated_for"] = (
                    "mRNAs (without isoforms)"
                )
                if "without_isoforms" in mrna_stats:
                    agat_stats_input = mrna_stats["without_isoforms"]["value"]
                elif "without_isoform" in mrna_stats:
                    agat_stats_input = mrna_stats["without_isoform"]["value"]
                else:
                    logger.info("AGAT stats for mRNAs without isoform stats not found")
            else:
                logger.warning("no transcript or mRNA stats detected in AGAT yaml file")
            all_agat_stats.update(key_agat_stats)
            map_stat_to_report(mapping_section=mapping_configs.key_agat_mappings, stat_input=agat_stats_input, report_output=key_agat_stats)
            for mapping_sect in [
                mapping_configs.key_agat_mappings,
                mapping_configs.additional_agat_mappings,
                mapping_configs.full_stat_agat_mappings,
                mapping_configs.mean_stat_agat_mappings,
                mapping_configs.median_stat_agat_mappings,
                mapping_configs.long_short_agat_mappings,
                mapping_configs.length_agat_mappings
            ]:
                map_stat_to_report(
                    mapping_section=mapping_sect, 
                    stat_input=agat_stats_input, 
                    report_output=all_agat_stats)
        stats_for_gnl.update(key_agat_stats)
    else:
        logger.info("No AGAT file specified")
        all_agat_stats["agat_input_provided"] = False
    agat_output = {"agat": all_agat_stats}

    # Tool-specific parsing could be a higher-level function (i.e. it calls the
    # lower-level mapping functions )
    all_busco_stats = {}
    if args.busco_file is not None:
        all_busco_stats["busco_input_provided"] = True
        # parse BUSCO json and map to new field names
        logger.info("Parsing BUSCO file")
        with open(args.busco_file, "rt") as f:
            key_busco_stats = {}
            all_busco_input = json.load(f)
            map_stat_to_report(
                mapping_section=mapping_configs.parameter_busco_mappings, 
                stat_input=all_busco_input["parameters"], 
                report_output=all_busco_stats
            )
            map_stat_to_report(
                mapping_section=mapping_configs.lineage_busco_mappings, 
                stat_input=all_busco_input["lineage_dataset"], 
                report_output=all_busco_stats
            )
            map_stat_to_report(
                mapping_section=mapping_configs.version_busco_mappings, 
                stat_input=all_busco_input["versions"], 
                report_output=all_busco_stats
            )
            map_stat_to_report(
                mapping_section=mapping_configs.result_busco_mappings, 
                stat_input=all_busco_input["results"], 
                report_output=all_busco_stats
            )
            map_one_to_many(
                stat_input=all_busco_input["results"],
                report_output=all_busco_stats,
                mapping_section=mapping_configs.busco_val_mappings
            )
            map_stat_to_report(
                mapping_section=mapping_configs.key_busco_mappings, 
                stat_input=all_busco_stats, 
                report_output=key_busco_stats
            )
        stats_for_gnl.update(key_busco_stats)
    else:
        logger.info("No BUSCO file specified")
        all_busco_stats["busco_input_provided"] = False
    busco_output = {"busco": all_busco_stats}

    all_omark_stats = {}
    if args.omark_file is not None:
        all_omark_stats["omark_input_provided"] = True
        # parse OMArk file and map to new field names
        logger.info("Parsing OMArk file")
        with open(args.omark_file, "rt") as f:
            key_omark_stats = {}
            key_omark_stats["detected_sp"] = []
            key_omark_stats["contaminant_sp"] = []
            all_omark_input = json.load(f)
            omark_spp = all_omark_input["detected_species"]
            map_stat_to_report(
                mapping_section=mapping_configs.omark_info_mappings, 
                stat_input=all_omark_input, 
                report_output=key_omark_stats
            )
            map_stat_to_report(
                mapping_section=mapping_configs.omark_key_mappings, 
                stat_input=all_omark_input["results_pcts"],
                report_output=key_omark_stats
            )
            all_omark_stats.update(key_omark_stats)
            map_stat_to_report(
                mapping_section=mapping_configs.omark_consistency_mappings, 
                stat_input=all_omark_input["results_pcts"],
                report_output=all_omark_stats
            )
            map_stat_to_report(
                mapping_section=mapping_configs.omark_conserved_hog_mappings, 
                stat_input=all_omark_input["conserv_pcts"],
                report_output=all_omark_stats
            )
            for spp in range(len(omark_spp)):
                if "Clade" in (omark_spp[spp]):
                    all_omark_stats["detected_sp"].append(omark_spp[spp])
                elif "Potential_contaminants" in (omark_spp[spp]):
                    all_omark_stats["contaminant_sp"].append(omark_spp[spp])
            if all_omark_stats["detected_sp"] == []:
                all_omark_stats["detected_sp"].append(None)
            if all_omark_stats["contaminant_sp"] == []:
                all_omark_stats["contaminant_sp"].append(None)
        stats_for_gnl.update(key_omark_stats)
    else:
        logger.info("No OMArk file specified")
        all_omark_stats["omark_input_provided"] = False
    omark_output = {"omark": all_omark_stats}

    all_oddities = {}
    if args.annooddities_file is not None:
        all_oddities["annooddities_input_provided"] = True
        # parse the annooddity summary file
        logger.info("Parsing AnnoOddities file")
        with open(args.annooddities_file, "rt") as f:
            oddity_table = csv.reader(f, delimiter="\t")
            next(oddity_table)  # take out the header
            oddity_dict = {}
            for row in oddity_table:
                key = row[0]
                value = int(row[1])
                oddity_dict[key] = value
            map_stat_to_report(
                mapping_section=mapping_configs.oddity_mappings, 
                stat_input=oddity_dict,
                report_output=all_oddities
            )
    else:
        logger.info("No AnnoOddities file specified")
        all_oddities["annooddities_input_provided"] = False
    oddity_output = {"annooddities": all_oddities}

    logger.info("Combining statistics and writing to JSON")

    combined_stats = (
        all_metadata | agat_output | busco_output | omark_output | oddity_output
    )

    # format genome note lite dictionary as 'annotation' object
    output_for_gnl = {"annotation": stats_for_gnl}

    write_data(json_stats_input=output_for_gnl, file_path=args.json_atol)
    write_data(json_stats_input=combined_stats, file_path=args.json_full)

    # populate typst template with json data
    full_results = {"full_results": json.dumps(convert_null_values(combined_stats))}

    logger.info("Rendering typst template")

    populate_template(
        template=args.template_file,
        input_data=full_results,
        output_path=args.output_file
    )

    logger.info(
        "AToL Annotation Report Tool completed. Report available as PDF ("
        + str(args.output_file)
        + ") and JSON ("
        + str(args.json_full)
        + ")"
    )

if __name__ == "__main__":
    main()
