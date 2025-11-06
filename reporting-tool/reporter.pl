#!/usr/bin/env perl
use warnings;
use strict;
use feature 'say';

# Script to generate annotation report.
#
# We assume a metadata file and an AGAT report file are provided 
# Example files are in this repo.
# The metadata file is a placeholder. It will change when the actual metadata
# schema + data are ready
# 
# The AGAT file is not useable by the PDF renderer, we have to remove the header
# line first.
#
# Futher analysis files, e.g. Busco, are TODO
#
# Requirements to run this are:
# Perl
# duckdb - duckdb.org
# typst - typst.app

use v5.10.1;
no warnings 'experimental';

use Data::Dumper;
use List::Util 'uniq';
use Getopt::Long;
use JSON;
use YAML::XS qw(LoadFile);

my ($meta_file, $gff_file, $agat_file, $busco_file);
GetOptions(
    'm=s' => \$meta_file,
    'g=s' => \$gff_file, # TODO
    'a=s' => \$agat_file,
    'b=s' => \$busco_file,
) or die_usage();

sub die_usage {
    die "Usage: $0 [-m metadata_file] [-g gff_file] [-a agat_file] [-b busco_file]";
}

sub check_exit {
    return if $? == 0;
    if ($? == -1) {
        die "failed to execute: $!\n";
    }
    elsif ($? & 127) {
        die sprintf "child died with signal %d, %s coredump\n",
        ($? & 127),  ($? & 128) ? 'with' : 'without';
    }
    else {
        die sprintf "child exited with value %d\n", $? >> 8;
    }
}


die "Need metadata csv file" unless ($meta_file);

my $json = qx(duckdb -json -c 'select bioproject_name, bioproject_id, refseq_accession, asm_name, release_date, organism_id, tol_prefix  from dtol_metadata limit 1;' $meta_file);
check_exit();

my $metadata = decode_json($json);
my $report_data = $metadata->[0];

if ($agat_file) {
    my $agat_yaml = LoadFile($agat_file);
    
    # Navigate to the statistics section
    my $stats = $agat_yaml->{transcript}{without_isoforms}{value};
    
    # Extract and consolidate selected AGAT fields into a single 'agat' section
    my %agat = ();
    
    # AGAT version - extract from YAML if available, otherwise placeholder
    $agat{version} = $agat_yaml->{version} // "unknown";
    
    # Extract key statistics with renamed fields (convert to numeric)
    $agat{gene_count} = $stats->{"Number of gene"} + 0;
    $agat{transcript_count} = $stats->{"Number of transcript"} + 0;
    $agat{mean_transcript_length} = $stats->{"mean transcript length (bp)"} + 0;
    $agat{mean_transcripts_per_gene} = $stats->{"mean transcripts per gene"} + 0;
    $agat{mean_exons_per_transcript} = $stats->{"mean exons per transcript"} + 0;
    
    # Additional useful statistics (convert to numeric)
    $agat{exon_count} = $stats->{"Number of exon"} + 0;
    $agat{mean_exon_length} = $stats->{"mean exon length (bp)"} + 0;
    $agat{mean_gene_length} = $stats->{"mean gene length (bp)"} + 0;
    $agat{total_gene_length} = $stats->{"Total gene length (bp)"} + 0;
    $agat{total_transcript_length} = $stats->{"Total transcript length (bp)"} + 0;
    
    # Full statistics for detailed table
    $agat{cds_count} = $stats->{"Number of cds"} + 0;
    $agat{intron_count} = $stats->{"Number of intron"} + 0;
    $agat{single_exon_gene_count} = $stats->{"Number of single exon gene"} + 0;
    $agat{single_exon_transcript_count} = $stats->{"Number of single exon transcript"} + 0;
    
    # Mean statistics
    $agat{mean_cds_length} = $stats->{"mean cds length (bp)"} + 0;
    $agat{mean_intron_length} = $stats->{"mean intron length (bp)"} + 0;
    $agat{mean_cdss_per_transcript} = $stats->{"mean cdss per transcript"} + 0;
    $agat{mean_exons_per_cds} = $stats->{"mean exons per cds"} + 0;
    $agat{mean_introns_per_transcript} = $stats->{"mean introns per transcript"} + 0;
    
    # Median statistics
    $agat{median_gene_length} = $stats->{"median gene length (bp)"} + 0;
    $agat{median_transcript_length} = $stats->{"median transcript length (bp)"} + 0;
    $agat{median_exon_length} = $stats->{"median exon length (bp)"} + 0;
    $agat{median_cds_length} = $stats->{"median cds length (bp)"} + 0;
    $agat{median_intron_length} = $stats->{"median intron length (bp)"} + 0;
    
    # Longest/Shortest statistics
    $agat{longest_gene} = $stats->{"Longest gene (bp)"} + 0;
    $agat{longest_transcript} = $stats->{"Longest transcript (bp)"} + 0;
    $agat{longest_exon} = $stats->{"Longest exon (bp)"} + 0;
    $agat{longest_cds} = $stats->{"Longest cds (bp)"} + 0;
    $agat{longest_intron} = $stats->{"Longest intron (bp)"} + 0;
    $agat{shortest_gene} = $stats->{"Shortest gene (bp)"} + 0;
    $agat{shortest_transcript} = $stats->{"Shortest transcript (bp)"} + 0;
    
    # Total lengths
    $agat{total_cds_length} = $stats->{"Total cds length (bp)"} + 0;
    $agat{total_exon_length} = $stats->{"Total exon length (bp)"} + 0;
    $agat{total_intron_length} = $stats->{"Total intron length (bp)"} + 0;
    
    $report_data->{agat} = \%agat;
    
    say "Processed AGAT YAML file: extracted and consolidated fields";
}

