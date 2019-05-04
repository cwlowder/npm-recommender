from flask import Flask, render_template, redirect, request, send_from_directory
import os, random, base64, json, sys
import subprocess as sp

from npm import extract_package_json
from worker_pool import addWorkers, addJob, stopWorkers
from utils import loadJSON, saveJSON

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

		allow_save = False
		if request.form.getlist('allow_save'):
			allow_save = request.form.getlist('allow_save')

		file = request.files['file']
		fileContent = file.read()

		try:
			fileContent = json.loads(fileContent.decode('utf-8'))

			fileContent = extract_package_json(fileContent, is_user=True)

			if fileContent is None:
				raise Exception("Bad package contents")

			ID = generateID()
			os.mkdir('uploads/'+ID)
			if allow_save:
				saveJSON('uploads/' + ID + '/package.json', fileContent)

			addJob(fileContent, ID)
			return redirect("/job/"+ID, code=302)
		except Exception as e:
			# Error occured
			print("ERROR:", e)
			return redirect(request.url)
	else:
		return app.send_static_file('index.html')

@app.route('/job/<ID>')
def job_view(ID):
	dir_exists = os.path.isdir("uploads/"+ID)
	results = None
	done = False
	if os.path.exists('uploads/'+ID+'/results.json'):
		done = True
		results = loadJSON('uploads/'+ID+'/results.json')
	return render_template("result.html", ID=ID, dir_exists=dir_exists, results=results, done=done)

@app.route('/<path:path>')
def static_serve(path):
	root_dir = os.path.dirname(os.getcwd())
	return send_from_directory('static/', path)

if __name__ == '__main__':
	# Check if uploads directory does not yet exist
	if not os.path.exists('uploads/'):
		os.mkdir('uploads/');

	addWorkers('data/user_pkgs.txt', 'data/object_pkgs.txt', 'uploads', processes=2)

	port = int(os.environ.get('PORT', 8000))
	app.run(host='0.0.0.0', port=port)