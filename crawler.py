from utils import _progBar, loadFile

from npm import extract_package_json, crawl_npm

from github import scrapeRedditForGithub, convertAllGithubToPackages

def crawl(github_links=None, package_json=None, print_progress=False, min_usr_deps=4, min_obj_uses=3, pkg_search_factor=1.):
	print("Crawling for data:")
	# If no prefecthing has been done
	if not github_links and not package_json:
		github_links = scrapeRedditForGithub(True)
		github_links = convertAllGithubToPackages(github_links, print_progress)
	# if github links have been extracted, but not the packages
	elif github_links and not package_json:
		package_json = convertAllGithubToPackages(github_links, print_progress)

	user_pkgs = []
	# dependency to number of mentions
	deps = {}
	i = 0
	print("Extracting information:")
	for pack in package_json:
		if print_progress:
			_progBar(i, len(package_json), u = 10, l = 20)
			i += 1
		#print(pack)
		extracted = extract_package_json(pack, is_user=True)
		if not extracted:
			continue
		if len(extracted['deps']) < min_usr_deps:
			continue
		user_pkgs.append(extracted)
		for user_dep in extracted['deps']:
			if user_dep in deps:
				deps[user_dep] += 1
			else:
				deps[user_dep] = 1

	trimmed_deps = []
	for dep, count in deps.items():
		#print(dep, count)
		# Remove uncommon dependents
		if count >= min_obj_uses:
			trimmed_deps.append(dep)

	# Remove uncommon dependencies
	deps = trimmed_deps
	# Explore based on these deps to retrieve some larger number of packages
	object_pkgs = crawl_npm(deps, max_size=int(len(deps)*pkg_search_factor))

	return user_pkgs, object_pkgs

if __name__ == "__main__":
	#github_links = loadFile("data/reddit_all_github.txt")
	package_json = loadFile("data/reddit_all_packages.txt")
	crawl(package_json=package_json, print_progress=True)