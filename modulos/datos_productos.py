
import numpy as np
import pandas as pd

import helium

from bs4 import BeautifulSoup

from time import sleep
from datetime import datetime, date, timedelta
import pickle
import re
import os.path

import streamlit as st 

from sklearn.linear_model import LogisticRegression
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score



def crear_lista_url_pag():
    lista_url_paginas,lista_pal_clave,lista_categoria=[],[],[]


    lista_categorias_id=[13100,12467,18000,17000,12461,12485,19000]
    lista_categorias_nombre=["Electrodomésticos","Hogar y jardin","Coleccionismo","Bicicletas","Niños y bebés","Otros","Construccion"]
    pal_clave=["urge","urgente","vestido regional","television antiguo","antiguo","videojuego antiguo","vintage","lote"]
    lista_categoria=lista_categorias_nombre + pal_clave


    distancia=100000
    lat=42.40161
    long=-8.80501
    time="today"

    # filtro=input("Buscar: ")
    # pal_clave.append(filtro)

    url_base=f"https://es.wallapop.com/app/search?time_filter={time}&"


    for pal in pal_clave:
        lista_pal_clave.append(pal.replace(" ","%20"))


    for cat in lista_categorias_id:
        lista_url_paginas.append(f"{url_base}latitude={lat}&longitude={long}&distance={distancia}&category_ids={cat}&filters_source=quick_filters&order_by=newest")

    for pal in lista_pal_clave:
        lista_url_paginas.append(f"{url_base}latitude={lat}&longitude={long}&distance={distancia}&keywords={pal}&filters_source=quick_filters&order_by=newest")

       


    # Guardar la lista  en el archivo local.

    with open(r"C:/Users/jonas/python/Proyecto Wallapop/lista_url_paginas.pickle", "wb") as f:
        pickle.dump(lista_url_paginas, f)
    
    with open(r"C:/Users/jonas/python/Proyecto Wallapop/lista_categoria.pickle", "wb") as f:
        pickle.dump(lista_categoria, f)

    




