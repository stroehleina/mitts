# mitts
MITTS - Mutations In Twenty Three S

Simple tool that estimates the number of 23S copies that contain a given point mutation, given a reference and a known position

*UNDER DEVELOPMENT*

# Installation

`conda create -n mitts pysam pysamstats bowtie2 samtools`

`conda activate mitts`

`git clone https://github.com/stroehleina/mitts`

# Quick start

`python mitts.py --help`

```
usage: mitts.py [-h] [--version] --species SPECIES --fastq1 FASTQ1 --fastq2
                FASTQ2 [--threads THREADS] [--output OUTPUT] [--mincov MINCOV]

MITTS - Mutations In Twenty Three S

optional arguments:
  -h, --help            show this help message and exit
  --version, -v         show program's version number and exit
  --species SPECIES, -s SPECIES
                        Species that you want to investigate 23S mutations
                        for, choose from ['ENTEROCOCCUS', 'NEISSERIA']
                        (default: None)
  --fastq1 FASTQ1, -1 FASTQ1
                        R1 reads in FASTQ format (can be gzipped) (default:
                        None)
  --fastq2 FASTQ2, -2 FASTQ2
                        R2 reads in FASTQ format (can be gzipped) (default:
                        None)
  --threads THREADS, -t THREADS
                        Number of threads to use (default: 1)
  --output OUTPUT, -o OUTPUT
                        Define prefix for output bam file (default: None)
  --mincov MINCOV, -m MINCOV
                        Minimum coverage at mutation position to make a call
                        (default: 60)
```

# Defining references

References are defined in the classs *Species* in `species.py` as follows:

```
    'MYSPECIESNAME' : {
      'reference' : '/path/to/fasta/reference.fa', # Should only contain one sequence
      'chrom' : 'my_fasta_header',  # The header of the fasta sequence (without ">")
      'bowtie_ref' : '/path/to/bowtie/database/bt_myspecies',  # Path to bowtie-2 database files created with bowtie2-build -f reference.fa bt_myspecies
      'positions' : [2589, 2518], # List of positions (1-based) in the reference that you want to investigate for mutations
      'reference_nucls' : ['G', 'G'], # List of nucleotides in the reference at the respective positions
      'variant_nucls' : ['T', 'A'], # List of mutated nucleotides that you want to report
      'mutations' : ['G2576T', 'G2505A'], # Name of mutation (e.g, if using E. coli numbering)
      'copy_number' : 6 # Number of 23S copies present in the genome
    }
```

If you have a reference sequence and know the positions of the point mutations that you are interested in you can simply add them to this file and then call `mitts` with the `--species myspecies` flag (`mitts` will automatically convert to uppercase so Myspecies, myspecies, MySpecies and MYSPECIES will work).

## Choice of reference

When choosing a reference, make sure that it contains a reasonably-sized (depending on your read length and insert size) flanking region up- and down-stream of all positions of interest, otherwise you will grossly underestimate the number of reads mapped to the position and thus, your call will become less accurate, or may be skipped if the coverage drops below `--mincov` (default: 60).
