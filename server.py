from flask import Flask, render_template, redirect, request, send_from_directory
import os, random, base64, json, sys
import subprocess as sp

from npm import extract_package_json
from worker_pool import addWorkers, addJob, stopWorkers

app = Flask(__name__)

def generateID():
	r1 = random.randint(10**2, 10**10)
	return base64.urlsafe_b64encode(bytes(str(r1), 'ascii'))[:-2].decode('ASCII').lower()

@app.route('/', methods=['GET', 'POST'])
def main():
	if request.method == 'POST':
		root_dir = os.path.dirname(os.getcwd())
		if 'file' not in request.files:
			# Error: No file included
			return redirect(request.url)
		file = request.files['file']
		fileContent = file.read()
		try:
			fileContent = json.loads(fileContent.decode('utf-8'))

			fileContent = extract_package_json(fileContent, is_user=True)

			if fileContent is None:
				raise Exception("Bad package contents")

			ID = generateID()
			os.mkdir('uploads/'+ID)
			if False:
				with open('uploads/' + ID + '/package.json', 'w+') as file:
					file.write(fileContent)

			addJob(fileContent, ID)
			return app.send_static_file('index.html')
		except Exception as e:
			# Error occured
			print("ERROR:", e)
			return redirect(request.url)
	else:
		return app.send_static_file('index.html')

@app.route('/<path:path>')
def static_serve(path):
	root_dir = os.path.dirname(os.getcwd())
	return send_from_directory('static/', path)

if __name__ == '__main__':
	addWorkers('data/user_pkgs.txt', 'data/object_pkgs.txt', 'uploads', processes=2)
	app.run(port=8000)