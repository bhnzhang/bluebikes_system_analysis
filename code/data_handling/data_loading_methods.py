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