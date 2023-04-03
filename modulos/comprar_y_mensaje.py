




import numpy as np
import pandas as pd
import streamlit as st

from time import sleep
from datetime import datetime, date, timedelta

from selenium import webdriver 
from selenium.webdriver.common.keys import Keys


    

def inicia_session(url):
    driver = webdriver.Chrome()
    
    driver.get("https://www.google.com")
    driver.maximize_window()

    windows = driver.window_handles
    

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


    sleep(2)
    driver.get("https://es.wallapop.com/")
    sleep(5)
    next_button = driver.find_element_by_css_selector("#onetrust-accept-btn-handler")
    next_button.click()

    sleep(1)
    next_button = driver.find_element_by_css_selector("body > header > a > img.main-header-logo--full")
    next_button.click()

    sleep(30)
    funcion_comprar_mensaje(driver,url)
    return driver


def funcion_comprar_mensaje(driver,url):

    sleep(10)
    try:
        df_compra1=pd.read_csv(filepath_or_buffer =r"C:\Users\jonas\python\Proyecto Wallapop\df_compra1.csv",sep=",")
        df_Final=pd.read_csv(filepath_or_buffer =r"C:\Users\jonas\python\Proyecto Wallapop\df_Final.csv",sep=",")
    except:
        pass
    # Inicializa el controlador de Selenium y carga la página
    
    

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

    sleep(8)
    # Pulso el boton de comprar
    button = driver.find_element_by_css_selector("body > tsl-root > tsl-private > div > div > div > tsl-chat > div > div.Chat__conversation.Chat__conversation--active.ng-star-inserted > tsl-current-conversation > div > div.messaging > div > div.input.send-message-container > tsl-input > form > div > div.send-btn-wrapper > a")
    button.click()

    sleep(8)
    mensaje= driver.find_element_by_css_selector("body > tsl-root > tsl-private > div > div > div > tsl-chat > div > div.Chat__conversation.Chat__conversation--active.ng-star-inserted > tsl-current-conversation > div > div.messaging > div > div.input.send-message-container > tsl-input > form > div > div.textarea-wrapper > textarea")
    mensaje.send_keys(f"buenas, acabo de comprar tu producto. Muchas gracias")


    sleep(40)
    button = driver.find_element_by_css_selector("body > tsl-root > tsl-private > div > div > div > tsl-chat > div > div.Chat__conversation.Chat__conversation--active.ng-star-inserted > tsl-current-conversation > div > div.messaging > div > div.input.send-message-container > tsl-input > form > div > div.send-btn-wrapper > a")
    button.click()



    sleep(1)
    button = driver.find_element_by_css_selector("body > tsl-root > tsl-private > div > div > div > tsl-chat > div > div.Chat__conversation.Chat__conversation--active.ng-star-inserted > tsl-current-conversation > div > div.messaging > div > tsl-delivery-banner > div > tsl-buy-banner > tsl-banner > ngb-alert > div > div.BuyBanner__CTA > tsl-button > button")
    button.click()
    
    df_compra1=pd.DataFrame()
    df_compra1=df_Final[df_Final["Urls"]==url]["Url Usuario"]

    df_compras=pd.concat([df_compras,df_compra1], ignore_index=True)

    df_compras.to_csv(r"C:\Users\jonas\python\Proyecto Wallapop\df_compras.csv",index=False)


    

   
   
        




