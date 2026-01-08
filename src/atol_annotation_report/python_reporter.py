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
from atol_annotation_report import mapping_configs

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

# Possibly break main up into sub-functions, e.g. one for the BUSCO file, one
# for the OMArk, etc. If you repeat code, it should be a function. (not always
# possible!)
def main():
    args = parse_arguments()

    # could be an arg with a default
    # path_to_template = Path(files(), "resources", "full_report_template.typ")

    # writing new functions for mapping
    def map_stat_to_report(mapping_section, stat_input, report_output):
        for report_field, stat_field in mapping_section.items():
            if stat_field in stat_input:
                report_output[report_field] = stat_input[stat_field]
            else:
                report_output[report_field] = None

    def map_one_to_many(one_to_many_maps, stat_input, report_output, report_field):
        for stat_field, stat_value in stat_input.items():
            if stat_field in one_to_many_maps:
                report_output[report_field] = stat_value

    # this dictionary will contain a json "annotation" object which can be inserted into the atol genome-note-lite input.
    stats_for_gnl = {}

    all_metadata = {}
    if args.metadata_file is not None:
        all_metadata["metadata_input_provided"] = True
        print("Parsing metadata") # could use a logger (see https://github.com/TomHarrop/atol-bpa-datamapper/blob/main/src/atol_bpa_datamapper/logger.py)
        with open(args.metadata_file, "rt") as f:
            metadata_input = json.load(f)
            for dict in metadata_input:
                key = dict["meta_key"]
                value = dict["meta_value"]
                all_metadata[key] = value
    else:
        print("No metadata file specified")
        all_metadata["metadata_input_provided"] = False

    # An alternative to storing configs here, is to add them to a module (e.g.
    # mapping_configs.py) and import them like this: `import mapping_configs`.
    # You can then use them as e.g. `mapping_configs.key_agat_mappings`. We
    # might also need to add the config file to the pyproject.toml.

    all_agat_stats = {}
    if args.agat_file is not None:
        # define mappings from agat yaml input to annotation schema fields
        # TODO: parse and map AGAT software version and add to key_agat_mappings
        # parse AGAT yaml and map to new field names
        all_agat_stats["agat_input_provided"] = True
        print("Parsing AGAT file")
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
                    print(
                        "AGAT stats for transcripts without isoform not found, looking for stats for mRNAs"
                    )
                '''
                # for the fun of it, with error handling (another way of
                # expressing the same thing).
                try:
                    agat_stats_input = transcript_stats["without_isoforms"]["value"]
                except KeyError as e:
                    logger.warning(
                        "AGAT stats for transcripts without isoform not found, looking for stats for mRNAs"
                    )
                    # Do some custom error handling, e.g.
                    # logger.error("You must supply a without_isoforms section")
                    # raise e
                    '''
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
                    print("AGAT stats mRNAs without isoform stats not found")
            else:
                print("error: no transcript or mRNA stats detected in AGAT yaml file")
            all_agat_stats.update(key_agat_stats)
            # The for blocks might be a candidate for a function (e.g. a
            # mapping function e.g. def map_value(field, value):)
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
                map_stat_to_report(mapping_section=mapping_sect, stat_input=agat_stats_input, report_output=all_agat_stats)
        stats_for_gnl.update(key_agat_stats)
    else:
        print("No AGAT file specified")
        all_agat_stats["agat_input_provided"] = False
    agat_output = {"agat": all_agat_stats}

    # Tool-specific parsing could be a higher-level function (i.e. it calls the
    # lower-level mapping functions )
    all_busco_stats = {}
    if args.busco_file is not None:
        all_busco_stats["busco_input_provided"] = True
        # parse BUSCO json and map to new field names
        print("Parsing BUSCO file")
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
            # In general, it's nice to avoid hard-coding... might be
            # difficult here?
            map_one_to_many(
                one_to_many_maps=mapping_configs.busco_complete_pct,
                stat_input=all_busco_input["results"],
                report_output=all_busco_stats,
                report_field="complete_percent"
            )
            map_one_to_many(
                one_to_many_maps=mapping_configs.busco_single_pct,
                stat_input=all_busco_input["results"],
                report_output=all_busco_stats,
                report_field="single_copy_percent"
            )
            map_one_to_many(
                one_to_many_maps=mapping_configs.busco_multi_pct,
                stat_input=all_busco_input["results"],
                report_output=all_busco_stats,
                report_field="duplicated_percent"
            )
            map_one_to_many(
                one_to_many_maps=mapping_configs.busco_frag_pct,
                stat_input=all_busco_input["results"],
                report_output=all_busco_stats,
                report_field="fragmented_percent"
            )
            map_one_to_many(
                one_to_many_maps=mapping_configs.busco_missing_pct,
                stat_input=all_busco_input["results"],
                report_output=all_busco_stats,
                report_field="missing_percent"
            )
            map_stat_to_report(
                mapping_section=mapping_configs.key_busco_mappings, 
                stat_input=all_busco_stats, 
                report_output=key_busco_stats
            )
        stats_for_gnl.update(key_busco_stats)
    else:
        print("No BUSCO file specified")
        all_busco_stats["busco_input_provided"] = False
    busco_output = {"busco": all_busco_stats}

    all_omark_stats = {}
    if args.omark_file is not None:
        all_omark_stats["omark_input_provided"] = True
        # parse OMArk file and map to new field names
        print("Parsing OMArk file")
        with open(args.omark_file, "rt") as f:
            key_omark_stats = {}
            all_omark_stats["detected_sp"] = []
            all_omark_stats["contaminant_sp"] = []
            all_omark_input = json.load(f)
            omark_spp = all_omark_input["detected_species"]
            map_stat_to_report(
                mapping_section=mapping_configs.omark_info_mappings, 
                stat_input=all_omark_input, 
                report_output=all_omark_stats
            )
            map_stat_to_report(
                mapping_section=mapping_configs.omark_key_mappings, 
                stat_input=all_omark_input["results_pcts"],
                report_output=all_omark_stats
            )
            key_omark_stats.update(all_omark_stats)
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
                else:
                    all_omark_stats["detected_sp"].append(None)
                if "Potential_contaminants" in (omark_spp[spp]):
                    all_omark_stats["contaminant_sp"].append(omark_spp[spp])
                else:
                    all_omark_stats["contaminant_sp"].append(None)
        stats_for_gnl.update(key_omark_stats)
    else:
        print("No OMArk file specified")
        all_omark_stats["omark_input_provided"] = False
    omark_output = {"omark": all_omark_stats}

    all_oddities = {}
    if args.annooddities_file is not None:
        all_oddities["annooddities_input_provided"] = True
        # parse the annooddity summary file
        print("Parsing AnnoOddities file")
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
        print("No AnnoOddities file specified")
        all_oddities["annooddities_input_provided"] = False
    oddity_output = {"annooddities": all_oddities}

    print(oddity_output)

    with open(args.json_atol, "w", encoding="utf-8") as f:
        output_for_gnl = {"annotation": stats_for_gnl}
        json.dump(output_for_gnl, f)

    print("Combining statistics and writing to JSON")
    combined_stats = (
        all_metadata | agat_output | busco_output | omark_output | oddity_output
    )

    # this could be a function? write_data(combined_stats, file_path)
    with open(args.json_full, "w", encoding="utf-8") as f:
        json.dump(combined_stats, f)

    # populate typst template with json dataa
    full_results = {"full_results": json.dumps(combined_stats)}

    print("Rendering typst template")

    # this could be a function?
    typst.compile(
        input=args.template_file, output=args.output_file, sys_inputs=full_results
    )

    # logger?
    print(
        "AToL Annotation Report Tool completed. Report available as PDF ("
        + str(args.output_file)
        + ") and JSON ("
        + str(args.json_full)
        + ")"
    )


if __name__ == "__main__":
    main()
