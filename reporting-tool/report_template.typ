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


// Heading
= Genome Annotation Report

#align(right + top)[
  #image("embl.svg", width: 20%)
]


// Various bits of data are not there yet

The [#rep.organism_id] genome assembly [#rep.refseq_accession] was annotated by
{facility/organisation/contact}. This annotation includes {transcript_number}
transcribed mRNAs from {gene_number} genes. The average transcript length is
{average_transcript_length} bp, with an average of
{average_coding_transcripts_per_gene} coding transcripts per gene and
{average_exons_per_transcripts} exons per transcript. The annotation file is
available at {url}.


// Table with core annotation info
// At the moment, this is an EnsEMBL metadata CSV - this will change to the
// proper metadata schema once this is ready
#table(
  columns: 2,
  [*Organism ID*],      [#rep.organism_id],
  [*ToL prefix*],       [#rep.tol_prefix],
  [*Bioproject name*],  [#rep.bioproject_name],
  [*Bioproject ID*],    [#rep.bioproject_id],
  [*Assembly name*],    [#rep.asm_name],
  [*Refseq accession*], [#rep.refseq_accession],
  [*Release Date*],     [#rep.release_date]
)


// Load and display statistics data from agat
// Assumes an agat file without the header line
#let agat-report = {
  let agat-report-raw = csv("report_input.csv", delimiter: "\t");
  rows-to-records(
    ("A", "B", "C", "D"),
    agat-report-raw.slice(0, -1), // The rest of the rows
  )
}

#let agat-report-head = agat-report.slice(0, 4);

#tabut(
  agat-report-head,
  (
    (header: [*Type*], func: r => r.A),
    (header: [*Number*], func: r => r.B),
    (header: [*Size total (kb)*], func: r => r.C),
    (header: [*Size mean (kb)*], func: r => r.D),
  ),
  fill: (_, row) => if calc.odd(row) { luma(240) } else { luma(220) },
  stroke: none
)
