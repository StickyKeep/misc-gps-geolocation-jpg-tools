#!/usr/bin/env python3

"""
Reads a list of GPS coordinates from text file and plots them on a map.

"""

import folium

# Initialize map centered at average location
m = folium.Map(location=[40.002, -99.999], zoom_start=13) 

# Here text file is formatted as imagename.jpg: X-coord, Y-coord
with open('gps_data.txt', 'r') as f:
    for line in f:
        image_name, coordinates = line.strip().split(':')
        lat, lon = map(float, coordinates.split(','))
        folium.Marker([lat, lon], popup=image_name).add_to(m)

m.save('map.html')
