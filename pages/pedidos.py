import streamlit as st
import pandas as pd
from st_xatadb_connection import XataConnection,XataClient
import asyncio
import requests


st.set_page_config(page_title='Inventario',page_icon='🩱',layout='wide')
xata = st.connection('xata',type=XataConnection)
client =XataClient(api_key=st.secrets['XATA_API_KEY'],db_url=st.secrets['XATA_DB_URL'])

st.markdown("""
<style>
#MainMenu, header, footer {visibility: hidden;}
.appview-container .main .block-container
{
    padding-top: 0.5px;
    padding-left: 1rem;
    padding-right: 1rem;
    padding-bottom: 0.5rem;
}
</style>
""",unsafe_allow_html=True)

async def get_random_image(size):
    try:
        data = await asyncio.to_thread(requests.get, f'https://source.unsplash.com/{size}/?swimsuit',timeout=1)
        return data.content
    except:
        return f'https://source.unsplash.com/{size}/?swimsuit'





@st.cache_data
def get_product_by_id(product_id):
    query = xata.get('Producto',product_id)
    return query

@st.cache_resource(experimental_allow_widgets=True)
def render_order(order):
    product = get_product_by_id(order['producto']['id'])
    with st.container(border=True):
        st.write('**Clave de Producto:** ',product['clave'])
        st.write('**Cantidad:** ',order['cantidad'])
        st.write('**Entregados:** ',order['entregado'])
        st.write('**Total:** ',product['precio']*order['cantidad'],"MXN")
        st.write('**Fecha de entrega:** ',order['fechaSalida'][:10])
        if order['abono'] != -1 or order['abono'] != product['precio']*order['cantidad']:
            st.write('**Restante:** ',product['precio']*order['cantidad']-order['abono'],"MXN")

        with st.popover('Detalles del Producto',):
            cols = st.columns([0.5,0.5])
            with cols[0]:
                st.write('**Clave:** ',product['clave'])
                st.write('**Modelo:** ',product['modelo'])
                st.write('**Corte:** ',product['corte'])
                st.write('**Genero:** ',product['genero'])
                st.write('**Talla:** ',product['talla'])
                st.write('**Existencia:** ',product['existencia'])
            with cols[1]:
                if 'imagenProducto' in product and 'url' in product['imagenProducto']:
                    st.image(product['imagenProducto']['url'],caption='Imagen del producto')
                else:
                    st.image(asyncio.run(get_random_image("600x600")),caption='Random Image')

def get_pending_sells():
    query = client.data().query('Venta',
        {
            'filter':{
                'completada': {"$is": False}
                }
        })
    return query


# Invetory Dashboard

navcols = st.columns([0.4,0.2,0.2,0.1,0.1])
navcols[0].title('Inventario')
navcols[2].page_link('pages/ProductosMain.py',label='Gestion de Productos',icon='🩱',help='Modifica, elimina y busca productos en el inventario',use_container_width=True)
navcols[3].page_link('pages/Ventas.py',label='Ventas',icon='💰',help='Registra las ventas de productos en la tienda',use_container_width=True)
navcols[4].page_link('Main.py',label='Inicio',icon='🏠',help='Regresa a la pagina principal',use_container_width=True)





psells = get_pending_sells()
st.write(psells)

tabbs = st.tabs(['Ventas Incompletas','Pedidos Pendientes'])

with tabbs[0]:
    with st.container(border=True):
        st.subheader('Ventas Incompletas')
        st.divider()
        scols = st.columns([0.2,0.2,0.2,0.2,0.2])
        k = 0
        for sell in psells['records']:
            with scols[k]:
                render_order(sell)
            k += 1
            if k > 4:
                k = 0
