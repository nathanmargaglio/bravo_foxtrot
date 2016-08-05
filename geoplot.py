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
		key = 'AIzaSyAOPK5kDNgtv4lLnCRKC9cjnGVU8-4TiYY'
		self.draw_file('logs/'+name+"/map.html", key)
		
	def draw_file(self, htmlfile, key=""):
		if not key == "":
			key = key+'&'
		f = open(htmlfile, 'w')
		f.write('<html>\n')
		f.write('<head>\n')
		f.write(
			'<meta name="viewport" content="initial-scale=1.0, user-scalable=no" />\n')
		f.write(
			'<meta http-equiv="content-type" content="text/html; charset=UTF-8"/>\n')
		f.write('<title>Google Maps - pygmaps </title>\n')
		f.write('<script type="text/javascript" src="https://maps.googleapis.com/maps/api/js?key='+key+'libraries=visualization&sensor=true_or_false"></script>\n')
		f.write('<script type="text/javascript">\n')
		f.write('\tfunction initialize() {\n')
		self.gmap.write_map(f)
		self.gmap.write_grids(f)
		self.gmap.write_points(f)
		self.gmap.write_paths(f)
		self.gmap.write_shapes(f)
		self.gmap.write_heatmap(f)
		f.write('\t}\n')
		f.write('</script>\n')
		f.write('</head>\n')
		f.write(
			'<body style="margin:0px; padding:0px;" onload="initialize()">\n')
		f.write(
			'\t<div id="map_canvas" style="width: 100%; height: 100%;"></div>\n')
		f.write('</body>\n')
		f.write('</html>\n')
		f.close()
		
