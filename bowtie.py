from subprocess import run, CalledProcessError
import sys

def _check_executable(executable):
	try:
	    which = run(['which', executable], capture_output=True, text=True, check=True)
	    path = which.stdout.strip()
	    print(f'{executable} executable found in {path}')
	    return path
	except CalledProcessError as e:
	    print(f'Could not find {executable} executable. Check {executable} is installed correctly and in $PATH.')
	    print(f'{e.cmd}: {e.output}')
	    raise SystemExit(e)


class BowtieRunner:
	'''A class that implements a bowtie2 run and does some simple checking of executables'''

	def __init__(self, bowtie_ref, reference, fastq1, fastq2, threads):
		self.path = _check_executable('bowtie2')
		self.sampath = _check_executable('samtools')
		self.bowtie_ref = bowtie_ref
		self.reference = reference
		self.fastq1 = fastq1
		self.fastq2 = fastq2
		self.threads = threads
		self.bam_file = self._create_output_filename()

	def _create_output_filename(self):
		'''Create a .bam file name based on the longest common string match between fastq1 and fastq2'''

		for pos, _ in enumerate(self.fastq1):
			if self.fastq1[pos] != self.fastq2[pos]:
				if not self.fastq1[:pos]:
					print(f'Creating output file MITTS_out.bam')
					return 'MITTS_out.bam'
				print(f'Creating output file {self.fastq1[:pos] + ".bam"}')
				return self.fastq1[:pos] + '.bam'

	def run_bowtie(self):
		'''Runs bowtie2 mapping the supplied reads against the supplied reference'''

		try:
			bowtie_args = ['bowtie2', '-x', self.bowtie_ref, '-1', self.fastq1, '-2', self.fastq2, '-p', self.threads]
			bowtie = run(bowtie_args, capture_output=True, check=True)
			samsort = run(['samtools', 'sort', '-@', self.threads], input=bowtie.stdout, capture_output=True, check=True)
			run(['samtools', 'view', '-@', self.threads, '-bT', self.reference, '-o', self.bam_file], input=samsort.stdout, check=True)
			run(['samtools', 'index', '-@', self.threads, self.bam_file], check=True)
			return self.bam_file

		except CalledProcessError as e:
			print(f'Execution of the command {e.cmd} stopped with a non-zero exit status')
			print(f'Output: {e.output}')
			raise SystemExit(e.returncode)
