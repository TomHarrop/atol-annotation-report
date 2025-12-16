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


def parse_arguments():

    argument_parser = argparse.ArgumentParser(
        description="This tool generates a JSON and PDF report of annotation metadata and metric vaules from BUSCO, OMArk, and AGAT evaulations for the purposes of QA"
    )

    input_group = argument_parser.add_argument_group("Input")
    output_group = argument_parser.add_argument_group("Output")

    input_group.add_argument(
        "-m",
        "--metadata_file",
        required=True,
        type=Path,
        help="a JSON file containing metadata according to the Annotation Metadata Schema",
    )
    input_group.add_argument(
        "-a",
        "--agat_file",
        required=True,
        type=Path,
        help="a YAML file generated as output from an AGAT analysis on your annotation file",
    )
    input_group.add_argument(
        "-b",
        "--busco_file",
        required=True,
        type=Path,
        help="a JSON file generated as output from a BUSCO analysis on your annotation file",
    )
    input_group.add_argument(
        "-om",
        "--omark_file",
        required=True,
        type=Path,
        help="a JSON file generated as output from an OMArk analysis on your annotation file",
    )

    output_group.add_argument(
        "-o",
        "--output_file",
        default=Path("test_out.pdf"),
        type=Path,
        help="your desired report file address for the output PDF report",
    )
    output_group.add_argument(
        "--json_atol",
        default=Path("json_atol.json"),
        type=Path,
        help="your desired report file address for the output PDF report",
    )
    output_group.add_argument(
        "--json_full",
        default=Path("json_full.json"),
        type=Path,
        help="your desired report file address for the output PDF report",
    )

    args = argument_parser.parse_args()

    return args


