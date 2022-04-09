# load all json information
# save all information to a csv

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

# pre-main ---------------

# init a pretty printer object
pp = pprint.PrettyPrinter(indent=4)

# main -------------------

# get all json filenames
basepath 	= 'U:\\bluebikes\\station data cropped' # subset of data
# basepath 	= 'U:\\bluebikes\\station data 220403 1319'
files 		= [ f for f in listdir(basepath) if isfile(join(basepath, f)) and 'json' in f ]

# list of dataframes where each DF contains data from one json file
alldata_df_list = []

# loop through each json file, add to a list of dataframe objects
for fname, i_file in zip( files, range(len(files)) ):

	# load the json as a list of station dictionaries
	# then convert each dictionary to a dataframe

	# load json as dictionary
	with open( basepath + os.sep + files[0] ) as f_opened:
	    this_entry = json.load(f_opened)

    # grab the station information
	allstation_data = this_entry['data']['stations']

	# convert to dataframe and append to dataframe list
	alldata_df_list.append( pd.DataFrame(allstation_data) )

	# display when we've loaded 100 files
	if i_file % 100 == 99:
		print( 'file ' + str(i_file) + ' of ' + str(len(files)) )

# end for fname...

# concatenate all the dataframes into one
alldata_df = pd.concat( alldata_df_list )

# convert the time to datetime format
alldata_df['last_reported'] = pd.to_datetime( alldata_df['last_reported'], unit='s' )

alldata_df.set_index(['last_reported'], inplace=True) # index by date

# debug print
print(alldata_df)
# print(alldata_df['last_reported'])

# save to csv
# alldata_df.to_csv('test.csv')

# now i want to add columns for the station information data

# load station information data
with urllib.request.urlopen("https://gbfs.bluebikes.com/gbfs/en/station_information.json") as url:
    station_info = json.loads(url.read().decode())['data']['stations']

# debug
# pp.pprint(station_info)

# convert station information to a DF
station_info_df = pd.DataFrame(station_info)

print(station_info_df)

# ok let me try merging
alldata_merged = alldata_df.merge( station_info_df, how='left', on='station_id')

print(alldata_merged)

# save to csv
alldata_merged.to_csv(basepath + os.sep + 'alldata.csv')

# ok that worked
# but i want to index by date

# allstation_data = []
