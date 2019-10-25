# -*- coding: utf-8 -*-
"""
Created on Sun Oct 20 12:38:48 2019

@author: Zaghis
"""


import urllib.request
import ssl

import json
import pandas as pd

from bokeh.plotting import figure, ColumnDataSource
from bokeh.tile_providers import get_provider, Vendors

from bokeh.palettes import RdYlBu11 as palette
from bokeh.models import HoverTool, LinearColorMapper, LabelSet
from bokeh.models.widgets import DataTable, TableColumn

from bokeh.layouts import column
from bokeh.application import Application
from bokeh.application.handlers.function import FunctionHandler
from bokeh.server.server import Server


# Header
ssl._create_default_https_context = ssl._create_unverified_context
opener = urllib.request.build_opener()
opener.addheaders = [(
        "User-agent",
        "Mozilla/5.0"
        )
]


# Funzione di conversione di coordinate da WSG84 a ESPG:3857(proiezione Mercatore)
def WGS84_ESPG3857(df, lon = "lon", lat = "lat"):
    
    import numpy as np
    
    k = 6378137
    
    df["x"] = df[lon] * (k * np.pi/180.0)
    df["y"] = np.log(np.tan((90 + df[lat]) * np.pi/360.0)) * k
    
    return df

def KTS_KMH(df, speed = "speed"):
    
    df["speed"] = round(df[speed]*1.852)
    
    return df


# Custruzione della funzione di tracciamento
def tracker(doc):
    source = ColumnDataSource({
                'hex' : [],
                'squak' : [],
                'flight' : [],
                'lat' : [],
                'lon' : [],
                'validposition' : [],
                'altitude' : [],
                "vert_rate" : [],
                "track" : [],
                "validtrack" : [],
                "speed" : [],
                "messages" : [],
                "seen" : [],
                "x" : [],
                "y"  : []
                }
    )
     
    
    # Aggiorno i dati di volo
    def update():
        
        
        # Scarico i dati dell'antenna
        request = opener.open('http://localhost:8080/data.json')
        data = request.read()
        data = data.decode("utf8")
        data = json.loads(data)
        request.close()
        
        db=pd.DataFrame(
                data,
                columns = [
                        'hex',
                        'squak',
                        'flight',
                        'lat',
                        'lon',
                        'validposition',
                        'altitude',
                        "vert_rate",
                        "track",
                        "validtrack",
                        "speed",
                        "messages",
                        "seen"
                        ]
                )
        db = db.fillna('No Data') 
        db = WGS84_ESPG3857(db)
        db = KTS_KMH(db)
        db.head()
            
        n_roll=len(db.index)
        source.stream(
                db.to_dict(orient='list'),
                n_roll
                )
        
    # Richiamo la funzione periodicamente ogni n
    time = 1000 # espresso in ms (1s = 1000s)
    doc.add_periodic_callback(
            update, 
            time
            )     
    
    # Inizializzo API OSM (mappa) 
    p = figure(
            x_range=(-2000000, 6000000), 
            y_range=(-1000000, 7000000),
            x_axis_type="mercator", 
            y_axis_type="mercator",
            sizing_mode='scale_width',
            plot_height = 550,
            plot_width = 1400
            )
    
    tile_provider = get_provider(Vendors.CARTODBPOSITRON)
    p.add_tile(tile_provider)
    
    # Inizializzo stronzate estetiche varie (parte spudaratamente copiata dalla documentazione ufficiale)
    my_hover=HoverTool()
    color_mapper = LinearColorMapper(palette = palette)
    
    my_hover.tooltips = [
            ("hex", "@hex"),
            ("CALL", "@flight"),
            ("velocità (km/h)", "@speed"),
            ("altitudine", "@altitude"),
            ("latitudine", "@lat"),
            ("longitudine", "@lon")
            ]
    labels = LabelSet(
            x = 'x', y = 'y', 
            text = 'flight', 
            x_offset = 5, y_offset = 5, 
            source = source, 
            render_mode = 'canvas',
            background_fill_color='skyblue',
            text_font_size = "8pt"
            )
    
    # Metto gli arei sulla mappa (e le stronzate estetiche agli arei)
    p.circle(
            "x", "y",
            source = source,
            fill_color = dict(
                    field = "altitude",
                    transform = color_mapper
                    ),
            hover_color = "yellow", 
            size = 10, 
            fill_alpha=0.8,
            line_width=0.5
            )
    
    p.add_tools(my_hover)
    p.add_layout(labels)
    
    # DataTable
    columns = [
            TableColumn(field = "hex",title = "HEX"),
            TableColumn(field = "flight",title = "CALL"),
            TableColumn(field = "speed",title = "VELOCITÀ (KM/H)"),
            TableColumn(field = "altitude",title = "ALTITUDINE"),
            TableColumn(field = "lat",title = "LATITUDINE"),
            TableColumn(field = "lon",title = "LONGITUDINE")
            ]
    data_table = DataTable(
            source = source, 
            columns = columns, 
            height = 150,
            width = 1400
            )

    
    # Metto un nome alla mappa
    doc.title = "Air Traffic Control at Home"
    
    # Imposto la mappa e datatable come radice per lo streaming
    doc.add_root(
            column(
                    data_table,
                    p
                    )
            )
    
    
# SERVER CODE
apps = {
        '/': Application(FunctionHandler(tracker))
        }
server = Server(
        apps, 
        port = 1000
        )
server.start()
