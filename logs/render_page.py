
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
	
###

import web

render = web.template.render('templates/')

urls = (
	'/qgis/(.*)', 'maps',
    	'/(.*)', 'index'
)

class index:
    def GET(self, name):
		if name == "qgis":
			return render.maps()
		if not name:
			dir_list = get_dir_list()
			return render.index(dir_list)
		else:
			try:
        	                return open('gifs/{}.gif'.format(name),'rb').read()
			except:
				print "Rendering Gif... (pronounced JIF)"
				subprocess.call('sudo ./render_gif.sh {} tmp'.format(name),shell=True)
				return open('gifs/{}tmp.gif'.format(name),'rb').read()

class maps:
	def GET(self,name):
		if not name:
			return render.maps()
		else:
			return open('static/{}.png'.format(name), 'rb').read()
if __name__ == "__main__":
    app = web.application(urls, globals())
    app.run()
