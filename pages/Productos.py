import streamlit as st
from streamlit_elements import mui, dashboard, lazy,sync,partial,elements
from streamlit_extras.switch_page_button import switch_page
from st_xatadb_connection import XataConnection
import asyncio
import requests
import base64

st.set_page_config(page_title='Inventario',page_icon='🩱',layout='wide',initial_sidebar_state='collapsed')
# Create a connection to the XataDB
xata = st.connection('xata',type=XataConnection)

st.markdown('''
<style>
[data-testid="collapsedControl"] {
        display: none
    }

#MainMenu, header, footer {visibility: hidden;}
</style>
''',unsafe_allow_html=True)


async def get_random_image():
    await asyncio.sleep(.1)
    data =  requests.get('https://source.unsplash.com/600x900/?swimsuit').content# 600
    return base64.b64encode(data).decode()

def render_card(product):
    if 'imagenProducto' in product:
        url = product['imagenProducto']['url']
    else:
        urlasync = asyncio.run(get_random_image())
        url = f'data:image/jpeg;base64,{urlasync}'
    # Render the cards
    with mui.Card(sx={'display': 'flex', 'flexDirection': 'row','alignItems': 'left','justifyContent': 'left',
    'margin': '10px','width': '100%','maxHeight': '300px'}):
        mui.CardMedia(
            component="img",
                height=194,
                image=url,
                alt=product['modelo'],
                sx={'display': 'flex', 'height': '100%','maxWidth': '70%'}
        )
        with mui.CardContent(sx={'display': 'flex', 'flexDirection': 'column','alignItems': 'left','justifyContent': 'left','width': '100%'}):
            mui.Typography(product['modelo'],variant='h5')
            mui.Typography(f'Existencia: {product["existencia"]}',variant='body',sx={'fontSize': '1rem'})
            mui.Typography(f'Precio: {product["precio"]} $',variant='body',sx={'fontSize': '1rem'})
            mui.Typography(f'Corte: {product["corte"]}',variant='body',sx={'fontSize': '1rem'})
            mui.Typography(f'Talla: {product["talla"]}',variant='body',sx={'fontSize': '1rem'})
            mui.Typography(f'Genero: {product["genero"]}',variant='body',sx={'fontSize': '1rem'})
            mui.Typography(f'Clave: {product["clave"]}',variant='caption')
            mui.Button(mui.icon.Visibility(),mui.Typography('Ver',variant='button',sx={'margin': '10px'}
            ),color='primary',variant='text',sx={'display': 'flex','alignItems': 'right','justifyContent': 'flex-end','width': '100%'})


def switch_page_main():
    st.session_state.menu_selected = 'Main'

def update_products():
    st.session_state.page_products = [xata.query("Producto",{'page': {'size': 10 }})]
    st.session_state.num_pageproducts = 0
    st.session_state.reload = True


def handle_search():
    st.session_state.option = 'search'

def handle_add():
    st.session_state.option = 'add'

def handle_delete():
    st.session_state.option = 'delete'

def handle_save():
    st.session_state.save = True
    st.session_state.modalsave = True


def update_corte(event):
    st.session_state.option = event.target.value


def update_corte(event):
    st.session_state.corte = event.target.value
def update_clave(event):
    st.session_state.clave = event.target.value
def update_modelo(event):
    st.session_state.modelo = event.target.value
def update_existencia(event):
    st.session_state.existencia = event.target.value
def update_precio(event):
    st.session_state.precio = event.target.value

def handle_modalsave():
    st.session_state.modalsave = 'Save'
def handle_closemodalsave():
    st.session_state.modalsave = False

def handle_closeimgmodal():
    st.session_state.img_modal = False

def handle_saveimg():
    st.session_state.img_modal = True

def handle_closeadd():
    st.session_state.option = 'None'

def handle_closesearch():
    st.session_state.option = 'None'

def handle_nextpage():
    data = xata.next_page('Producto',st.session_state.page_products[st.session_state.num_pageproducts],pagesize=10)
    if data is not None:
        st.session_state.page_products.append(data)
        st.session_state.num_pageproducts += 1
        st.session_state.reload = True

def handle_previouspage():
    if st.session_state.num_pageproducts > 0:
        st.session_state.num_pageproducts -= 1
        st.session_state.reload = True


if 'menu_selected' not in st.session_state:
    st.session_state.menu_selected = 'Productos'

if 'reload' not in st.session_state:
    st.session_state.reload = False

if 'imgtoast' not in st.session_state:
    st.session_state.imgtoast = False

