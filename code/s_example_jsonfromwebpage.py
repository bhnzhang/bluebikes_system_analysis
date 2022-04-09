# example code showing how to load in a json file from a webpage

import urllib.request, json 

# load data
with urllib.request.urlopen("https://gbfs.bluebikes.com/gbfs/en/station_status.json") as url:
    data = json.loads(url.read().decode())
    print(data)

# save to file
with open('data.json', 'w', encoding='utf-8') as f:
    json.dump(data, f, ensure_ascii=False, indent=4)