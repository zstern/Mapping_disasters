from flask import render_template, flash, redirect, url_for, request
from app import app
from app.forms import AddressForm, PhotoForm, SurveyForm
from app.functions import get_coordinates, latlong_to_address, zillow_pull
from geopy import geocoders
import zillow
import os
import requests
import re
import exifread

# ...
bing_key = ''
zillow_key = ''
google_key = ''

@app.route('/')

#    return render_template('index.html', title='Submit Photo', form=form)
@app.route('/index', methods=['GET', 'POST'])
def photoaddress():
    form = PhotoForm(csrf_enabled = False)

    if form.validate_on_submit():
        photo = form.photo.data

        filename = photo.filename.replace(' ', '')

        basepath = os.path.abspath('app/')

        photo.save(f'/{basepath}/uploads/{filename}')

        # run lat_long / heading function, streetview function, and zillow function

        address = latlong_to_address(f'{basepath}/uploads/{filename}')

        # assign all to database
        price = zillow_pull(address)
        address = address['name']

        # Set image_url to Google Street View of address
        # I don't know how this will need to be saved / returned for use in Flask

## CHANGE THIS TO GET COORDS AND HEADING FOR CORRECT IMAGE
        coords = get_coordinates(f'{basepath}/uploads/{filename}')

        heading = coords[1]
        coords = coords[0]

        image_url = f'https://maps.googleapis.com/maps/api/streetview?size=600x600&location={coords[0]}, {coords[1]}&heading={heading}&key={google_key}'
## CHANGE CHANGE CHANGE

        # Put image handling code for Flask here
        image = requests.get(image_url)

        filelist = re.findall(r'\w+', address)
        filename2 = ''.join(filelist)
        final_path = f'{basepath}/uploads/{filename2}.jpg'
        open(f'{final_path}', 'wb').write(image.content)

        # return render_template to photo_form page
        return redirect(url_for('surveyform', price = price, address = address, goog_photo = f'{filename2}.jpg', filename = filename))
        # return render_template('photo_form.html', form=SurveyForm(), filename = filename, address = address, price = price, goog_photo = f'{filename2}.jpg')

    return render_template('index.html', form=form)


@app.route('/textaddress', methods=['GET', 'POST'])
def textaddress():
    form = AddressForm()


    if form.validate_on_submit():
        # flash('Login requested for user {}'.format(form.address.data))

        address = form.address.data

        bing_key = ''
        bing_locator = geocoders.Bing(bing_key)
        address = bing_locator.geocode(address).raw

        zillow_key = ''
        zillow_api = zillow.ValuationApi()
        house = address['address']['addressLine']
        postal_code = address['address']['postalCode']

        house_data = zillow_api.GetSearchResults(zillow_key, house, postal_code)
        price = house_data.zestimate.amount
        address = address['name']

        google_key = ''



        ### START GOOGLE STREET VIEW IMAGE HANDLING ###

        # Set image_url to Google Street View of address
        # I don't know how this will need to be saved / returned for use in Flask
        image_url = f'https://maps.googleapis.com/maps/api/streetview?size=600x600&location={address}&key={google_key}'

        # Put image handling code for Flask here
        image = requests.get(image_url)

        basepath = os.path.abspath('app/')
        filelist = re.findall(r'\w+', address)
        filename = ''.join(filelist)
        final_path = f'{basepath}/uploads/{filename}.jpg'
        open(f'{final_path}', 'wb').write(image.content)



        return render_template('text_form.html', title = 'Output', price = price, file_path = f'{filename}.jpg', photo = open(f'{final_path}', 'rb'))

        # return redirect('/textaddress')

    return render_template('textaddress.html', title='Submit Address', form=form)

# not routing here...
@app.route('/photo_form', methods=['GET', 'POST'])
def surveyform():

    form = SurveyForm(csrf_enabled = False)

    if form.validate_on_submit():
        dropdown = form.dropdown.data
        multiple = form.multiple.data
        single = form.singletext.data
        # print(dropdown)

        # return redirect(url_for('testformresponse', dropdown = dropdown, single = single))

        return render_template('testformresponse.html', dropdown = dropdown, single = single, multiple = multiple) # singletext = singletext) #, multiple = multiple)

    return render_template('photo_form.html', form=form, price = request.args.get('price'), address = request.args.get('address'), goog_photo = request.args.get('goog_photo'), filename = request.args.get('filename'))

#@app.route('/testformresponse', methods=['GET', 'POST'])
#def testformresponse():
#    return render_template('testformresponse.html', dropdown = request.args.get('dropdown'), single = request.arges.get('single'), 302)

#@app.route('/text_form', methods=['GET', 'POST'])
#def photo():
#    photo = open(f'/Users/nickgayliard/Desktop/DSI/project-4-team-street/code/flask_app/app/{final_path}', 'rb')
