#import "@preview/tabut:1.0.2": tabut, records-from-csv, tabut-cells, rows-to-records

// Page styling
#set page(
  paper: "a4",
  flipped: true,
  margin: (x: 1.8cm, y: 1.5cm),
)

#set text(
  size: 14pt
)

#set par(
  justify: true,
  leading: 0.52em,
)

// Load report data
#let rep = json(sys.inputs.at("file"))

#grid(columns: (1fr, auto), column-gutter: 1em, [
  #heading(level: 1, "Genome Annotation Report")
  _Report generated: #datetime.today().display()_
], [
  #image("embl.svg", width: 150pt)
])


The #text(fill: rgb("#009f4c"))[#rep.scientific_name]
genome assembly #text(fill: rgb("#009f4c"))[#rep.assembly_accession]
was annotated by #text(fill: rgb("#009f4c"))[#rep.contact_name (#rep.contact_id)].
This annotation includes #text(fill: rgb("#009f4c"))[#rep.agat.transcript_count]
transcribed mRNAs from #text(fill: rgb("#009f4c"))[#rep.agat.gene_count] genes.
The average transcript length is #text(fill: rgb("#009f4c"))[#calc.round(rep.agat.mean_transcript_length, digits: 2)] bp,
with an average of #text(fill: rgb("#009f4c"))[#rep.agat.mean_transcripts_per_gene]
coding transcripts per gene and #text(fill: rgb("#009f4c"))[#rep.agat.mean_exons_per_transcript]
exons per transcript. The annotation file is available at #text(fill: rgb("#009f4c"))[#rep.annotation_file_url_or_path].

#v(1em)

// Summary Section
== Summary

