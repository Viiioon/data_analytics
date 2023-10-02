# Libraries
import os
import requests
import json
import folium
from pandas import json_normalize
import os
import platform
import socket
from platform import python_version
from datetime import datetime

# Ignore warnings
import warnings
warnings.filterwarnings("ignore")

# Show current working directory
print(os.getcwd())

# Overpass API URL
url = 'http://overpass-api.de/api/interpreter'

# Overpass turbo query
query = f"""
        [out:json];
        area["ISO3166-1"="CH"][admin_level=2];
        node ["shop"="supermarket"](area);
        out;"""

# Web API request
r = requests.get(url, params={'data': query})
data = r.json()['elements']

# Save data to file
with open('supermarkets.json', 'w') as json_file:
    json.dump(data, json_file)

# Store data in data frame
df = json_normalize(data)

# Number of rows and columns
print(df.shape)

# First rows
df.head()

# Subset of supermarkets by brand
locations = df[["lat", "lon", "tags.brand", "tags.shop"]].loc[df["tags.brand"].isin(['Migros', 'Coop'])]
print(locations.head(5))

# Create map
map = folium.Map(location=[locations.lat.mean(), 
                           locations.lon.mean()], 
                 zoom_start=8, 
                 control_scale=True)

# Add maker symbols
for index, location_info in locations.iterrows():
    folium.Marker([location_info["lat"], 
                   location_info["lon"]], 
                  popup=location_info["tags.brand"]).add_to(map)

# Plot map
map

print('-----------------------------------')
print(os.name.upper())
print(platform.system(), '|', platform.release())
print('Datetime:', datetime.now().strftime("%Y-%m-%d %H:%M:%S"))
print('Python Version:', python_version())
print('-----------------------------------')