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

def trainNetwork(dh):
	input_vector, output_vector = dh.getIOData()
	raw = dh.getRawData()
	nn = NeuralNet(input_vector.shape[1])
	nn.name = sys.argv[1] + "_" + nn.name
	name = nn.name
	
	# This generates a topology and learning_rate (currently randomly)
	topology, learning_rate = nn.getTopology()
	# This generates a random NN model
	model = nn.getModel()
	
	dataset = zip(input_vector, output_vector)
	data_vectors = concatenate((input_vector, output_vector),axis=1)
	data_vectors = data_vectors[~isnan(data_vectors).any(axis=1)]

	pltD = plotDevice(name)
	pltD.setParams(dh.getTrainingParameters())
	
	error = []
	epochs=25
	decay_rate = 0.5
	batch_ratio = 1#random.choice(linspace(0.01,0.1,10))
	batch_size = int(len(data_vectors)*batch_ratio)
	lowest_error = [0,3.]
	
	lg = Logger(name)
	lg.log_header([name, topology, learning_rate, decay_rate, batch_ratio, epochs])
	lg.toterm()
	for i in range(100):
		working_data = array(random.sample(data_vectors, batch_size))
		#~ working_data = data_vectors
		wi_vec = array(working_data[:,:-1], dtype=float32)
		wo_vec = array(working_data[:,-1], dtype=float32)
		print "Iter:  " + str(i).zfill(3)+" --- "+str(epochs*i)
		hist = model.fit(wi_vec, wo_vec, verbose = 0, nb_epoch=epochs)  # starts training
		current_error = hist.history['mean_absolute_error'][-1]
		print "Error: " + str(current_error)
		print "LR:    " + str(model.optimizer.lr.get_value())
		print
		
		actual = []
		guessed = []
		
		for val in dataset:
			res = float((model.predict(array([val[0]]))))
			act = val[1]
			
			actual.append(act)
			guessed.append(res)
			
		actual = array(actual)
		guessed = array(guessed)

		ave_error = (abs(actual-guessed)/actual).mean()
		
		error.append(hist.history['mean_absolute_error'][-1])
		
		lowest_error[0] += 1
		if lowest_error[1] > error[-1]:
			lowest_error = [0, error[-1]]
		if lowest_error[0] >= 3:
			pltD.plot(raw, actual, guessed, error, 0,filepath = 'logs/static/'+name+'.png')
			return error[-1]
		try:
			if error[-1] > error[-2]:
				model.optimizer.lr.set_value(array(decay_rate*model.optimizer.lr.get_value(),dtype=float32))
				if error[-1] > error[-3]:
					pltD.plot(raw, actual, guessed, error, 0,filepath = 'logs/pics/'+name+'.png')
					return error[-1]
		except:
			pass
		
		pltD.addData([name, topology, learning_rate, decay_rate, batch_ratio, epochs])
		pltD.plot(raw, actual, guessed, error, i)
	pltD.plot(raw, actual, guessed, error, 0,filepath = 'logs/static/'+name+'.png')
	return error[-1]
	
dh = DataHandle()
for param_set in ['alpha','beta','gamma']:
	print "Starting Training..."
	dh.setTrainingParameters(param_set)
	results = trainNetwork(dh)
	print "Training Complete..."
	print
	
