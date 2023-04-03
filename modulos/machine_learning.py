import numpy as np
import pandas as pd
import streamlit as st
import helium

from bs4 import BeautifulSoup

from time import sleep
from datetime import datetime, date, timedelta


from sklearn.ensemble import RandomForestRegressor, GradientBoostingRegressor, AdaBoostRegressor

from sklearn.tree import DecisionTreeRegressor
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LinearRegression
from sklearn.svm import SVR
from sklearn.neighbors import KNeighborsRegressor

from sklearn.metrics import mean_squared_error
from sklearn.metrics import r2_score
from sklearn.metrics import mean_absolute_error

def machine_learning(n_estimators,learning_rate,C,n_neighbors):

    df_Final_vendidos=pd.read_csv(r"C:/Users/jonas/python/Proyecto Wallapop/df_Final_vendidos.csv",sep=",")

    data=df_Final_vendidos
    data=data[data["Vendido"]==1]

    data=data[["Categoria","Valoraciones","Estrellas","Precio","Fecha subida","Estado","Envio","Vendido Fecha"]]


    # Convertir la fecha subida y la fecha vendido a objetos datetime
    data['Fecha subida'] = pd.to_datetime(data['Fecha subida'], format='%d-%b-%Y')
    data['Vendido Fecha'] = pd.to_datetime(data['Vendido Fecha'], format='%Y-%m-%d')

    # Calcular el tiempo de venta y agregarlo como una nueva columna
    data['Tiempo de venta'] = (data['Vendido Fecha'] - data['Fecha subida']).dt.days

    # Convertir el estado a valores numéricos
    estado_map = {"NO":0, 'Nuevo': 1, 'Como nuevo': 2, 'Bueno': 3, 'Regular': 4, 'Malo': 5,"Lo ha dado todo":6,"Sin abrir":7,"Aceptable":8}
    data['Estado'] = data['Estado'].map(estado_map)

    # Convertir el envío a valores numéricos
    data['Envio']=data['Envio'].replace("SI",1)
    data['Envio']=data['Envio'].replace("NO",0)
    data['Envio']=data['Envio'].astype(int)

    # Convertir la categoría a variables dummies
    data = pd.get_dummies(data, columns=['Categoria'])

    data.dropna(inplace=True)

    # Seleccionar las columnas relevantes para la regresión logística
    X=data.drop(columns=["Fecha subida",'Vendido Fecha','Tiempo de venta'])
    y = data['Tiempo de venta']

    # cargar datos y dividir en conjuntos de entrenamiento y prueba
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.3, random_state=42)


    # Diferentes modelos
    # especificar los modelos a combinar


    estimators = [
        ( RandomForestRegressor(n_estimators=n_estimators, random_state=42)),
        (GradientBoostingRegressor(n_estimators=n_estimators, learning_rate=0.1, max_depth=2, random_state=42)),
        ( SVR(kernel='rbf', C=C, gamma=0.1, epsilon=.1)),
        ( KNeighborsRegressor(n_neighbors=n_neighbors))
    ]


    st.warning(f"Conjunto de X - Train / X -Test : {X_train.shape}  /  {X_test.shape}\n")
    st.warning(f"Conjunto de y - Train / y -Test : {y_train.shape}  /  {y_test.shape}\n")


    # creamos el modelo AdaBoostRegressor
    ada_model = AdaBoostRegressor()

    for estimator in estimators:
        ada_model.base_estimator_ = estimator
        ada_model.fit(X_train, y_train)
        yhat = ada_model.predict(X_test).round(0)
        
        st.success(f"  \n   \t \t METRICAS {estimator.__class__.__name__}:")
        
        mse = mean_squared_error(y_test, yhat)
        st.write(f"Error cuadrático medio del modelo {estimator.__class__.__name__}: {mse}")  
        
        mae = mean_absolute_error(y_test, yhat)
        st.write(f"Error absoluto medio del modelo {estimator.__class__.__name__}: {mae}")
        
        r2 = r2_score(y_test, yhat)
        st.write(f"R-cuadrado del model {estimator.__class__.__name__}: {r2} ")
    st.text("\n ")    
    st.text(" \n  Comparación de predicciones ")    
    for i, j in zip(yhat, y_test):
        st.text(f"Predicción:  {i} -- \t -- Valor real:  {j}") 
    

    data.to_csv(r"C:/Users/jonas/python/Proyecto Wallapop/df_machine_learnine.csv",index=False)
    



    
def machine_learning_porducto(n_estimators,df,df_machine_learnine):


    data=df

    data=data[["Categoria","Valoraciones","Estrellas","Precio","Fecha subida","Estado","Envio"]]


    
   
    # Convertir el estado a valores numéricos
    estado_map = {"NO":0, 'Nuevo': 1, 'Como nuevo': 2, 'Bueno': 3, 'Regular': 4, 'Malo': 5,"Lo ha dado todo":6,"Sin abrir":7,"Aceptable":8}
    data['Estado'] = data['Estado'].map(estado_map)

    # Convertir el envío a valores numéricos
    data['Envio']=data['Envio'].replace("SI",1)
    data['Envio']=data['Envio'].replace("NO",0)
    data['Envio']=data['Envio'].astype(int)

    # Convertir la categoría a variables dummies
    data=pd.concat([data,df_machine_learnine],ignore_index=True)
   
    cat=data["Categoria"][0]
    
    data[f"Categoria_{cat}"]=1
    data.fillna(0,inplace=True)
    
    data.dropna(inplace=True)
    predice=data.drop(columns=["Categoria","Fecha subida",'Vendido Fecha','Tiempo de venta'])
    predice=predice.iloc[[0]]


    
   
    # Seleccionar las columnas relevantes para la regresión logística
    X=df_machine_learnine.drop(columns=["Fecha subida",'Vendido Fecha','Tiempo de venta'])
    y = df_machine_learnine['Tiempo de venta']
    

  

    estimators = [( RandomForestRegressor(n_estimators=n_estimators, random_state=42))]

    # creamos el modelo AdaBoostRegressor
    ada_model = AdaBoostRegressor()

    for estimator in estimators:

        ada_model.base_estimator_ = estimator
        ada_model.fit(X, y)
        yhat = ada_model.predict(predice).round(0)[0]
      
    
    
    st.success(f"El tiempo que tardarás en vender este producto será alrededor de {yhat} días.") 
    


