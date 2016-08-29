from flask import Flask, render_template, redirect
import pandas as pd
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

app = Flask(__name__)

@app.route("/")
def index():
	dir_list = get_dir_list()
	return render_template("index.html", dl=dir_list)
	
@app.route("/<exp>")
def exp(exp):
	try:
		data = pd.read_csv("data/"+exp+"/results.csv")
		return render_template("expires.html", data=data, cols=SHOW_COLS)
	except:
		return redirect("/")

if __name__ == "__main__":
    app.run(host="0.0.0.0",port=80,debug=True)
