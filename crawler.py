from queue import Queue
import urllib.request as request
import urllib.error
import json
import time

def extract_package_json(package_json, q, seen):
	latest = package_json["dist-tags"]['latest']

	data = {
		'name': package_json['name'],
		'deps': []
	}

	try:
		#skip depricated packages
		if 'depricated' in package_json['versions'][latest]:
			return None

		# Add useful information
		if 'keywords' in package_json['versions'][latest]:
			data['keywords'] = package_json['versions'][latest]['keywords']

		if 'description' in package_json['versions'][latest]:
			data['description'] = package_json['versions'][latest]['description']

		if 'repository' in package_json['versions'][latest]:
			# Handle different implementations of repository
			if isinstance(package_json['versions'][latest]['repository'], str):
				data['repository'] = package_json['versions'][latest]['repository']
			else:	
				data['repository'] = package_json['versions'][latest]['repository']['url']
	except Exception  as e:
		print("Error trying to parse ->", e)
		return None

	# extract dependencies
	if 'dependencies' in package_json['versions'][latest]:
		for dep in package_json['versions'][latest]['dependencies']:
			if dep not in data['deps']:
				# Add another dependency to this package
				data['deps'].append(dep)
				if dep not in seen:
					# Only add non seen packages
					q.put(dep)
	
	# extract dev dependencies
	if 'devDependencies' in package_json['versions'][latest]:
		for dep in package_json['versions'][latest]['devDependencies']:
			if dep not in data['deps']:
				# Add another dependency to this package
				data['deps'].append(dep)
				if dep not in seen:
					# Only add non seen packages
					q.put(dep)
	return data

def crawl_npm(seed_list, max_size=200000):
	seen = set({})
	q = Queue()
	npm_registry = 'http://registry.npmjs.com/'

	for seed in seed_list:
		q.put(seed)

	data = {}

	counter = 0
	while counter < max_size and not q.empty():
		package = q.get()
		if package in seen:
			continue

		# sleep after every 100 downloads
		if counter % 100 == 0:
			print("Sleeping...")
			time.sleep(10)

		print("{:6d} {:6d}".format(counter, q.qsize()),package)
		
		counter += 1
		seen.add(package)

		try:
			f = request.urlopen(npm_registry + package, timeout=10)
			package_json = json.load(f)
		except urllib.error.HTTPError as e:
			print('The package', package, 'is not found', str(e))
			continue

		try:
			data_package = extract_package_json(package_json, q, seen)
			if data_package is not None:
				data[package] = data_package
			else:
				# Failed packages should not count towards limit
				counter -= 1
		except:
			# Skip any fails
			counter -= 1
	return data

if __name__ == "__main__":
	data = crawl_npm(['express','chalk','supertest', '@prairielearn/prairielib', "ghost"])
	print("Found", len(data), "packages")
	with open('data2.json', 'w') as outfile:
		json.dump(data, outfile)
	#print(json.dumps(data, indent=4, sort_keys=True))