import pandas as pd
from numpy import *
from time import time
import os
import random
import sys

from keras.models import Sequential
from keras.callbacks import Callback
from keras.layers import Dense, Activation
from keras.optimizers import SGD, Adam
from keras.layers.normalization import BatchNormalization

class NeuralNet:
	def __init__(self, num_of_params):
		self.name = str(int(time()))
		self.topology, self.learning_rate, self.epochs = self.genTopology()
		self.num_of_params = num_of_params
		self.model = self.makeModel(self.topology, self.learning_rate,
									self.num_of_params)
		
	def genTopology(self):
		topology = []
		topology.append(random.randint(2,20))
		for i in range(random.randint(1,2)):
			topology.append(random.randint(2,20))
		learning_rate = 5e-3
		epochs=10
		return topology, learning_rate, epochs
		
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

		sgd = SGD(lr=lr)
		#~ adam = Adam(lr = lr)
		model.compile(loss='mae', optimizer=sgd, metrics=['MAE'])
		return model
		
	def getTopology(self):
		return self.topology, self.learning_rate, self.epochs
		
	def getModel(self):
		return self.model