#table(
  columns: 2,
  stroke: none,
  [*Number of genes:*], [#rep.agat.gene_count],
  [*Number of CDSs:*], [#rep.agat.cds_count],
  [*Number of transcripts:*], [#rep.agat.transcript_count],
  [*Mean transcript length:*], [#calc.round(rep.agat.mean_transcript_length, digits: 2) bp],
  [*Mean transcripts per gene:*], [#rep.agat.mean_transcripts_per_gene],
  [*Mean exons per transcript:*], [#rep.agat.mean_exons_per_transcript],
  [*BUSCO summary:*], [#rep.busco.one_line_summary],
  [*BUSCO lineage dataset:*], [#rep.busco.lineage_name],
  [*BUSCO mode:*], [#rep.busco.mode],
  [*OMArk completeness:*], [#rep.omark.omark_completeness_summary],
  [*OMArk lineage:*], [#rep.omark.omark_lineage],
  [*OMArk consistency:*], [#rep.omark.omark_consistency_summary],
//  [*Number of proteins in proteome:*], [#rep.omark.omark_protein_count],
//  [#pad(left: 1em)[*Proportion consistent:*]], [#rep.omark.omark_percent_consistent%],
//  [#pad(left: 1em)[*Proportion inconsistent:*]], [#rep.omark.omark_percent_inconsistent%],
//  [#pad(left: 1em)[*Proportion contaminants:*]], [#rep.omark.omark_percent_contaminant%],
//  [#pad(left: 1em)[*Proportion unknown:*]], [#rep.omark.omark_percent_unknown%]
)

#v(1em)

// Metadata Table
== Metadata

#table(
  columns: 2,
  stroke: none,
[*Project ID:*], [#rep.project_id],
[*Study name:*], [#rep.study_name],
[*Project description:*], [#rep.project_description],
[*Contact name:*], [#rep.contact_name],
[*Contact ID:*], [#rep.contact_id],
[*Contact email:*], [#rep.contact_email],
[*Taxon ID:*], [#rep.taxon_id],
[*Scientific name:*], [#rep.scientific_name],
[*Assembly accession:*], [#rep.assembly_accession],
[*Assembly seqcol digest:*], [#rep.seqcol_digest],
[*Assembly aliases:*], [#rep.assembly_aliases],
[*Evidence ID:*], [#rep.evidence_id],
[*Evidence type:*], [#rep.evidence_type],
[*Evidence version or date of retrieval:*], [#rep.evidence_version_or_date_of_retrieval],
[*Evidence source:*], [#rep.evidence_source],
[*Annotation tools:*], [#rep.annotation_tools],
[*Annotation tool versions:*], [#rep.annotation_tool_versions],
[*Annotation protocol:*], [#rep.annotation_workflow_or_protocol],
[*Annotation file label:*], [#rep.annotation_file_local_id],
[*Annotation file URL:*], [#rep.annotation_file_url_or_path],
[*Annotation file type:*], [#rep.annotation_file_type],
[*Annotation file checksum:*], [#rep.annotation_file_checksum]
)

#v(1em)

// AGAT Full Stats
== AGAT Full Stats

=== Counts
#table(
  columns: (25%, auto),
  stroke: none,
  [*AGAT stats calculated from:*], [annotated #rep.agat.feature_stats_calculated_for],
  [*Genes:*], [#rep.agat.gene_count],
  [*Transcripts:*], [#rep.agat.transcript_count],
  [*Exons:*], [#rep.agat.exon_count],
  [*CDS:*], [#rep.agat.cds_count],
  [*Introns:*], [#rep.agat.intron_count],
  [*Single exon genes:*], [#rep.agat.single_exon_gene_count],
  [*Single exon transcripts:*], [#rep.agat.single_exon_transcript_count],
)

#v(0.5em)

=== Mean Ratios
#table(
  columns: (25%, auto),
  stroke: none,
  [*Transcripts per gene:*], [#rep.agat.mean_transcripts_per_gene],
  [*Exons per transcript:*], [#rep.agat.mean_exons_per_transcript],
  [*Exons per CDS:*], [#rep.agat.mean_exons_per_cds],
  [*CDS per transcript:*], [#rep.agat.mean_cdss_per_transcript],
  [*Introns per transcript:*], [#rep.agat.mean_introns_per_transcript],
)

#v(0.5em)

=== Mean Lengths (bp)
#table(
  columns: (25%, auto),
  stroke: none,
  [*Gene:*], [#calc.round(rep.agat.mean_gene_length, digits: 2)],
  [*Transcript:*], [#calc.round(rep.agat.mean_transcript_length, digits: 2)],
  [*Exon:*], [#calc.round(rep.agat.mean_exon_length, digits: 2)],
  [*CDS:*], [#calc.round(rep.agat.mean_cds_length, digits: 2)],
  [*Intron:*], [#calc.round(rep.agat.mean_intron_length, digits: 2)],
)

#v(0.5em)

=== Median Lengths (bp)
#table(
  columns: (25%, auto),
  stroke: none,
  [*Gene:*], [#calc.round(rep.agat.median_gene_length, digits: 2)],
  [*Transcript:*], [#calc.round(rep.agat.median_transcript_length, digits: 2)],
  [*Exon:*], [#calc.round(rep.agat.median_exon_length, digits: 2)],
  [*CDS:*], [#calc.round(rep.agat.median_cds_length, digits: 2)],
  [*Intron:*], [#calc.round(rep.agat.median_intron_length, digits: 2)],
)

#v(0.5em)

=== Total Lengths (bp)
#table(
  columns: (25%, auto),
  stroke: none,
  [*Genes:*], [#rep.agat.total_gene_length],
  [*Transcripts:*], [#rep.agat.total_transcript_length],
  [*Exons:*], [#rep.agat.total_exon_length],
  [*CDS:*], [#rep.agat.total_cds_length],
  [*Introns:*], [#rep.agat.total_intron_length],
)


#v(0.5em)

=== Longest Features (bp)
#table(
  columns: (25%, auto),
  stroke: none,
  [*Gene:*], [#rep.agat.longest_gene],
  [*Transcript:*], [#rep.agat.longest_transcript],
  [*Exon:*], [#rep.agat.longest_exon],
  [*CDS:*], [#rep.agat.longest_cds],
  [*Intron:*], [#rep.agat.longest_intron],
)

#v(0.5em)

=== Shortest Features (bp)
#table(
  columns: (25%, auto),
  stroke: none,
  [*Gene:*], [#rep.agat.shortest_gene],
  [*Transcript:*], [#rep.agat.shortest_transcript],
)

#v(1em)

// BUSCO Full Stats
== BUSCO Full Stats

#table(
  columns: (25%, auto),
  stroke: none,
  [*Version:*], [#rep.busco.version_busco],
  [*Lineage dataset:*], [#rep.busco.lineage_name],
  [*Mode:*], [#rep.busco.mode],
  [*One line summary:*], [#rep.busco.one_line_summary],
  [*Complete BUSCOs:*], [#rep.busco.complete_percent%],
  [*Single-copy:*], [#rep.busco.single_copy_percent%],
  [*Duplicated:*], [#rep.busco.duplicated_percent%],
  [*Fragmented:*], [#rep.busco.fragmented_percent%],
  [*Missing:*], [#rep.busco.missing_percent%],
  [*Total markers:*], [#rep.busco.n_markers],
)

#v(1em)

// Omark Full Stats
== OMArk Full Stats

=== Assessment information
#table(
  columns: 2,
  stroke: none,
  [*OMAmer version:*], [#rep.omark.omamer_version],
  [*OMAmer database version:*], [#rep.omark.omamer_db_version],
)

#v(0.5em)

=== Completeness Assessment
#table(
  columns: 2,
  stroke: none,
  [*Clade:*], [#rep.omark.omark_lineage],
  [*Total HOGs:*], [#rep.omark.conserved_hogs],
  [*Single-copy:*], [#rep.omark.single_hog_percent%],
  [*Total duplicated:*], [#rep.omark.duplicated_hog_percent%],
  [ #pad(left: 1em)[Duplicated (expected):]], [#rep.omark.expected_dup_hog_percent%],
  [ #pad(left: 1em)[Duplicated (unexpected):]], [#rep.omark.unexpected_dup_hog_percent%],
  [*Missing:*], [#rep.omark.missing_hog_percent%],
)

#v(0.5em)

=== Consistency Assessment
#table(
  columns: 2,
  stroke: none,
  [*Total proteins:*], [#rep.omark.omark_protein_count],
  [*Consistent:*], [#rep.omark.omark_percent_consistent%],
  [#pad(left: 1em)[Partial consistent:]], [#rep.omark.percent_consistent_partial%],
  [#pad(left: 1em)[Fragmented consistent:]], [#rep.omark.percent_consistent_fragments%],
  [*Inconsistent:*], [#rep.omark.omark_percent_inconsistent%],
  [#pad(left: 1em)[Partial inconsistent:]], [#rep.omark.percent_inconsistent_partial%],
  [#pad(left: 1em)[Fragmented inconsistent:]], [#rep.omark.percent_inconsistent_fragments%],
  [*Contaminants*:], [#rep.omark.omark_percent_contaminant%],
  [#pad(left: 1em)[Partial contaminants:]], [#rep.omark.percent_contaminant_partial%],
  [#pad(left: 1em)[Fragmented contaminants:]], [#rep.omark.percent_contaminant_fragments%],
  [*Unknown:*], [#rep.omark.omark_percent_unknown%],
)

#v(0.5em)
#let rows = rep.omark.detected_sp.map(r => (r.Clade, r.NCBI_taxid, r.Number_of_associated_proteins, r.Percentage_of_proteomes_total))

=== Detected Species
#table(
  columns: 4,
  stroke: none,
  table.header(
    [*Clade*], [*Taxon ID*], [*Protein count*], [*Proteome %*]
  ),
  ..for (clade, taxid, number, perc) in rows {
    ([#clade], [#taxid], [#number], [#perc])
  }
)