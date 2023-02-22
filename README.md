# mitts
MITTS - Mutations In Twenty Three S

Simple tool that estimates the number of 23S copies that contain a given point mutation, given a reference and a known position

*UNDER DEVELOPMENT*

# Installation

`conda create -n mitts pysam pysamstats bowtie2 samtools`

`git clone https://github.com/stroehleina/mitts`

# Quick start

`python mitts.py --help`

```
usage: mitts.py [-h] [--version] [--species SPECIES] [--fastq1 FASTQ1]
                [--fastq2 FASTQ2] [--threads THREADS] [--mincov MINCOV]

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
  --mincov MINCOV, -m MINCOV
                        Minimum coverage at mutation position to make a call
                        (default: 60)
```
