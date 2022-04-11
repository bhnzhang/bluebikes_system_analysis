"""
calculate average + std capacity for each station
"""

# add project base path to system path
import os
import sys

# need to append project root before importing other in package dependencies
PROJECT_ROOT = os.path.abspath(os.path.join(
                  os.path.dirname(__file__), 
                  os.pardir)
)
sys.path.append(PROJECT_ROOT)

# dependencies -------------------

# json loading
import json

# url crawling
import urllib.request

# for time string manipulation
import datetime

import os
from os import listdir
from os.path import isfile, join, isdir

# numpy
import numpy as np

# python debugger
import pdb
from matplotlib import pyplot as plt

# pandas
import pandas as pd

# pretty printer
import pprint

# remove unneeded columns
from data_handling.remove_unneeded_columns import f_remove_unneeded_columns

# for getting station info
from data_handling.data_loading_methods import *

# ------------------------------
# main

if __name__ == '__main__':

	# load csv
	# file to load
	# filetoload = 'U:\\bluebikes\\station data 220403 1319\\alldata.csv'
	# filetoload = 'U:\\bluebikes\\station data cropped\\alldata2.csv'
	filetoload = 'U:\\bluebikes\\station data 2022 03\\alldata.csv'

	# read csv into df
	alldata_df = pd.read_csv(filetoload, index_col=0)

	# convert the time to datetime format
	alldata_df['last_reported'] = pd.to_datetime( alldata_df['last_reported'], unit='s' )
	alldata_df.set_index('last_reported', inplace=True)

	# calculate capacity ratio and add that as a column
	alldata_df['capacity_ratio'] = alldata_df['num_bikes_available']/alldata_df['capacity']

	# plot for station 3
	

	# group by station id and calculate mean for each column
	data_avg_by_id = alldata_df.groupby(['station_id']).mean()
	data_std_by_id = alldata_df.groupby(['station_id']).std()

	# plot avg and std
	plt.scatter( data_avg_by_id.index, data_avg_by_id['capacity_ratio'] )
	plt.scatter( data_std_by_id.index, data_std_by_id['capacity_ratio'] )
	# data_avg_by_id.plot.scatter(y='capacity_ratio')
	# data_std_by_id.plot.scatter(y='capacity_ratio')
	plt.show()

	# data_grouped_by_id = alldata_df.groupby(['station_id'])

	# plot all the data on one plot dont do this
	# data_grouped_by_id['capacity_ratio'].plot(legend=True)

	# another way to do it by just looking at capacity ratio data

	# calculate mean and average vs. station
	# data_grouped_capacityratio = data_grouped_by_id['capacity_ratio']
	# data_avged  = data_grouped_capacityratio.mean()
	# data_std 	= data_grouped_capacityratio.std()

	# # debugging
	# # print(alldata_df)
	# print(data_grouped_capacityratio)
	# print(data_avged)
	# print(data_std)
	# print(data_grouped_by_id.size())

	# plot avg and std
	# data_avged.plot()
	# data_std.plot()

	
	# plot capacity over time for a station
	station_id = 66
	data_chosenstation = alldata_df.loc[alldata_df['station_id'] == station_id]

	print(data_chosenstation)

	# set datetime to be index
	# data_chosenstation.set_index( 'last_reported', inplace=True )
	# data_chosenstation['capacity_ratio'].plot()
	# plt.show()

	# # pivot table on station id
	# pivot_table_test = pd.pivot_table( alldata_df.reset_index(),
	# 						index='last_reported', columns='station_id', values='capacity_ratio')
	# print(pivot_table_test)

	# pivot_table_test[3].plot()
	# plt.show()

	# get a specific group
	data_group_station66 = data_grouped_capacityratio.get_group(66)
	print(data_group_station66)

	

	# # testing std function
	# df = pd.DataFrame({'person_id': [0, 1, 2, 3],
	# 					'age': [21, 25, 62, 43],
	# 					'height': [1.61, 1.87, 1.49, 2.01]}
	# 					).set_index('person_id')

	# print(df.std(ddof=0))