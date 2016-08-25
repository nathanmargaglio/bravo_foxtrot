import pandas as pd
from numpy import *

from time import time
import os
import random
import sys

import matplotlib.pyplot as plt

from datahandle import DataHandle
from neuralnet import NeuralNet
from plotdevice import plotDevice
from logger import Logger

def initializeModel(dh):
	# create a starting topology
	topology = [20,10]
	
	# we initialize a neural net using the topology
	nn = NeuralNet(dh.getInputSize(), topology)

	return nn
	
def randomModel(dh):
	nn = NeuralNet(dh.getInputSize())
	
	# This generates a topology and learning_rate (currently randomly)
	topology, learning_rate, epochs = nn.getTopology()
	
	return nn
	
def exitTraining(nn, lg, pltD, raw, actual, guessed, trn_error, val_error):
	lg.log_header([nn.name, nn.topology, trn_error, val_error])
	pltD.addData([nn.name, nn.topology, trn_error, val_error])
	pltD.plot(raw, actual, guessed, trn_error, val_error, 1,filepath = 'logs/static/'+nn.name+'.png')
	nn.saveModel()

def trainNetwork(dh):
	# we initialize a dataset
	wi_vec, wo_vec, vi_vec, vo_vec = dh.getWorkingData()
	raw = dh.getRawData()
	
	nn = initializeModel(dh)
	#~ nn = randomModel(dh)
	model = nn.getModel()
	topology, learning_rate, epochs = nn.getTopology()
	
	if len(sys.argv) > 1:
		nn.name = sys.argv[1] + "_" + nn.name
	name = nn.name
	
	print "Starting Training on " + name
	print "Topology: " + " - ".join(array(topology,dtype=str))
	print "--------------------"

	pltD = plotDevice(name)
	pltD.setParams(dh.getTrainingParameters())
	
	error = []
	decay_rate = 0.1
	batch_ratio = 1#random.choice(linspace(0.01,0.1,10))
	#~ batch_size = int(len(data_vectors)*batch_ratio)
	lowest_error = [0,None]
	
	lg = Logger(name)
	
	trn_error = []
	val_error = []
	for i in range(100):
		hist = model.fit(wi_vec, wo_vec, verbose = 0, nb_epoch=epochs)  # starts training
		
		guessed = []
		input_vector, output_vector = dh.getIOData()
		for input_single in input_vector:
			guessed.append(float(model.predict(array([input_single]))))
			
		actual = array(output_vector)
		guessed = array(guessed)
		
		### training error
		wguessed = []
		for wi in zip(wi_vec,wo_vec):
			wguessed.append(float(model.predict(array([wi[0]]))))
		
		wactual = array(wo_vec)
		wguessed = array(wguessed)
		valid_set = ~isnan(wguessed)
		raw_trn_error = abs(wactual[valid_set]-wguessed[valid_set])/wactual[valid_set]
		#~ raw_trn_error = sorted(raw_trn_error)[:int(len(raw_trn_error)*0.682)]
		trn_error.append( mean(raw_trn_error) )
		
		### validation error
		vguessed = []
		for vi in zip(vi_vec,vo_vec):
			vguessed.append(float(model.predict(array([vi[0]]))))
		
		vactual = array(vo_vec)
		vguessed = array(vguessed)
		valid_set = ~isnan(vguessed)
		raw_val_error = abs(vactual[valid_set]-vguessed[valid_set])/vactual[valid_set]
		#~ raw_val_error = sorted(raw_val_error)[:int(len(raw_val_error)*0.682)]
		val_error.append( mean(raw_val_error) )
		#~ val_error.append( mean(abs(vactual[valid_set]-vguessed[valid_set])/vactual[valid_set]) )
		
		lowest_error[0] += 1
		if not lowest_error[1]:
			lowest_error[1] = trn_error[-1]
		if lowest_error[1] > trn_error[-1]:
			lowest_error = [0, trn_error[-1]]
			
		if lowest_error[0] >= 3:
			model.optimizer.lr.set_value(array(decay_rate*model.optimizer.lr.get_value(),dtype=float32))
			
		if lowest_error[0] >= 13:
			exitTraining(nn, lg, pltD, raw, actual, guessed, trn_error, val_error)
			return 0

		nn.saveModel()
		pltD.addData([name, topology, trn_error, val_error])
		pltD.plot(raw, actual, guessed, trn_error, val_error, i)
		
		print "Iteration       : " + str(i).zfill(3)
		print "Training Error  : " + str(trn_error[-1])
		print "Validation Error: " + str(val_error[-1])
		
		try:
			print "Delta Trn Error : " + str(abs(trn_error[-1]-trn_error[-2]))
			print "Delta Val Error : " + str(abs(val_error[-1]-val_error[-2]))
		except:
			pass
		print
	
	exitTraining(nn, lg, pltD, raw, actual, guessed, trn_error, val_error)
	return 0

dh = DataHandle("gamma")
results = trainNetwork(dh)
print "Training Complete."
	
