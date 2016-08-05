import gmplot as gm
from numpy import *
import pandas as pd

class GeoPlot:
	def __init__(self, name):
		self.name = name
		self.gmap = gm.GoogleMapPlotter(43, -79, 10)
	
	def draw(self, raw):
		name = self.name
		z = array(raw['Z'])
		
		#~ import matplotlib.pyplot as plt
		#~ plt.plot(sort(z))
		#~ plt.show()
		
		gradients = ['green', 'yellowgreen', 'yellow', 'orange', 'orangered', 'red']
		bins = len(gradients)
		alpha_vals = linspace(0.25,1,bins)
		val = max(z)/bins
		for i in range(bins):
			wd = raw[raw['Z'] > i*val]
			if i != bins-1:
				wd = wd[wd['Z'] < (i+1)*val]
			
			lats = array(wd['Latitude'])
			lngs = array(wd['Longitude'])
			coords = zip(lats, lngs)
			for c in coords:
				self.gmap.circle(c[0], c[1], radius=100, edge_width=0, face_alpha=alpha_vals[i], face_color = gradients[i])
				
		open('logs/'+name+"/map.html",'w').close()
		self.gmap.draw('logs/'+name+"/map.html")
