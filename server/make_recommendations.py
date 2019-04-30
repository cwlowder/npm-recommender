from recommender import Recommender
from npm import extract_package_json

user_source = loadFile('data/user_pkgs.txt')
user_data = []
for u in user_source:
    user_data.append(json.loads(u))
object_source = loadJSON('data/object_pkgs.txt')
r = Recommender(user_data, object_source, processes=2)

def make_rec(package, num=20):
	pkg = extract_package_json(package, is_user=True)
	if not pkg:
		return None

	r.recommend(pkg)
	recs = r.recommend(pkg)
    recommendations = [(k, recs[k]) for k in sorted(recs, key=recs.get, reverse=True)]

    # Retrieve top num recommendations
    out = []
    for item, val in recommendations:
        if item not in pkg['deps']:
            print(item, val, sep=",")
            out.append({'item': item, 'val': val})
        if len(out) > num:
            break