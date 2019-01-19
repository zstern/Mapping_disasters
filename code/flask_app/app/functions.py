from flask import render_template, flash, redirect, url_for
from app import app
from app.forms import AddressForm, PhotoForm, SurveyForm
from geopy import geocoders
import zillow
import os
import requests
import re
import exifread

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

    return [(lat_coord, lng_coord), heading]



def latlong_to_address(img_path_str):
# run get_coordinates function for lat, long
    coords = get_coordinates(img_path_str)[0]

    bing_key = ''

#instantiate bing geocoder
    bing_locator = geocoders.Bing(bing_key)

    address = bing_locator.reverse(coords).raw

    # street_address = address['address']['addressLine']

    return address



def zillow_pull(address):
    zillow_api = zillow.ValuationApi()
    zillow_key = ''

    # get house and postal code info from dictionary
    house = address['address']['addressLine']
    postal_code = address['address']['postalCode']

    # Grab Zillow price and set to price variable
    try:
        house_data = zillow_api.GetSearchResults(zillow_key, house, postal_code)
        price = house_data.zestimate.amount

    except:
        price = 'Zillow does not have price for this address'

# Error handling if Zillow has no price output
    if price == None:
        price = 'This address does not have a price estimate in Zillow'

    return price