if ($busco_file) {
    open(my $busco_fh, '<', $busco_file) or die "Error opening file $busco_file: $!";
    my $busco_content = do { local $/; <$busco_fh> };
    close($busco_fh) or die "Error closing file $busco_file: $!";
    
    my $busco_data = decode_json($busco_content);
    
    my %busco = ();
    
    if ($busco_data->{lineage_dataset}) {
        $busco{lineage_name} = $busco_data->{lineage_dataset}{name};
    }
    
    if ($busco_data->{versions}) {
        $busco{version_busco} = $busco_data->{versions}{busco};
        $busco{version_hmmsearch} = $busco_data->{versions}{hmmsearch};
        $busco{version_metaeuk} = $busco_data->{versions}{metaeuk};
    }
    
    if ($busco_data->{results}) {
        $busco{one_line_summary} = $busco_data->{results}{one_line_summary};
        $busco{complete_percent} = $busco_data->{results}{Complete};
        $busco{single_copy_percent} = $busco_data->{results}{"Single copy"};
        $busco{duplicated_percent} = $busco_data->{results}{"Multi copy"};
        $busco{fragmented_percent} = $busco_data->{results}{Fragmented};
        $busco{missing_percent} = $busco_data->{results}{Missing};
        $busco{n_markers} = $busco_data->{results}{n_markers};
        $busco{domain} = $busco_data->{results}{domain};
    }
    
    if ($busco_data->{parameters}) {
        $busco{mode} = $busco_data->{parameters}{mode};
        $busco{gene_predictor} = $busco_data->{parameters}{gene_predictor};
    }
    
    $report_data->{busco} = \%busco;
    
    say "Processed BUSCO file: extracted and consolidated selected fields";
}

# Write the combined data to file report_main.json
my $json_encoder = JSON->new->pretty->canonical;
my $output_json = $json_encoder->encode([$report_data]);

open (my $fh, '>', 'report_main.json') or die "Error opening file report_main.json: $!";
print $fh $output_json;
close($fh) or die "Error closing file report_main.json: $!";

say "Generated report_main.json with metadata and BUSCO data";

# Compile PDF
say qx(typst compile --input file=report_main.json report_template.typ report.pdf);
check_exit();

say "Build OK. PDF file is report.pdf";
