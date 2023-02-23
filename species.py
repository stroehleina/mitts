
class Species:

	available = {

		'ENTEROCOCCUS' : {
			'reference' : '/home/astroehlein/resources/23S/Efaecium_23S_wildtype.fa',
			'chrom' : 'NR_103056.1',
			'bowtie_ref' : '/home/astroehlein/resources/23S/bt_Efaecium',
			'positions' : [2589, 2518],
			'reference_nucls' : ['G', 'G'],
			'variant_nucls' : ['T', 'A'],
			'mutations' : ['G2576T', 'G2505A'],
			'copy_number' : 6
		},

		'NEISSERIA' : {
			# 'reference' : '/home/astroehlein/resources/23S/Ngono_23S_wildtype.fa',
			'reference' : '/home/astroehlein/resources/23S/NR_103957.1_FA_1090_23S.fa',
			# 'chrom' : '23S_100',
			'chrom' : 'NR_103957.1_FA_1090_23S',
			# 'bowtie_ref' : '/home/astroehlein/resources/23S/bt_Ngono',
			'bowtie_ref' : '/home/astroehlein/resources/23S/bt_Ngono',
			'positions' : [2062, 2617],
			# 'positions' : [9, 561],
			'reference_nucls' : ['A', 'C'],
			'variant_nucls' : ['G', 'T'],
			'mutations' : ['A2059G', 'C2611T'],
			'copy_number' : 4
		}


		# ADD YOUR OWN SPECIES HERE
		# DON'T FORGET THE COMMA AFTER THE LAST DICT ENTRY :)

	}

	def __init__(self, species):
		if species.upper() in Species.available:
			species = species.upper()
			self.reference = Species.available[species]['reference']
			self.chrom = Species.available[species]['chrom']
			self.bowtie_ref = Species.available[species]['bowtie_ref']
			self.positions = Species.available[species]['positions']
			self.reference_nucls = Species.available[species]['reference_nucls']
			self.variant_nucls = Species.available[species]['variant_nucls']
			self.mutations = Species.available[species]['mutations']
			self.copy_number = Species.available[species]['copy_number']
		else:
			raise ValueError(f'No reference and point mutations available for species {species}. Exiting')
