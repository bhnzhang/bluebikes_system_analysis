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

# geopandas
import geopandas

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
		with open( jsonpath + os.sep + files[i_file] ) as f_opened:
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


# function to load massachussetts city limits data
def load_MA_citylimits():
	# load the city limits data
	shapefile = r"C:\Users\beezy\git\bluebikes_system_analysis\data\state of mass datasets\townssurvey_shp.zip!"
	dataset_name = "TOWNSSURVEY_POLYM.shp" # this one keeps one area per city. i think this is what i want to use
	citylimits = geopandas.read_file(shapefile + dataset_name, crs='EPSG:4269')

	# towns_to_keep = [ 'BOSTON', 'CAMBRIDGE', 'SOMERVILLE', 'BROOKLINE', 'EVERETT',
	#                   'REVERE', 'CHELSEA', 'MALDEN', 'ARLINGTON', 'MEDFORD', 'BELMONT',
	#                   'WATERTOWN', 'NEWTON' ]

	# citylimits = citylimits.loc[ citylimits['TOWN'].isin(towns_to_keep) ]

	citylimits = citylimits.to_crs( 'EPSG:4269' )

	return citylimits


# function to load 2020 census tract geography data
def load_census_tractdata():
	""" Loads 2020 census tract geography data """

	# path to database
	zipfile_base =  "zip://C:\\Users\\beezy\\git\\bluebikes_system_analysis\\data\\census data\\tl_2020_25_all_mass_shapefile.zip!"
	database_name = 'tl_2020_25_tract20.shp'
	zipfile = zipfile_base + database_name

	# load
	tract_shapefile = r'C:\Users\beezy\git\bluebikes_system_analysis\data\census data\tl_2020_25_all_mass_shapefile\tl_2020_25_tract20.shp'
	geodata = geopandas.read_file(tract_shapefile)

	# keep only tracts in counties around boston
	suffolk_county_id = '025'
	middlesex_county_id = '017'
	norfolk_county_id = '021'
	geodata = geodata.loc[ (geodata['COUNTYFP20'] == suffolk_county_id) | 
	                       (geodata['COUNTYFP20'] == middlesex_county_id) |
	                       (geodata['COUNTYFP20'] == norfolk_county_id) ]

	# rename some things to be more intelligible
	geodata = geodata.rename( columns={'GEOID20':'geo_id', 'ALAND20':'land_area', 
	                                   'AWATER20':'water_area', 'INTPTLAT20':'lat',
	                                  'INTPTLON20':'lon', 'COUNTYFP20':'countyid'} )

	# remove unneeded columns
	geodata = geodata.drop( columns=['STATEFP20', 'TRACTCE20', 'NAME20',
	                                'NAMELSAD20', 'MTFCC20', 'FUNCSTAT20'] )

	# add a column for total area
	geodata['total_area'] = geodata['land_area'] + geodata['water_area']

	return geodata


# function to load 2020 census population data
def load_census_popdata():
	""" load 2020 census population data for massachussetts by tract """
	# all of mass, by tract
	pop_datafile = r'C:\Users\beezy\git\bluebikes_system_analysis\data\census data\DECENNIALPL2020.P1_2022-08-29T095602 mass data per census tracts\DECENNIALPL2020.P1-Data.csv'

	popdata = pd.read_csv(pop_datafile, skiprows=[1], header=0, usecols=['GEO_ID','P1_001N'])

	# change column names
	popdata = popdata.rename(columns={'P1_001N':'population', 'GEO_ID':'geo_id'} )

	# remove excess characters from geo id
	popdata['geo_id'] = popdata['geo_id'].map( lambda x: x[9:] )

	return popdata


# function to merge census geographic and population data and calculate population density
def merge_geo_pop_data( tractdata, popdata, citylimits ):
	""" 
	merges geographic and population data by tract from the 2020 census
	"""

	mergeddata = tractdata.merge(popdata, on='geo_id' )

	# add population density columns
	mergeddata['popdense_landarea'] = mergeddata['population']/mergeddata['land_area']
	mergeddata['popdense_totalarea'] = mergeddata['population']/(mergeddata['land_area'] + mergeddata['water_area'])

	#     # only keep data within chosen city limits
	#     is_incitylimits = mergeddata['geometry'].map(lambda x: citylimits['geometry'].intersects( x ).any() )
	#     mergeddata = mergeddata.loc[is_incitylimits]

	# remove tracts with less than a certain # of residents
	pop_thresh = 200
	mergeddata = mergeddata.loc[ mergeddata['population'] > pop_thresh ]

	return mergeddata