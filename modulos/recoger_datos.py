from datos_productos import datos_productos , crear_lista_url_pag
from datos_usuario import datos_usuarios
from comprobar_vendidos import comprobar_vendidos
import streamlit as st




# crear_lista_url_pag()
st.write("Recogiendo datos de productos..")
datos_productos()

st.write("Recogiendo datos los usuarios nuevos..")
datos_usuarios()
st.success("Datos de usuarios guardados correctamente")

st.write("Comprabando si se ha vendido algun producto para información interna")
comprobar_vendidos()
st.success("Terminado proceso de comprobar vendidos")
st.success("FINALIZADO LA RECOLECCIÓN DE DATOS")