from subprocess import run, CalledProcessError

def _check_executable(executable):
	try:
	    which = run(['which', executable], capture_output=True, text=True, check=True)
	    path = which.stdout.strip()
	    msg(f'{executable} executable found in {path}')
	    return path
	except CalledProcessError as e:
	    msg(f'Could not find {executable} executable. Check {executable} is installed correctly and in $PATH.')
	    msg(f'{e.cmd}: {e.output}')
	    raise SystemExit(e)


class BowtieRunner:
	'''A class that implements a bowtie2 run and does some simple checking of executables'''

	def __init__(reference, fastq1, fastq2, threads):
		self.path = _check_executable('bowtie2')
		self.sampath = _check_executable('samtools')
		self.reference = reference
		self.fastq1 = fastq1
		self.fastq2 = fastq2
		self.threads = threads
		self.bam_file = _create_output_filename(fastq1, fastq2)

	def _create_output_filename(fastq1, fastq2):
		'''Create a .bam file name based on the longest common string match between fastq1 and fastq2'''

		for pos, _ in enumerate(fastq1):
			while fastq1[pos] == fastq2[pos]:
				continue
			if not fastq1[:position]:
				return 'MITTS_out.bam'
			return fastq1[:position] + '.bam'

	def run_bowtie():
		'''Runs bowtie2 mapping the supplied reads against the supplied reference'''

		try:
			bowtie_args = ['bowtie2', '-x', self.reference, '-1', self.fastq1, '-2', self.fastq2, '-p', self.threads]
			bowtie = run(bowtie_args, capture_output=True, check=True, text=True)
			samsort = run(['samtools', 'sort', '-@', self.threads], input=bowtie.stdout, capture_output=True, check=True, text=True)
			samview = run(['samtools', 'view', '-@', self.threads, '-bT', self.reference, '-o', self.bam_file], input=samsort.stdout, capture_output=True, check=True, text=True)
			samindex = run(['samtools', 'index', '-@', self.threads, self.bam_file], capture_output=True, check=True, text=True)

		except CalledProcessError as e:
			msg(f'Execution of the command {e.cmd} stopped with a non-zero exit status')
			msg(f'Output: {e.output}')
			raise SystemExit(e.returncode)
