import pandas as pd
from numpy import *

from time import time
import os
import random
import sys

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

def trainNetwork(dh):
	# we initialize a dataset
	wi_vec, wo_vec, vi_vec, vo_vec = dh.getWorkingData()
	raw = dh.getRawData()
	
	#~ nn = initializeModel(dh)
	nn = randomModel(dh)
	model = nn.getModel()
	topology, learning_rate, epochs = nn.getTopology()
	
	if len(sys.argv) > 1:
		nn.name = sys.argv[1] + "_" + nn.name
	name = nn.name

	pltD = plotDevice(name)
	pltD.setParams(dh.getTrainingParameters())
	
	error = []
	decay_rate = 0.1
	batch_ratio = 1#random.choice(linspace(0.01,0.1,10))
	#~ batch_size = int(len(data_vectors)*batch_ratio)
	lowest_error = [0,None]
	
	lg = Logger(name)
	lg.log_header([name, topology, learning_rate, decay_rate, batch_ratio, epochs])
	lg.toterm()
	
	val_error = []
	for i in range(100):
		print "Iter:  " + str(i).zfill(3)+" --- "+str(epochs*i)
		hist = model.fit(wi_vec, wo_vec, verbose = 0, nb_epoch=epochs)  # starts training
		current_error = hist.history['mean_absolute_error'][-1]
		print "Error: " + str(current_error)
		print "LR:    " + str(model.optimizer.lr.get_value())
		print
		
		guessed = []
		input_vector, output_vector = dh.getIOData()
		for input_single in input_vector:
			guessed.append(float(model.predict(array([input_single]))))
			
		actual = array(output_vector)
		guessed = array(guessed)
		valid_set = ~isnan(guessed)
		error.append( mean(abs(actual[valid_set]-guessed[valid_set])/actual[valid_set]) )
		
		val_error_raw = []
		vguessed = []
		for vi in zip(vi_vec,vo_vec):
			vguessed.append(float(model.predict(array([vi[0]]))))
		
		vactual = array(vo_vec)
		vguessed = array(vguessed)
		valid_set = ~isnan(vguessed)
		val_error.append( mean(abs(vactual[valid_set]-vguessed[valid_set])/vactual[valid_set]) )
		
		lowest_error[0] += 1
		if not lowest_error[1]:
			lowest_error[1] = error[-1]
		if lowest_error[1] > error[-1]:
			lowest_error = [0, error[-1]]
			
		if lowest_error[0] >= 3:
			model.optimizer.lr.set_value(array(decay_rate*model.optimizer.lr.get_value(),dtype=float32))
			
		if lowest_error[0] >= 13:
			pltD.plot(raw, actual, guessed, error, val_error, 0,filepath = 'logs/static/'+name+'.png')
			return error[-1]
		
		nn.saveModel()
		pltD.addData([name, topology, learning_rate, decay_rate, batch_ratio, epochs])
		pltD.plot(raw, actual, guessed, error, val_error, i)
	
	nn.saveModel()
	pltD.plot(raw, actual, guessed, error, val_error, 0,filepath = 'logs/static/'+name+'.png')
	return error[-1]
	
dh = DataHandle()
while True:
	print "Starting Training..."
	dh.setTrainingParameters('gamma')
	results = trainNetwork(dh)
	print "Training Complete..."
	print
	
