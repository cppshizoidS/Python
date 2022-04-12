import pandas as pd
import numpy as np
import plotly.offline as py
import plotly.graph_objs as go
import json

py.init_notebook_mode(connected=False)

izip = zip

df = pd.read_csv('https://raw.githubusercontent.com/plotly/datasets/master/globe_contours.csv')
df.head()

contours = []

scl = ['rgb(213,62,79)', 'rgb(244,109,67)', 'rgb(253,174,97)', \
       'rgb(254,224,139)', 'rgb(255,255,191)', 'rgb(230,245,152)', \
       'rgb(171,221,164)', 'rgb(102,194,165)', 'rgb(50,136,189)']


def pairwise(iterable):
    a = iter(iterable)
    return izip(a, a)


i = 0
for lat, lon in pairwise(df.columns):
    contours.append(dict(
        type='scattergeo',
        lon=df[lon],
        lat=df[lat],
        mode='lines',
        line=dict(
            width=2,
            color=scl[i]
        )
    ))
    i = 0 if i + 1 >= len(df.columns) / 4 else i + 1

layout = dict(
    margin=dict(t=0, l=0, r=0, b=0),
    showlegend=False,
    geo=dict(
        showland=True,
        showlakes=True,
        showcountries=True,
        showocean=True,
        countrywidth=0.5,
        landcolor='rgb(230, 145, 56)',
        lakecolor='rgb(0, 255, 255)',
        oceancolor='rgb(0, 255, 255)',
        projection=dict(
            type='orthographic',
            rotation=dict(lon=0, lat=0, roll=0)
        ),
        lonaxis=dict(
            showgrid=True,
            gridcolor='rgb(102, 102, 102)',
            gridwidth=0.5
        ),
        lataxis=dict(
            showgrid=True,
            gridcolor='rgb(102, 102, 102)',
            gridwidth=0.5
        )
    )
)

sliders = []

lon_range = np.arange(-180, 180, 10)
lat_range = np.arange(-90, 90, 10)

sliders.append(
    dict(
        active=len(lon_range) / 2,
        currentvalue={"prefix": "Longitude: "},
        pad={"t": 0},
        steps=[{
            'method': 'relayout',
            'label': str(i),
            'args': ['geo.projection.rotation.lon', i]} for i in lon_range]
    )
)

sliders.append(
    dict(
        active=len(lat_range) / 2,
        currentvalue={"prefix": "Latitude: "},
        pad={"t": 100},
        steps=[{
            'method': 'relayout',
            'label': str(i),
            'args': ['geo.projection.rotation.lat', i]} for i in lat_range]
    )
)

projections = ["equirectangular", "mercator", "orthographic", "natural earth", "kavrayskiy7",
               "miller", "robinson", "eckert4", "azimuthal equal area", "azimuthal equidistant",
               "conic equal area", "conic conformal", "conic equidistant", "gnomonic", "stereographic",
               "mollweide", "hammer", "transverse mercator", "albers usa", "winkel tripel"]

buttons = [dict(args=['geo.projection.type', p], label=p, method='relayout') for p in projections]

annot = list([dict(x=0.1, y=0.8, text='Projection', yanchor='bottom',
                   xref='paper', xanchor='right', showarrow=False)])

# Update Layout Object

layout['updatemenus'] = list([dict(x=0.1, y=0.8, buttons=buttons, yanchor='top')])

layout['annotations'] = annot

layout['sliders'] = sliders
fig = dict(data=contours, layout=layout)
py.iplot(fig)
