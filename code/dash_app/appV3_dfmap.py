import datetime
import dash
from dash.dependencies import Input, Output, State
import dash_core_components as dcc
import dash_html_components as html
import dash_table

from geopy import geocoders
import exifread
import requests
import re
import os
import base64
from IPython.display import Image
import folium
from folium import IFrame
import pandas as pd
import numpy as np

#import Map_from_df_fin

df = pd.read_csv('../csvs/add_data1')

app = dash.Dash(__name__)

# app.layout = dash_table.DataTable(
#     id='table',
#     columns=[{"name": i, "id": i} for i in df.columns],
#     data=df.to_dict("rows"),
# )


app.layout = html.Div([
    html.H1("Photo Mapper"),
        dcc.Upload(
            id='upload-image',
            children=html.Div([
                'Drag and Drop or ',
                html.A('Select Files')
            ]),
            style={
                'width': '100%',
                'height': '60px',
                'lineHeight': '60px',
                'borderWidth': '1px',
                'borderStyle': 'dashed',
                'borderRadius': '5px',
                'textAlign': 'center',
                'margin': '10px'
            },
            # Allow multiple files to be uploaded
            multiple=True
        ),
        html.Iframe(srcDoc=open('./multi_map_200.html','r').read(),width ='75%',height = '800'),
        html.Div(id='output-image-upload'),
        dash_table.DataTable(
        id='table',
        columns=[{"name": i, "id": i} for i in df.columns],
        data=df.to_dict("rows"),
    ),

    #html.Iframe(srcDoc=open('multi_map_100.html','r').read(),width ='50%',height = '600'))



])




if __name__ == '__main__':
    app.run_server(debug=True)