if 'option' not in st.session_state:
    st.session_state.option = 'None'


if 'gender' not in st.session_state:
    st.session_state.gender = 'Hombre'

if 'talla' not in st.session_state:
    st.session_state.talla = 26

if 'corte' not in st.session_state:
    st.session_state.corte = None

if 'clave' not in st.session_state:
    st.session_state.clave = None

if 'modelo' not in st.session_state:
    st.session_state.modelo = None

if 'existencia' not in st.session_state:
    st.session_state.existencia = 0.0

if 'precio' not in st.session_state:
    st.session_state.precio = 0.0



if 'save' not in st.session_state:
    st.session_state.save = False

if 'modalsave' not in st.session_state:
    st.session_state.modalsave = False


if 'img_modal' not in st.session_state:
    st.session_state.img_modal = False

if 'page_products' not in st.session_state:
    st.session_state.page_products = [xata.query("Producto",{'page': {'size': 10 }})]

if 'num_pageproducts' not in st.session_state:
    st.session_state.num_pageproducts = 0

if 'last_insert' not in st.session_state:
    st.session_state.last_insert = None
# Invetory Dashboard

if st.session_state.reload:
    st.session_state.reload = False
    st.rerun()

if st.session_state.menu_selected == 'Main':
    switch_page('Main')

if st.session_state.imgtoast:
    st.toast('Imagen Guardada',icon='🎉')
    st.session_state.imgtoast = False


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
              'margin': '10px',
              'fontSize': '3vw'
            })
    with mui.Box(sx={'display': 'flex', 'flexDirection': 'row', 'justifyContent': 'flex-end', 'alignItems': 'right'}):
        with mui.ButtonGroup(variant="text", aria_label="loading button group",sx={'display': 'flex'}):
            mui.Button(mui.icon.LocalShipping(),mui.Typography('Pendientes',variant='caption',sx={'margin': '2px'}),color='primary')
            mui.Button(mui.icon.Home(),mui.Typography('Inicio',variant='caption',sx={'margin': '2px'}),color='primary',onClick=switch_page_main)
            mui.Button(mui.icon.LocalAtm(),mui.Typography('Ventas',variant='caption',sx={'margin': '2px'}),color='primary')

    with mui.Paper(sx={'display': 'flex', 'flexDirection': 'column','margin': '10px' , 'backgroundColor': 'secondary','width': '100%',},
    variant='elevation'):
        with mui.Box(sx={'display': 'flex', 'flexDirection': 'row','margin': '2px'}):
            mui.icon.LocalOffer(color='primary',sx={'fontSize': '3vw'})
            mui.Typography('Productos',variant='h6',sx={'margin': '5px','fontSize': '3.5vw','fontFamily': 'Monospace','fontWeight': 700})
        mui.Divider()
        with mui.Box(sx={'display': 'flex', 'flexDirection': 'row',}):
            mui.Button(mui.icon.Search(),mui.Typography('Buscar',variant='caption',sx={'margin': '10px','fontSize': '2vw'}),color='secondary',onClick=handle_search)
            mui.Button(mui.icon.Add(),mui.Typography('Agregar',variant='caption',sx={'margin': '10px','fontSize': '2vw'}),color='secondary',onClick=handle_add)
            mui.Button(mui.icon.DeleteForever(),mui.Typography('Eliminar',variant='caption',sx={'margin': '10px','fontSize': '2vw'}),color='secondary',onClick=handle_delete)



if st.session_state.option == 'search':
    with elements('search'):
        with mui.Box(sx={'display': 'flex', 'flexDirection': 'row','alignItems': 'center'}):
            mui.icon.Search()
            mui.TextField(label='Buscar',variant='outlined',sx={'margin': '10px','fontSize': '2vw','width': '100%'})
            mui.Button(mui.icon.Close(),color='error',variant='text',onClick=handle_closesearch)
