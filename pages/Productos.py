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


if 'gender' not in st.session_state:
    st.session_state.gender = 'Hombre'

if 'talla' not in st.session_state:
    st.session_state.talla = 26

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
    with elements('search'):
        with mui.Box(sx={'display': 'flex', 'flexDirection': 'row','alignItems': 'center'}):
            mui.icon.Search()
            mui.TextField(label='Buscar',variant='outlined',sx={'margin': '10px','fontSize': '2vw','width': '100%'})
elif st.session_state.option == 'add':
    with elements('add'):
        with mui.Box(sx={'display': 'flex', 'flexDirection': 'row','alignItems': 'center'}):
            mui.icon.Abc()
            mui.TextField(label='Clave',variant='outlined',sx={'margin': '10px','fontSize': '2vw','width': '100%'})
            mui.icon.Ballot()
            mui.TextField(label='Modelo',variant='outlined',sx={'margin': '10px','fontSize': '2vw','width': '100%'})
        with mui.Box(sx={'display': 'flex', 'flexDirection': 'row','alignItems': 'center'}):
            mui.icon.Female()
            with mui.FormControl(sx={"width":"100%", "margin": "10px"}):
                mui.InputLabel("Genero",id="genero")
                with mui.Select(value=st.session_state.gender.props.value if st.session_state.gender != "Hombre" else "Hombre"
                ,labelId="genero", id="gender", label="Genero", sx={"width":"100%"}, onChange=sync(None,'gender')) :
                    mui.MenuItem("Hombre", value="H")
                    mui.MenuItem("Mujer", value="M")
            mui.icon.ContentCut()
            mui.TextField(label='Corte',variant='outlined',sx={'margin': '10px','fontSize': '2vw','width': '100%'})

        with mui.Box(sx={'display': 'flex', 'flexDirection': 'row','alignItems': 'center'}):
            mui.icon.Straighten()
            with mui.FormControl(sx={"width":"100%", "margin": "10px"}):
                mui.InputLabel("Talla",id="talla")
                with mui.Select(value=st.session_state.talla.props.value if st.session_state.talla != 26 else 26,
                labelId="talla", id="talla", label="Talla", sx={"width":"100%"}, onChange=sync(None,'talla')) :
                    mui.MenuItem("26", value=26)
                    mui.MenuItem("28", value=28)
                    mui.MenuItem("30", value=30)
                    mui.MenuItem("32", value=32)
                    mui.MenuItem("34", value=34)
                    mui.MenuItem("36", value=36)
            mui.icon.Inventory()
            mui.TextField(label='Existencia',type='number',variant='outlined',sx={'margin': '10px','fontSize': '2vw','width': '100%'})

        with mui.Box(sx={'display': 'flex', 'flexDirection': 'row','alignItems': 'center'}):
            mui.icon.Paid()
            mui.TextField(label='Precio',type='number',variant='outlined',sx={'margin': '10px','fontSize': '2vw','width': '100%'})

        with mui.Box(sx={ '& > :not(style)': { 'm': 1 }, 'display': 'flex', 'flexDirection': 'row', 'justifyContent': 'flex-end', 'alignItems': 'right'}):
            with mui.Fab(color="primary", aria_label="add"):
                mui.icon.Save()
