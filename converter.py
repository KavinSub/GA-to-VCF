import time
import json

# TODO:
# 1. Fill in missing constant values
# 2. Add error catching
# 3. Fetch, format, and write variant data

def write_header(file, key, value):
	file.write("##{}={}\n".format(key, value))

### CONSTANTS
filename = "test"
version = "VCFv4.1"
filedate = time.strftime("%Y%m%d")
metafile = "metadata"

if __name__ == '__main__':
	# [1] Write to VCF file
	with open(filename, 'w') as f:
		# [a] Meta-information constants
		write_header(f, "fileformat", version)
		write_header(f, "filedate", filedate)
		write_header(f, "source", "NULL")
		write_header(f, "reference", "NULL")
		write_header(f, "phasing", "NULL")

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

		# [c] Header line
		f.write("#CHROM\tPOS\tID\tREF\tALT\tQUAL\tFILTER\tINFO")