#!/usr/bin/env python3

# AGAT mappings

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

# BUSCO mappings

parameter_busco_mappings = {
    "mode": "mode",
    "gene_predictor": "gene_predictor"
}
lineage_busco_mappings = {
    "lineage_name": "name"
}
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

# OMArk mappings

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

# AnnoOddity mappings

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

# busco mappings for different versions

busco_complete_pct = [
    "Complete percentage", 
    "Complete"
]
busco_single_pct = [
    "Single copy percentage", 
    "Single copy"
]
busco_multi_pct = [
    "Multi copy percentage",
    "Multi copy"
]
busco_frag_pct = [
    "Fragmented percentage",
    "Fragmented"
]
busco_missing_pct = [
    "Missing percentage",
    "Missing"
]

# pseudocode (doesn't work)
# if key in busco.mapping.field:
#     field = value
busco = {
    "mappings": {
        "complete_pct" : [
            "Complete",
            "complete",
            "complete pct",
            "Complete %"

        ]
    }
}