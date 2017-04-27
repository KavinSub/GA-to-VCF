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

	# [3] Get metadata, store in dictionary
	metadata = {
		'data': []
	}
	for data in variant_set.metadata:
		if '.' in data.key:
			key, identity = (str(x) for x in data.key.split('.'))
			metadata['data'].append({
				'key': key,
				'id': identity,
				'number': data.number,
				'type': data.type,
				'description': data.description
			})

	# [4] Write hardcoded metadata tags not on server
	metadata['data'].append({
		'key': 'FORMAT',
		'id': 'GT',
		'number': 1,
		'type': 'String',
		'description': 'Genotype'
	})
	metadata['data'].append({
		'key': 'FORMAT',
		'id': 'GQ',
		'number': 1,
		'type': 'Integer',
		'description': 'Genotype Quality'
	})
	metadata['data'].append({
		'key': 'FORMAT',
		'id': 'DP',
		'number': 1,
		'type': 'Integer',
		'description': 'Read Depth'
	})
	metadata['data'].append({
		'key': 'FORMAT',
		'id': 'HQ',
		'number': 2,
		'type': 'Integer',
		'description': 'Haplotype Quality'
	})

	# [5] Write metadata to file
	filename = "metadata"
	with open(filename, 'w') as f:
		json.dump(metadata, f, indent=4)