from species import Species
from bowtie import BowtieRunner
import pysam
import pysamstats
import argparse


VERSION = '0.0.1'

def set_parser():
    '''Sets command line argument options and parses them'''
    parser = argparse.ArgumentParser(description='MITTS - Mutations In Twenty Three S',formatter_class=argparse.ArgumentDefaultsHelpFormatter)
    parser.add_argument('--version', '-v', action='version', version='%(prog)s ' + VERSION)
    parser.add_argument('--species', '-s', help=f'Species that you want to investigate 23S mutations for, choose from {list(Species.available.keys())}', required=True)
    parser.add_argument('--fastq1', '-1', help=f'R1 reads in FASTQ format (can be gzipped)', required=True)
    parser.add_argument('--fastq2', '-2', help=f'R2 reads in FASTQ format (can be gzipped)', required=True)
    parser.add_argument('--threads', '-t', help=f'Number of threads to use', default='1')
    parser.add_argument('--output', '-o', help=f'Define prefix for output bam file')
    parser.add_argument('--mincov', '-m', help=f'Minimum coverage at mutation position to make a call', default='60')
    # TODO also report novel

    args = parser.parse_args()
    return args

def main():

    args=set_parser()
    species = Species(args.species)
    bt_runner = BowtieRunner(bowtie_ref=species.bowtie_ref, reference=species.reference, fastq1=args.fastq1, fastq2=args.fastq2, threads=args.threads, bamout=args.output)
    bam_file = bt_runner.run_bowtie()
    bam = pysam.AlignmentFile(bam_file)


    # iterate over each position in the species object
    for idx, position in enumerate(species.positions):

        # To truncate output to exactly the selected region, provide a truncate=True keyword argument.
        # opt.iter_pileup (pysamstats): one record is generated for each genome position in the selected range, based on a pileup column.
        # This should always run exactly once
        for rec in pysamstats.stat_variation(bam, chrom=species.chrom, fafile=species.reference, start=position-1, end=position, truncate=True):
            # only check the one mutation that has been provided, not others
            # Only consider properly paired reads ('_pp' suffix)
            pos, ref, reads, mutation = rec['pos'], rec['ref'], rec['reads_pp'], rec[species.variant_nucls[idx] + '_pp']
            
            assert ref == species.reference_nucls[idx]

            if reads < int(args.mincov):
                print(f'WARNING: Coverage at position of potential point mutation {species.mutations[idx]} for {args.output} is ({reads}), smaller than the minimum coverage specified ({args.mincov}). Skipping.')
            else:
                perc_at_mutation_position = mutation/reads*100
                percentages =  {x:100/species.copy_number*x for x in range(0,species.copy_number+1)}
                copies_with_mutation, closest_perc = min(percentages.items(), key = lambda x: abs(x[1]-perc_at_mutation_position))
                #  = [count for count, perc in percentages.items() if perc == closest_perc].pop()
                # print(f'An estimated {copies_with_mutation} out of {species.copy_number} 23S copies have mutation {species.mutations[idx]} ({mutation} / {reads} reads, {perc_at_mutation_position:.2f}%).')
                print("\t".join([str(x) for x in [args.output, copies_with_mutation, species.copy_number, species.mutations[idx], mutation, reads, f'{perc_at_mutation_position:.2f}']]))

if __name__ == "__main__":
    main()    
