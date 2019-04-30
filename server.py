from flask import Flask, render_template, redirect, request, send_from_directory
import os, random, base64, json

from npm import extract_package_json

app = Flask(__name__)

def generateID():
	r1 = random.randint(0, 10**10)
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
		print("TEST:", fileContent.decode('utf-8'))
		try:
			fileContent = json.loads(fileContent.decode('utf-8'))

			fileContent = extract_package_json(fileContent)
			print(fileContent)

			ID = generateID()
			os.mkdir('uploads/'+ID)
			if False:
				file.save('uploads/'+ID, 'package.json')
		except Exception as e:
			# Error occured
			print("ERROR:", e)
			return redirect(request.url)
		return app.send_static_file('index.html')
	else:
		return app.send_static_file('index.html')

@app.route('/<path:path>')
def static_serve(path):
	root_dir = os.path.dirname(os.getcwd())
	return send_from_directory('static/', path)

if __name__ == '__main__':
	app.run(port=8000)