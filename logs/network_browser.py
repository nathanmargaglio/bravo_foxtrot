import os
from PIL import Image
import webbrowser
import subprocess

def get_dir_list():
	dir_list = []
	for i in os.listdir('.'):
		if os.path.isdir(i):
			if i != 'gifs':
				dir_list.append(i)
	return dir_list
	
###

import web

render = web.template.render('templates/')

urls = (
    '/(.*)', 'index'
)

class index:
    def GET(self, name):
		if not name:
			dir_list = get_dir_list()
			return render.index(dir_list)
		elif name[0]=='1':
			try:
				return open('gifs/{}.gif'.format(name),'rb').read()
			except:
				subprocess.Popen('sudo ./render_gif.sh {}'.format(name))
				print "Rendering Gif... (pronounced JIF)"
				return open('gifs/{}.gif'.format(name),'rb').read()

if __name__ == "__main__":
    app = web.application(urls, globals())
    app.run()
