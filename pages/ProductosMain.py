import streamlit as st
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
        data = await asyncio.to_thread(requests.get, f'https://source.unsplash.com/{size}/?swimsuit',timeout=3)
        return data.content
    except:
        return f'https://source.unsplash.com/{size}/?swimsuit'


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
    data = [xata.query("Producto",{'page': {'size': 9 }})]

    while len(data) < len(st.session_state.products_data):
        ap = xata.next_page('Producto',data[-1],9)
        if ap:
            data.append(ap)
        else:
            break

    st.session_state.products_data = data
    st.session_state.page_products = 0
    st.session_state.search = []


@st.cache_data(ttl=60)
def search_products(s: str):
    data = xata.search_on_table('Producto', {
  "query": s,
  "fuzziness": 2,
  "prefix": "phrase",
})
    return data['records']



def update_product(product,nwproduct,nimg):
    res = client.records().update("Producto",product['id'],nwproduct)
    print(res)
    if res.status_code != 200:
        st.toast('Error al actualizar el producto',icon='⚠️')
    else:
        st.toast('Producto actualizado',icon='🎉')
        if nimg is None:
            reload_data()

    if nimg:
        res = client.files().put("Producto",product['id'],'imagenProducto',nimg,content_type=nimg.type)
        print(res)
        if res.status_code != 200:
            st.toast('Error al subir la imagen',icon='⚠️')
        else:
            st.toast('Imagen subida',icon='🎉')
            reload_data()


def del_product(productid=None):
    res = client.records().delete("Producto",productid)
    print(res)
    if len(res)  > 0:
        st.toast('Error al eliminar el producto',icon='⚠️')
    else:
        st.toast('Producto eliminado',icon='🎉')
        reload_data()

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


        with cols[1].popover('Editar Producto',help='Editar este producto',use_container_width=True):
            nclave = st.text_input('Clave',value=product['clave'],help='La clave del producto es unica',key=f"clave_{product['id']}"+ad)
            nmodelo = st.text_input('Modelo',value=product['modelo'],help='Distintas claves pueden tener el mismo modelo',key=f"modelo_{product['id']}"+ad)
            ncorte = st.text_input('Corte',value=product['corte'],key=f"corte_{product['id']}"+ad)
            ngenero = st.selectbox('Genero', ['Hombre', 'Mujer', 'Niño', 'Niña','M','H'],index=['Hombre', 'Mujer', 'Niño', 'Niña','M','H'].index(product['genero'].capitalize()),help='Seleccione el genero del producto',key=f"genero_{product['id']}"+ad)
            ntalla = st.selectbox('Talla', [26, 28, 30, 32, 34, 36],index=[26, 28, 30, 32, 34, 36].index(product['talla']),help='Seleccione la talla del producto',key=f"talla_{product['id']}"+ad)
            nexistencia = st.number_input('Existencia',min_value=0,step=1,value=product['existencia'],help='Cantidad de productos en existencia',key=f"existencia_{product['id']}"+ad)
            nprecio = st.number_input('Precio',min_value=0.0,step=0.01,format="%.2f",value=float(product['precio']),help='Precio del producto',key=f"precio_{product['id']}"+ad)
            imgn = st.file_uploader('Imagen del producto',type=['jpg','png','jpeg'],key=f"imagen_{product['id']}"+ad)

            if (has_changed(product,nclave,nmodelo,ncorte,ngenero,ntalla,nexistencia,nprecio) and validate_product(nclave,nmodelo,ncorte,nexistencia,nprecio)) or imgn is not None:
                np = {'clave': nclave.upper(), 'modelo': nmodelo.upper(), 'corte': ncorte.upper(), 'genero': ngenero.upper(), 'talla': int(ntalla), 'existencia': int(nexistencia), 'precio': float(nprecio)}
                if st.button('Guardar Cambios',key=f"save_{product['id']}"+ad,on_click=update_product,args=(product,np,imgn)):
                    st.rerun()

        with cols[0]:
            if 'imagenProducto' in product and 'url' in product['imagenProducto']:
                st.image(product['imagenProducto']['url'],caption='Imagen del producto')
            else:
                st.image(asyncio.run(get_random_image("600x600")),caption='Random Image')

        with cols[0].popover('Eliminar Producto',help='Eliminar este producto de la base de datos',use_container_width=True):
            if st.button(':red[Eliminar Producto]',key=f"delete_{product['id']}"+ad):
                st.write('¿Esta seguro de eliminar el producto? este cambio no se puede deshacer')
                if st.button('Si, eliminar',on_click=del_product,kwargs={'productid': product['id']},key=f"delete_confirm_{product['id']}"+ad):
                    st.rerun()

                st.button('Cancelar')

if 'products_data' not in st.session_state:
    st.session_state.products_data = [xata.query("Producto",{'page': {'size': 9 }})]

if 'page_products' not in st.session_state:
    st.session_state.page_products = 0

if 'search' not in st.session_state:
    st.session_state.search = []


navcols = st.columns([0.5,0.2,0.1,0.1,0.1])
navcols[0].subheader('🩱Gestion de Productos')
navcols[4].page_link('Main.py',label='Inicio',icon='🏠',help='Regresa a la pagina principal',use_container_width=True)
navcols[1].page_link('pages/simpleProducts.py',label='Agregar Producto',icon='➕',help='Agrega un producto al inventario',use_container_width=True)
navcols[2].page_link('pages/Ventas.py',label='Ventas',icon='💰',help='Registra las ventas de productos en la tienda',use_container_width=True)
navcols[3].page_link('pages/pedidos.py',label='Pedidos',icon='🚚',help='Revise los pedidos pendientes y entregados de la tienda',use_container_width=True)



tabs = st.tabs(['Productos','Buscar'])

with tabs[0]:
    _,rel = st.columns([.8,.2])
    rel.button('Actualizar Productos',on_click=reload_data,use_container_width=True)
    colspages = st.columns(3)
    if st.session_state.page_products == -1:
        lascols = st.columns([.4,.2,.4])
        lascols[1].image('https://i.pinimg.com/originals/7b/08/64/7b0864456aab583193c7776d80a4c493.gif',caption='No hay mas productos',use_column_width=True)

    if st.button('Cargar mas productos',use_container_width=True,disabled=st.session_state.page_products == -1):
        datas = xata.next_page('Producto',st.session_state.products_data[-1],9)
        if datas:
            st.session_state.products_data.append(datas)
        else:
            st.session_state.page_products = -1

        st.rerun()

k = 0
k2 = 0

with tabs[1]:
    srch = st.text_input('Buscar Producto',help='Busca un producto por clave o modelo')
    if st.button('Buscar',use_container_width=True):
        st.session_state.search = search_products(srch)
    scols = st.columns(3)


for i in st.session_state.search:
    with scols[k2]:
        render_card(i,True)
    k2 += 1
    if k2 == 3:
        k2 = 0


for chunk in st.session_state.products_data:
    dchunk = chunk['records']

    for i in dchunk:
        with colspages[k]:
            render_card(i)
        k += 1
        if k == 3:
            k = 0



#st.image(asyncio.run(get_random_image("600x600")),caption='Random Image')
