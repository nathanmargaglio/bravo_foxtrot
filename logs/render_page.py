
import os
from PIL import Image
import webbrowser
import subprocess

def get_dir_list():
	dir_list = {}
	for i in os.listdir('.'):
		if os.path.isdir(i):
			try:
				f = open("{}/{}.txt".format(i,i))
				dir_list[i]=f.read()
			except:
				pass
	return dir_list

def get_exp_list():
	exp_list = []
	for i in os.listdir('./exp'):
		if os.path.isdir("./exp/"+i):
			exp_list.append(i)
	return exp_list
	
###

import web

render = web.template.render('templates/')

urls = (
	'/favicon.ico','icon',
	'/qgis/(.*)', 'maps',
	#'/exp/(.*)','exp',
    	'/(.*)', 'index'
)

class icon:
	def GET(self): raise web.seeother("static/favicon.ico")

class index:
    def GET(self, name):
		if name == "qgis":
			return render.maps()
		if "exp" in name:
			print name
			print "~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~"
			if name == "exp":
				exp_list = get_exp_list()
				return render.exp(exp_list)
			else:
				return open(name+"/page.html",'rb').read()
		if "gmap" in name:
			trunc = "_".join(name.split('_')[1:])
			return open('{}/map.html'.format(trunc),'rb').read()
		if not name:
			dir_list = get_dir_list()
			return render.index(dir_list)
		else:
			try:
        	                return open('gifs/{}.gif'.format(name),'rb').read()
			except:
				try:
					print "Rendering Gif... (pronounced JIF)"
					subprocess.call('sudo ./render_gif.sh {} tmp'.format(name),shell=True)
					return open('gifs/{}tmp.gif'.format(name),'rb').read()
				except:
					print name
class maps:
	def GET(self,name):
		if not name:
			return render.maps()
		else:
			return open('static/{}.png'.format(name), 'rb').read()
if __name__ == "__main__":
    app = web.application(urls, globals())
    app.run()
