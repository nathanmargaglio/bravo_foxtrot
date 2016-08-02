import sys
import os

from numpy import *

class Logger:
	def __init__(self, name):
		if not os.path.exists('logs'):
			os.mkdir('logs')
		os.mkdir('logs/'+name)
		os.mkdir('logs/'+name+'/img')
		f = open('logs/'+name+'/'+name+".txt",'w')
		f.close()
	
		self.oldstdout = sys.stdout
		self.f = open('logs/'+name+'/'+name+".txt",'a')
		sys.stdout = self.f
		
	def log_header(self, initilizers):
		name, topology, learning_rate, decay_rate, batch_ratio, epochs = initilizers
		print "Start Training: " + name
		print "Topology     : " + " - ".join(array(topology,dtype=str))
		print "Learn Rate   : " + str(learning_rate)
		print "LR_Decay Rate: " + str(decay_rate)
		print "Batch Ratio  : " + str(batch_ratio)
		print "Epochs       : " + str(epochs)
		print
		
	def save(self):
		self.f.close()
		self.f = open('logs/'+name+'/'+name+".txt",'a')
		sys.stdout = self.f
		
	def toterm(self):
		sys.stdout = self.oldstdout
