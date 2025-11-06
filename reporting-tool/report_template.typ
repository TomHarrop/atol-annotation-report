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
#let rep_in = json(sys.inputs.at("file"))
#let rep = rep_in.at(0)


#grid(columns: (1fr, auto), column-gutter: 1em, [
  #heading(level: 1, "Genome Annotation Report")
  _Report generated: #datetime.today().display()_
], [
  #image("embl.svg", width: 150pt)
])


The #text(fill: rgb("#009f4c"))[{species_name}] genome assembly #text(fill: rgb("#009f4c"))[#rep.refseq_accession] was annotated by
#text(fill: rgb("#009f4c"))[{facility/organisation/contact}]. This annotation includes #text(fill: rgb("#009f4c"))[#rep.agat.transcript_count]
transcribed mRNAs from #text(fill: rgb("#009f4c"))[#rep.agat.gene_count] genes. The average transcript length is
#text(fill: rgb("#009f4c"))[#rep.agat.mean_transcript_length] bp, with an average of
#text(fill: rgb("#009f4c"))[#rep.agat.mean_transcripts_per_gene] coding transcripts per gene and
#text(fill: rgb("#009f4c"))[#rep.agat.mean_exons_per_transcript] exons per transcript. The annotation file is
available at #text(fill: rgb("#009f4c"))[{url}].

#v(1em)

// Summary Section
== Summary

#table(
  columns: 2,
  stroke: none,
  [*Number of genes:*], [#rep.agat.gene_count],
  [*Number of transcripts:*], [#rep.agat.transcript_count],
  [*Mean transcript length:*], [#calc.round(rep.agat.mean_transcript_length, digits: 2) bp],
  [*Mean transcripts per gene:*], [#rep.agat.mean_transcripts_per_gene],
  [*Mean exons per transcript:*], [#rep.agat.mean_exons_per_transcript],
  [*BUSCO summary:*], [#rep.busco.one_line_summary],
  [*BUSCO lineage dataset:*], [#rep.busco.lineage_name],
  [*BUSCO mode:*], [#rep.busco.mode],
  // TO DO Add OMARk stats:
  // [*OMARK clade:*], [TO DO],
  // [*OMAmer database version:*], [TO DO],
  // [*OMARK version:*], [TO DO],
  // [*Number of proteins in proteome:*], [TO DO],
)

#v(1em)

// Metadata Table
== Metadata

#table(
  columns: 2,
  [*Taxon ID*],      [{taxon_id}],
  [*Species name*],      [{species_name}],
  [*ToL prefix*],       [#rep.tol_prefix],
  [*Assembly accession*], [#rep.refseq_accession],
)

#v(1em)


#v(0.5em)

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

#v(0.5em)

// AGAT Full Stats
== AGAT Full Stats

=== Counts
#table(
  columns: (25%, auto),
  stroke: none,
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


// TO DO add OMARK Full Stats
== OMARK Full Stats