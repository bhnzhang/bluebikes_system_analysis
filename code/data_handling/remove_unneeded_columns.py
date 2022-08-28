# load station data and remove unneeded columns

# dependencies -------------------

# json loading
import json

# url crawling
import urllib.request

# for time string manipulation
import datetime

# for scheduling repeated events
import sched, time

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

# ------------------------
# function defs

# remove unneeded columns
def f_remove_unneeded_columns( df ):
	"""
	input:
		df
			type: dataframe object
			desc: DF to remove columns from
	"""

	# list of columns to remove
	columns_to_remove = [ 'num_ebikes_available', 'eightd_has_available_keys', 
				  	'legacy_id_x', 'external_id', 'electric_bike_surcharge_waiver',
				  	'legacy_id_y', 'eightd_station_services', 'short_name', 'station_type',
				  	'rental_methods', 'has_kiosk', 'eightd_has_key_dispenser', 'eightd_active_station_services', 
				  	'valet', 'capacity' ]

	return df.drop( columns_to_remove, axis=1, errors='ignore')
# end remove_unneeded_columns()

# main -------------------

if __name__ == '__main__':

	# file to load
	# filetoload = 'U:\\bluebikes\\station data 220403 1319\\alldata.csv'
	filetoload = 'U:\\bluebikes\\station data cropped\\alldata.csv'

	# read csv into df
	alldata_df = pd.read_csv(filetoload, index_col=0)

	# print out df before removing columns
	print(alldata_df.head(5))
	print(alldata_df.columns)


	# remove unneeded columns
	alldata_df = remove_unneeded_columns(alldata_df)

	# print out df after
	print(alldata_df)
	print(alldata_df.columns)

	# save
	alldata_df.to_csv(filetoload, index=False)
