import numpy as np
import pandas as pd
import streamlit as st

import helium

from bs4 import BeautifulSoup

from time import sleep
from datetime import datetime, date, timedelta


def datos_usuarios():
    
    df_Final=pd.read_csv(filepath_or_buffer =r"C:\Users\jonas\python\Proyecto Wallapop\df_Final.csv", sep = ",")
    df_final_usu=pd.read_csv(filepath_or_buffer =r"C:\Users\jonas\python\Proyecto Wallapop\df_final_usu.csv", sep = ",")
    
 
    
    # Convertir los arrays en conjuntos
    set_x = set(df_Final["Url Usuario"])
    set_y = set(df_final_usu["Url Usuario"]) 

    # Obtener la diferencia entre los conjuntos
    set_z = set_x - set_y

    # Convertir el conjunto resultante en un array
    lista_urls_usuarios = list(set_z)
    print("LEN: ",len(lista_urls_usuarios))

    
    lista_url_usuario, lista_nusuario, lista_nventas , lista_ncompras , lista_nenvios , lista_cp  , lista_vactuales  =[],[],[],[],[],[],[]
    
    
    for url_usuario in lista_urls_usuarios:
        
        browser_usu = helium.start_chrome(url_usuario, headless = True)
        
        lista_url_usuario.append(url_usuario)
        st.write(url_usuario)

        sleep(3)
        
        
            
        # Hacemos .page_source para tomar el html de la página
        soup_usu = BeautifulSoup(browser_usu.page_source, "html.parser")
        helium.kill_browser()


        try:
            nombre_usuario = soup_usu.find("h3",class_="UserBasicInfo__name mb-1").text.strip()
            lista_nusuario.append(nombre_usuario)
        except:
            lista_nusuario.append(np.nan)

        try:
            numero_ventas = soup_usu.find("div",class_="mr-1 ProfileUser__counter--bold").text.strip()
            lista_nventas.append(numero_ventas)
        except:
            lista_nventas.append(np.nan)

        try:
            numero_compras = soup_usu.find('div', {'id': 'buysCounter'}).text
            lista_ncompras.append(numero_compras)
        except:
            lista_ncompras.append(np.nan)

        try:
            numero_envios = soup_usu.find('div', {'id': 'shippingCounter'}).text
            lista_nenvios.append(numero_envios)
        except:
            lista_nenvios.append(np.nan)

        try:
            cod_postal = soup_usu.find_all("div", class_="d-flex align-items-center mb-2 ng-star-inserted")[-1].text[:-13]
            lista_cp.append(cod_postal)
        except:
            lista_cp.append(np.nan)

        try:
            ventas_actuales = soup_usu.find("span", class_="ProfileTabs__link__counter").text
            lista_vactuales.append(ventas_actuales)
        except:
            lista_vactuales.append(np.nan)
                


    df_usu=pd.DataFrame()

       #RELLENO EL DATA FRAME  CON LAS LISTAS  
    df_usu["Url Usuario"]=lista_url_usuario
    df_usu["Nombre de usuario"]=lista_nusuario
    df_usu["Ventas totales"]=lista_nventas
    df_usu["Compras totales"]=lista_ncompras
    df_usu["Envíos"]=lista_nenvios
    df_usu["C.P."]=lista_cp
    df_usu["Ventas actuales"]=lista_vactuales
    
    #Guardamos los datos en un csv
    df_usu.to_csv(r"C:\Users\jonas\python\Proyecto Wallapop\df_usu.csv",index=False) 

    df_final_usu=pd.concat([df_usu,df_final_usu], ignore_index=True)
    df_final_usu.dropna(inplace=True)
    df_final_usu.reset_index(drop=True,inplace=True)
    df_final_usu.to_csv(r"C:\Users\jonas\python\Proyecto Wallapop\df_final_usu.csv",index=False)

    
    
    