def datos_productos():

    lista_titulos_page,lista_soup=[],[]

    with open(r"C:/Users/jonas/python/Proyecto Wallapop/lista_url_paginas.pickle", "rb") as f:
        lista_url_paginas = pickle.load(f)
        st.write("lista  de paginas por categorias: ",lista_url_paginas)
    
    with open(r"C:/Users/jonas/python/Proyecto Wallapop/lista_categoria.pickle", "rb") as p:
        lista_categoria = pickle.load(p)


    for url in lista_url_paginas:
        

        browser = helium.start_chrome(url, headless = True)
       
    
        sleep(3)

        # Hacemos .page_source para tomar el html de la página
        soup = BeautifulSoup(browser.page_source, "html.parser")
        lista_soup.append(soup)

        lista_titulos_page.append(soup.find_all("p", class_ = "ItemCard__title my-1"))
        #Matamos el proceso de helium sino nos saturaba la memoria Ram
        helium.kill_browser()


    lista_titulos=[]
    for page in lista_titulos_page:
        
        lista_titulos.append([p.text.strip() for p in page])

    lista_imagenes_titulos=[]

    # Creación de titulos  de los productos
    for soup in lista_soup:

        imagenes = soup.find_all("div", class_ = "ItemCard__image ItemCard__image--with-description")

        lista_imagenes = [img.find("img")["src"] for img in imagenes]

        lista_imagenes = [img.split("/")[-2].split("p")[-1] for img in lista_imagenes]
        
        lista_imagenes_titulos.append(lista_imagenes)


    # Limpieza de titulos
    lista_titulos_limpios_titulos=[]
    

    for lista_titulos in lista_titulos:
        
        lista_titulos_limpios = [re.sub('[^A-Za-z0-9_À-ÿ-+. ]', '', titulo.lower()) for titulo in lista_titulos]
        lista_titulos_limpios_titulos.append(lista_titulos_limpios)

    lista_titulos_limpios2=[]
    dict_tildes = {"ñ" : "n",
               "á" : "a",
               "é" : "e", 
               "í" : "i",
               "ó" : "o",
               "ú" : "u", 
               "+" : "-", 
               "." : "-"} 

    # Remplazamos el diccionario que hemos creado
    for lista_titulos_limpios in lista_titulos_limpios_titulos:    
        
    # Primero eliminamos los puntos finales de las cadenas por que no los queremos
        for i in range(len(lista_titulos_limpios)):
            if lista_titulos_limpios[i][-1] == ".":
                lista_titulos_limpios[i] = lista_titulos_limpios[i].rstrip(".")

        lista_titulos_limpios2.append(["".join([t if t not in dict_tildes else dict_tildes[t] for t in titulo]).replace(" ", "-") for titulo in lista_titulos_limpios])




    lista_url_final=[]
    for lista_titulos_limp, lista_imagenes in zip (lista_titulos_limpios2,lista_imagenes_titulos):
        
        wallapop_url = "https://es.wallapop.com/item"
        
        lista_url = [f"{wallapop_url}/{t}-{i}"  for t, i in zip(lista_titulos_limp, lista_imagenes)]
        
        lista_url_final.append(lista_url)

        

    # Creamos el DataFrame 
    df = pd.DataFrame({"Urls": lista_url_final,"Titulos": lista_titulos_limpios2,"Categoria":lista_categoria})

    # Usamos la función explode para expandir la columna de listas
    df_exploded = df.explode(["Urls","Titulos"])

    # Mostramos el DataFrame resultante
    df_exploded.dropna(inplace=True)
    df_exploded.reset_index(drop=True,inplace=True)
    

    df=df_exploded
    # borramos datos en memoria
    df_exploded=pd.DataFrame()



    #Obtenemos datos por cada URL que hemos metido en  el DataFrame
    lista_reservado , lista_descripcion , lista_valoraciones , lista_estrellas , lista_precios  , lista_fecha ,  lista_loEnvia  , lista_direccion , lista_visto , lista_megusta , lista_estado =[],[],[],[],[],[],[],[],[],[],[]
    lista_usuarios_url=[]
    lista_img,lista_img1=[],[]

    url_base_usuario="https://es.wallapop.com/app/user/"

    # Obtener fecha actual
    today = date.today()

    fecha_ayer = today - timedelta(days=1)


    for url1  in df["Urls"]:
            
        
        try:
    
            browser1 = helium.start_chrome(url1, headless = True)
            print(url1)

            sleep(1.2)

            # Hacemos .page_source para tomer el html de la página
            soup1 = BeautifulSoup(browser1.page_source, "html.parser")
            #Matamos el proceso de Chrome
            helium.kill_browser()          
        except:
            print("ERROR:   ",url1)
            
            
        #Cojo  las fechas del  producto subido
        try:
            fecha=soup1.find("div",class_="card-product-detail-user-stats-published").text.strip()
            # establecer la configuración regional en español
            
            formato = '%d-%b-%Y'

            # Mapeo de nombres de los meses en español a inglés
            meses_espanol_a_ingles = {
                'ene': 'Jan',
                'feb': 'Feb',
                'mar': 'Mar',
                'abr': 'Apr',
                'may': 'May',
                'jun': 'Jun',
                'jul': 'Jul',
                'ago': 'Aug',
                'sep': 'Sep',
                'oct': 'Oct',
                'nov': 'Nov',
                'dic': 'Dec'
            }


            # Reemplaza el nombre del mes en español por su equivalente en inglés
            for mes_espanol, mes_ingles in meses_espanol_a_ingles.items():
                fecha = fecha.replace(mes_espanol, mes_ingles)
            fecha_date = datetime.strptime(fecha, formato).date()

            lista_fecha.append(fecha)

            # Comparar fechas
            if fecha_ayer == fecha_date:
                
                #Cojo  las descripciones
                try:
                    descripcion=soup1.find("p",class_="js__card-product-detail--description card-product-detail-description").text
                    lista_descripcion.append(descripcion)
                except:
                    lista_descripcion.append(np.nan)
                    
                #cojo las imagenes
                try:
                    slider = soup1.find("ul", class_="card-slider-main")
                    images = slider.find_all("img")
                    lista_img1=list()
                    for img in images:
                        lista_img1.append(img['src'])
                    lista_img.append(lista_img1)
                except:
                    lista_img.append(np.nan)


                #Cojo precios
                try:
                    precio=soup1.find("span",class_="card-product-detail-price").text
                    
                    precio=precio[:-4]
                    precio = precio.replace(".","")
                    precio = int(precio.replace(',', '.'))
                    lista_precios.append(precio)
                except:
                    lista_precios.append(np.nan)

                #Cojo valoraciones
                try:
                    valoracion=soup1.find("span",class_="recived-reviews-count").text
                    lista_valoraciones.append(valoracion)
                except:
                    lista_valoraciones.append(np.nan)

                #Cojo estrellas
                try:
                    estrellas=soup1.find("div",class_="card-profile-rating")["data-score"]
                    lista_estrellas.append(estrellas)
                except:
                    lista_estrellas.append(np.nan)


                #Cojo si lo envia 
                try:
                    envio=soup1.find("div",class_="detail-icon").text
                    lista_loEnvia.append("SI")
                except:
                    lista_loEnvia.append("NO")

                #Cojo si la direccion  
                try:
                    direccion=soup1.find("div",class_="card-product-detail-location").text.strip()
                    lista_direccion.append(direccion)
                except:
                    lista_direccion.append(np.nan)

                #Cojo los me gusta    
                try:
                    megusta=soup1.find_all("div",class_="card-product-detail-user-stats-right")[0].text
                    lista_megusta.append(megusta)
                except:
                    lista_megusta.append(np.nan)

                #Cojo las veces visto    
                try:
                    visto=soup1.find_all("div",class_="card-product-detail-user-stats-right")[1].text
                    lista_visto.append(visto)
                except:
                    lista_visto.append(np.nan)

                #Cojo el estado del producto    
                try:
                    estado=soup1.find_all("span",class_="ExtraInfo__text")[-1].text
                    lista_estado.append(estado)
            
                except:
                    lista_estado.append("NO")

                #Cojo si está reservado    
                try:   
                    reservado=soup1.find("div", class_="status-icon to-left").text 
                    if reservado=="Reservado" :
                        lista_reservado.append("SI")
                    else:
                        lista_reservado.append("NO")
                        
                except:
                    lista_reservado.append("NO")



                try:
                    #Cogemos nombre de usuario
                    enlace = soup1.find('a', {'class': 'card-user-right'})['href']
                    nom_usu = enlace.split('/user/')[1]
                    
                except:
                    nom_usu=np.nan

                try:
                    #cogemos el numero valor del usuario
                    elemento_div = soup1.find("div", {"class": "detail-item"})
                    valor_usu = elemento_div["data-seller-user-id"]
                    
                except:
                    valor_usu=np.nan

                #https://es.wallapop.com/app/user/luisc-131935092-owzypg83dvz5/published
                lista_usuarios_url.append(f"{url_base_usuario}{nom_usu}-{valor_usu}/published")
                
                #Matamos el proceso de Chrome
                helium.kill_browser()
                
            #Si la fecha no es de hoy que rellene de NaNs que despues los elimino   
            else:
                
                lista_descripcion.append(np.nan)
                lista_valoraciones.append(np.nan)
                lista_precios.append(np.nan)
                lista_estrellas.append(np.nan)
                lista_direccion.append(np.nan)
                lista_visto.append(np.nan)
                lista_megusta.append(np.nan)
                lista_estado.append(np.nan)
                lista_loEnvia.append(np.nan)
                lista_reservado.append(np.nan)
                lista_usuarios_url.append(np.nan)
                lista_img.append(np.nan)
                
                
                #Matamos el proceso de Chrome
                helium.kill_browser()           
                
                
        except:
            lista_fecha.append(np.nan)
            lista_descripcion.append(np.nan)
            lista_valoraciones.append(np.nan)
            lista_precios.append(np.nan)
            lista_estrellas.append(np.nan)
            lista_direccion.append(np.nan)
            lista_visto.append(np.nan)
            lista_megusta.append(np.nan)
            lista_estado.append(np.nan)
            lista_loEnvia.append(np.nan)
            lista_reservado.append(np.nan)
            lista_usuarios_url.append(np.nan)
            lista_img.append(np.nan)
            
            #Matamos el proceso de Chrome
            helium.kill_browser() 
            

    
            
    #RELLENO EL DATA FRAME  CON LAS LISTAS     

    df["Descripcion"]=lista_descripcion
    df["Valoraciones"]=lista_valoraciones
    df["Precio"]=lista_precios
    df["Estrellas"]=lista_estrellas
    df["Fecha subida"]=today
    df["Direccion"]=lista_direccion
    df["Num veces visto"]=lista_visto
    df["Me gustas"]=lista_megusta
    df["Estado"]=lista_estado
    df["Envio"]=lista_loEnvia
    df["Reservado"]=lista_reservado
    df["Url Usuario"]=lista_usuarios_url
    df["Imagenes"]=lista_img

    
    st.write("Terminado el Dataframe")
    df.to_csv(r"C:\Users\jonas\python\Proyecto Wallapop\data.csv",index=False)


    # Guardamos los datos y los añadimos a los anteriores
    df_final=pd.read_csv(filepath_or_buffer =r"C:\Users\jonas\python\Proyecto Wallapop\df_Final.csv",sep=",")

    df_final=pd.concat([df,df_final], ignore_index=True)
    df_final.dropna(inplace=True)
    df_final.reset_index(drop=True,inplace=True)
    st.success("Guardado datos de productos!")
    df_final.to_csv(r"C:\Users\jonas\python\Proyecto Wallapop\df_Final.csv",index=False)

