import json
from ga4gh.client import client

def get_value(value):
	if value.string_value != "": return value.string_value
	elif value.int32_value != 0: return value.int32_value
	elif value.int64_value != 0: return value.int64_value
	else: return value.double_value

if __name__ == '__main__':
	# Data that will be dumped into file
	data = {}

	# [1] Boilerplate code to initialize GA4GH client
	c = client.HttpClient("http://1kgenomes.ga4gh.org")
	dataset = c.search_datasets().next()

	# [2] Fetch variant set
	for variant_set in c.search_variant_sets(dataset_id=dataset.id):
		if variant_set.name == "phase3-release":
			var_set = variant_set

	# [3] Fetch max_count number of callsets
	call_set_ids = []
	call_set_names = []
	count = 0
	max_count = 3
	for call_set in c.search_call_sets(variant_set_id=var_set.id):
		if count >= max_count:
			break
		call_set_ids.append(call_set.id)
		call_set_names.append(call_set.name)
		count += 1
	data['samples'] = call_set_names

	# [4] Fetch variant data
	count = 0
	variants = []
	start_pos = 1
	end_pos = 20000
	reference_name = "1"
	for variant in c.search_variants(call_set_ids=call_set_ids, variant_set_id=var_set.id, reference_name=reference_name, start=start_pos, end=end_pos):
		item = {}
		variants.append(item)
		item["CHROM"] = variant.reference_name
		item["POS"] = variant.start + 1
		item["ID"] = ";".join([str(x) for x in variant.names])
		item["REF"] = variant.reference_bases
		item["ALT"] = ",".join([str(x) for x in variant.alternate_bases])
		item["QUAL"] = "100"
		item["FILTER"] = "PASS"
		item["INFO"] = ";".join(["{}={}".format(key, get_value(value.values[0])) for key, value in variant.attributes.attr.items()])
		item["FORMAT"] = "GT"
		item["SAMPLES"] = {}
		for call in variant.calls:
			item["SAMPLES"][call.call_set_name] = {
				'phased': '|' if call.phaseset == "True" else '\\',
				'genotype': (call.genotype.values[0].number_value, call.genotype.values[1].number_value)
			}
	data['variants'] = variants

	# [5] Write variant data to file
	filename = "variants"
	with open(filename, 'w') as f:
		json.dump(data, f, indent=4)