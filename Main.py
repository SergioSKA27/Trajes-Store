import streamlit as st
from streamlit_elements import mui, dashboard, lazy,sync,partial,elements,html
from streamlit_extras.switch_page_button import switch_page
from st_xatadb_connection import XataConnection
import asyncio
import requests
import base64

st.set_page_config(page_title='Inventario',page_icon='🩱',layout='wide',initial_sidebar_state='collapsed')
# Create a connection to the XataDB
xata = st.connection('xata',type=XataConnection)

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
    data = await asyncio.to_thread(requests.get, f'https://source.unsplash.com/{size}/?swimsuit')
    return base64.b64encode(data.content).decode()


def switch_page_productos():
    st.session_state.menu_selected = 'Productos'

if 'menu_selected' not in st.session_state:
    st.session_state.menu_selected = 'Main'


if 'bannerquery' not in st.session_state:
    st.session_state.bannerquery = xata.query('Producto',{'columns':['id','imagenProducto.url'], 'page':{ 'size': 5}})



# Invetory Dashboard

navcols = st.columns([0.4,0.2,0.2,0.1,0.1])
navcols[0].title('Inventario')
navcols[2].page_link('pages/ProductosMain.py',label='Gestion de Productos',icon='🩱',help='Modifica, elimina y busca productos en el inventario',use_container_width=True)
navcols[3].page_link('pages/Ventas.py',label='Ventas',icon='💰',help='Registra las ventas de productos en la tienda',use_container_width=True)
navcols[4].page_link('pages/pedidos.py',label='Pedidos',icon='🚚',help='Revise los pedidos pendientes y entregados de la tienda',use_container_width=True)


@st.cache_resource(experimental_allow_widgets=True,ttl=60)
def banner():
    with elements('banner'):
        mui.Divider()
        imgs =  st.session_state.bannerquery['records']
        with mui.ImageList(sx={ 'width': '100%', 'height': '100%' },variant="quilted",cols=4,rowHeight="auto"):
            with mui.ImageListItem(key='img', cols=2, rows=2):
                if len(imgs) > 0 and 'imagenProducto' in imgs[0] and 'url' in imgs[0]['imagenProducto']:
                    img1 = imgs[0]['imagenProducto']['url']
                    html.img(src=img1, alt='swimsuit',style={'width':'100%','height':'100%'})
                else:
                    img1 = asyncio.run(get_random_image('1920x1080'))
                    html.img(src=f"data:image/png;base64,{img1}",alt='swimsuit',style={'width':'100%','height':'100%'})

            with mui.ImageListItem(key='img-2'):
                img2 = asyncio.run(get_random_image('600x600'))
                html.img(src=f"data:image/png;base64,{img2}",
                alt='swimsuit',style={'width':'100%','height':'100%'})

            with mui.ImageListItem(key='img-3',):
                img3 = asyncio.run(get_random_image('600x600'))
                html.img(src=f"data:image/png;base64,{img3}",
                alt='swimsuit',style={'width':'100%','height':'100%'})

            with mui.ImageListItem(key='img-4',cols=2):
                if len(imgs) > 1 and 'imagenProducto' in imgs[1] and 'url' in imgs[1]['imagenProducto']:
                    img4 = imgs[1]['imagenProducto']['url']
                    html.img(src=img4, alt='swimsuit',style={'width':'100%','height':'100%'})
                else:
                    img4 = asyncio.run(get_random_image('1920x1080'))
                    html.img(src=f"data:image/png;base64,{img4}",alt='swimsuit',style={'width':'100%','height':'100%'})

            with mui.ImageListItem(key='img-5',cols=2):
                if len(imgs) > 2 and 'imagenProducto' in imgs[2] and 'url' in imgs[2]['imagenProducto']:
                    img5 = imgs[2]['imagenProducto']['url']
                    html.img(src=img5, alt='swimsuit',style={'width':'100%','height':'100%'})
                else:
                    img5 = asyncio.run(get_random_image('1920x1080'))
                    html.img(src=f"data:image/png;base64,{img5}",alt='swimsuit',style={'width':'100%','height':'100%'})

            with mui.ImageListItem(key='img-6', cols=2, rows=2):
                img6 = asyncio.run(get_random_image('1920x1080'))
                html.img(src=f"data:image/png;base64,{img6}",
                alt='swimsuit',style={'width':'100%','height':'100%'})

            with mui.ImageListItem(key='img-7',):
                img7 = asyncio.run(get_random_image('1920x1080'))
                html.img(src=f"data:image/png;base64,{img7}",
                alt='swimsuit',style={'width':'100%','height':'100%'})

            with mui.ImageListItem(key='img-8',):
                if len(imgs) > 3 and 'imagenProducto' in imgs[3] and 'url' in imgs[3]['imagenProducto']:
                    img8 = imgs[3]['imagenProducto']['url']
                    html.img(src=img8, alt='swimsuit',style={'width':'100%','height':'100%'})
                else:
                    img8 = asyncio.run(get_random_image('1920x1080'))
                    html.img(src=f"data:image/png;base64,{img8}",alt='swimsuit',style={'width':'100%','height':'100%'})
            with mui.ImageListItem(key='img-9',cols=2):
                img9 = asyncio.run(get_random_image('1920x1080'))
                html.img(src=f"data:image/png;base64,{img9}",
                alt='swimsuit',style={'width':'100%','height':'100%'})

            with mui.ImageListItem(key='img-10',cols=1,rows=1):
                if len(imgs) > 4 and 'imagenProducto' in imgs[4] and 'url' in imgs[4]['imagenProducto']:
                    img10 = imgs[4]['imagenProducto']['url']
                    html.img(src=img10, alt='swimsuit',style={'width':'100%','height':'100%'})
                else:
                    img10 = asyncio.run(get_random_image('1920x1080'))
                    html.img(src=f"data:image/png;base64,{img10}",alt='swimsuit',style={'width':'100%','height':'100%'})

            with mui.ImageListItem(key='img-11'):
                img11 = asyncio.run(get_random_image('1920x1080'))
                html.img(src=f"data:image/png;base64,{img11}",
                alt='swimsuit',style={'width':'100%','height':'100%'})


banner()
