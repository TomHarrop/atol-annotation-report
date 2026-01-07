#!/usr/bin/env python3

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