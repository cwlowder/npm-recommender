from math import sqrt
import json
import sys

class Recommender:
    def __init__(self, data_source):
        self.data = json.load(data_source)
        self.packages = self.data.keys()
        for p in self.packages:
            self.data[p]['deps'] = set(self.data[p]['deps'])
            # Percent of dependencies for this package versus all packages
            self.data[p]['n'] = len(self.data[p]['deps']) / len(self.packages)

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
        not_deps = len(self.packages) - len(deps)

        # update numbers for non dependencies
        ntor += not_deps * (pkg_a['n']) * (pkg_b['n'])
        dtor_a += not_deps*(pkg_a['n']) ** 2
        dtor_b += not_deps*(pkg_b['n']) ** 2
    
        dtor = sqrt(dtor_a * dtor_b) + 0.0001
        return ntor / dtor

    def recommend(self, pkg):
        recs = {i : 0 for i in self.packages}
        n_a = len(pkg['deps']) / len(self.packages)
        pkg['n'] = n_a
        pkg['deps'] = set(pkg['deps'])
        # Loop through objects
        counter = 0
        sims_cache = {}
        for j in self.packages:
            ntor = 0.0
            dtor = 0.0001
            if counter % 10 == 0:
                sys.stdout.write('Counter: ' + str(counter) + ' \r')
                sys.stdout.flush()
            counter += 1
            # Loop through users
            for i in self.packages:
                x_ij = 1 if (j in self.data[i]['deps']) else 0
                if i not in sims_cache:
                    sims_cache[i] = self.similarity(self.data[i], pkg)
                ntor += sims_cache[i] * (x_ij - self.data[i]['n'])
                dtor += sims_cache[i]
            recs[j] = ntor / dtor
        recs = {i : recs[i] + n_a for i in self.packages}
        return recs

if __name__ == '__main__':
    f = open('dataAll.json', 'r')
    r = Recommender(f)
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


    deps = set({
     "eslint",
     "coveralls",
     "nyc",
     "prettier",
     "istanbul",
     "tape"
    })
    pkg = {
        'name': 'test',
        'deps': deps
    }
    recs = r.recommend(pkg)
    recommendations = [(k, recs[k]) for k in sorted(recs, key=recs.get, reverse=True)]

    counter = 0
    for item, val in recommendations:
        if item not in deps:
            print(item, val)
            counter += 1
        if counter > 20:
            break