import os
from PIL import Image
import webbrowser

def get_dir_list():
	dir_list = []
	for i in os.listdir('.'):
		if os.path.isdir(i):
			if i != 'gifs':
				dir_list.append(i)
	return dir_list
	
###

import web

urls = (
    '/(.*)', 'index'
)

class index:
    def GET(self):
	return "hello world"

if __name__ == "__main__":
    app = web.application(urls, globals())
    app.run()
