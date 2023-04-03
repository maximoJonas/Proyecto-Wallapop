import numpy as np
import pandas as pd

import helium
from selenium import webdriver 
from bs4 import BeautifulSoup

from time import sleep
from datetime import datetime, date, timedelta

import folium
from folium import plugins
from streamlit_folium import st_folium


def crear_venta(Url_Usuario):
    df_usuario_final=pd.read_csv(filepath_or_buffer =r"C:\Users\jonas\python\Proyecto Wallapop\df_final_usu.csv",sep=",")
    df_final=pd.read_csv(filepath_or_buffer =r"C:\Users\jonas\python\Proyecto Wallapop\df_Final.csv",sep=",")
    df_lat_long=pd.read_csv(filepath_or_buffer =r"C:\Users\jonas\python\Proyecto Wallapop\base_datos\listado-codigos-postales-con-LatyLon.csv",sep=";")
    df_compras_pagadas=pd.read_csv(filepath_or_buffer =r"C:\Users\jonas\python\Proyecto Wallapop\df_compras_pagadas.csv",sep=",")



    df_final=df_final[df_final["Url Usuario"].isin(Url_Usuario)]
    df_final["Url Usuario"]=df_final["Url Usuario"].drop_duplicates()

    df_compras=pd.DataFrame()
    lista_lon,lista_lat=list(),list()
    lista_tit,lista_precio=list(),list()

    df_lat_long=df_lat_long[df_lat_long["provincia"].isin(["Pontevedra","Lugo","A Coruña","Ourense"])]


    df_usuario_final=df_usuario_final[df_usuario_final["Ventas totales"].isin(Url_Usuario)]
    df_usuario_final.dropna(inplace=True)


    df_compras["Url Usuario"]=df_usuario_final["Url Usuario"]
    df_compras["C.P."]=df_usuario_final["C.P."]
    df_compras["Nombre de usuario"]=df_usuario_final["Nombre de usuario"]

    

    tit=np.array(df_final[df_final["Url Usuario"]==usu]["Titulos"])[0]
    precio=np.array(df_final[df_final["Url Usuario"]==usu]["Precio"])[0]

    df_compras["Titulos"]=tit
    df_compras["Precio"]=precio
    df_compras["Recogido"]="NO"
    df_compras["fecha"]=date.today()

    for cod  in df_compras["C.P."]:
        cod=cod[1:6]
        lon=float(df_lat_long[df_lat_long["codigopostalid"]==int(cod)]["lon"])

        lat=float(df_lat_long[df_lat_long["codigopostalid"]==int(cod)]["lat"])

    df_compras["lat"]=lat
    df_compras["lon"]=lon

    
    df_compras_pagadas=pd.concat([df_compras_pagadas,df_compras],ignore_index=True)
    df_compras_pagadas.to_csv(r"C:\Users\jonas\python\Proyecto Wallapop\df_compras_pagadas.csv",index=False)

     


def mapa_compras(df):
    
    df.lat=df.lat.astype(float)
    df.lon=df.lon.astype(float)
    heat_df=df[["lat","lon"]]

    heat_data=list(zip(df.lat, df.lon))

    m = folium.Map(location=( 42.878212,-8.544844), zoom_start=8, width="%100",height="%100")
    minimap = plugins.MiniMap()
    m.add_child(minimap)

    for lon, lat ,nombre,precio,titulo in zip(df["lat"],df["lon"],df["Nombre de usuario"],df["Precio"],df["Titulos"]):
    
        folium.Marker(location=[lat,lon], popup = f" Nombre: {nombre}. \Precio :  {precio}€ , Titulo: {titulo}",
                                            icon= folium.Icon( icon       = "fa-car",                                                             
                                                                prefix     = "fa")).add_to(m)

    folium.plugins.HeatMap(heat_data).add_to(m)

    return m



