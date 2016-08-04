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

class plotDevice:
	def __init__(self, name):
		self.name = name
		self.fig = plt.figure(figsize=(12,8), dpi=80)

	def addData(self, top):
		self.data_info = top
		
	def setParams(self, params):
		self.params = params

	def getData(self):
		return self.data_info

	def plot(self, raw, actual, guessed, error, val_error, i, filepath=None):
		name = self.name
		if not filepath:
			#Default file path
			filepath = 'logs/'+name+'/img/'+str(i)+'.png'
		fig = self.fig
		name, topology, learning_rate, decay_rate, batch_ratio, epochs = self.getData()
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
		
		# Plot Everything
		#~ xi = linspace(min(raw_plot['X']), max(raw_plot['X']), 50)
		#~ yi = linspace(min(raw_plot['Y']), max(raw_plot['Y']), 50)
		
		#Plot arbitrary region
		xi = linspace(-1., 0, 50)
		yi = linspace(-1., 0, 50)
		
		X, Y = meshgrid(xi, yi)
				
		#~ raw_plot[['Z','Latitude','Longitude']].to_csv("qgis_data.csv")
		
		Z = griddata(	raw_plot['X'], 
						raw_plot['Y'], 
						array(raw_plot['Z']), 
						xi, yi)
						
		Gx, Gy = gradient(Z)
		G = (Gx**2+Gy**2)**.5
		N = G/G.max()
		#~ surf = ax11.plot_surface(X, Y, Z, rstride=10, cstride=1, facecolors=cm.cool(N),
						#~ linewidth=1, antialiased=True)

		wire = ax11.plot_wireframe(X, Y, Z)
		contour = ax12.contourf(X, Y, Z)

		ax11.set_xlim3d(min(xi), max(xi))
		ax11.set_ylim3d(min(yi), max(yi))
		ax11.set_zlim3d(min(guessed), max(guessed))
		
		ax21.plot(actual,'g')
		ax21.plot(guessed, 'r')

		ax22.plot(error,'g')
		ax22.plot(val_error,'r')
		plt.title(str(error[-1]))
		
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
		
		txtstr += "Start Training: " + name + "\n"
		txtstr += "Topology     : " + " - ".join(array(topology,dtype=str)) + "\n"
		txtstr += "Learn Rate   : " + str(learning_rate) + "\n"
		txtstr += "LR_Decay Rate: " + str(decay_rate) + "\n"
		txtstr += "Batch Ratio  : " + str(batch_ratio) + "\n"
		txtstr += "Epochs       : " + str(epochs)

		ax12.annotate(txtstr, xy=(25,600), xycoords='figure pixels')
		ax12.annotate(self.params, xy=(25,25), xycoords='figure pixels')
		plt.savefig(filepath)

		ax11.cla()
		ax12.cla()
		ax22.cla()
		ax21.cla()

		
