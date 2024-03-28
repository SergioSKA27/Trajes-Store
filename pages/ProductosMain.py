import streamlit as st
from st_xatadb_connection import XataConnection,XataClient
import time
import asyncio
import requests
import base64


st.set_page_config(page_title='Inventario',page_icon='🩱',layout='wide')
xata = st.connection('xata',type=XataConnection)
client =XataClient(api_key=st.secrets['XATA_API_KEY'],db_url=st.secrets['XATA_DB_URL'])


async def get_random_image(size):
    data = await asyncio.to_thread(requests.get, f'https://source.unsplash.com/{size}/?swimsuit')
    return data.content


def validate_product(clave,modelo,corte,existencia,precio):
    if clave == '':
        st.error('La clave del producto no puede estar vacia')
        return False
    if modelo == '':
        st.error('El modelo del producto no puede estar vacio')
        return False
    if corte == '':
        st.error('El corte del producto no puede estar vacio')
        return False
    if existencia == 0:
        st.error('La existencia del producto no puede ser 0')
        return False
    if precio == 0:
        st.error('El precio del producto no puede ser 0')
        return False
    return True


def has_changed(product,clave,modelo,corte,genero,talla,existencia,precio):
    if product['clave'] != clave:
        return True
    if product['modelo'] != modelo:
        return True
    if product['corte'] != corte:
        return True
    if product['genero'] != genero:
        return True
    if product['talla'] != talla:
        return True
    if product['existencia'] != existencia:
        return True
    if product['precio'] != precio:
        return True
    return False
def reload_data():
    st.session_state.products_data = [xata.query("Producto",{'page': {'size': 9 }})]

@st.cache_resource(experimental_allow_widgets=True)
def render_card(product):


    with st.container(border=True):
        cols = st.columns([.6,.4])
        with cols[1]:
            st.write('**Clave:** ',product['clave'])
            st.write('**Modelo:** ',product['modelo'])
            st.write('**Corte:** ',product['corte'])
            st.write('**Genero:** ',product['genero'])
            st.write('**Talla:** ',product['talla'])
            st.write('**Existencia:** ',product['existencia'])
            st.write('**Precio:** ',product['precio'],"MXN")


        with cols[1].popover('Editar Producto',help='Editar este producto',use_container_width=True):
            nclave = st.text_input('Clave',value=product['clave'],help='La clave del producto es unica',key=f"clave_{product['id']}")
            nmodelo = st.text_input('Modelo',value=product['modelo'],help='Distintas claves pueden tener el mismo modelo',key=f"modelo_{product['id']}")
            ncorte = st.text_input('Corte',value=product['corte'],key=f"corte_{product['id']}")
            ngenero = st.selectbox('Genero', ['Hombre', 'Mujer', 'Niño', 'Niña','M','H'],index=['Hombre', 'Mujer', 'Niño', 'Niña','M','H'].index(product['genero'].capitalize()),help='Seleccione el genero del producto',key=f"genero_{product['id']}")
            ntalla = st.selectbox('Talla', [26, 28, 30, 32, 34, 36],index=[26, 28, 30, 32, 34, 36].index(product['talla']),help='Seleccione la talla del producto',key=f"talla_{product['id']}")
            nexistencia = st.number_input('Existencia',min_value=0,step=1,value=product['existencia'],help='Cantidad de productos en existencia',key=f"existencia_{product['id']}")
            nprecio = st.number_input('Precio',min_value=0.0,step=0.01,format="%.2f",value=float(product['precio']),help='Precio del producto',key=f"precio_{product['id']}")
            if has_changed(product,nclave,nmodelo,ncorte,ngenero,ntalla,nexistencia,nprecio) and validate_product(nclave,nmodelo,ncorte,nexistencia,nprecio):
                if st.button('Guardar Cambios',key=f"save_{product['id']}"):
                    pass
        with cols[0]:
            if 'imagenProducto' in product and 'url' in product['imagenProducto']:
                st.image(product['imagenProducto']['url'],caption='Imagen del producto')
            else:
                st.image(asyncio.run(get_random_image("600x600")),caption='Random Image')

        with cols[0].popover('Eliminar Producto',help='Eliminar este producto de la base de datos',use_container_width=True):
            if st.button(':red[Eliminar Producto]',key=f"delete_{product['id']}"):
                st.write('¿Esta seguro de eliminar el producto? este cambio no se puede deshacer')
                st.button('Si, eliminar')

                st.button('Cancelar')

if 'products_data' not in st.session_state:
    st.session_state.products_data = [xata.query("Producto",{'page': {'size': 9 }})]

if 'page_products' not in st.session_state:
    st.session_state.page_products = 0



colspages = st.columns(3)

k = 0

for chunk in st.session_state.products_data:
    dchunk = chunk['records']

    for i in dchunk:
        with colspages[k]:
            render_card(i)
        k += 1
        if k == 3:
            k = 0

if st.button('Cargar mas productos',use_container_width=True):
    datas = xata.next_page('Producto',st.session_state.products_data[-1],9)
    if datas:
        st.session_state.products_data.append(datas)
    else:
        st.error('No hay mas productos para mostrar')

    st.rerun()

st.image(asyncio.run(get_random_image("600x600")),caption='Random Image')
