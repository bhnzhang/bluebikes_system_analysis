# want to try loading some data and doing some simple manipulation
# probably load all the json files and grab the info for one of the stations

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

print(commave_station_capacity)

# load from npz file
# filepath    = 'C:\\Users\\beezy\\Desktop\\station data\\'
filepath    = 'G:\\My Drive\\Personal projects\\bluebikes\\station data\\numpy\\'
filename    = 'data_220217_2250.npz'
data        = np.load( filepath + filename )

timestamps          = data['timestamps']  # epoch time
capacity_vs_time    = data['capacity_vs_time']

# plt.show()

avg_capacity = np.mean(capacity_vs_time)
print(avg_capacity)

std_dev = np.std(capacity_vs_time)
print(std_dev)

# # use datetime class to initialize a datetime object using epoch time
# # grab the hour from that object
# dt_obj = datetime.datetime.fromtimestamp(timestamps[0])
# print(dt_obj.hour)

# convert timestamp in epoch to hour of day, and day of week
hour_vec    = np.asarray([ datetime.datetime.fromtimestamp(t).hour for t in timestamps ])
day_vec     = np.asarray([ datetime.datetime.fromtimestamp(t).weekday() for t in timestamps ])
# print(day_vec)

# grab data between specific hourly range

# pick hourly range and get indexing vector
min_hour    = 3
max_hour    = 4
day_to_plot = 0 # 0 = monday, 6 = sunday
indx_myhourrange = ( min_hour <= hour_vec ) & ( max_hour > hour_vec ) # boolean vector for indexing hourly data in desired range
indx_mydaytoplot = day_to_plot == day_vec
indx_myhourandday = indx_myhourrange & indx_mydaytoplot
# print(len(indx_myhourrange))

# grab data 
hour_vec_inrange = hour_vec[indx_myhourandday]
capacity_inrange = capacity_vs_time[indx_myhourandday]
# print(hour_vec_inrange)


# plot all data
plt.figure(0)
plt.plot( timestamps, capacity_vs_time, '.' )
plt.title('capacity over time for griggs st station')
plt.xlabel("time")
plt.ylabel("capacity (bikes/total docks)")

# plot data in range selected
plt.plot( timestamps[indx_myhourandday], capacity_inrange, '.' )

# replace x labels with human readable time stamps
locs, labels    = plt.xticks() # get current locations and labels
datetime_strs   = [ datetime.datetime.fromtimestamp(t).strftime('%Y %m %d %H %M %S') for t in locs ]
plt.xticks(locs, datetime_strs, rotation=70)
plt.tight_layout() # to make sure bottom margin shows the xlabels

# plt.show(block=True)


# collect data in buckets for each hour of the day
# only look at weekdays
# take average of each of those buckets
avg_cap_vs_hour = np.empty( 24 )
std_cap_vs_hour = np.empty( 24 )
hours           = range(24)
for hour in hours:
    # for each hour

    # grab data 
    capacity_inrange = capacity_vs_time[( hour <= hour_vec ) & ( hour+1 > hour_vec )]

    # calculate average and std of capacity data in that range
    avg_cap_vs_hour[hour] = np.mean(capacity_inrange)
    std_cap_vs_hour[hour] = np.std(capacity_inrange)

# end for hour in range()


# plot average capacity per hour across entire dataset
plt.figure(1)
plt.plot( hours, avg_cap_vs_hour, '.' )
plt.title('Average capacity per hour')
plt.xlabel("hour of day")
plt.ylabel("average capacity (bikes/total docks)")

# plot std of capacity per hour across entire dataset
plt.figure(2)
plt.plot( hours, std_cap_vs_hour, '.' )
plt.title('Standard deviation of capacity per hour')
plt.xlabel("hour of day")
plt.ylabel("std of capacity (bikes/total docks)")


# test - count every time the station is between certain range of capacity
# do this for all range of capacities, plot histogram
center_capacity     = 0.5
capacity_range      = 0.1
indx_capwithinrange =   ( capacity_vs_time >= (center_capacity - capacity_range/2) ) & \
                        ( capacity_vs_time < (center_capacity + capacity_range/2) )

# debug, plotting when capacity is within chosen range
plt.figure(3)
plt.plot( timestamps, capacity_vs_time, '.' )
plt.plot( timestamps[indx_capwithinrange], capacity_vs_time[indx_capwithinrange], '.' )
plt.title('capacity over time for griggs st station')
plt.xlabel("time")
plt.ylabel("capacity (bikes/total docks)")