elif st.session_state.option == 'add':
    with elements('add'):
        with mui.Box(sx={'display': 'flex', 'flexDirection': 'row','alignItems': 'left','justifyContent': 'space-between'}):
            mui.Typography(mui.icon.DataSaverOn(),'Agregar Producto',variant='h6',sx={'margin': '10px','fontSize': '3vw','fontFamily': 'Bebas Neue'})
            mui.Button(mui.icon.Close(),color='error',variant='text',onClick=handle_closeadd)
        mui.Divider()
        with mui.Box(sx={'display': 'flex', 'flexDirection': 'row','alignItems': 'center'}):
            mui.icon.Abc()
            mui.TextField(label='Clave',variant='outlined',sx={'margin': '10px','fontSize': '2vw','width': '100%'},onChange=lazy(update_clave))
            mui.icon.Ballot()
            mui.TextField(label='Modelo',variant='outlined',sx={'margin': '10px','fontSize': '2vw','width': '100%'},onChange=lazy(update_modelo))
        with mui.Box(sx={'display': 'flex', 'flexDirection': 'row','alignItems': 'center'}):
            mui.icon.Female()
            with mui.FormControl(sx={"width":"100%", "margin": "10px"}):
                mui.InputLabel("Genero",id="genero")
                with mui.Select(value=st.session_state.gender.props.value if st.session_state.gender != "Hombre" else "Hombre"
                ,labelId="genero", id="gender", label="Genero", sx={"width":"100%"}, onChange=sync(None,'gender')) :
                    mui.MenuItem("Hombre", value="H")
                    mui.MenuItem("Mujer", value="M")
            mui.icon.ContentCut()
            mui.TextField(label='Corte',variant='outlined',sx={'margin': '10px','fontSize': '2vw','width': '100%'},onChange=lazy(update_corte))

        with mui.Box(sx={'display': 'flex', 'flexDirection': 'row','alignItems': 'center'}):
            mui.icon.Straighten()
            with mui.FormControl(sx={"width":"100%", "margin": "10px"}):
                mui.InputLabel("Talla",id="talla")
                with mui.Select(value=st.session_state.talla.props.value if st.session_state.talla != 26 else 26,
                labelId="talla", id="talla", label="Talla", sx={"width":"100%"}, onChange=sync(None,'talla')):
                    mui.MenuItem("26", value=26)
                    mui.MenuItem("28", value=28)
                    mui.MenuItem("30", value=30)
                    mui.MenuItem("32", value=32)
                    mui.MenuItem("34", value=34)
                    mui.MenuItem("36", value=36)
            mui.icon.Inventory()
            mui.TextField(label='Existencia',type='number',variant='outlined',sx={'margin': '10px','fontSize': '2vw','width': '100%'},onChange=update_existencia)

        with mui.Box(sx={'display': 'flex', 'flexDirection': 'row','alignItems': 'center'}):
            mui.icon.Paid()
            mui.TextField(label='Precio',type='number',variant='outlined',sx={'margin': '10px','fontSize': '2vw','width': '100%'},onChange=update_precio)

        with mui.Box(sx={ '& > :not(style)': { 'm': 1 }, 'display': 'flex', 'flexDirection': 'row', 'justifyContent': 'flex-end', 'alignItems': 'right'}):
            with mui.Fab(color="primary", aria_label="add",onClick=handle_save):
                mui.icon.Save()

    try:
        precio = float(st.session_state.precio)
        existencia = int(st.session_state.existencia)
    except:
        st.warning('Precio y Existencia deben ser numeros')

else:
    with elements('products'):
        productss = st.session_state.page_products[st.session_state.num_pageproducts]['records']
        with mui.Stack(direction={'xs': 'column', 'sm': 'row'},justifyContent="space-between"):
            mui.Typography(mui.icon.ShoppingBasket(sx={'fontSize': '4vw',}),'Catalogo de Productos',variant='h6',sx={'margin': '0px','fontSize': '4vw','fontFamily': 'Bebas Neue'})
            with mui.ButtonGroup(variant="outlined", aria_label="loading button group",sx={'display': 'flex','alignItems': 'center','justifyContent': 'flex-end',
            'margin': '0px'}):
                mui.Button(mui.icon.Cached(),color='primary',onClick=update_products)
                mui.Button(mui.icon.ArrowBackIos(),color='primary',onClick=handle_previouspage,disabled=st.session_state.num_pageproducts == 0)
                mui.Button(mui.icon.ArrowForwardIos(),color='primary',onClick=handle_nextpage)
        mui.Divider(sx={'margin': '10px'})
        with mui.Stack(direction={'xs': 'column', 'sm': 'row'},spacing=1):
            if len(productss) > 0:
                render_card(productss[0])
            if len(productss) > 1:
                render_card(productss[1])
        with mui.Stack(direction={'xs': 'column', 'sm': 'row'},spacing=1):
            if len(productss) > 2:
                render_card(productss[2])
            if len(productss) > 3:
                render_card(productss[3])

        with mui.Stack(direction={'xs': 'column', 'sm': 'row'},spacing=1):
            if len(productss) > 4:
                render_card(productss[4])
            if len(productss) > 5:
                render_card(productss[5])

        with mui.Stack(direction={'xs': 'column', 'sm': 'row'},spacing=1):
            if len(productss) > 6:
                render_card(productss[6])
            if len(productss) > 7:
                render_card(productss[7])

        with mui.Stack(direction={'xs': 'column', 'sm': 'row'},spacing=1):
            if len(productss) > 8:
                render_card(productss[8])
            if len(productss) > 9:
                render_card(productss[9])





