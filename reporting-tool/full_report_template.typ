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
//  #image("embl.svg", width: 150pt)
])

#if rep.metadata_input_provided == true [
  The #emph[#rep.scientific_name]
  genome assembly #rep.assembly_accession
  was annotated by #rep.contact_name (#rep.contact_id).
]
#if rep.agat.agat_input_provided == true [
  #if rep.agat.transcript_count != "N/A" [
    This annotation includes #rep.agat.transcript_count
    transcribed mRNAs from #rep.agat.gene_count genes.
  ]
  #if rep.agat.mrna_count != "N/A" [
    This annotation includes #rep.agat.mrna_count
    mRNAs from #rep.agat.gene_count genes.
  ]
  #if rep.agat.mean_transcript_length != "N/A" [
    The average transcript length is  
    #calc.round(rep.agat.mean_transcript_length, digits: 2)bp,
    with an average of #rep.agat.mean_transcripts_per_gene
    coding transcripts per gene and #rep.agat.mean_exons_per_transcript
    exons per transcript.
  ]
  #if rep.agat.mean_mrna_length != "N/A" [
    The average mRNA length is 
    #calc.round(rep.agat.mean_mrna_length, digits: 2)bp,
    with an average of #rep.agat.mean_mrnas_per_gene
    mRNAs per gene and #rep.agat.mean_exons_per_mrna
    exons per mRNA.
  ]
]
#if rep.metadata_input_provided == true [
  The annotation file is available at #rep.annotation_file_url_or_path.
]

#v(1em)

// Summary Section
== Summary

