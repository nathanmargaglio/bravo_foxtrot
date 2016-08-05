import pandas as pd
from numpy import *
from time import time
import os
import random
import sys

class DataHandle:
	def __init__(self, params='all', targets='default'):
		self.raw = self.importData()
		self.master_coords = self.importGeoData()
		self.raw = self.joinData(self.raw, self.master_coords)
		self.raw = self.basicClean(self.raw)
		self.setTrainingParameters(params)
		self.setTargetParameters(targets)
		
		self.input_matrix, self.output_matrix = \
			self.genIOMatrix(self.raw, 
								self.training_columns, 
								self.target_columns)
								
	def setTrainingParameters(self, params='all'):
		if type(params) == 'list':
			self.training_columns = params
		if params == 'all':
			self.training_columns = ['X', 'Y', 'Beds Total', 'Assessed Value', 'DOM',
								'Sq Ft Total', 'Lot Dimensions Depth', 'Lot Dimensions Frontage',
								'Numof Acres', 'Numof Stories', 'Numof Garage Spaces', 
								'Numof Rooms', 'Baths Half', 'Baths Full','Age']
		if params == 'alpha':
			# alpha is initially trained on (X,Y) coordinates
			self.training_columns = ['X','Y']
		if params == 'beta':
			# alpha is initially trained on (X,Y) coordinates
			self.training_columns = ['Assessed Value']
		if params == 'gamma':
			# alpha is initially trained on (X,Y) coordinates
			self.training_columns = ['X','Y','Assessed Value']
	
	def setTargetParameters(self, params='default'):
		if type(params) == 'list':
			self.target_columns = params
		if params == 'default':
			self.target_columns = ['Sale Price']
			
	def getTrainingParameters(self):
		return self.training_columns
		
	def getTargetParameters(self):
		return self.target_columns
		
	def getIOData(self):
		return self.input_matrix, self.output_matrix
		
	def getRawData(self):
		return self.raw
		
	def getInputSize(self):
		return self.input_matrix.shape[1]
		
	def importData(self):
		raw = None
		#~ for fn in os.listdir('data'):
		for fn in ['erie_2015_v2.csv']:
			next_file = pd.read_csv("data/{}".format(fn), thousands=',')
			raw = pd.concat((raw, next_file))
		raw.reset_index()
		return raw

	def importGeoData(self):
		master_coords = None
		for fn in ['erie_2015_geo.csv']:
			coords = pd.read_csv("data/{}".format(fn))
			if 'LAT_M' in coords.columns:
				coords['Latitude'] = array(coords['LAT_D']) + array(coords['LAT_M'])/60. + array(coords['LAT_S'])/3600.
				coords['Longitude'] = array(coords['LNG_D']) + array(coords['LNG_M'])/60. + array(coords['LNG_S'])/3600.
				wdf = pd.DataFrame(coords[['Address','City','Zip','Latitude','Longitude']], columns = ['Address','City','Zip','Latitude','Longitude'])
			if 'Latitude' in coords.columns:
				wdf = pd.DataFrame(coords[['Address','City','Zip','Latitude','Longitude']], columns = ['Address','City','Zip','Latitude','Longitude'])
			
			master_coords = pd.concat((master_coords, wdf))
			master_coords['Zip Code'] = master_coords['Zip']
			#~ raw = raw.drop_duplicates(subset=['X','Y'])
		return master_coords

	def joinData(self, raw, master_coords):
		raw = pd.merge(raw, master_coords, on = ('Address', 'City', 'Zip Code'), how='inner')

		raw['X'] = raw['Latitude']
		raw['Y'] = raw['Longitude']

		return raw

	def basicClean(self, raw):
		# create 'SP/AV' column, remove "Changed" and "AV == 0" listings,
		# and trimming 'weird' listings
		raw[['Sale Price','Assessed Value']] = \
						(raw[['Sale Price','Assessed Value']]
						.replace( '[\$,)]','', regex=True )).astype(float)
		raw['SP/AV'] = raw['Sale Price']/raw['Assessed Value']
		raw['SP/SF'] = raw['Sale Price']/raw['Sq Ft Total']
		raw = raw[raw['Assessed Value'] != 0].reset_index()
		raw = raw[raw['SP/AV'] < 10]
		raw = raw[raw['SP/SF'] < 200]
		return raw
		
	def normalize(self, data):
		# This function does a min/max normalization.
		# It returns the normalized vector.
		data = pd.Series(data)
		try:
			data -= mean(data)
		except:
			for n,d in enumerate(data):
				if type(d) == str:
					data.iloc[n] = 0
		data = data - min(data)
		data = data/max(data)
		data -= 0.5
		data *=2
		return data
		
	def genIOMatrix(self, raw, training, targets):
		input_vector = empty((len(raw),len(training)), dtype=float)
		output_vector = empty((len(raw),len(targets)), dtype=float)

		for n,c in enumerate(training):
			raw[c] = self.normalize(raw[c])
			input_vector[:,n] = array(raw[c], dtype=object)
		for n, c in enumerate(targets):
			output_vector[:,n] = array(raw[c], dtype=object)
			
		return input_vector, output_vector
		
	def getWorkingData(self):
		input_vector, output_vector = self.getIOData()

		#~ dataset = zip(input_vector, output_vector)
		data_vectors = concatenate((input_vector, output_vector),axis=1)
		data_vectors = data_vectors[~isnan(data_vectors).any(axis=1)]
		
		random.shuffle(data_vectors)
		training_data = array(data_vectors[:int(len(data_vectors)*0.8)])
		validation_data = array(data_vectors[int(len(data_vectors)*0.8):])
		
		wi_vec = array(training_data[:,:-1], dtype=float32)
		wo_vec = array(training_data[:,-1], dtype=float32)
		
		vi_vec = array(validation_data[:,:-1], dtype=float32)
		vo_vec = array(validation_data[:,-1], dtype=float32)

		return wi_vec, wo_vec, vi_vec, vo_vec
		
if __name__ == "__main__":
	dh = DataHandle()
	print dh.getInputSize()
		
		
