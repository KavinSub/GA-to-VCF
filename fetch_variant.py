import json
from ga4gh.client import client

if __name__ == '__main__':
	# [1] Boilerplate code to initialize GA4GH client
	c = client.HttpClient("http://1kgenomes.ga4gh.org")
	dataset = c.search_datasets().next()

	# [2] Fetch variant set
	for variant_set in c.search_variant_sets(dataset_id=dataset.id):
		if variant_set.name == "phase3-release":
			var_set = variant_set

	# [3] Fetch 1 callset
	call_set_ids = []
	count = 0
	for call_set in c.search_call_sets(variant_set_id=var_set.id):
		if count > 0:
			break
		call_set_ids.append(call_set.id)
		count += 1
	print("Call set ids")

	# [4] Fetch all calls belonging to a callset
	count = 0
	for variant in c.search_variants(call_set_ids=call_set_ids, variant_set_id=var_set.id, reference_name="1", start=1, end=10500):
		for call in variant.calls:
			print("CHROM: {}".format(variant.reference_name))
			print("POS: {}".format(variant.start))
			print("ID: {}".format(",".join([str(x) for x in variant.names])))
			print("REF: {}".format(variant.reference_bases))
			print("ALT: {}".format(",".join([str(x) for x in variant.alternate_bases])))
			print("QUAL:")
			print("FILTER:")
			print("INFO:")
			print(call)
			print("")