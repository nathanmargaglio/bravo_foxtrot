import matplotlib
matplotlib.use('Agg') # omit this for live plot, need it for SSH
import matplotlib.pyplot as plt
from matplotlib import gridspec
from matplotlib import text
from mpl_toolkits.mplot3d import Axes3D
from matplotlib import cm
from matplotlib.mlab import griddata

import pandas as pd
from numpy import *
from geoplot import GeoPlot

class plotDevice:
	def __init__(self, name):
		self.name = name
		self.fig = plt.figure(figsize=(12,8), dpi=80)
		self.gp = GeoPlot(name)

	def addData(self, top):
		self.data_info = top
		
	def setParams(self, params):
		self.params = params

	def getData(self):
		return self.data_info

	def plot(self, raw, actual, guessed, trn_error, val_error, i, filepath=None):
		name = self.name
		if not filepath:
			#Default file path
			filepath = 'logs/'+name+'/img/'+str(i)+'.png'
		fig = self.fig
		name, topology, trn_error, val_error = self.getData()
		ax11 = plt.subplot2grid((4, 8), (0, 0), rowspan=3, colspan=4, 	projection='3d')
		ax12 = plt.subplot2grid((4, 8), (0, 4), rowspan=3, colspan=4)
		ax21 = plt.subplot2grid((4, 8), (3, 0), rowspan=1, colspan=4)
		ax22 = plt.subplot2grid((4, 8), (3, 4), rowspan=1, colspan=4)

		raw_plot = raw.copy()
		raw_plot.reset_index
		raw_plot['Z'] = pd.Series(guessed, index=raw_plot.index)
		raw_plot = raw_plot.drop_duplicates(subset=['X','Y'])
		
		raw_plot = raw_plot[~array(raw_plot['X'].apply(isnan))]
		raw_plot = raw_plot[~array(raw_plot['Y'].apply(isnan))]
		raw_plot = raw_plot[~array(raw_plot['Z'].apply(isnan))]
		
		del self.gp
		self.gp = GeoPlot(name)
		self.gp.draw(raw_plot)
		
		# Plot Everything
		#~ xi = linspace(min(raw_plot['X']), max(raw_plot['X']), 50)
		#~ yi = linspace(min(raw_plot['Y']), max(raw_plot['Y']), 50)
		
		#Plot arbitrary region (for wire frame)
		xi_wire = linspace(41.5, 43.5, 50)
		yi_wire = linspace(-80., -77., 50)
		
		X_wire, Y_wire = meshgrid(xi_wire, yi_wire)
		
		Z_wire = griddata(	raw_plot['Latitude'], 
						raw_plot['Longitude'], 
						array(raw_plot['Z']), 
						xi_wire, yi_wire)
		
		#Plot arbitrary region

		xi = linspace(41.5, 43.5, 50)
		yi = linspace(-80., -77., 50)
		
		X, Y = meshgrid(xi, yi)

		Z = griddata(	raw_plot['Latitude'], 
						raw_plot['Longitude'], 
						array(raw_plot['Z']), 
						xi, yi)
						
		Gx, Gy = gradient(Z)
		G = (Gx**2+Gy**2)**.5
		N = G/G.max()
		#~ surf = ax11.plot_surface(X, Y, Z, rstride=10, cstride=1, facecolors=cm.cool(N),
						#~ linewidth=1, antialiased=True)

		wire = ax11.plot_wireframe(X_wire, Y_wire, Z_wire)
		contour = ax12.contourf(X, Y, Z)

		ax11.set_xlim3d(min(xi), max(xi))
		ax11.set_ylim3d(min(yi), max(yi))
		ax11.set_zlim3d(min(guessed), max(guessed))
		
		ax21.plot(actual,'g')
		ax21.plot(guessed, 'r')

		ax22.plot(trn_error,'g')
		ax22.plot(val_error,'r')
		#~ plt.title(str(trn_error[-1]) + ' / ' + str(val_error[-1]))
		
		ax11.grid(b=False)
		ax12.grid(b=False)
		
		ax11.azim=i*10
		ax12.azim=0
		ax12.elev=90
		
		ax11.set_zticks([])
		ax11.set_yticks([])
		ax11.set_xticks([])
		
		ax12.set_yticks([])
		ax12.set_xticks([])
		
		ax22.set_yticks([])

		txtstr = ""
		
		txtstr += "Model Name       : " + name + '\n'
		txtstr += "Topology         : " + " - ".join(array(topology,dtype=str)) + '\n'
		txtstr += "Training Error   : " + str(trn_error[-1]) + '\n'
		txtstr += "Validation Error : " + str(val_error[-1]) + '\n'

		ax12.annotate(txtstr, xy=(25,675), xycoords='figure pixels')
		ax12.annotate(self.params, xy=(25,25), xycoords='figure pixels')
		plt.savefig(filepath)

		ax11.cla()
		ax12.cla()
		ax22.cla()
		ax21.cla()

		
