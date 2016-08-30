from flask import Flask, render_template, redirect, request
import pandas as pd
import json
import os

SHOW_COLS = ['ML #', 'Address', 'City', 'Zip Code_x', 'Owner 1 First Name',
				'Owner 1 Last Name', 'List Date', 'DOM', 'Phone']

def get_dir_list():
	dir_list = []
	for i in os.listdir('data'):
		try:
			f = open("data/{}/results.csv".format(i))
			dir_list.append(i)
		except:
			pass
	return dir_list
	
def get_saved_data(exp):
	try:
		with open("data/"+exp+"/saved.json") as infile:
			saved = json.load(infile)
	except:
		tmp = {}
		data = pd.read_csv("data/"+exp+"/results.csv")
		for i in range(len(data)):
			tmp[i]=False
		with open("data/"+exp+"/saved.json", 'w') as outfile:
			json.dump(tmp,outfile)
		with open("data/"+exp+"/saved.json") as infile:
			saved = json.load(infile)
	print saved
	return saved

app = Flask(__name__)

@app.route("/")
def index():
	dir_list = get_dir_list()
	return render_template("index.html", dl=dir_list)
	
@app.route("/<exp>")
def exp(exp):
	try:
		data = pd.read_csv("data/"+exp+"/results.csv")
		saved = get_saved_data(exp)
		return render_template("expires.html", exp=exp,data=data, cols=SHOW_COLS, saved=saved)
	except:
		return redirect("/")
		
@app.route('/submit_<exp>', methods=['POST'])
def submit(exp):
	res= request.form.to_dict()
	results = {}
	for k,i in res.iteritems():
		if i == "True":
			val = True
		else:
			val = False
		results[int(k)] = val
	print results
	with open("data/"+exp+"/saved.json", 'w') as outfile:
			json.dump(results,outfile)
	return redirect('/')

if __name__ == "__main__":
    app.run(host="0.0.0.0",port=80,debug=True)
