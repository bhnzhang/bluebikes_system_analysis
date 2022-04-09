# script to automatically ping and download bluebikes station data on a recurring basis

# dependencies -------------------

# for getting json data from url
import urllib.request, json

# for time string manipulation
import datetime

# for scheduling repeated events
import sched, time

import os

# ------------------------
# function definitions

# grab station data every refresh_t seconds
def grab_station_data(sc, refresh_t, save_path): 
    """
    inputs:
        sc
            type: scheduler object
        refresh_t
            type: int or float
            desc: refresh time in seconds
        save_path
            type: str
            desc: path to save station data to
    """

    # load data
    with urllib.request.urlopen("https://gbfs.bluebikes.com/gbfs/en/station_status.json") as url:
        data = json.loads(url.read().decode())

    # get the timestamp in human readable format
    datetime_str = datetime.datetime.fromtimestamp(data['last_updated']).strftime('%Y_%m_%d_%H_%M_%S')
    # datetime_str  = datetime_time.strftime('%Y_%m_%d_%H_%M_%S')

    # save to file
    with open( save_path + os.sep + datetime_str + '.json', 'w', encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False, indent=4)

    # logging
    print("Saving data for time stamp " + datetime_str)
    
    # schedule the next execution
    s.enter(refresh_t, 1, grab_station_data, (sc,))

# end def grab_station_data()


# main -------------------

# set refresh time in seconds
refresh_t = 5*60 

# set directory to save data
# save_path = 'G:\\My Drive\\Personal projects\\bluebikes\\station data'
save_path = 'D:\\Google Drive\\Personal projects\\bluebikes\\station data'

# make scheduler object
s = sched.scheduler(time.time, time.sleep)

# schedule the first execution
s.enter(0, 1, grab_station_data, (s,refresh_t,save_path))

# run continuously
s.run()


