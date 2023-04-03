import pandas as pd
import streamlit as st
from PIL import Image
import requests
from io import BytesIO
import astroid as ast

from modulos.compara_productos import *
from modulos.comprobar_vendidos import *
from modulos.datos_productos import *
from modulos.datos_usuario import *
from modulos.machine_learning import *
from modulos.compras_mapa import *
from modulos.mensaje_regateo import *
from modulos.comprar_y_mensaje import *


from datetime import datetime, timedelta,date
from streamlit_folium import folium_static
import folium



def main():

    st.set_page_config(page_title = "Another one Life",
                    # page_icon = ":moneybag:",
                    page_icon = Image.open("otra_vida.jpg"),
                    layout = "wide",
                    initial_sidebar_state = "auto")

    # st.set_page_config(**PAGE_CONFIG)
    data=pd.read_csv(filepath_or_buffer ="df_Final.csv", sep = ",")
    df_Final_vendidos=pd.read_csv(filepath_or_buffer ="df_Final_vendidos.csv", sep = ",")

    button_style = """
                    <style>
                    .stButton button {
                        background-color: green;
                        color: white;
                        font-size: 18px;
                        padding: 8px 12px;
                        border-radius: 4px;
                        }

                    </style>
                """
    st.markdown(button_style, unsafe_allow_html=True)
    



    menu = ["Inicio","Compras", "Ventas", "Me gustan", "Machine Learning Model", "Gráficos PowerBI", "Gestión"]


    choice = st.sidebar.selectbox(label = "Menu", options = menu, index = 0,label_visibility="visible")

    # Emoji: https://streamlit-emoji-shortcodes-streamlit-app-gwckff.streamlit.app/

    
    windows =[1]

    st.title(body = "Another one Life")

    if choice=="Inicio":
        st.image("imagenes/1624897744_39523_gif-url.gif")        
        st.text("Hay varias razones por las que puede ser beneficioso comprar cosas de segunda mano: \n \n Ahorro de dinero: Comprar cosas usadas puede ser mucho más económico que comprar algo nuevo. \n  En general, los artículos de segunda mano se venden a precios mucho más bajos que los nuevos, lo que significa que puedes ahorrar una cantidad \n  significativa de dinero en tu compra.\n\n Menor impacto ambiental: Comprar cosas de segunda mano también es bueno para el medio ambiente. \n  Al comprar artículos usados, estás evitando que se generen más residuos y que se agoten los recursos naturales necesarios para fabricar \n  nuevos productos. Además, al reducir la demanda de productos nuevos, estás ayudando a reducir las emisiones de gases de efecto invernadero \n  asociadas con la fabricación y el transporte de productos nuevos.\n \n Variedad: Otra ventaja de comprar cosas de segunda mano es que a menudo puedes encontrar artículos únicos y raros que no están disponibles. \n  Las tiendas de segunda mano y los mercados de pulgas son lugares ideales para encontrar productos antiguos o de colección que podrían no estar \n  disponibles en las tiendas.\n\n Reducción del consumo de energía: La producción de nuevos artículos consume energía y emite gases de efecto invernadero. \n  Al comprar artículos de segunda mano, se evita el consumo de energía asociado con la producción y el transporte de nuevos productos.\n \n En resumen, comprar cosas de segunda mano puede ser beneficioso para tu bolsillo, el medio ambiente y puede ofrecerte una amplia variedad de opciones únicas.")
        st.image("imagenes/DT_G76_Recycling-energy-Animated-GIF-Icon-pack.gif")
        st.text("Comprar cosas de segunda mano es algo que beneficia a nuestro planeta y que cada vez va a ser más normal. ")
        st.text(". \t \t \t\t\t Firmado: Jonás D.C. ")
        

    if choice=="Compras":
 
        tabs = ("Compras diarias","Negociando", "Pagados sin recoger", "Comprados")

        tab_content = st.tabs(tabs)

        with tab_content[0]:
            st.header("Compras diarias")

            
            # Obtener la fecha
            fecha_actual = date.today()

            # Restar un día a la fecha actual
            fecha_anterior = fecha_actual - timedelta(days=1)

            dia = st.slider(label     = "Selecciona desde el día que quieres ver los productos",
                            min_value = fecha_actual - timedelta(days=14),
                            max_value = fecha_actual,
                            value     = fecha_anterior)

            dia_format= dia.strftime('%d-%b-%Y').lower()
            df_diario=pd.DataFrame()
            df_diario=data[data["Fecha subida"]==dia_format]


            # Esperamos a que se haga clic en una fila de la tabla
            st.write('### Tabla diaria', df_diario)
            selected_indices  = st.multiselect('Seleciona los indices:', df_diario.index)
            selected_rows = df_diario.loc[selected_indices]
            st.write('### Filas seleccionadas', selected_rows)    
                
            

            row_index = st.number_input('Selecciona el índice de la fila que deseas imprimir', min_value=0, max_value=len(data)-1, step=1)
            
            
             # DIVIDIMOS EN 2 COLUMNAS LA PANTALLAS
            izquierda, derecha = st.columns(2)


            with izquierda:
                st.write(data.iloc[row_index])

           

            with derecha:
                # for index, row in data.iterrows():
                titulo=data.iloc[row_index]['Titulos']
                st.success(data.iloc[row_index]['Titulos'])

                estado=data.iloc[row_index]['Estado']
                st.success(data.iloc[row_index]['Estado'])

                st.info(data.iloc[row_index]['Descripcion'])

                precio_producto=data.iloc[row_index]['Precio']
                st.warning(data.iloc[row_index]['Precio'])

                url=data.iloc[row_index]['Urls']
                
                st.write("\n")
                st.write("\n")

            with izquierda:

                imagen=eval(data.iloc[row_index]['Imagenes'])    
                for i in range(len(imagen)):
                    st.write(imagen[i])

                
                
                response = requests.get(imagen[0])
                img = Image.open(BytesIO(response.content))


           
            # Muestra la imagen en la columna izquierda
            izquierda.image(img, caption=data.iloc[row_index]['Titulos'],use_column_width=True)

  


          

                

                 

            
           
            # Muestra los botones en la columna derecha
            with derecha:
                st.write("\n")
                st.write("\n")
                
                load= st.button("COMPARAR",help="Esto puede tardar un par de minutos",key="comparar")

                if "load_state" not in st.session_state :

                    st.session_state.load_state=False

                if load :
                    st.session_state.load_state=True

                    mensaje=st.success("COMPARANDO...")


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

                    
                        quieres=st.write("¿Quieres actualizarlo? :")
                            
                        respuesta = st.selectbox(label = "Marca 'Si actualizar' si quieres actualizarlo o 'No' si no quieres crear un archivo nuevo:",
                                                options=("","Si actualizar","No")
                                                    )
                
                        if respuesta=="Si actualizar":
                                actual=st.write("Actualiando...")
                                df_compara= url_compara(titulo,estado)

                        elif respuesta=="No":
                                df_compara=pd.read_csv(filepath_or_buffer =f"C:/Users/jonas/python/Proyecto Wallapop/base_datos/df_{titulo}_{estado}.csv", sep = ",")
                                
                        load=False        
                            
                        
                    else:
                        crear=st.success("El archivo no existe, vamos a crearlo.")
                        df_compara= url_compara(titulo,estado)
                        load=False 
                    

                    
                    imagenes_list=list()
                    try:

                        if df_compara.shape[0] != 0:
                            st.dataframe(df_compara)

                            for imagenes, titulos in zip(df_compara["Imagenes"], df_compara["Titulos"]):
                                try:
                                    imagenes = eval(imagenes)[0]
                                except:
                                    imagenes = imagenes[0]
                                
                                response = requests.get(imagenes)
                                img = Image.open(BytesIO(response.content))
                                derecha.image(img, caption=titulos,use_column_width=True)
                                imagenes_list.append((img, titulos))

                               
  
                    except:
                        pass

                

                    mensaje.empty()
                    
                    
                    with izquierda:
                        
                        if st.button("Limpiar"):
                            limpiar=st.button("Limpiar todo",key="limp")
                            limpiar=True
                            st.session_state.load_state=False
                                
                            imagenes_list.remove((img, titulos))

                            limpiar=True
                        
                            try:
                                
                                quieres.empty()
                                texto.empty()
                                crear.empty()
                                derecha.empty()
                                actual.empty()
                            except:
                                pass


                if st.button("ME GUSTA",help="Añadimos a la tabla de me gusta"):


                    st.success("Se añadio a la lista de me gusta")
                    df_me_gusta=pd.read_csv(filepath_or_buffer =r"C:\Users\jonas\python\Proyecto Wallapop\base_datos\df_me_gusta.csv" )
                    url=data.iloc[row_index]['Urls']
                    Titulos=data.iloc[row_index]['Titulos']
                    Precio=data.iloc[row_index]['Precio']

                    nueva_fila = pd.DataFrame({"Urls":[url],"Titulos":[Titulos],"Precio":[Precio]})
                    df_me_gusta = pd.concat([df_me_gusta,nueva_fila], ignore_index=True)
                    df_me_gusta.to_csv(r"C:\Users\jonas\python\Proyecto Wallapop\base_datos\df_me_gusta.csv",index=False)

                    



    

                if st.button("COMPRAR Y MENSAJE", help="Compramos producto y enviamos mensaje de cuando lo vamos a recoger", key="comprar_mens"):
                    st.success("Producto comprado, termina el proceso desde chrome")

                   
                    print("len(windows)1: ",len(windows))
                    if len(windows)>1:
                        funcion_comprar_mensaje(driver,url)
                        print("len(windows)2: ",len(windows))
                    else:
                        driver=inicia_session(url)
                        windows = driver.window_handles
                        print("len(windows)3: ",len(windows))
                    



                load1= st.button("MENSAJE BAJAR PRECIO",help="Negocia el precio")

                if "load_state" not in st.session_state:
                    st.session_state.load_state=False

                if load1 or st.session_state.load_state:
                    st.session_state.load_state=True
                

                    st.write("Elige el portentaje que quieres bajar:")
                    porcentaje=float(st.slider(label="Descuento %",min_value=0,max_value=100,value=30))
                    total_con_descuento=float(precio_producto)-(porcentaje*float(precio_producto))/100
                
                    st.write("Porcentaje",porcentaje)
                    st.write("Precio: ",precio_producto)
                    st.write("Rebaja",(porcentaje*float(precio_producto))/100)

                    st.write("Precio final es: ",total_con_descuento)
                    st.write("Recuerda iniciar sesion la primera vez para poder enviar mensajes")
                    enviar_m=st.button("ENVIAR")
                    if enviar_m:
                        st.success("Mensaje enviado")
                        funcion_mensaje_regateo(url,total_con_descuento)
                        load1=False
                        st.session_state.load_state=False
                        

                    

                    






                     
                     


                

               

           

          
            
        
        with tab_content[1]:
            st.header("Negociando")
            df_negociando=pd.read_csv(filepath_or_buffer =r"C:\Users\jonas\python\Proyecto Wallapop\df_negociando.csv" )
            st.dataframe(df_negociando)


           
                
                

            

        with tab_content[2]:
            st.header("Pagados sin recoger")
            # df=crear_venta()
            # df.to_csv(r"C:\Users\jonas\python\Proyecto Wallapop\df_compras_pagadas.csv",index=False)
            try:
                df_compras_historial=pd.read_csv(filepath_or_buffer =r"C:\Users\jonas\python\Proyecto Wallapop\df_compras_historial.csv" )
            except:
                pass
            df=pd.read_csv(filepath_or_buffer =r"C:\Users\jonas\python\Proyecto Wallapop\df_compras_pagadas.csv" )

            my_map = mapa_compras(df)
            folium_static(my_map)
            min1=df["lon"].min()
            max1=df["lon"].max()
            
           
            min_value, max_value= st.slider("Selecciona longitud para pedidos en el Norte o en el Sur: ", min_value= min1 ,max_value= max1,value=(min1 , max1) )

            st.write("Valor mínimo:", min_value)
            st.write("Valor máximo:", max_value)
            
            

            df1=df[(df["lon"]>=min_value) & (df["lon"]<=max_value) & (df["Recogido"]=="NO")]
            contar=df1["lon"].count()
            precioTotal=df1["Precio"].sum()
            st.success(f"Tenemos que recoger {contar} paquetes en total. ")
            st.warning(f"Con un valor de {precioTotal} €" )



            my_map = mapa_compras(df1)
            folium_static(my_map)
         

            st.write('### Tabla Recogidos', df1)
            selected_indices  = st.multiselect('Seleciona los indices:', df1.index,key="recogidos")
            selected_rows = df1.loc[selected_indices]
            st.write('### Filas seleccionadas', selected_rows) 
            st.write(selected_indices)
           

            
            if st.button("RECOGIDO"):
                
                for selec in selected_indices:
                     df1.loc[selec, "Recogido"] = "SI"
                st.dataframe(df1)
                df2=pd.DataFrame()
                df2=df1[df1["Recogido"]=="SI"]
                df1=df1[df1["Recogido"]=="NO"]

                contar=df1["lon"].count()
                precioTotal=df1["Precio"].sum()
                st.success(f"Tenemos que recoger {contar} paquetes en total. ")
                st.warning(f"Con un valor de {precioTotal} €" )
                df1.to_csv(r"C:\Users\jonas\python\Proyecto Wallapop\df_compras_pagadas.csv",index=False)


                df2=pd.concat([df_compras_historial,df2],ignore_index=True)
                df2.to_csv(r"C:\Users\jonas\python\Proyecto Wallapop\df_compras_historial.csv",index=False)


                my_map = mapa_compras(df1)
                folium_static(my_map)
                
            
                    

            




            
        with tab_content[3]:
            st.header("Comprados historial")
            df_compras_historial=pd.read_csv(filepath_or_buffer =r"C:\Users\jonas\python\Proyecto Wallapop\df_compras_historial.csv" )
            st.dataframe(df_compras_historial)






    if choice=="Ventas":

        st.header("Vendidos:")
        df_ventas=df_machine_learnine=pd.read_csv(r"C:\Users\jonas\python\Proyecto Wallapop\df_ventas.csv",sep=",")
        st.dataframe(df_ventas)

        # powerbi por fechas,meses...
            

    if choice=="Me gustan":
        
        st.write("### Seguimiento de productos que me gustan")
        df_me_gusta=pd.read_csv(filepath_or_buffer =r"C:\Users\jonas\python\Proyecto Wallapop\base_datos\df_me_gusta.csv")
        df_me_gusta.reset_index(drop=True,inplace=True)
        # Esperamos a que se haga clic en una fila de la tabla
        st.write('### Tabla me gusta')
        st.dataframe(df_me_gusta)
        selected_indices  = st.multiselect('Seleciona los indices que quieres borrar:', df_me_gusta.index)
        selected_rows = df_me_gusta.loc[selected_indices]
        st.write('### Filas seleccionadas') 
        st.table(selected_rows)
        st.write(selected_indices)
    
  

        if st.button("Borrar"):
            for indi in selected_indices:
                st.write(indi)
                df_me_gusta=df_me_gusta.drop(index=indi)
            df_me_gusta.to_csv(r"C:\Users\jonas\python\Proyecto Wallapop\base_datos\df_me_gusta.csv",index=False)
        if st.button("Actualizar"):
            st.success("Actualizado")
            

        


    if choice=="Machine Learning Model":


        st.write("Seleciona")

        
        df_machine_learnine=pd.read_csv(r"C:\Users\jonas\python\Proyecto Wallapop\df_machine_learnine.csv",sep=",")

        st.write("### Machine Learning para calcular cuanto tiempo voy a tardar en vender el producto")
        st.dataframe(df_machine_learnine)

        
        n_estimators=st.sidebar.slider(label="Número de estimadores (también para la predicción del producto):",min_value=50,max_value=300)
        learning_rate=st.sidebar.slider(label="Tasa de aprendizaje GradientBoostingRegressor:",min_value=0.01,max_value=0.3,step=0.05)
        C=st.sidebar.slider(label="C en la función SVR de scikit-learn :",min_value=1,max_value=100)
        n_neighbors=st.sidebar.slider(label="Neighbors en KNeighborsRegressor:",min_value=2,max_value=12)
        st.write("Seleciona los mejores parametros")
        
        machine_learning(n_estimators,learning_rate,C,n_neighbors)

        # Crea un campo de entrada de texto para el índice del DataFrame
        st.warning("Predecimos el tiempo de venta de un producto")
        df_Final=pd.read_csv(r"C:/Users/jonas/python/Proyecto Wallapop/df_Final_vendidos.csv",sep=",")
        st.dataframe(df_Final)
        max_indice = df_Final.shape[0] - 1
        indice = st.number_input("Introduce el índice del DataFrame (entero entre 0 y {})".format(max_indice), min_value=0, max_value=max_indice, value=0, step=1)

        if indice >=0 and indice <= max_indice :
            # Muestra la fila correspondiente al índice en el DataFrame
            
            st.write("Fila correspondiente al índice", indice, ":", df_Final.iloc[indice])
            machine_learning_porducto(n_estimators,df_Final[df_Final.index==indice],df_machine_learnine)
        


       




        



            
    if choice=="Gráficos PowerBI":
 
        st.header("Gráficos")

        st.markdown('<iframe title="general" width="1024" height="804" src="https://app.powerbi.com/view?r=eyJrIjoiNTIwNzk3ZDgtM2U4YS00ZGYyLTlkYmQtM2Y3ZDEwNWFjODQzIiwidCI6ImVkY2MxODZjLTkxZjEtNGI3YS04ZTRjLThmMWJmNzYxNmEyNSIsImMiOjl9&pageName=ReportSection" frameborder="0" allowFullScreen="true"></iframe>',unsafe_allow_html=True)


    if choice=="Gestión":
        st.header("Gestión")
        
        df_gastos_mes=df_machine_learnine=pd.read_csv(r"C:\Users\jonas\python\Proyecto Wallapop\df_gastos_mes.csv",sep=",")
        df_gastos_facturas=df_machine_learnine=pd.read_csv(r"C:\Users\jonas\python\Proyecto Wallapop\df_gastos_facturas.csv",sep=",")
        

   
        st.write("Gastos mensuales:")
        st.dataframe(df_gastos_mes)
        st.write("Facturas:")
        st.dataframe(df_gastos_facturas)
        mes=st.slider(label="Elige el mes: " ,min_value=1,max_value=12,value=3)

        st.write(f"Gastos del  mens {mes}:")
        df_gastos_mes["Fecha"]=pd.to_datetime(df_gastos_mes["Fecha"])
        df_gastos_mes["mes"]=df_gastos_mes["Fecha"].dt.month
        st.dataframe(df_gastos_mes[df_gastos_mes["mes"]==mes])


        st.write(f"Facturas del mes {mes}:")
        df_gastos_facturas["Fecha"]=pd.to_datetime(df_gastos_facturas["Fecha"])
        df_gastos_facturas["mes"]=df_gastos_facturas["Fecha"].dt.month
        st.dataframe(df_gastos_facturas[df_gastos_facturas["mes"]==mes])


        # PowerBI por fechas
        
 

    





   
    
        







    # with st.expander(label = "Posibles compras", expanded = False):

    #     data=pd.read_csv(filepath_or_buffer ="df_Final.csv", sep = ",")
            
    #     st.dataframe(data)


    # st.write("Dale vida")


  
   


if __name__ == "__main__":
    main()