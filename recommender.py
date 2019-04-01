from math import sqrt
import json

class Recommender:
    def __init__(self, data_source):
        self.data = json.load(data_source)
        self.packages = self.data.keys()
        for p in self.packages:
            # Percent of dependencies for this package versus all packages
            self.data[p]['n'] = len(self.data[p]['deps']) / len(self.packages)

    def similarity(self, pkg_a, pkg_b):
        """ Uses Pearson correlation coefficient """
        ntor = 0.0
        dtor_a = 0.0
        dtor_b = 0.0
        for j in self.packages:
            x_aj = 1 if (j in pkg_a['deps']) else 0
            x_bj = 1 if (j in pkg_b['deps']) else 0
            ntor += (x_aj - pkg_a['n']) * (x_bj - pkg_b['n'])
            dtor_a += (x_aj - pkg_a['n']) ** 2
            dtor_b += (x_bj - pkg_b['n']) ** 2
        dtor = sqrt(dtor_a * dtor_b) + 0.0001
        return ntor / dtor

    def recommend(self, pkg):
        recs = {i : 0 for i in self.packages}
        n_a = len(pkg['deps']) / len(self.packages)
        pkg['n'] = n_a
        # Loop through objects
        for j in self.packages:
            ntor = 0.0
            dtor = 0.0001
            # Loop through users
            for i in self.packages:
                x_ij = 1 if (j in self.data[i]['deps']) else 0
                ntor += self.similarity(self.data[i], pkg) * (x_ij - self.data[i]['n'])
                dtor += self.similarity(self.data[i], pkg)
            recs[j] = ntor / dtor
        recs = {i : recs[i] + n_a for i in self.packages}
        return recs

if __name__ == '__main__':
    f = open('data.json', 'r')
    r = Recommender(f)
    pkg = {
        'name': 'zyspawn',
        'deps': [
            'lodash',
            'jest'
        ]
    }
    print(json.dumps(r.recommend(pkg)))
