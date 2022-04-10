"""
useful/utility bluebike data loading methods
"""

# ----------------------------
# dependencies

# url crawling
import urllib.request

# json loading
import json

# pandas
import pandas as pd

# file handling
import os
from os import listdir
from os.path import isfile, join, isdir

# ----------------------------
# function defs


def load_station_info():
	"""
	reads station data from web
	loads and returns as dataframe
	"""

	# load station information data
	with urllib.request.urlopen("https://gbfs.bluebikes.com/gbfs/en/station_information.json") as url:
		station_info = json.loads(url.read().decode())['data']['stations']

    # convert station information to a DF
	return pd.DataFrame(station_info)

# end load_station_info()


def load_jsons_toDF( jsonpath ):
	"""
	Reads in json files and combines them into a single DF

	inputs:
		jsonpath
			type: str
			desc: base path where jsons are located
	"""

	# get all json filenames
	files = [ f for f in listdir(jsonpath) if isfile(join(jsonpath, f)) and 'json' in f ]

	# init list of dataframes where each DF contains data from one json file
	alldata_df_list = []

	# loop through each json file, add to a list of dataframe objects
	print('Loading ' + str(len(files)) + ' JSON files...')
	for fname, i_file in zip( files, range(len(files)) ):

		# load the json as a list of station dictionaries
		# then convert each dictionary to a dataframe

		# load json as dictionary
		with open( jsonpath + os.sep + files[0] ) as f_opened:
		    this_entry = json.load(f_opened)

		# grab the station information
		allstation_data = this_entry['data']['stations']

		# convert to dataframe and append to dataframe list
		alldata_df_list.append( pd.DataFrame(allstation_data) )

		# display when we've loaded 100 files
		if i_file % 100 == 99:
			print( 'loaded file ' + str(i_file) + ' of ' + str(len(files)) )

	# end for fname...
	print('done loading.')

	# concatenate all the dataframes into one
	return pd.concat( alldata_df_list )

# end load_jsons_toDF()
