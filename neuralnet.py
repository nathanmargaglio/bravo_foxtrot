import pandas as pd
from numpy import *
from time import time
import os
import random
import sys

from keras.models import Sequential, model_from_json
from keras.callbacks import Callback
from keras.layers import Dense, Activation
from keras.optimizers import SGD, Adam
from keras.layers.normalization import BatchNormalization

class NeuralNet:
	def __init__(self, num_of_params, topology=None):
		self.name = str(int(time()))
		
		if not topology: # if we do not pass any topology at init
			# generate a random topology
			self.topology = self.genTopology()
		else: # otherwise
			self.topology = topology
		
		self.learning_rate = 1e-2
		self.epochs = 100
		self.num_of_params = num_of_params
		self.model = self.makeModel(self.topology, self.learning_rate,
									self.num_of_params)

	def genTopology(self):
		topology = []
		topology.append(random.randint(10,20))
		for i in range(random.randint(1,3)):
			topology.append(random.randint(10,20))
		return topology
		
	def makeModel(self,topology, lr, num_of_params):
		model = Sequential()

		model.add(Dense(topology[0], 
						input_dim=num_of_params, init='uniform',
						activation="tanh", bias=True))
		model.add(BatchNormalization())
		
		for i in range(1,len(topology)):
			model.add(Dense(output_dim=topology[i], init='uniform',
							activation="tanh", bias=True))
		
			model.add(BatchNormalization())

		model.add(Dense(output_dim=1, init='uniform', 
						activation="linear",bias=True))

		#~ sgd = SGD(lr=lr)
		adam = Adam(lr = lr)
		model.compile(loss='mae', optimizer=adam, metrics=['MAE'])
		return model
		
	def getTopology(self):
		return self.topology, self.learning_rate, self.epochs
		
	def getModel(self):
		return self.model
		
	def saveModel(self):
		model_json = self.model.to_json()
		with open('logs/'+self.name+'/model.json', "w") as json_file:
			json_file.write(model_json)
		# serialize weights to HDF5
		self.model.save_weights('logs/'+self.name+'/weights.h5',overwrite=True)

class PredictionModel:
	def __init__(self, name):
		self.name = name
		self.model = self.loadModel(model_id=name)
		
	def loadModel(self, model_id=None, weights=True):
		if not model_id:
			model_id=self.name
		json_file = open('logs/'+model_id+'/model.json', 'r')
		loaded_model_json = json_file.read()
		json_file.close()
		
		model = model_from_json(loaded_model_json)
		if weights:
			model.load_weights('logs/'+model_id+'/weights.h5')
		sgd = SGD(lr=5e-3)
		model.compile(loss='mae', optimizer=sgd, metrics=['MAE'])
		return model
