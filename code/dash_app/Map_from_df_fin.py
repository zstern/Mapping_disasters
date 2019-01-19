#!/usr/bin/env python
# coding: utf-8

# In[11]:


# !pip install ExifRead


# In[12]:


import exifread

import requests
import re

import os
import pandas as pd
import numpy as np
from geopy import geocoders
import folium
from folium import IFrame
import base64

from IPython.display import Image
import zillow

import time

# In[13]:


#use this folder to input photos '../images/Test_exif_pics/'


# In[31]:


def files_to_process():
    """List the files in the upload directory."""
    img_files = []


    for filename in os.listdir('./uploads/'):
        path = os.path.join('./uploads/', filename)
        if os.path.isfile(path):
            img_files.append(f'./uploads/{filename}')
    for file in img_files:
        if '.DS' in file:
            img_files.remove(file)

    return img_files


# In[32]:


files_to_process()


# In[33]:


#taken from repo documentation:
def get_coordinates(filepath_str):


    f = open(filepath_str, 'rb')

    # Return Exif tags
    tags = exifread.process_file(f)

    lng_ref_tag_name = "GPS GPSLongitudeRef"
    lng_tag_name = "GPS GPSLongitude"
    lat_ref_tag_name = "GPS GPSLatitudeRef"
    lat_tag_name = "GPS GPSLatitude"

    # Check if these tags are present
    gps_tags = [lng_ref_tag_name,lng_tag_name,lat_tag_name,lat_tag_name]
    for tag in gps_tags:
        if not tag in tags.keys():
            print ("Skipping file. Tag {} not present.".format(tag))
            return None

    convert = lambda ratio: float(ratio.num)/float(ratio.den)

    lng_ref_val = tags[lng_ref_tag_name].values
    lng_coord_val = [convert(c) for c in tags[lng_tag_name].values]

    lat_ref_val = tags[lat_ref_tag_name].values
    lat_coord_val = [convert(c) for c in tags[lat_tag_name].values]

    lng_coord = sum([c/60**i for i,c in enumerate(lng_coord_val)])
    lng_coord *= (-1)**(lng_ref_val=="W")

    lat_coord = sum([c/60**i for i,c in enumerate(lat_coord_val)])
    lat_coord *= (-1)**(lat_ref_val=="S")

    heading = tags['GPS GPSImgDirection'].values[0].num / tags['GPS GPSImgDirection'].values[0].den
    return (lat_coord, lng_coord, heading)


# In[34]:


def image_return(img_list):
    houses = []
    for img in img_list:
        house = {}
        coords = get_coordinates(img)
        address = f'+{coords[0]},{coords[1]}'
        heading = coords[2]
        g_key = ''
        url = f'https://maps.googleapis.com/maps/api/streetview?size=300x600&location={address}&heading={heading}&{g_key}'
        img = requests.get(url)
        filelist = re.findall(r'\w+', address)
        filename = ''.join(filelist)
        final_path = f'./SVphotos//{filename}.jpg'
        open(final_path, 'wb').write(img.content)
        house['street_view'] = final_path
        house['Lat'] = coords[0]
        house['Lon'] = coords[1]
        house['heading'] = heading
        houses.append(house)

    return houses


# In[35]:


def latlong_to_address(img_list):
    # run get_coordinates function for lat, long
    addresses = []
    bing_key = ''
    zillow_key = ''
    zillow_api = zillow.ValuationApi()

    for img in img_list:
        #get address from Lat/lon
        coords = get_coordinates(img)


        #instantiate bing geocoder
        bing_locator = geocoders.Bing(bing_key)

        address = bing_locator.reverse(coords).raw
        street_address = address['name']
        house = address['address']['addressLine']
        postal_code = address['address']['postalCode']
        #zillow api call
        try:
            house_data = zillow_api.GetSearchResults(zillow_key, house, postal_code)
            price = house_data.zestimate.amount
        except:
            price='$__'


        addresses.append(f'{street_address}: ${price}')
        time.sleep(.5)
    return addresses


def map_objects():
    map = folium.Map(tiles='Stamen Toner', location=[df['Lat'][0], df['Lon'][0]], zoom_start=10,)
    for lat,lon,sv_photo,address in zip(df['Lat'],df['Lon'],df['street_view'],df['address_price']):


        encoded = base64.b64encode(open(sv_photo, 'rb').read()).decode()

        #zillow = f'{address}: $$$'

        html = '<img src="data:image/jpeg;base64,{}" >'.format
        resolution, width, height = 75, 50, 25
        iframe = IFrame(html(encoded), width=300, height=600)
        popup = folium.Popup(iframe, max_width=1000)
        icon = folium.Icon(color="red", icon="home")
        marker = folium.Marker(location=[lat, lon], popup=popup, icon=icon,tooltip=address)
        marker.add_to(map)

    map.save('multi_map_200.html')

def final_df():
    batch_list = files_to_process()
    if len(batch_list) > 0:

        df = pd.DataFrame(image_return(batch_list))
        df['address_price']=latlong_to_address(batch_list)
        df.to_csv('../csvs/add_data1',index=False)

        return df
    else:
        pass




df = final_df()
map_objects()
