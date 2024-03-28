import streamlit as st
from st_xatadb_connection import XataConnection,XataClient
import asyncio
import requests


st.set_page_config(page_title='Inventario',page_icon='🩱',layout='wide')
xata = st.connection('xata',type=XataConnection)
client =XataClient(api_key=st.secrets['XATA_API_KEY'],db_url=st.secrets['XATA_DB_URL'])

async def get_random_image(size):
    try:
        data = await asyncio.to_thread(requests.get, f'https://source.unsplash.com/{size}/?swimsuit',timeout=1)
        return data.content
    except:
        return f'https://source.unsplash.com/{size}/?swimsuit'



@st.cache_data(ttl=60)
def search_products(s: str):
    data = xata.search_on_table('Producto', {
  "query": s,
  "fuzziness": 2,
  "prefix": "phrase",
})
    return data['records']

@st.cache_resource(experimental_allow_widgets=True)
def render_card(product,serach=False):


    with st.container(border=True):
        cols = st.columns([.6,.4])
        ad = '' if serach else '_search'
        with cols[1]:
            st.write('**Clave:** ',product['clave'])
            st.write('**Modelo:** ',product['modelo'])
            st.write('**Corte:** ',product['corte'])
            st.write('**Genero:** ',product['genero'])
            st.write('**Talla:** ',product['talla'])
            st.write('**Existencia:** ',product['existencia'])
            st.write('**Precio:** ',product['precio'],"MXN")



        with cols[0]:
            if 'imagenProducto' in product and 'url' in product['imagenProducto']:
                st.image(product['imagenProducto']['url'],caption='Imagen del producto')
            else:
                st.image(asyncio.run(get_random_image("600x600")),caption='Random Image')


tabs = st.tabs(['Ventas individuales', 'Ventas por lote'])


with tabs[0]:

    product = None
    search = st.text_input('Buscar Producto',help='Busca un producto por clave, modelo o corte')
    if search:
            data = search_products(search)
            if len(data) > 0:
                product = st.selectbox('Productos',options=data,)
    colsventas = st.columns([.6,.4])
    if search:
        with colsventas[0]:
            if product is not None:
                render_card(product,serach=True)

        with colsventas[1]:
            cantidad = st.number_input('Cantidad',min_value=1,max_value=product['existencia'],help='Cantidad de productos a vender')
            entregados = st.number_input('Entregados',min_value=0,max_value=product['existencia'],value=cantidad,help='Cantidad de productos entregados')
            fechasa = st.date_input('Fecha de entrega',help='Fecha de entrega de los productos')
            abono = -1
            if not st.toggle('Pagado',value=True):
                abono = st.number_input('Abono',min_value=0.0,step=0.01,format="%.2f",help='Abono del cliente')
            if product is not None:
                st.write('**Total:**',product['precio']*cantidad,"MXN")
                if abono != -1:
                    st.write('**Restante:**',product['precio']*cantidad-abono,"MXN")

    if product is not None:

        with colsventas[1].popover('Vender Producto',help='Vender este producto',use_container_width=True):
            st.write('**Detalle de la venta**')
            st.write('Cantidad de productos vendidos:',cantidad)
            st.write('Productos entregados:',entregados)
            st.write('Productos restantes:',cantidad-entregados)
            st.write('Total:',product['precio']*cantidad,"MXN")
            st.write('Restante:',product['precio']*cantidad-abono,"MXN")
            st.write('Fecha de entrega:',fechasa)
            if st.button('Vender',on_click=lambda: st.toast('Producto vendido',icon='🎉')):
                st.write('Producto vendido')
