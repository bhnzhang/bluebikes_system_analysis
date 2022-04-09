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

# pre-main ---------------

# init a pretty printer object
pp = pprint.PrettyPrinter(indent=4)

# main -------------------

# file to load
filetoload = 'U:\\bluebikes\\station data 220403 1319\\alldata.csv'
# filetoload = 'U:\\bluebikes\\station data cropped\\alldata.csv'

alldata_df = pd.read_csv(filetoload, index_col=0)

print(alldata_df.head(5))

print(alldata_df.columns)

# list of columns to remove
columns_to_remove = [ 'num_ebikes_available', 'eightd_has_available_keys', 
				  	'legacy_id_x', 'external_id', 'electric_bike_surcharge_waiver',
				  	'legacy_id_y', 'eightd_station_services', 'short_name', 'station_type',
				  	'rental_methods', 'has_kiosk', 'eightd_has_key_dispenser']

alldata_df.drop( columns_to_remove, inplace=True, axis=1, errors='ignore')

print(alldata_df)
print(alldata_df.columns)

# save
alldata_df.to_csv(filetoload, index=False)
