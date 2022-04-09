# load all json information
# save all information to a numpy data file for quicker loading

# dependencies -------------------

# for getting json data from url
import urllib.request, json

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

# main -------------------

# load station information data
with urllib.request.urlopen("https://gbfs.bluebikes.com/gbfs/en/station_information.json") as url:
    station_info = json.loads(url.read().decode())

# comm ave griggs st station
indx_commavegriggs          = 57
commave_station_info        = station_info['data']['stations'][indx_commavegriggs]
commave_station_capacity    = commave_station_info['capacity']

# load all json files
basepath1	= 'C:\\Users\\beezy\\Desktop\\station data\\station data 220217 1012' #G:\\My Drive\\Personal projects\\bluebikes\\station data'
basepath2   = 'D:\\Google Drive\\Personal projects\\bluebikes\\station data'
if isdir(basepath1):
    basepath = basepath1
else:
    basepath = basepath2
onlyfiles 	= [ f for f in listdir(basepath) if isfile(join(basepath, f)) and 'json' in f ]

# i want to
# load all the json files
# in each json file i want to read the status for the griggs st dock
# then i want to save basically... capacity over time.

# init numpy arrays
capacity_vs_time = np.empty( len(onlyfiles) )
timestamps       = np.empty( len(onlyfiles) )

allstation_data = []

print('loading station data...')
# i_file = 0
for fname, i_file in zip( onlyfiles, range(len(onlyfiles)) ):

    # load json
    with open( basepath + os.sep + fname ) as f_opened:
        this_entry = json.load(f_opened)

    # grab data for this file
    allstation_data.append( this_entry['data'] )

    # grab # of bikes available
    this_station_data   = this_entry['data']['stations'][indx_commavegriggs]
    n_docks_avail       = this_station_data['num_docks_available']
    n_bikes_avail       = this_station_data['num_bikes_available']

    capacity_vs_time[i_file] = n_bikes_avail/commave_station_capacity
    timestamps[i_file]       = this_entry['last_updated'] # in epoch time

    # pdb.set_trace()
    # i_file += 1
    if i_file % 100 == 99:
        print( 'file ' + str(i_file) + ' of ' + str(len(onlyfiles)) )

# end for loop
print('...done')

# pdb.set_trace()

# plot data
plt.plot( timestamps, capacity_vs_time, '.' )
plt.title('capacity over time for griggs st station')
plt.xlabel("time")
plt.ylabel("capacity (bikes/total docks)")

# replace x labels with human readable time stamps
locs, labels    = plt.xticks() # get current locations and labels
datetime_strs   = [ datetime.datetime.fromtimestamp(t).strftime('%Y %m %d %H %M %S') for t in locs ]
plt.xticks(locs, datetime_strs, rotation=70)
plt.tight_layout() # to make sure bottom margin shows the xlabels

plt.show()

# save data to numpy binary
# save_filename = 'C:\\Users\\beezy\\Desktop\\station data\\data_220212_2254'
# save_filename = os.path.abspath('C:\\Users\\beezy\\Desktop\\station data\\station data 220217 1012\\data_220217_2250')
save_filename = os.path.abspath('C:\\Users\\beezy\\Desktop\\station data\\station data 220217 1012\\data_allstations_220217_2250')

# np.savez(save_filename, timestamps=timestamps, capacity_vs_time=capacity_vs_time)
np.save(save_filename, allstation_data=allstation_data)