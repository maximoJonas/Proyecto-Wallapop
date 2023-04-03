import numpy as np
import pandas as pd

import helium

from bs4 import BeautifulSoup

from time import sleep
from datetime import datetime, date, timedelta



def comprobar_vendidos():
    
    #Creo una columna nueva y le meto un 0 si no se vendio y un 1 si ya no se encuentra el producto o esta reservado
    today = date.today()
    lista_vendidos=list()
    lista_vendidos_fecha=list()
    
    df_Final_vendidos=pd.read_csv(filepath_or_buffer =r"C:\Users\jonas\python\Proyecto Wallapop\df_Final_vendidos.csv", sep = ",")
    
    df_Final0=df_Final_vendidos[df_Final_vendidos["Vendido"]==0]
    df_Final1=df_Final_vendidos[df_Final_vendidos["Vendido"]==1]

    for Urls in df_Final0["Urls"]:
#         COMPROBAR PRIMERO SI YA ESTA VENDIDO.. OSEA SI YA TIENE UN 1
        
        
        try:

            browser1 = helium.start_chrome(Urls, headless = True)
            print(Urls)

            sleep(1.5)

            # Hacemos .page_source para tomer el html de la página
            soup1 = BeautifulSoup(browser1.page_source, "html.parser")
            helium.kill_browser()
             #Cojo si está reservado y compruebo si ha cambiado    
            try:   
                reservado=soup1.find("div", class_="status-icon to-left").text 
                if reservado=="Reservado" :
                                        
                    lista_vendidos.append(1)
                    lista_vendidos_fecha.append(today)
                else:
                    lista_vendidos.append(0)
                    lista_vendidos_fecha.append(0)

            except:
                lista_vendidos.append(0)
                lista_vendidos_fecha.append(0)

        except:
        
            lista_vendidos.append(1)
            lista_vendidos_fecha.append(today)
            helium.kill_browser()

        
            
            
    df_Final0["Vendido"]=lista_vendidos
    df_Final0["Vendido Fecha"]=lista_vendidos_fecha
    df_Final=pd.concat([df_Final0,df_Final1], ignore_index=True)
    df_Final.to_csv(r"C:\Users\jonas\python\Proyecto Wallapop\df_Final_vendidos.csv",index=False)
    