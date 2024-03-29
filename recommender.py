from math import sqrt
import json
import sys
import multiprocessing as mp

from utils import _progBar, _chunkIt, loadFile, loadJSON

class Recommender:
    def __init__(self, user_source, object_source, processes=4):
        self.user_data = user_source
        self.object_data = object_source
        self.objects = self.object_data.keys()
        self.users = {}
        self.processes = processes
        counter = 0
        for u_data in self.user_data:
            if not isinstance(u_data, set):
                u_data['deps'] = set(u_data['deps'])
            # Percent of dependencies for this package versus all packages
            u_data['n'] = len(u_data['deps']) / len(self.objects)
            # Add ID field
            u_data['id'] = counter
            self.users[counter] = u_data
            counter += 1

    def similarity(self, pkg_a, pkg_b):
        """ Uses Pearson correlation coefficient """
        ntor = 0.0
        dtor_a = 0.0
        dtor_b = 0.0
        deps = pkg_a['deps'] | pkg_b['deps']
        for j in pkg_a['deps'] | pkg_b['deps']:
            x_aj = 1 if (j in pkg_a['deps']) else 0
            x_bj = 1 if (j in pkg_b['deps']) else 0
            ntor += (x_aj - pkg_a['n']) * (x_bj - pkg_b['n'])
            dtor_a += (x_aj - pkg_a['n']) ** 2
            dtor_b += (x_bj - pkg_b['n']) ** 2
        # number of packages that are not dependencies
        not_deps = len(self.objects) - len(deps)

        # update numbers for non dependencies
        ntor += not_deps * (pkg_a['n']) * (pkg_b['n'])
        dtor_a += not_deps*(pkg_a['n']) ** 2
        dtor_b += not_deps*(pkg_b['n']) ** 2

        # Handle negative numbers on numerator
        factor = 1.0 if dtor_a*dtor_b >= 0 else -1.0
        dtor = factor*sqrt(abs(dtor_a * dtor_b)) + 0.0001
        return ntor / dtor

    def recommend_job(self, pkg, objects={}, sims_cache={}, ret=None, print_progress=False):
        if ret == None:
            raise Error("Must define return method for each ")
        if print_progress:
            print("Started New Job")
        recs = {i : 0 for i in objects}
        n_a = pkg['n']
        # Loop through objects
        counter = 0
        for j in objects:
            ntor = 0.0
            dtor = 0.0001
            if print_progress:
                _progBar(counter, len(objects))
            counter += 1
            # Loop through users
            for i, u_data in self.users.items():
                x_ij = 1 if (j in u_data['deps']) else 0
                ntor += sims_cache[i] * (x_ij - u_data['n'])
                dtor += sims_cache[i]
            recs[j] = ntor / dtor
        recs = {i : recs[i] + n_a for i in objects}
        if print_progress:
            print("Finished Job")
        ret.put(recs)
        return

    def recommend(self, pkg, print_progress=False):
        n_a = len(pkg['deps']) / len(self.objects)
        pkg['n'] = n_a
        if not isinstance(pkg, set):
            pkg['deps'] = set(pkg['deps'])

        # Build up similarity cache
        sims_cache = {}
        for i, u_data in self.users.items():
            sims_cache[i] = self.similarity(u_data, pkg)

        jobs = []

        objects = _chunkIt(list(self.objects), self.processes)

        for job_id in range(0, self.processes):
            q = mp.Queue()
            process = mp.Process(target=self.recommend_job,
                                                args=(pkg, objects[job_id], sims_cache, q, print_progress))
            process.start()
            jobs.append((q, process))

        recs = {}
        for q, j in jobs:
            recs.update(q.get())
            j.join()
        return recs

if __name__ == '__main__':
    # Load data from files
    user_source = loadFile('data/user_pkgs.txt')
    user_data = []
    for u in user_source:
        user_data.append(json.loads(u))
    object_source = loadJSON('data/object_pkgs.txt')
    r = Recommender(user_data, object_source, processes=2)
    deps = set({
            "@prairielearn/prairielib": "^1.5.2",
            "ace-builds": "^1.4.2",
            "adm-zip": "^0.4.13",
            "archiver": "^3.0.0",
            "async": "^2.6.1",
            "async-stacktrace": "0.0.2",
            "aws-sdk": "^2.382.0",
            "backbone": "^1.3.3",
            "base64url": "^3.0.1",
            "blocked-at": "^1.1.3",
            "body-parser": "^1.18.3",
            "bootstrap": "^4.3.1",
            "byline": "^5.0.0",
            "chart.js": "^2.7.3",
            "cheerio": "^0.22.0",
            "clipboard": "^2.0.4",
            "cookie-parser": "^1.4.3",
            "crypto-js": "^3.1.9-1",
            "csv": "^5.0.1",
            "csvtojson": "^2.0.8",
            "debug": "^4.1.1",
            "diff": "^3.5.0",
            "dockerode": "^2.5.5",
            "ejs": "^2.6.1",
            "express": "^4.16.4",
            "fs-extra": "^7.0.1",
            "googleapis": "^36.0.0",
            "handlebars": "^4.1.0",
            "http-status": "^1.3.1",
            "is-my-json-valid": "^2.17.2",
            "javascript-natural-sort": "^0.7.1",
            "jju": "^1.3.0",
            "jquery": "^3.3.1",
            "json-stringify-safe": "^5.0.1",
            "lodash": "^4.17.10",
            "lru-cache": "^5.1.1",
            "mathjax": "^2.7.4",
            "mersenne": "0.0.4",
            "moment": "^2.23.0",
            "multer": "^1.4.1",
            "mustache": "^3.0.1",
            "nodemon": "^1.18.9",
            "numeric": "^1.2.6",
            "oauth-signature": "^1.5.0",
            "on-finished": "^2.3.0",
            "parse5": "^5.0.0",
            "passport": "^0.4.0",
            "passport-azure-ad": "^4.0.0",
            "pg": "^7.7.1",
            "plist": "^3.0.0",
            "popper.js": "^1.14.6",
            "qrcode-svg": "^1.0.0",
            "redis": "^2.8.0",
            "redis-lru": "^0.5.0",
            "request-promise-native": "^1.0.5",
            "requirejs": "^2.3.5",
            "s3-upload-stream": "^1.0.7",
            "search-string": "^3.1.0",
            "serve-favicon": "^2.5.0",
            "socket.io": "^2.2.0",
            "socket.io-client": "^2.2.0",
            "socket.io-redis": "^5.2.0",
            "streamifier": "^0.1.1",
            "supports-color": "^6.0.0",
            "tar": "^4.4.8",
            "three": "^0.99.0",
            "uuid": "^3.2.1",
            "viz.js": "^2.1.2",
            "winston": "^3.1.0",
            "yargs": "^12.0.5",
            "yargs-parser": "^11.1.1",
            "chai": "^4.1.2",
            "colors": "^1.3.3",
            "coveralls": "^3.0.1",
            "eslint": "^5.11.1",
            "jsdoc": "^3.5.5",
            "mocha": "^5.2.0",
            "nyc": "^13.3.0",
            "request": "^2.87.0",
            "tmp": "0.0.33"
        }.keys())

    deps = {
        "@turf/turf": "^5.1.6",
        "cookie-parser": "^1.4.4",
    }
    pkg = {
        'name': 'test',
        'deps': deps
    }
    recs = r.recommend(pkg)
    recommendations = [(k, recs[k]) for k in sorted(recs, key=recs.get, reverse=True)]

    counter = 0
    for item, val in recommendations:
        if item not in deps:
            print(item, val, sep=",")
            counter += 1
        if counter > 20:
            break