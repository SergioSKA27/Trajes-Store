import streamlit as st
from streamlit_elements import mui, dashboard, lazy,sync,partial,elements
from st_xatadb_connection import XataConnection

# Create a connection to the XataDB
xata = st.connection('xata',type=XataConnection)

def handle_search():
    st.session_state.option = 'search'

def handle_add():
    st.session_state.option = 'add'

def handle_delete():
    st.session_state.option = 'delete'

if 'option' not in st.session_state:
    st.session_state.option = 'None'


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
            mui.Button(mui.icon.LocalOffer(),mui.Typography('Productos',variant='caption',sx={'margin': '2px'}),color='primary')
            mui.Button(mui.icon.LocalAtm(),mui.Typography('Ventas',variant='caption',sx={'margin': '2px'}),color='primary')

    with mui.Paper(sx={'padding': '20px', 'margin': '20px', 'display': 'flex', 'flexDirection': 'row',}):
        mui.icon.LocalOffer()
        mui.Typography('Productos',variant='h6',sx={'margin': '5px','fontSize': '3vw',})
        mui.Button(mui.icon.Search(),mui.Typography('Buscar',variant='caption',sx={'margin': '10px','fontSize': '2vw'}),color='secondary',onClick=handle_search)
        mui.Button(mui.icon.Add(),mui.Typography('Agregar',variant='caption',sx={'margin': '10px','fontSize': '2vw'}),color='secondary',onClick=handle_add)
        mui.Button(mui.icon.DeleteForever(),mui.Typography('Eliminar',variant='caption',sx={'margin': '10px','fontSize': '2vw'}),color='secondary',onClick=handle_delete)

    if st.session_state.option == 'search':
        with mui.Box(sx={'display': 'flex', 'flexDirection': 'row','alignItems': 'center'}):
            mui.icon.Search()
            mui.TextField(label='Buscar',variant='outlined',sx={'margin': '10px','fontSize': '2vw','width': '100%'})
