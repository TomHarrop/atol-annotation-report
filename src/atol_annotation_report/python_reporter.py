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


def main():
    args = parse_arguments()

    path_to_template = Path(files(), "resources", "full_report_template.typ")

    # this dictionary will contain a json "annotation" object which can be inserted into the atol genome-note-lite input.
    stats_for_gnl = {}

    all_metadata = {}
    if args.metadata_file is not None:
        path_to_metadata = args.metadata_file
        all_metadata["metadata_input_provided"] = True
        print("Parsing metadata")
        with open(path_to_metadata, "rt") as f:
            metadata_input = json.load(f)
            for dict in metadata_input:
                key = dict["meta_key"]
                value = dict["meta_value"]
                all_metadata[key] = value
    else:
        print("No metadata file specified")
        all_metadata["metadata_input_provided"] = False

    all_agat_stats = {}
    if args.agat_file is not None:
        path_to_agat = args.agat_file
        # define mappings from agat yaml input to annotation schema fields
        key_agat_mappings = {
            "gene_count": "Number of gene",
            "cds_count": "Number of cds",
            "transcript_count": "Number of transcript",
            "mrna_count": "Number of mrna",
            "mean_transcript_length": "mean transcript length (bp)",
            "mean_mrna_length": "mean mrna length (bp)",
            "mean_transcripts_per_gene": "mean transcripts per gene",
            "mean_mrnas_per_gene": "mean mrnas per gene",
            "mean_exons_per_transcript": "mean exons per transcript",
            "mean_exons_per_mrna": "mean exons per mrna",
        }
        additional_agat_mappings = {
            "exon_count": "Number of exon",
            "mean_exon_length": "mean exon length (bp)",
            "mean_gene_length": "mean gene length (bp)",
            "total_gene_length": "Total gene length (bp)",
            "total_transcript_length": "Total transcript length (bp)",
            "total_mrna_length": "Total mrna length (bp)",
        }
        full_stat_agat_mappings = {
            "intron_count": "Number of intron",
            "single_exon_gene_count": "Number of single exon gene",
            "single_exon_transcript_count": "Number of single exon transcript",
            "single_exon_mrna_count": "Number of single exon mrna",
        }
        mean_stat_agat_mappings = {
            "mean_cds_length": "mean cds length (bp)",
            "mean_intron_length": "mean intron length (bp)",
            "mean_cdss_per_transcript": "mean cdss per transcript",
            "mean_cdss_per_mrna": "mean cdss per mrna",
            "mean_exons_per_cds": "mean exons per cds",
            "mean_introns_per_transcript": "mean introns per transcript",
        }
        median_stat_agat_mappings = {
            "median_gene_length": "median gene length (bp)",
            "median_transcript_length": "median transcript length (bp)",
            "median_mrna_length": "median mrna length (bp)",
            "median_exon_length": "median exon length (bp)",
            "median_cds_length": "median cds length (bp)",
            "median_intron_length": "median intron length (bp)",
        }
        long_short_agat_mappings = {
            "longest_gene": "Longest gene (bp)",
            "longest_transcript": "Longest transcript (bp)",
            "longest_mrna": "Longest mrna (bp)",
            "longest_exon": "Longest exon (bp)",
            "longest_cds": "Longest cds (bp)",
            "longest_intron": "Longest intron (bp)",
            "shortest_gene": "Shortest gene (bp)",
            "shortest_transcript": "Shortest transcript (bp)",
            "shortest_mrna": "Shortest mrna (bp)",
        }
        length_agat_mappings = {
            "total_cds_length": "Total cds length (bp)",
            "total_exon_length": "Total exon length (bp)",
            "total_intron_length": "Total intron length (bp)",
        }
        # TODO: parse and map AGAT software version and add to key_agat_mappings
        # parse AGAT yaml and map to new field names
        all_agat_stats["agat_input_provided"] = True
        print("Parsing AGAT file")
        with open(path_to_agat, "rt") as f:
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
            for reporting_field, agat_field in key_agat_mappings.items():
                if agat_field in agat_stats_input:
                    key_agat_stats[reporting_field] = agat_stats_input[agat_field]
            all_agat_stats.update(key_agat_stats)
            for reporting_field, agat_field in additional_agat_mappings.items():
                if agat_field in agat_stats_input:
                    all_agat_stats[reporting_field] = agat_stats_input[agat_field]
            for reporting_field, agat_field in full_stat_agat_mappings.items():
                if agat_field in agat_stats_input:
                    all_agat_stats[reporting_field] = agat_stats_input[agat_field]
            for reporting_field, agat_field in mean_stat_agat_mappings.items():
                if agat_field in agat_stats_input:
                    all_agat_stats[reporting_field] = agat_stats_input[agat_field]
            for reporting_field, agat_field in median_stat_agat_mappings.items():
                if agat_field in agat_stats_input:
                    all_agat_stats[reporting_field] = agat_stats_input[agat_field]
            for reporting_field, agat_field in long_short_agat_mappings.items():
                if agat_field in agat_stats_input:
                    all_agat_stats[reporting_field] = agat_stats_input[agat_field]
            for reporting_field, agat_field in length_agat_mappings.items():
                if agat_field in agat_stats_input:
                    all_agat_stats[reporting_field] = agat_stats_input[agat_field]
        for key, value in key_agat_mappings.items():
            if key not in all_agat_stats.keys():
                all_agat_stats[key] = "N/A"
        for key, value in additional_agat_mappings.items():
            if key not in all_agat_stats.keys():
                all_agat_stats[key] = "N/A"
        for key, value in full_stat_agat_mappings.items():
            if key not in all_agat_stats.keys():
                all_agat_stats[key] = "N/A"
        for key, value in mean_stat_agat_mappings.items():
            if key not in all_agat_stats.keys():
                all_agat_stats[key] = "N/A"
        for key, value in median_stat_agat_mappings.items():
            if key not in all_agat_stats.keys():
                all_agat_stats[key] = "N/A"
        for key, value in long_short_agat_mappings.items():
            if key not in all_agat_stats.keys():
                all_agat_stats[key] = "N/A"
        for key, value in length_agat_mappings.items():
            if key not in all_agat_stats.keys():
                all_agat_stats[key] = "N/A"
        # agat_output = {'agat':all_agat_stats}
        stats_for_gnl.update(key_agat_stats)
    else:
        print("No AGAT file specified")
        all_agat_stats["agat_input_provided"] = False
    agat_output = {"agat": all_agat_stats}

    all_busco_stats = {}
    if args.busco_file is not None:
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
        all_busco_stats["busco_input_provided"] = True
        # parse BUSCO json and map to new field names
        print("Parsing BUSCO file")
        with open(path_to_busco, "rt") as f:
            key_busco_stats = {}
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
                        all_busco_stats[reporting_field] = busco_result_info[
                            busco_field
                        ]
            for atol_field, reporting_field in key_busco_mappings.items():
                key_busco_stats[atol_field] = all_busco_stats[reporting_field]
        for key, value in parameter_busco_mappings.items():
            if key not in all_busco_stats.keys():
                all_busco_stats[key] = "N/A"
        for key, value in lineage_busco_mappings.items():
            if key not in all_busco_stats.keys():
                all_busco_stats[key] = "N/A"
        for key, value in version_busco_mappings.items():
            if key not in all_busco_stats.keys():
                all_busco_stats[key] = "N/A"
        for key, value in result_busco_mappings.items():
            if key not in all_busco_stats.keys():
                all_busco_stats[key] = "N/A"
        for key, value in result_busco_mappings.items():
            if key not in all_busco_stats.keys():
                all_busco_stats[key] = "N/A"
        stats_for_gnl.update(key_busco_stats)
    else:
        print("No BUSCO file specified")
        all_busco_stats["busco_input_provided"] = False
    busco_output = {"busco": all_busco_stats}

    all_omark_stats = {}
    if args.omark_file is not None:
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
        all_omark_stats["omark_input_provided"] = True
        # parse OMArk file and map to new field names
        print("Parsing OMArk file")
        with open(path_to_omark, "rt") as f:
            key_omark_stats = {}
            all_omark_stats["detected_sp"] = []
            all_omark_stats["contaminant_sp"] = []
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
            for spp in range(len(omark_spp)):
                if "Clade" in (omark_spp[spp]):
                    all_omark_stats["detected_sp"].append(omark_spp[spp])
                elif "Potential_contaminants" in (omark_spp[spp]):
                    all_omark_stats["contaminant_sp"].append(omark_spp[spp])
        for key, value in omark_key_mappings.items():
            if key not in all_omark_stats.keys():
                all_omark_stats[key] = "N/A"
        for key, value in omark_info_mappings.items():
            if key not in all_omark_stats.keys():
                all_omark_stats[key] = "N/A"
        for key, value in omark_conserved_hog_mappings.items():
            if key not in all_omark_stats.keys():
                all_omark_stats[key] = "N/A"
        for key, value in omark_consistency_mappings.items():
            if key not in all_omark_stats.keys():
                all_omark_stats[key] = "N/A"
        if all_omark_stats["detected_sp"] == []:
            all_omark_stats["detected_sp"].append("N/A")
        if all_omark_stats["contaminant_sp"] == []:
            all_omark_stats["contaminant_sp"].append("N/A")
        stats_for_gnl.update(key_omark_stats)
    else:
        print("No OMArk file specified")
        all_omark_stats["omark_input_provided"] = False
    omark_output = {"omark": all_omark_stats}

    all_oddities = {}
    if args.annooddities_file is not None:
        path_to_oddities = args.annooddities_file
        # define mappings from annooddity output
        oddity_mappings = {
            "single_exon_transcripts": "exon_num == 1",
            "multi_exon_transcripts": "exon_num > 1",
            "five_utr_above_10000bp": "five_utr_length > 10000",
            "five_utr_num_above_5": "five_utr_num > 5",
            "three_utr_above_10000bp": "three_utr_length > 10000",
            "three_utr_num_above_4": "three_utr_num > 4",
            "incomplete_transcripts": "not is_complete",
            "missing_start_codon": "not has_start_codon",
            "missing_stop_codon": "not has_stop_codon",
            "fragmented": "is_fragment",
            "has_inframe_stop_codons": "has_inframe_stop",
            "max_exon_above_10000bp": "max_exon_length > 10000",
            "max_intron_above_120000bp": "max_intron_length > 120000",
            "min_exon_below_5bp": "min_exon_length <= 5",
            "min_intron_bw_0_and_5bp": "0 < min_intron_length <= 5",
            "cds_fraction_below_30pc": "selected_cds_fraction <= 0.3",
            "has_non_canonical_introns": "canonical_intron_proportion != 1",
            "only_non_canonical_splicing": "only_non_canonical_splicing",
            "has_suspicious_splicing": "suspicious_splicing",
        }
        all_oddities["annooddities_input_provided"] = True
        # parse the annooddity summary file
        print("Parsing AnnoOddities file")
        with open(path_to_oddities, "rt") as f:
            oddity_table = csv.reader(f, delimiter="\t")
            next(oddity_table)  # take out the header
            oddity_dict = {}
            for row in oddity_table:
                key = row[0]
                value = int(row[1])
                oddity_dict[key] = value
            for reporting_field, oddity_field in oddity_mappings.items():
                all_oddities[reporting_field] = oddity_dict[oddity_field]
        for key, value in oddity_mappings.items():
            if key not in all_oddities.keys():
                all_oddities[key] = "N/A"
    else:
        print("No AnnoOddities file specified")
        all_oddities["annooddities_input_provided"] = False
    oddity_output = {"annooddities": all_oddities}

    with open(args.json_atol, "w", encoding="utf-8") as f:
        output_for_gnl = {"annotation": stats_for_gnl}
        json.dump(output_for_gnl, f)

    print("Combining statistics and writing to JSON")
    combined_stats = (
        all_metadata | agat_output | busco_output | omark_output | oddity_output
    )

    with open(args.json_full, "w", encoding="utf-8") as f:
        json.dump(combined_stats, f)

    # populate typst template with json dataa
    full_results = {"full_results": json.dumps(combined_stats)}

    print("Rendering typst template")

    typst.compile(
        input=path_to_template, output=args.output_file, sys_inputs=full_results
    )

    print(
        "AToL Annotation Report Tool completed. Report available as PDF ("
        + str(args.output_file)
        + ") and JSON ("
        + str(args.json_full)
        + ")"
    )


if __name__ == "__main__":
    main()
