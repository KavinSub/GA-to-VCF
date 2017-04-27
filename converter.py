import time
import json

# TODO:
# 1. Get source, reference and phasing
# 2. Add error catching as needed
# 3. Get quality data
# 4. Check api for format tags
# 5. Check api for other filter tags
# 6. Ensure that all other tags have been retrieved

def write_header(file, key, value):
	file.write("##{}={}\n".format(key, value))

### CONSTANTS
filename = "test"
version = "VCFv4.1"
filedate = time.strftime("%Y%m%d")
source = "1kGenomes"
reference = "NULL"
phasing = "NULL"

metafile = "metadata"
variantfile = "variants"

if __name__ == '__main__':
	with open(filename, 'w') as f:
		# [1] Metadata
		# [a] Meta-information constants
		write_header(f, "fileformat", version)
		write_header(f, "fileDate", filedate)
		write_header(f, "source", source)
		write_header(f, "reference", reference)
		write_header(f, "phasing", phasing)

		# [b] Metadata
		metadata = json.load(open(metafile, 'r'))['data']
		for item in metadata:
			key = item['key']
			identity = item['id']
			number = item['number']
			vtype = item['type']
			description = item['description']

			if key == "INFO": 
				value = "<ID={},Number={},Type={},Description=\"{}\">".format(identity, number, vtype, description)
			elif key == "FILTER": 
				value = "<ID={},Description=\"{}\">".format(identity, description)
			elif key == "FORMAT": 
				value = "<ID={},Number={},Type={},Description=\"{}\">".format(identity, number, vtype, description)

			write_header(f, key, value)

		# [2] Sample data
		data = json.load(open(variantfile, 'r'))

		# [a] Header line
		f.write("#CHROM\tPOS\tID\tREF\tALT\tQUAL\tFILTER\tINFO\tFORMAT\t{}\n".format("\t".join(data['samples'])))

		# [b] Data lines
		# Sort variants by chromosome, then starting position
		variants = sorted(data['variants'], key=lambda x: (int(x["CHROM"]), x["POS"]))
		for variant in variants:
			f.write("{}\t".format(variant["CHROM"]))
			f.write("{}\t".format(variant["POS"]))
			f.write("{}\t".format(variant["ID"]))
			f.write("{}\t".format(variant["REF"]))
			f.write("{}\t".format(variant["ALT"]))
			f.write("{}\t".format(variant["QUAL"]))
			f.write("{}\t".format(variant["FILTER"]))
			f.write("{}\t".format(variant["INFO"]))
			f.write("{}".format(variant["FORMAT"]))
			for sample in data['samples']:
				item = variant["SAMPLES"][sample]
				f.write("\t")
				f.write("{}{}{}".format(item['genotype'][0], item['phased'], item['genotype'][1]))
			f.write("\n")