# debug, count # of trues
print(np.count_nonzero([ True, True, False ]))
print(np.count_nonzero(indx_capwithinrange))

# count all instances of capacity within each range percentile
percentile_range            = 1.0/commave_station_capacity
# center_percentiles           = np.linspace(0, 1.0, num=11)
center_percentiles          = np.arange(0, 1.01, percentile_range)
num_cap_within_percentiles  = np.empty( center_percentiles.size )

for i_percent in range( len(center_percentiles) ):
    # for each percentile

    # count # of instances and save
    num_cap_within_percentiles[i_percent] = np.count_nonzero( ( capacity_vs_time > (center_percentiles[i_percent] - percentile_range/2) ) & \
                                                              ( capacity_vs_time < (center_percentiles[i_percent] + percentile_range/2) ) )
# end for i_percent

print(num_cap_within_percentiles)

# close all other figures
plt.close('all')

# plot histogram of capacity
plt.figure()
plt.bar( center_percentiles, num_cap_within_percentiles, width = percentile_range )
plt.title('Histogram of timestamps spent in each capacity percentile')
plt.xlabel("Capacity percentile")
plt.ylabel("Counts within capacity percentile")


# given a certain percentile range, count the occurances spent in that percentile range
# as a function of hour of day
center_percentiles      = [ 0.0, 6.0/15, 12.0/15 ]

counts_perhour_perpercentile = np.empty( ( 24, len(center_percentiles) ) )

for i_percentile in range(len(center_percentiles)):
    # for each selected percentile range

    # get the occurances when the station is in that percentile range 
    indx_inpercentile_range =   ( capacity_vs_time > (center_percentiles[i_percentile] - percentile_range/2) ) & \
                                ( capacity_vs_time < (center_percentiles[i_percentile] + percentile_range/2) )

    # get the hours for each of those occurances
    hour_vec_inpercentile_range = hour_vec[indx_inpercentile_range]

    # counting the occurances per hour
    counts_perhour_perpercentile[:,i_percentile] = [  np.count_nonzero( (hour_vec_inpercentile_range >= i_hour) \
                                                        & (hour_vec_inpercentile_range < i_hour+1) ) \
                                                        for i_hour in range(24) ] 

# end for i_percentile...

# # plot histogram of capacity
# plt.figure()
# plt.bar( range(24), counts_perhour_perpercentile[:,2], width = 0.8 )
# plt.title('Histogram of timestamps per hour spent at zero capacity')
# plt.xlabel("Hour")
# plt.ylabel("Counts")

# use subplots to plot our count data
f, (ax1, ax2, ax3) = plt.subplots(1, 3, sharey=True)
ax1.bar( range(24), counts_perhour_perpercentile[:,0], width = 0.8 )
ax1.set_title('0 capacity')
ax2.bar( range(24), counts_perhour_perpercentile[:,1], width = 0.8 )
ax2.set_title( str(center_percentiles[1]) + ' capacity')
ax3.bar( range(24), counts_perhour_perpercentile[:,2], width = 0.8 )
ax3.set_title( str(center_percentiles[2]) + ' capacity')


# capture all the instances when the station capacity is between 0 and 1/3rd
# from those instances, count # of instances versus hour of day
counts_perhour_perrange = np.empty( ( 24, 3 ) )
for i_range in range(3):

    # get instances when station is in range
    indx_inpercentile_range =   ( capacity_vs_time >= i_range * 1.0/3.0 ) & \
                                ( capacity_vs_time < (i_range+1) * 1.0/3.0 )

    # get the hours for each of those occurances
    hour_vec_inpercentile_range = hour_vec[ indx_inpercentile_range ]

    # counting the occurances per hour
    counts_perhour_perrange[:,i_range] = [  np.count_nonzero( (hour_vec_inpercentile_range >= i_hour) \
                                                        & (hour_vec_inpercentile_range < i_hour+1) ) \
                                                        for i_hour in range(24) ] 

# plot histogram of counts versus hour of day when station is b/w 0 and 1/3rd full
f, (ax1, ax2, ax3) = plt.subplots(1, 3, sharey=True)
ax1.bar( range(24), counts_perhour_perrange[:,0], width = 0.8 )
ax1.set_title('0 to 1/3rd capacity')
ax2.bar( range(24), counts_perhour_perrange[:,1], width = 0.8 )
ax2.set_title('1/3rd to 2/3rd capacity')
ax3.bar( range(24), counts_perhour_perrange[:,2], width = 0.8 )
ax3.set_title('2/3rd to 1 capacity')


# leave plot showing for last
plt.show()