def main():
    args = parse_arguments()

    path_to_template = Path(files(), "resources", "full_report_template.typ")

    # this dictionary will contain a json "annotation" object which can be inserted into the atol genome-note-lite input.
    stats_for_gnl = {}

    path_to_metadata = args.metadata_file
    print("Parsing metadata")
    with open(path_to_metadata, "rt") as f:
        metadata_input = json.load(f)
        all_metadata = {}
        for dict in metadata_input:
            key = dict["meta_key"]
            value = dict["meta_value"]
            all_metadata[key] = value

    path_to_agat = args.agat_file
    # define mappings from agat yaml input to annotation schema fields
    key_agat_mappings = {
        "gene_count": "Number of gene",
        "cds_count": "Number of cds",
        "transcript_count": "Number of transcript",
        "mean_transcript_length": "mean transcript length (bp)",
        "mean_transcripts_per_gene": "mean transcripts per gene",
        "mean_exons_per_transcript": "mean exons per transcript",
    }
    additional_agat_mappings = {
        "exon_count": "Number of exon",
        "mean_exon_length": "mean exon length (bp)",
        "mean_gene_length": "mean gene length (bp)",
        "total_gene_length": "Total gene length (bp)",
        "total_transcript_length": "Total transcript length (bp)",
    }
    full_stat_agat_mappings = {
        "intron_count": "Number of intron",
        "single_exon_gene_count": "Number of single exon gene",
        "single_exon_transcript_count": "Number of single exon transcript",
    }
    mean_stat_agat_mappings = {
        "mean_cds_length": "mean cds length (bp)",
        "mean_intron_length": "mean intron length (bp)",
        "mean_cdss_per_transcript": "mean cdss per transcript",
        "mean_exons_per_cds": "mean exons per cds",
        "mean_introns_per_transcript": "mean introns per transcript",
    }
    median_stat_agat_mappings = {
        "median_gene_length": "median gene length (bp)",
        "median_transcript_length": "median transcript length (bp)",
        "median_exon_length": "median exon length (bp)",
        "median_cds_length": "median cds length (bp)",
        "median_intron_length": "median intron length (bp)",
    }
    long_short_agat_mappings = {
        "longest_gene": "Longest gene (bp)",
        "longest_transcript": "Longest transcript (bp)",
        "longest_exon": "Longest exon (bp)",
        "longest_cds": "Longest cds (bp)",
        "longest_intron": "Longest intron (bp)",
        "shortest_gene": "Shortest gene (bp)",
        "shortest_transcript": "Shortest transcript (bp)",
    }
    length_agat_mappings = {
        "total_cds_length": "Total cds length (bp)",
        "total_exon_length": "Total exon length (bp)",
        "total_intron_length": "Total intron length (bp)",
    }
    # TODO: parse and map AGAT software version and add to key_agat_mappings
    # parse AGAT yaml and map to new field names
    print("Parsing AGAT file")
    with open(path_to_agat, "rt") as f:
        key_agat_stats = {}
        all_agat_stats = {}
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
        elif "mrna" in full_agat_input:
            mrna_stats = full_agat_input["mrna"]
            key_agat_stats["feature_stats_calculated_for"] = "mRNAs (without isoforms)"
            if "without_isoforms" in mrna_stats:
                agat_stats_input = mrna_stats["without_isoforms"]["value"]
            elif "without_isoform" in mrna_stats:
                agat_stats_input = mrna_stats["without_isoform"]["value"]
            else:
                print("AGAT stats mRNAs without isoform stats not found")
        else:
            print("error: no transcript or mRNA stats detected in AGAT yaml file")
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
    agat_output = {"agat": all_agat_stats}
    stats_for_gnl.update(key_agat_stats)

    path_to_busco = args.busco_file
    # define mappings from BUSCO json input to annotation schema fields
    parameter_busco_mappings = {"mode": "mode", "gene_predictor": "gene_predictor"}
    lineage_busco_mappings = {"lineage_name": "name"}
    version_busco_mappings = {
        "version_busco": "busco",
        "version_hmmsearch": "hmmsearch",
        "version_metaeuk": "metaeuk",
        "version_augustus": "augustus",
        "version_miniprot": "miniprot",
    }
    result_busco_mappings = {
        "one_line_summary": "one_line_summary",
        "n_markers": "n_markers",
        "domain": "domain",
    }
    # these are mappings from the annotation schema to the atol schema
    key_busco_mappings = {
        "annot_busco_mode": "mode",
        "annot_busco_lineage": "lineage_name",
        "annot_busco_summary": "one_line_summary",
        "annot_busco_version": "version_busco",
    }
    # parse BUSCO json and map to new field names
    print("Parsing BUSCO file")
    with open(path_to_busco, "rt") as f:
        key_busco_stats = {}
        all_busco_stats = {}
        all_busco_input = json.load(f)
        busco_param_info = all_busco_input["parameters"]
        busco_lineage_info = all_busco_input["lineage_dataset"]
        busco_version_info = all_busco_input["versions"]
        busco_result_info = all_busco_input["results"]
        for reporting_field, busco_field in parameter_busco_mappings.items():
            if busco_field in busco_param_info:
                all_busco_stats[reporting_field] = busco_param_info[busco_field]
        for reporting_field, busco_field in lineage_busco_mappings.items():
            all_busco_stats[reporting_field] = busco_lineage_info[busco_field]
        for reporting_field, busco_field in version_busco_mappings.items():
            if busco_field in busco_version_info:
                all_busco_stats[reporting_field] = busco_version_info[busco_field]
        for busco_result_field, busco_result_value in busco_result_info.items():
            if busco_result_field in ["Complete percentage", "Complete"]:
                all_busco_stats["complete_percent"] = busco_result_value
            elif busco_result_field in ["Single copy percentage", "Single copy"]:
                all_busco_stats["single_copy_percent"] = busco_result_value
            elif busco_result_field in ["Multi copy percentage", "Multi copy"]:
                all_busco_stats["duplicated_percent"] = busco_result_value
            elif busco_result_field in ["Fragmented percentage", "Fragmented"]:
                all_busco_stats["fragmented_percent"] = busco_result_value
            elif busco_result_field in ["Missing percentage", "Missing"]:
                all_busco_stats["missing_percent"] = busco_result_value
            else:
                for reporting_field, busco_field in result_busco_mappings.items():
                    all_busco_stats[reporting_field] = busco_result_info[busco_field]
        for atol_field, reporting_field in key_busco_mappings.items():
            key_busco_stats[atol_field] = all_busco_stats[reporting_field]
    busco_output = {"busco": all_busco_stats}
    stats_for_gnl.update(key_busco_stats)

    path_to_omark = args.omark_file
    # define mappings from omark output
    omark_key_mappings = {
        "omark_percent_consistent": "consistent",
        "omark_percent_inconsistent": "inconsistent",
        "omark_percent_contaminant": "likely_contamination",
        "omark_percent_unknown": "unknown",
    }
    omark_info_mappings = {
        "omark_lineage": "selected_clade",
        "conserved_hogs": "conserved_hogs",
        "omark_protein_count": "proteins_in_proteome",
        "omamer_version": "omamer_version",
        "omamer_db_version": "db_version",
        "omark_completeness_summary": "conserv_pcts_raw",
        "omark_consistency_summary": "results_pcts_raw",
    }
    omark_conserved_hog_mappings = {
        "single_hog_percent": "single",
        "duplicated_hog_percent": "duplicated",
        "unexpected_dup_hog_percent": "duplicated_unexpected",
        "expected_dup_hog_percent": "duplicated_expected",
        "missing_hog_percent": "missing",
    }
    omark_consistency_mappings = {
        "percent_consistent_partial": "consistent_partial_hits",
        "percent_consistent_fragments": "consistent_fragmented",
        "percent_inconsistent_partial": "inconsistent_partial_hits",
        "percent_inconsistent_fragments": "inconsistent_fragmented",
        "percent_contaminant_partial": "likely_contamination_partial_hits",
        "percent_contaminant_fragments": "likely_contamination_fragmented",
    }
    omark_detected_sp_mappings = {
        "taxon": "Clade",
        "NCBI_taxid": "NCBI_taxid",
        "associated_protein_count": "Number_of_associated_proteins",
        "associated_protein_pc": "Percentage_of_proteomes_total",
    }
    omark_detected_sp_mappings = {"detected_sp": "detected_species"}
    # parse OMArk file and map to new field names
    print("Parsing OMArk file")
    with open(path_to_omark, "rt") as f:
        key_omark_stats = {}
        all_omark_stats = {}
        all_omark_input = json.load(f)
        omark_hogs = all_omark_input["conserv_pcts"]
        omark_consistency = all_omark_input["results_pcts"]
        omark_spp = all_omark_input["detected_species"]
        for reporting_field, omark_field in omark_info_mappings.items():
            all_omark_stats[reporting_field] = all_omark_input[omark_field]
        for reporting_field, omark_field in omark_key_mappings.items():
            all_omark_stats[reporting_field] = omark_consistency[omark_field]
        key_omark_stats.update(all_omark_stats)
        for reporting_field, omark_field in omark_consistency_mappings.items():
            all_omark_stats[reporting_field] = omark_consistency[omark_field]
        for reporting_field, omark_field in omark_conserved_hog_mappings.items():
            all_omark_stats[reporting_field] = omark_hogs[omark_field]
        for reporting_field, omark_field in omark_detected_sp_mappings.items():
            all_omark_stats[reporting_field] = []
            for spp in range(len(omark_spp)):
                all_omark_stats[reporting_field].append(omark_spp[spp])
    omark_output = {"omark": all_omark_stats}
    stats_for_gnl.update(key_omark_stats)

    with open(args.json_atol, "w", encoding="utf-8") as f:
        output_for_gnl = {"annotation": stats_for_gnl}
        json.dump(output_for_gnl, f)

    print("Combining statistics and writing to JSON")
    combined_stats = all_metadata | agat_output | busco_output | omark_output

    with open(args.json_full, "w", encoding="utf-8") as f:
        json.dump(combined_stats, f)

    # populate typst template with json dataa
    print("Rendering typst template")

    #     subprocess.run(
    #         [
    #             "typst",
    #             "compile",
    #             str(path_to_template),
    #             str(args.output_file),
    #             "--input", "file=src/atol_annotation_report/resources/json_full.json"
    # #            "file=" + str(args.json_full),
    #         ],
    #         check=True,
    #     )

    full_results = {"full_results": json.dumps(combined_stats)}

    typst.compile(
        input=path_to_template, output=args.output_file, sys_inputs=full_results
    )

    print(
        "Script completed. Report available as PDF ("
        + str(args.output_file)
        + ") and JSON ("
        + str(args.json_full)
        + ")"
    )


if __name__ == "__main__":
    main()
