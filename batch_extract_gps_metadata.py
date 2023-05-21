#!/usr/bin/env python3

"""
Extracts GPS metadata from images and writes coordinates to a file
"""


import os
from PIL import Image
from PIL.ExifTags import GPSTAGS, TAGS 

def get_geotagging(exif):
    if not exif:
        raise ValueError("No EXIF metadata found")

    geotagging = {}
    for (idx, tag) in TAGS.items():
        if tag == 'GPSInfo':
            if idx not in exif:
                raise ValueError("No EXIF geotagging found")

            for (t, value) in GPSTAGS.items():
                if t in exif[idx]:
                    geotagging[value] = exif[idx][t]

    return geotagging

def get_decimal_from_dms(dms, ref):
    degrees = dms[0]
    minutes = dms[1] / 60.0
    seconds = dms[2] / 3600.0

    if ref in ['S', 'W']:
        degrees = -degrees
        minutes = -minutes
        seconds = -seconds

    return round(degrees + minutes + seconds, 5)

def get_coordinates(geotags):
    lat = get_decimal_from_dms(geotags['GPSLatitude'], geotags['GPSLatitudeRef'])
    lon = get_decimal_from_dms(geotags['GPSLongitude'], geotags['GPSLongitudeRef'])

    return (lat,lon)

def write_to_file(file_path, coordinates, image_name):
    with open(file_path, 'a') as f:
        f.write(f'{image_name}: {coordinates[0]}, {coordinates[1]}\n')

def process_images(directory):
    filenames = sorted(os.listdir(directory))
    for filename in filenames:
        if filename.endswith(".jpg") or filename.endswith(".jpeg"):
            img_path = os.path.join(directory, filename)
            image = Image.open(img_path)
            exif = image._getexif()
            geotagging = get_geotagging(exif)
            coordinates = get_coordinates(geotagging)
            write_to_file('gps_data.txt', coordinates, filename)

process_images('/etc/photodirectory')  # replace this with your directory