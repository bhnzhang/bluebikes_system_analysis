"""
Loading the station information and charting coordinates
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

# ----------------------------
# dependencies

# for loading station information
from data_handling.data_loading_methods import load_station_info

# matplotlib
import matplotlib.pyplot as plt

# ----------------------------
# main

if __name__ == '__main__':

	station_info_df = load_station_info()

	print(station_info_df)
	print(station_info_df.columns)

	# plot lat and long
	station_info_df.plot.scatter(x='lon', y='lat')
	plt.show()