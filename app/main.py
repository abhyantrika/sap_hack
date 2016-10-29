from flask import Flask, request, redirect, flash, render_template
from werkzeug.utils import secure_filename
from urllib import *
import os

#import pyhdb

app = Flask(__name__)

"""
@app.route('/')
def form():
    return render_template('home.html')
"""

@app.route('/')
#@app.route('/main.html')
def home_html():
	return render_template('main.html')

@app.route('/upload', methods=['POST'])
def upload_file():
	print(request.method)
	if request.method == 'POST':
		f = request.files['file']
		f.save(secure_filename('Chapter1.pdf'))
		return redirect('/suggest')
	return redirect('')

@app.route('/suggest')
def suggest():
	os.system('pdf2txt.py {file} > Chapter1_structured.txt'.format(file = 'Chapter1.pdf'))
	f = open('output.txt')
	a = f.readlines()
	b = []
	for i in a:
		if i.strip():
			b.append(i.split()[0])
	c = []
	for i in range(len(b)):
		try:
			c = c + [b[i:len(b)-i:5]]
		except:
			break

	c = list(filter(bool,c))
	d = []
 	for i in c:
		d = d + [' '.join(map(str,i))]

	return render_template('suggest.html',o = d[:5])

port = os.getenv('PORT', '5000')
if __name__ == "__main__":
	app.run(host='0.0.0.0', port=int(port))


#@app.route('/suggest')

