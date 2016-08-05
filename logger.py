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
		name, topology, trn_error, val_error = initilizers
		print "Model Name       : " + name
		print "Topology         : " + " - ".join(array(topology,dtype=str))
		print "Training Error   : " + str(trn_error)
		print "Validation Error : " + str(val_error)
		print
		
	def save(self):
		self.f.close()
		self.f = open('logs/'+name+'/'+name+".txt",'a')
		sys.stdout = self.f
		
	def toterm(self):
		sys.stdout = self.oldstdout
