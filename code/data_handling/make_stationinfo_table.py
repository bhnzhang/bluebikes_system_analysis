# load station data and make a table in postgre

# dependencies -------------------

# postgresql
import psycopg2
from psycopg2.extensions import AsIs

# for getting json file from url
import urllib.request

# json
import json

# numpy
import numpy as np

# main -------------------

# load station information data
with urllib.request.urlopen("https://gbfs.bluebikes.com/gbfs/en/station_information.json") as url:
    station_info = json.loads(url.read().decode())

# print(station_info)

station_info = station_info['data']['stations']

# print(station_info)

# for station in station_info:
# 	print(station)

station0 = station_info[0]

print(station0.keys())

# i'm just gonna make a list of the keys that i want to save
keys_to_save = [ 'name', 'legacy_id', 'lat', 
				'lon', 'short_name', 
				'station_id', 
				'capacity', 'region_id'
				]

datatypes = [ 'varchar', 'varchar', 'float8', 
			  'float8', 'varchar', 
			  'varchar', 
			  'int', 'varchar' ]

# combine together
keys_datatypes = [ i + ' ' + j for i,j in zip(keys_to_save, datatypes)]

print(keys_datatypes)
print(','.join(keys_datatypes))

# Connect to an existing database
conn = psycopg2.connect("dbname=mydb user=postgres password=temppwpwpw")

# Open a cursor to perform database operations
cur = conn.cursor()

# create new table
# print( cur.mogrify( "CREATE TABLE test (%s);", (','.join(keys_datatypes)) ) )
# cur.execute( "CREATE TABLE station_info (name varchar,legacy_id varchar,lat float8,lon float8,short_name varchar,station_id varchar,capacity int,region_id varchar);")

# make changes persistent
# conn.commit()

# add the station info to this table
for station in station_info:

	# grab data for the keys i wanted
	data = [station[k] for k in keys_to_save]

	# add to database
	insert_statement = 'insert into station_info (%s) values %s'
	cur.execute(insert_statement, (AsIs(','.join(keys_to_save)), tuple(data) ) )

	# commit changes
	conn.commit()


# Close communication with the database
cur.close()
conn.close()