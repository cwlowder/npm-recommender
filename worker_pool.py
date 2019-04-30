import multiprocessing as mp
import json
from recommender import Recommender
from utils import loadFile, loadJSON

job_queue = mp.Queue()

result_queue = mp.Queue()

workers = []

save_worker = None

class Worker():
	def __init__(self, user_source, object_source, processes=4, num=10):
		self.recommender = Recommender(user_source, object_source, processes)
		self.running = True
		self.processes = processes
		self.num = num

	def run(self):
		while self.running:
			cont, ID, pkg = job_queue.get()
			if not cont:
				# Re add end flag
				job_queue.put((False, None, None))
				return
			recs = self.recommender.recommend(pkg, self.processes)

			# Select top num recommendations
			out = []
			recommendations = [(k, recs[k]) for k in sorted(recs, key=recs.get, reverse=True)]
			counter = 0
			for item, val in recommendations:
				if item not in pkg['deps']:
					out.append({"dep": item, "val": val})
					counter += 1
				if counter > self.num:
					break
			result_queue.put((ID, out))

class SaveWorker:
	def __init__(self, uploads):
		self.running = True
		self.uploads = uploads

	def run(self):
		while self.running:
			ID, recs = result_queue.get()
			print(ID)
			if not ID:
				# Re add end flag
				result_queue.put((None, None))
				return
			print("Saving for ID")
			with open(self.uploads + "/" + ID + "/results.json", 'w+') as file:
				file.write(json.dumps(recs))

def addWorkers(user_path, object_path, upload_path, numWorkers=2, processes=4, num_recs=10):
	user_raw = loadFile(user_path)
	user_source = []
	for u in user_raw:
		user_source.append(json.loads(u))
	object_source = loadJSON(object_path)

	for job_id in range(0, numWorkers):
		worker = Worker(user_source, object_source, processes, num_recs)
		process = mp.Process(target=worker.run, args=())
		process.start()
		workers.append(process)

	saveWorker = SaveWorker(upload_path)
	process = mp.Process(target=saveWorker.run)
	process.start()
	save_worker = process

def addJob(pkg, ID):
	job_queue.put((True, ID, pkg))

def stopWorkers():
	job_queue.put((False, None, None))
	result_queue.put((None, None))

if __name__ == "__main__":
	addWorkers('data/user_pkgs.txt', 'data/object_pkgs.txt', '.')
	deps = {
		"@turf/turf",
		"cookie-parser"
	}
	pkg = {
		'name': 'test',
		'deps': deps
	}
	addJob(pkg, "TEST")
	stopWorkers()