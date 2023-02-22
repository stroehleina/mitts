
class Species:

	available = {

		'ENTEROCOCCUS' : {
			'file' : '/home/astroehlein/resources/23S/Efaecium_23S_wildtype.fa'
			'chrom' : 'NR_103056.1'
			'bowtie' : '/home/astroehlein/resources/23S/bt_Efaecium'
			'positions' : [2589, 2518]
			'reference_nucls' : ['G', 'G']
			'variant_nucls' : ['T', 'A']
			'mutations' : ['G2576T', 'G2505A']
			'copy_number' = 6
		},

		'NEISSERIA' : {
			'reference' : '/home/astroehlein/resources/23S/Ngono_23S_wildtype.fa'
			'chrom' : '23S_100'
			'bowtie' : '/home/astroehlein/resources/23S/bt_Ngono'
			'positions' : [9, 561]
			'reference_nucls' : ['A', 'C']
			'variant_nucls' : ['G', 'T']
			'mutations' : ['A2059G', 'C2611T']
			'copy_number' : 4
		}
	}

	def __init__(species):
		if species.upper() in Species.available:
			self.reference = Species.available['reference']
			self.chrom = Species.available['chrom']
			self.bowtie = Species.available['bowtie']
			self.positions = Species.available['positions']
			self.reference_nucls = Species.available['reference_nucls']
			self.variant_nucls = Species.available['variant_nucls']
			self.mutations = Species.available['mutations']
			self.copy_number = Species.available['copy_number']
		else:
			raise ValueError(f'No reference and point mutations available for species {species}. Exiting')
