import streamlit as st
from streamlit_elements import mui, dashboard, lazy,sync,partial,elements,html
from streamlit_extras.switch_page_button import switch_page
from st_xatadb_connection import XataConnection
import asyncio
import requests
import base64
# Create a connection to the XataDB
xata = st.connection('xata',type=XataConnection)

async def get_random_image(size):
    asyncio.sleep(.1)
    data =  requests.get(f'https://source.unsplash.com/{size}/?swimsuit').content# 600
    return base64.b64encode(data).decode()


def switch_page_productos():
    st.session_state.menu_selected = 'Productos'

if 'menu_selected' not in st.session_state:
    st.session_state.menu_selected = 'Main'


if 'bannerquery' not in st.session_state:
    st.session_state.bannerquery = xata.query('Producto',{'columns':['id','imagenProducto.url'], 'page':{ 'size': 5}})


if st.session_state.menu_selected == 'Productos':
    switch_page('Productos')

# Invetory Dashboard

with elements('header'):
    with mui.AppBar (position='static'):
        with mui.Toolbar():
            mui.icon.ShoppingCart()
            mui.Typography('Inventario',variant='h6',sx={
              'mr': 2,
              'display': { 'xs': 'none', 'md': 'flex' },
              'fontFamily': 'monospace',
              'fontWeight': 700,
              'letterSpacing': '.3rem',
              'color': 'inherit',
              'textDecoration': 'none',
            })
    with mui.Box(sx={'display': 'flex', 'flexDirection': 'row', 'justifyContent': 'flex-end', 'alignItems': 'right'}):
        with mui.ButtonGroup(variant="text", aria_label="loading button group",sx={'display': 'flex'}):
            mui.Button(mui.icon.LocalShipping(),mui.Typography('Pendientes',variant='caption',sx={'margin': '2px'}),color='primary')
            mui.Button(mui.icon.LocalOffer(),mui.Typography('Productos',variant='caption',sx={'margin': '2px'}),color='primary',onClick=switch_page_productos)
            mui.Button(mui.icon.LocalAtm(),mui.Typography('Ventas',variant='caption',sx={'margin': '2px'}),color='primary')



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
