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
	name = nn.name
	
	# This generates a topology and learning_rate (currently randomly)
	topology, learning_rate = nn.getTopology()
	# This generates a random NN model
	model = nn.getModel()
	
	dataset = zip(input_vector, output_vector)
	data_vectors = concatenate((input_vector, output_vector),axis=1)
	data_vectors = data_vectors[~isnan(data_vectors).any(axis=1)]

	pltD = plotDevice(name)
	
	error = []
	epochs=random.randint(1,100)
	past_error= 3
	decay_rate = random.choice(linspace(0.1,1,10))
	batch_ratio = random.choice(linspace(0.01,0.1,10))
	batch_size = int(len(data_vectors)*batch_ratio)
	dec_seq = random.randint(10,25)
	lowest_error = 0.5
	lowest_count = 0
	
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

		if past_error < current_error:
			model.optimizer.lr.set_value(array(decay_rate*model.optimizer.lr.get_value(),dtype=float32))
		past_error = current_error
		
		if lowest_error > current_error:
			lowest_error = current_error
			lowest_count = 0
		else:
			lowest_count += 1
			if lowest_count == dec_seq:
				return error[-1]
		
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
		
		pltD.addData([name, topology, learning_rate, decay_rate, batch_ratio, epochs])
		pltD.plot(raw, actual, guessed, error, i)
	
dh = DataHandle()
while True:
	print "Starting Training..."
	trainNetwork(dh)
	sys.stdout = oldstdout
	print "Training Complete..."
	print
	
