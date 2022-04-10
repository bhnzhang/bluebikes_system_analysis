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
	# filetoload = 'U:\\bluebikes\\station data cropped\\alldata.csv'
	filetoload = 'U:\\bluebikes\\station data 2022 03\\alldata.csv'

	# read csv into df
	alldata_df = pd.read_csv(filetoload, index_col=0)

	# calculate capacity ratio and add that as a column
	alldata_df['capacity_ratio'] = alldata_df['num_bikes_available']/alldata_df['capacity']

	# plot for station 3
	

	# group by station id and calculate mean for each column
	data_avg_by_id = alldata_df.groupby(['station_id']).mean()
	data_std_by_id = alldata_df.groupby(['station_id']).std()

	# print(alldata_df)
	print(alldata_df.groupby(['station_id']).mean())

	# plot avg and std
	plt.scatter( data_avg_by_id.index, data_avg_by_id['capacity_ratio'] )
	plt.scatter( data_std_by_id.index, data_std_by_id['capacity_ratio'] )
	# data_avg_by_id.plot.scatter(y='capacity_ratio')
	# data_std_by_id.plot.scatter(y='capacity_ratio')
	plt.show()