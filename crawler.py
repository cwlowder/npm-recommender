from queue import Queue
import urllib.request as request
import urllib.error
import json

def crawl_npm(seed_list, max_size=2000):
	seen = set({})
	npm_registry = 'http://registry.npmjs.com/'
	q = Queue()

	for seed in seed_list:
		q.put(seed)

	data = {}

	counter = 0
	while counter < max_size and not q.empty():
		package = q.get()
		print("{:6d}".format(q.qsize()),package)
		if package in seen:
			continue
		counter += 1
		seen.add(package)
		data[package] = {
			'name': package,
			'deps': []
		}

		try:
			f = request.urlopen(npm_registry + package)
			package_json = json.load(f)
		except urllib.error.HTTPError as e:
			print('The package', package, 'is not found')
			continue

		latest = package_json["dist-tags"]['latest']

		# extract dependencies
		if 'dependencies' in package_json['versions'][latest]:
			for dep in package_json['versions'][latest]['dependencies']:
				if dep not in data[package]:
					# Add another dependency to this package
					data[package]['deps'].append(dep)
					if dep not in seen:
						# Only add non seen packages
						q.put(dep)
		'''
		if 'devDependencies' in package_json['versions'][latest]:
			for dep in package_json['versions'][latest]['devDependencies']:
				if dep not in data[package]:
					# Add another dependency to this package
					data[package]['deps'].append(dep)
					if dep not in seen:
						# Only add non seen packages
						q.put(dep)
		'''
	return data

if __name__ == "__main__":
	data = crawl_npm(['express','chalk','supertest'])
	print("Found", len(data), "packages")
	with open('data.json', 'w') as outfile:
		json.dump(data, outfile)
	#print(json.dumps(data, indent=4, sort_keys=True))