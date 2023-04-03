import numpy as np
import pandas as pd
import helium
from bs4 import BeautifulSoup
from time import sleep
from datetime import datetime, date, timedelta
import re
import os.path
import streamlit as st

# Quitamos filtros de tiempo, distancia en las ulr y hacemos urls nuevas de toda España para comparar precios


def url_compara(titulo,estado):


    lista_titulos_page,lista_soup=[],[]
    lista_titulos=[]
    lista_imagenes_titulos=[]

    dicc={"En su caja":"in_box",
               "Nuevo":"new",
          "Como nuevo":"as_good_as_new",
               "Bueno":"good",
           "Aceptable":"fair",
     "Lo ha dado todo":"has_given_it_all"}

    titulo=titulo.replace(" ","-")

    for clave, valor in dicc.items():
        estado = estado.replace(clave, valor)

    lat=42.40161
    long=-8.80501

    url_base=f"https://es.wallapop.com/app/search?"

    url_nombre=f"{url_base}latitude={lat}&longitude={long}&keywords={titulo}&filters_source=quick_filters&condition={estado}"
    print(url_nombre)

    browser = helium.start_chrome(url_nombre, headless = True)
    sleep(4)

    # Hacemos .page_source para tomar el html de la página
    soup = BeautifulSoup(browser.page_source, "html.parser")
    lista_soup.append(soup)

    lista_titulos_page.append(soup.find_all("p", class_ = "ItemCard__title my-1"))
    
    #Matamos el proceso de helium sino nos saturaba la memoria Ram
    helium.kill_browser()

    #Titulos
    for page in lista_titulos_page:
     
        lista_titulos.append([p.text.strip() for p in page])

    # Creación de titulos  de los productos
    
    
    for soup in lista_soup:

        imagenes = soup.find_all("div", class_ = "ItemCard__image ItemCard__image--with-description")

        lista_imagenes = [img.find("img")["src"] for img in imagenes]

        lista_imagenes = [img.split("/")[-2].split("p")[-1] for img in lista_imagenes]

        lista_imagenes_titulos.append(lista_imagenes)


    # Limpieza de titulos
    lista_titulos_limpios_titulos,lista_titulos_limpios2=[],[]

    for lista_titulos in lista_titulos:
    
        lista_titulos_limpios = [re.sub('[^A-Za-z0-9_À-ÿ-+. ]', '', titulo.lower()) for titulo in lista_titulos]
        lista_titulos_limpios_titulos.append(lista_titulos_limpios)

    
    
    
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
    df = pd.DataFrame({"Urls": lista_url_final,"Titulos": lista_titulos_limpios2})

    # Usamos la función explode para expandir la columna de listas
    df = df.explode(["Urls","Titulos"])
    df=df[:5]

    # Mostramos el DataFrame resultante
    df.reset_index(drop=True,inplace=True)    
    
    
    
    
    lista_reservado , lista_descripcion , lista_valoraciones , lista_estrellas , lista_precios=list(),list(),list(),list(),list()
    lista_fecha ,  lista_loEnvia  , lista_direccion , lista_visto =list(),list(),list(),list() 
    lista_megusta , lista_estado , lista_usuarios_url,lista_img,lista_img1=list(),list(),list(),list(),list()

    url_base_usuario="https://es.wallapop.com/app/user/"    

    for url1  in df["Urls"][:5]:
        
        

        try:

            browser1 = helium.start_chrome(url1, headless = True)
            print(url1)

            sleep(1.5)

            # Hacemos .page_source para tomer el html de la página
            soup1 = BeautifulSoup(browser1.page_source, "html.parser")
        except:
            st.write("No hay nada parecido para comparar, puede que sea algo muy especifico")


           #Cojo  las fechas del  producto subido
        try:
            fecha=soup1.find("div",class_="card-product-detail-user-stats-published").text.strip()
            lista_fecha.append(fecha)
        except:
            lista_fecha.append(np.nan)

        #Cojo  las descripciones
        try:
            descripcion=soup1.find("p",class_="js__card-product-detail--description card-product-detail-description").text
            lista_descripcion.append(descripcion)
        except:
            lista_descripcion.append(np.nan)

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


        #Cojo si lo envia 
        try:
            envio=soup1.find("div",class_="detail-icon").text
            lista_loEnvia.append("SI")
        except:
            lista_loEnvia.append("NO")

        #Cojo la direccion  
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
            estado1=soup1.find_all("span",class_="ExtraInfo__text")[-1].text
            lista_estado.append(estado1)        
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

        lista_usuarios_url.append(f"{url_base_usuario}{nom_usu}-{valor_usu}/published")

        #Matamos el proceso de Chrome
        helium.kill_browser()



       #RELLENO EL DATA FRAME  CON LAS LISTAS     

    df["Descripcion"]=lista_descripcion
    df["Valoraciones"]=lista_valoraciones
    df["Precio"]=lista_precios
    df["Estrellas"]=lista_estrellas
    df["Fecha subida"]=lista_fecha
    df["Direccion"]=lista_direccion
    df["Num veces visto"]=lista_visto
    df["Me gustas"]=lista_megusta
    df["Estado"]=lista_estado
    df["Envio"]=lista_loEnvia
    df["Reservado"]=lista_reservado
    df["Url Usuario"]=lista_usuarios_url
    df["Imagenes"]=lista_img

    
    df=df[1:]
    
    df.dropna(inplace=True)
    df.reset_index(drop=True,inplace=True)
    df.to_csv(f"C:/Users/jonas/python/Proyecto Wallapop/base_datos/df_{titulo}_{estado}.csv",index=False)


    return df




def compara_productos(titulo,estado): #RETORNA UN DF CON 10 PRODUCTOS PARECIDOS COMO MUCHO
   
    dicc={"En su caja":"in_box",
               "Nuevo":"new",
          "Como nuevo":"as_good_as_new",
               "Bueno":"good",
           "Aceptable":"fair",
     "Lo ha dado todo":"has_given_it_all"}

    titulo=titulo.replace(" ","-")

    for clave, valor in dicc.items():
        estado = estado.replace(clave, valor)
    
#     Comprobamos si el archivo ya existe
    filename = f"C:/Users/jonas/python/Proyecto Wallapop/base_datos/df_{titulo}_{estado}.csv"


    if os.path.isfile(filename):

        ctime = os.path.getctime(filename)
        ctime_str = datetime.fromtimestamp(ctime).strftime('%Y-%m-%d %H:%M:%S')

        texto=st.write(f"El archivo fue creado el {ctime_str}")

      
        st.write("¿Quieres actualizarlo? :")
            
        respuesta = st.selectbox(label = "Marca 'Si actualizar' si quieres actualizarlo o 'No' si no quieres crear un archivo nuevo:",
                                options=("","Si actualizar","No")
                                      )

    
        
 
        if respuesta=="Si actualizar":
                st.write("Actualiando...")
                return url_compara(titulo,estado)

        elif respuesta=="No":
                df=pd.read_csv(filepath_or_buffer =f"C:/Users/jonas/python/Proyecto Wallapop/base_datos/df_{titulo}_{estado}.csv", sep = ",")
                return df
            
            
        
    else:
        st.write("El archivo no existe, vamos a crearlo.")
        return url_compara(titulo,estado)

    