#table(
  columns: 2,
  stroke: none,
  [*Number of genes:*], [#if rep.agat.agat_input_provided == true [#rep.agat.gene_count] else [Not calculated]],
  [*Number of CDSs:*], [#if rep.agat.agat_input_provided == true [#rep.agat.cds_count] else [Not calculated]],
  [#if rep.agat.agat_input_provided == true [#if rep.agat.mrna_count != "N/A" [*Number of mRNAs:*] else [*Number of transcripts:*]] else [*Number of transcripts:*]], [#if rep.agat.agat_input_provided == true [#if rep.agat.mrna_count != "N/A" [#rep.agat.mrna_count] else [#rep.agat.transcript_count]] else [Not calculated]],
  [#if rep.agat.agat_input_provided == true [#if rep.agat.mean_mrna_length != "N/A" [*Mean mRNA length:*] else [*Mean transcript length:*]] else [*Mean transcript length:*]], [#if rep.agat.agat_input_provided == true [#if rep.agat.mean_mrna_length != "N/A" [#calc.round(rep.agat.mean_mrna_length, digits: 2)] else if rep.agat.mean_transcript_length != "N/A" [#calc.round(rep.agat.mean_transcript_length, digits: 2)]] else [Not calculated]],
  [#if rep.agat.agat_input_provided == true [#if rep.agat.mean_mrnas_per_gene != "N/A" [*Mean mRNAs per gene:*] else [*Mean transcripts per gene:*]] else [*Mean transcripts per gene:*]], [#if rep.agat.agat_input_provided == true [#if rep.agat.mean_mrnas_per_gene != "N/A" [#rep.agat.mean_mrnas_per_gene] else [#rep.agat.mean_transcripts_per_gene]] else [Not calculated]],
  [#if rep.agat.agat_input_provided == true [#if rep.agat.mean_exons_per_mrna != "N/A" [*Mean exons per mRNA:*] else [*Mean exons per transcript:*]] else [*Mean exons per transcript:*]], [#if rep.agat.agat_input_provided == true [#if rep.agat.mean_exons_per_mrna != "N/A" [#rep.agat.mean_exons_per_mrna] else [#rep.agat.mean_exons_per_transcript]] else [Not calculated]],
  [*BUSCO summary:*], [#if rep.busco.busco_input_provided == true [#rep.busco.one_line_summary] else [Not calculated]],
  [*BUSCO lineage dataset:*], [#if rep.busco.busco_input_provided == true [#rep.busco.lineage_name] else [Not calculated]],
  [*BUSCO mode:*], [#if rep.busco.busco_input_provided == true [#rep.busco.mode] else [Not calculated]],
  [*OMArk completeness:*], [#if rep.omark.omark_input_provided == true [#rep.omark.omark_completeness_summary] else [Not calculated]],
  [*OMArk lineage:*], [#if rep.omark.omark_input_provided == true [#rep.omark.omark_lineage] else [Not calculated]],
  [*OMArk consistency:*], [#if rep.omark.omark_input_provided == true [#rep.omark.omark_consistency_summary] else [Not calculated]],
//  [*Number of proteins in proteome:*], [#rep.omark.omark_protein_count],
//  [#pad(left: 1em)[*Proportion consistent:*]], [#rep.omark.omark_percent_consistent%],
//  [#pad(left: 1em)[*Proportion inconsistent:*]], [#rep.omark.omark_percent_inconsistent%],
//  [#pad(left: 1em)[*Proportion contaminants:*]], [#rep.omark.omark_percent_contaminant%],
//  [#pad(left: 1em)[*Proportion unknown:*]], [#rep.omark.omark_percent_unknown%]
)

#if rep.metadata_input_provided == true [

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
  [*Scientific name:*], [#emph[#rep.scientific_name]],
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
]

#if rep.agat.agat_input_provided == true [

  #v(1em)

  // AGAT Full Stats
  == AGAT Full Stats

  === Counts
  #table(
    columns: (25%, auto),
    stroke: none,
    [*AGAT stats calculated from:*], [annotated #rep.agat.feature_stats_calculated_for],
    [*Genes:*], [#rep.agat.gene_count],
    [#if rep.agat.mrna_count != "N/A" [*mRNAs:*] else [*Transcripts:*]], [#if rep.agat.mrna_count != "N/A" [#rep.agat.mrna_count] else [#rep.agat.transcript_count]],
    [*Exons:*], [#rep.agat.exon_count],
    [*CDS:*], [#rep.agat.cds_count],
    [*Introns:*], [#rep.agat.intron_count],
    [*Single exon genes:*], [#rep.agat.single_exon_gene_count],
    [#if rep.agat.single_exon_mrna_count != "N/A" [*Single exon mRNAs:*] else [*Single exon transcripts:*]], [#if rep.agat.single_exon_mrna_count != "N/A" [#rep.agat.single_exon_mrna_count] else [#rep.agat.single_exon_transcript_count]],
  )

  #v(0.5em)

  === Mean Ratios
  #table(
    columns: (25%, auto),
    stroke: none,
    [#if rep.agat.mean_mrnas_per_gene != "N/A" [*mRNAs per gene:*] else [*Transcripts per gene:*]], [#if rep.agat.mean_mrnas_per_gene != "N/A" [#rep.agat.mean_mrnas_per_gene] else [#rep.agat.mean_transcripts_per_gene]],
    [#if rep.agat.mean_exons_per_mrna != "N/A" [*Exons per mRNA:*] else [*Exons per transcript:*]], [#if rep.agat.mean_exons_per_mrna != "N/A" [#rep.agat.mean_exons_per_mrna] else [#rep.agat.mean_exons_per_transcript]],
    [*Exons per CDS:*], [#rep.agat.mean_exons_per_cds],
    [#if rep.agat.mean_cdss_per_mrna != "N/A" [*CDS per mRNA:*] else [*CDS per transcript:*]], [#if rep.agat.mean_cdss_per_mrna != "N/A" [#rep.agat.mean_cdss_per_mrna] else [#rep.agat.mean_cdss_per_transcript]],
    [*Introns per transcript:*], [#rep.agat.mean_introns_per_transcript],
  )

  #v(0.5em)

  === Mean Lengths (bp)
  #table(
    columns: (25%, auto),
    stroke: none,
    [*Gene:*], [#calc.round(rep.agat.mean_gene_length, digits: 2)],
    [#if rep.agat.mean_mrna_length != "N/A" [*mRNA:*] else [*Transcript:*]], [#if rep.agat.mean_mrna_length != "N/A" [#calc.round(rep.agat.mean_mrna_length, digits: 2)] else if rep.agat.mean_transcript_length != "N/A" [#calc.round(rep.agat.mean_transcript_length, digits: 2)] else [N/A]],
    [*Exon:*], [#calc.round(rep.agat.mean_exon_length, digits: 2)],
    [*CDS:*], [#calc.round(rep.agat.mean_cds_length, digits: 2)],
    [*Intron:*], [#if rep.agat.mean_intron_length != "N/A" [#calc.round(rep.agat.mean_intron_length, digits: 2)] else [#rep.agat.mean_intron_length]],
  )

  #v(0.5em)

  === Median Lengths (bp)
  #table(
    columns: (25%, auto),
    stroke: none,
    [*Gene:*], [#calc.round(rep.agat.median_gene_length, digits: 2)],
    [#if rep.agat.median_mrna_length != "N/A" [*mRNA:*] else [*Transcript:*]], [#if rep.agat.median_mrna_length != "N/A" [#calc.round(rep.agat.median_mrna_length, digits: 2)] else if rep.agat.median_transcript_length != "N/A" [#calc.round(rep.agat.median_transcript_length, digits: 2)] else [N/A]],
    [*Exon:*], [#calc.round(rep.agat.median_exon_length, digits: 2)],
    [*CDS:*], [#calc.round(rep.agat.median_cds_length, digits: 2)],
    [*Intron:*], [#if rep.agat.median_intron_length != "N/A" [#calc.round(rep.agat.median_intron_length, digits: 2)] else [#rep.agat.median_intron_length]],
  )

  #v(0.5em)

  === Total Lengths (bp)
  #table(
    columns: (25%, auto),
    stroke: none,
    [*Genes:*], [#rep.agat.total_gene_length],
    [#if rep.agat.total_mrna_length != "N/A" [*mRNAs:*] else [*Transcripts:*]], [#if rep.agat.total_mrna_length != "N/A" [#rep.agat.total_mrna_length] else [#rep.agat.total_transcript_length]],
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
    [#if rep.agat.longest_mrna != "N/A" [*mRNA:*] else [*Transcript:*]], [#if rep.agat.longest_mrna != "N/A" [#rep.agat.longest_mrna] else [#rep.agat.longest_transcript]],
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
    [#if rep.agat.shortest_transcript != "N/A" [*mRNA:*] else [*Transcript:*]], [#if rep.agat.shortest_transcript != "N/A" [#rep.agat.shortest_transcript] else [#rep.agat.shortest_transcript]],
  )
]

#if rep.busco.busco_input_provided == true [

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
]

#if rep.omark.omark_input_provided == true [

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

  #if rep.omark.detected_sp != ("N/A",) {
    [
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
    ]
  }

  #if rep.omark.contaminant_sp != ("N/A",) {
    [
      #v(0.5em)
      #let contam_rows = rep.omark.contaminant_sp.map(r => (r.Potential_contaminants))

      === Detected Contaminant Species
      #table(
        columns: 2,
        stroke: none,
        ..for contam in contam_rows {
          ([*Potential contaminant:*], [#contam])
        }
      )
    ]
  }
]

#if rep.annooddities.annooddities_input_provided == true [

  #v(1em)

  // AnnoOddities results
  == AnnoOddities Results

  #table(
    columns: 2,
    stroke: none,
    [*Single exon transcripts:*], [#rep.annooddities.single_exon_transcripts],
    [*Multi-exon transcripts:*], [#rep.annooddities.multi_exon_transcripts],
    [*Transcripts with 5' UTR > 10,000bp:*], [#rep.annooddities.five_utr_above_10000bp],
    [*Transcripts with more than 5 5' UTRs:*], [#rep.annooddities.five_utr_num_above_5],
    [*Transcripts with 3' UTR > 10,000bp:*], [#rep.annooddities.three_utr_above_10000bp],
    [*Transcripts with more than 4 3' UTRs:*], [#rep.annooddities.three_utr_num_above_4],
    [*Incomplete transcripts:*], [#rep.annooddities.incomplete_transcripts],
    [*Transcripts without start codons:*], [#rep.annooddities.missing_start_codon],
    [*Transcripts without stop codons:*], [#rep.annooddities.missing_stop_codon],
    [*Fragmented transcripts:*], [#rep.annooddities.fragmented],
    [*Transcripts with inframe stop codons:*], [#rep.annooddities.has_inframe_stop_codons],
    [*Transcripts with an exon > 10,000bp:*], [#rep.annooddities.max_exon_above_10000bp],
    [*Transcripts with an intron > 120,000bp:*], [#rep.annooddities.max_intron_above_120000bp],
    [*Transcripts with an exon < 4bp:*], [#rep.annooddities.min_exon_below_5bp],
    [*Transcripts with an intron between 1 and 5bp:*], [#rep.annooddities.min_intron_bw_0_and_5bp],
    [*Transcripts with CDS proprtion < 30%:*], [#rep.annooddities.cds_fraction_below_30pc],
    [*Transcripts with non-canonical introns:*], [#rep.annooddities.has_non_canonical_introns],
    [*Transcripts with non-canonical splicing only:*], [#rep.annooddities.only_non_canonical_splicing],
    [*Transcripts with suspicious_splicing:*], [#rep.annooddities.has_suspicious_splicing]
  )
]