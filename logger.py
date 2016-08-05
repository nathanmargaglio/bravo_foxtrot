import sys
import os

from numpy import *

class Logger:
	def __init__(self, name):
		self.name=name
		if not os.path.exists('logs'):
			os.mkdir('logs')
		os.mkdir('logs/'+name)
		os.mkdir('logs/'+name+'/img')
		f = open('logs/'+name+'/'+name+".txt",'w')
		f.close()
		
	def log_header(self, initilizers):

		f = open('logs/'+self.name+'/'+self.name+".txt",'a')

		name, topology, trn_error, val_error = initilizers
		
		txtstr = ""
		
		txtstr += "Model Name       : " + name + '\n'
		txtstr += "Topology         : " + " - ".join(array(topology,dtype=str)) + '\n'
		txtstr += "Training Error   : " + str(trn_error[-1]) + '\n'
		txtstr += "Validation Error : " + str(val_error[-1]) + '\n'
		
		f.write(txtstr)
		f.close()
		
		
