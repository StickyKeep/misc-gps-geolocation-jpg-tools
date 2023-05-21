#!/usr/bin/env python3

"""
Extracts metadata from a pictures in a folder, in addition to searching for a specific string
"""


import os
from PIL import Image
from PIL.ExifTags import TAGS 

def get_image_size_in_mb(filepath):
    size_in_bytes = os.path.getsize(filepath)
    size_in_mb = size_in_bytes / (1024 * 1024)
    return round(size_in_mb, 2)

def get_metadata(exif):
    if not exif:
        raise ValueError("No EXIF metadata found")
    
    metadata = {}
    for (idx, tag) in TAGS.items():
        if idx in exif:
            metadata[tag] = exif[idx]
    
    return metadata

def write_to_file(file_path, metadata, image_name, image_size_pixels, image_size_mb):
    with open(file_path, 'a') as f:
        f.write(f'Metadata for image: {image_name}\n')
        f.write(f'Image size (pixels): {image_size_pixels}\n')
        f.write(f'Image size (MB): {image_size_mb}\n')
        for key, val in metadata.items():
            f.write(f'{key}: {val}\n')
        f.write('\n')

def search_for_string(filepath, search_string):
    with open(filepath, 'rb') as f:
        data = f.read()
        if search_string.encode() in data:
            print(f'Found "{search_string}" in {filepath}')

def process_images(directory):
    filenames = sorted(os.listdir(directory))
    for filename in filenames:
        if filename.endswith(".jpg") or filename.endswith(".jpeg"):
            img_path = os.path.join(directory, filename)
            image = Image.open(img_path)
            image_size_pixels = image.size
            image_size_mb = get_image_size_in_mb(img_path)
            exif = image._getexif()
            metadata = get_metadata(exif)
            write_to_file('metadata.txt', metadata, filename, image_size_pixels, image_size_mb)
            search_for_string(img_path, "your_search_string_here") # add search string


process_images('/etc/photodirectory')  # replace this with your directory