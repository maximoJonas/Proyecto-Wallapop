import numpy as np
import pandas as pd
import streamlit as st

from time import sleep
from datetime import datetime, date, timedelta

from selenium import webdriver 
from selenium.webdriver.common.keys import Keys

def funcion_mensaje_regateo(url,total_con_descuento):
 
    sleep(10)
    
    try:
        df_negociando=pd.read_csv(filepath_or_buffer =r"C:\Users\jonas\python\Proyecto Wallapop\df_negociando.csv",sep=",")
        df_Final=pd.read_csv(filepath_or_buffer =r"C:\Users\jonas\python\Proyecto Wallapop\df_Final.csv",sep=",")
    except:
        pass
    
    
    driver = webdriver.Chrome()

    

    def inicia_session():

# Inicializa el controlador de Selenium y carga la página
        
        driver.get("https://www.google.com")
        driver.maximize_window()
            
   
        # Encuentra el botón que abre la ventana emergente y haz clic en él
        sleep(2)
        button = driver.find_element_by_css_selector("#L2AGLb > div")
        button.click()
        
        sleep(1)
        button = driver.find_element_by_css_selector("#gb > div > div.gb_xe > a > span")
        button.click()

        sleep(1)
        email= driver.find_element_by_css_selector("#identifierId")
        email.send_keys("recogidaadomicilio@gmail.com")

        sleep(2)
        next_button = driver.find_element_by_css_selector("#identifierNext > div > button > span")
        next_button.click()

        sleep(5)
        passw= driver.find_element_by_css_selector("#password > div.aCsJod.oJeWuf > div > div.Xb9hP > input")
        passw.send_keys("hab123123")

        sleep(3)
        next_button = driver.find_element_by_css_selector("#passwordNext > div > button > span")
        next_button.click()


        sleep(1)
        driver.get("https://es.wallapop.com/")
        sleep(5)
        next_button = driver.find_element_by_css_selector("#onetrust-accept-btn-handler")
        next_button.click()

        sleep(2)
        next_button = driver.find_element_by_css_selector("body > header > a > img.main-header-logo--full")
        next_button.click()

        sleep(30)
        



    windows = driver.window_handles
    if len(windows)==1:

        sleep(3)
        driver.execute_script("window.open('');")
        ventanas = driver.window_handles


        # Cambia a la segunda pestaña (el índice 1 de la lista de ventanas)
        driver.switch_to.window(ventanas[-1])


        driver.get(url)
        sleep(3)

        # Abrir CHAT 
        button = driver.find_element_by_class_name("js-detail-chat-send-message-detail")
        button.click()
        
        sleep(4)
        # Obtén los identificadores de ventana de todas las ventanas abiertas
     
        ventanas = driver.window_handles
        # Cambia a la segunda pestaña (el índice 1 de la lista de ventanas)
        driver.switch_to.window(ventanas[-1])


       

        sleep(12)
        mensaje= driver.find_element_by_css_selector("body > tsl-root > tsl-private > div > div > div > tsl-chat > div > div.Chat__conversation.Chat__conversation--active.ng-star-inserted > tsl-current-conversation > div > div.messaging > div > div.input.send-message-container > tsl-input > form > div > div.textarea-wrapper > textarea")
        mensaje.send_keys(f"buenas, estoy interesado en tu producto y podría comprarlo entre hoy y mañana o incluso ir a buscarlo si te viene bien, pero me lo podrias dejar en {total_con_descuento}€. Muchas gracias")


        sleep(30)
        button = driver.find_element_by_css_selector("body > tsl-root > tsl-private > div > div > div > tsl-chat > div > div.Chat__conversation.Chat__conversation--active.ng-star-inserted > tsl-current-conversation > div > div.messaging > div > div.input.send-message-container > tsl-input > form > div > div.send-btn-wrapper > a")
        button.click()

        df_negociando_1=pd.Dataframe()
        df_negociando=pd.Dataframe()


        try:
            df_negociando=pd.read_csv(filepath_or_buffer =r"C:\Users\jonas\python\Proyecto Wallapop\df_negociando.csv",sep=",")
            df_Final=pd.read_csv(filepath_or_buffer =r"C:\Users\jonas\python\Proyecto Wallapop\df_Final.csv",sep=",")
        except:
            pass

        df_negociando_1["Urls"]=url

        
        df_negociando_1["Titulos"] = list(df_Final[df_Final["Urls"] ==url]["Titulos"])
        df_negociando_1["Precio"]=list(df_Final[df_Final["Urls"] ==url]["Precio"])
        df_negociando_1["Precio regateo"]=list(df_Final[df_Final["Urls"] ==url]["Precio"]/2)

        df_negociando_1["Comprado"]=["NO"][0]

        df_negociando=pd.concat([df_negociando,df_negociando_1], ignore_index=True)

        df_negociando.to_csv(r"C:/Users/jonas/python/Proyecto Wallapop/df_negociando.csv",index=False)
        
    else:


        
    
        inicia_session()

        sleep(4)
        # Obtén los identificadores de ventana de todas las ventanas abiertas
        driver.execute_script("window.open('');")
        ventanas = driver.window_handles


        # Cambia a la segunda pestaña (el índice 1 de la lista de ventanas)
        driver.switch_to.window(ventanas[-1])


        driver.get(url)

        sleep(3)

        # Abrir CHAT 
        button = driver.find_element_by_class_name("js-detail-chat-send-message-detail")
        button.click()
        
        sleep(3)
        ventanas = driver.window_handles
        # Cambia a la segunda pestaña (el índice 1 de la lista de ventanas)
        driver.switch_to.window(ventanas[-1])


        sleep(10)
        mensaje= driver.find_element_by_css_selector("body > tsl-root > tsl-private > div > div > div > tsl-chat > div > div.Chat__conversation.Chat__conversation--active.ng-star-inserted > tsl-current-conversation > div > div.messaging > div > div.input.send-message-container > tsl-input > form > div > div.textarea-wrapper > textarea")
        mensaje.send_keys(f"buenas, estoy interesado en tu producto y podría comprarlo entre hoy y mañana o incluso ir a buscarlo si te viene bien, pero me lo podrias dejar en {total_con_descuento}€. Muchas gracias")


        sleep(20)
        button = driver.find_element_by_css_selector("body > tsl-root > tsl-private > div > div > div > tsl-chat > div > div.Chat__conversation.Chat__conversation--active.ng-star-inserted > tsl-current-conversation > div > div.messaging > div > div.input.send-message-container > tsl-input > form > div > div.send-btn-wrapper > a")
        button.click()

        df_negociando_1=pd.Dataframe()
        df_negociando=pd.Dataframe()



   
        df_negociando_1["Urls"]=url

        
        df_negociando_1["Titulos"] = list(df_Final[df_Final["Urls"] ==url]["Titulos"])
        df_negociando_1["Precio"]=list(df_Final[df_Final["Urls"] ==url]["Precio"])
        df_negociando_1["Precio regateo"]=list(df_Final[df_Final["Urls"] ==url]["Precio"]/2)

        df_negociando_1["Comprado"]=["NO"][0]

        df_negociando=pd.concat([df_negociando,df_negociando_1], ignore_index=True)

        df_negociando.to_csv(r"C:\Users\jonas\python\Proyecto Wallapop\df_negociando.csv",index=False)