if st.session_state.save:
    with elements('add_modal'):
        mui.Typography('Desea guardar los cambios?',variant='h6',sx={'margin': '10px','fontSize': '3vw','fontFamily': 'Bebas Neue','display': 'flex', 'alignItems': 'right','justifyContent': 'flex-end'})
        with mui.Box(sx={'display': 'flex', 'flexDirection': 'row','alignItems': 'right','justifyContent': 'flex-end'}):
            with mui.ButtonGroup(variant="text", aria_label="loading button group",sx={'display': 'flex'}):
                mui.Button('Cancelar',color='error',onClick=handle_closemodalsave)
                mui.Button('Guardar Producto',color='primary',onClick=handle_modalsave,key='sendtoxata')
    st.session_state.save = False

if st.session_state.modalsave == 'Save':
    if st.session_state.clave is None or st.session_state.clave == '':
        st.error('Clave no puede estar vacia')
    elif st.session_state.modelo is None or st.session_state.modelo == '':
        st.error('Modelo no puede estar vacio')
    elif st.session_state.existencia is None or st.session_state.existencia == '':
        st.error('Existencia no puede estar vacia')
    elif st.session_state.precio is None or st.session_state.precio == '':
        st.error('Precio no puede estar vacio')
    elif st.session_state.corte is None or st.session_state.corte == '':
        st.error('Corte no puede estar vacio')
    else:
        with st.spinner('Guardando Producto...'):
            try:
                result = xata.insert("Producto", {
                    "clave": st.session_state.clave.upper(),
                    "modelo": st.session_state.modelo.upper(),
                    "genero": st.session_state.gender.props.value if st.session_state.gender != "Hombre" else "H",
                    "talla": st.session_state.talla.props.value if st.session_state.talla != 26 else 26,
                    "existencia": int(st.session_state.existencia),
                    "corte": st.session_state.corte.upper(),
                    "precio": float(st.session_state.precio),
                    })
                st.session_state.last_insert = result
                st.toast('Producto Guardado',icon='🎉')
            except Exception as e:
                st.error(f'Error al guardar el producto: {e}')

            st.session_state.modalsave = False

        with elements('img_modal'):
            mui.Typography('Desearia agregar una imagen al producto?',variant='h6',sx={'margin': '10px','fontSize': '3vw','fontFamily': 'Bebas Neue','display': 'flex', 'alignItems': 'right','justifyContent': 'flex-end'})
            with mui.Box(sx={'display': 'flex', 'flexDirection': 'row','alignItems': 'right','justifyContent': 'flex-end'}):
                with mui.ButtonGroup(variant="text", aria_label="loading button group",sx={'display': 'flex'}):
                    mui.Button('Cancelar',color='error',onClick=handle_closeimgmodal)
                    mui.Button('Agregar Imagen',color='primary',onClick=handle_saveimg,key='imgupload')

if st.session_state.img_modal:
    colsimg = st.columns([0.6,0.4])
    img = None
    with colsimg[1]:
        img = st.file_uploader('Subir Imagen',type=['jpg','png','jpeg'])
        if st.button('Guardar Imagen',use_container_width=True):
            if img is not None:
                with st.spinner('Guardando Imagen...'):
                    try:
                        resultimg = xata.upload_file('Producto',st.session_state.last_insert['id'],'imagenProducto',img.read(),content_type=img.type)
                        st.session_state.imgtoast = True
                        st.session_state.img_modal = False
                        st.rerun()
                    except Exception as e:
                        st.error(f'Error al guardar la imagen: {e}')
            else:
                st.toast('No se ha seleccionado ninguna imagen los productos sin imagen se muestran con una imagen aleatoria',icon='⚠️')
            st.session_state.img_modal = False

    with colsimg[0]:
        if img is not None:
            st.image(img,use_column_width=True)
        else:
            st.write('No se ha seleccionado ninguna imagen')






#st.write(st.session_state.page_products[st.session_state.num_pageproducts])


#st.session_state
