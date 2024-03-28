import streamlit as st
from st_xatadb_connection import XataConnection


st.set_page_config(page_title='Inventario',page_icon='🩱',layout='wide')
xata = st.connection('xata',type=XataConnection)


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


if 'upload' not in st.session_state:
    st.session_state.upload = False


st.title('Agregar Producto',anchor=False)
st.divider()

clave = st.text_input('Clave',placeholder='Clave del producto',help='La clave del producto es unica')
modelo = st.text_input('Modelo',placeholder='Modelo del producto',help='Distintas claves pueden tener el mismo modelo')

corte = st.text_input('Corte')


cols = st.columns(2)
with cols[0]:

    genero = st.selectbox('Genero', ['Hombre', 'Mujer', 'Niño', 'Niña'],placeholder='Seleccione el genero del producto',help='Seleccione el genero del producto')

    talla = st.selectbox('Talla', ['26', '28', '30', '32', '34', '36'],placeholder='Seleccione la talla del producto',help='Seleccione la talla del producto')

with cols[1]:

    existencia = st.number_input('Existencia',min_value=0,step=1,help='Cantidad de productos en existencia')

    precio = st.number_input('Precio',min_value=0.0,step=0.01,format="%.2f",help='Precio del producto')



if st.button('Guardar',use_container_width=True):
    if validate_product(clave,modelo,corte,existencia,precio):
        try:
            result = xata.insert("Producto", {
                        "clave": clave.upper(),
                        "modelo": modelo.upper(),
                        "genero": genero.upper(),
                        "talla": int(talla),
                        "existencia": int(existencia),
                        "corte": corte.upper(),
                        "precio": float(precio),
                        })
            st.toast('Producto Guardado',icon='🎉')
        except Exception as e:
            st.error(f'Error al guardar el producto: {e}')
            st.stop()

        imgcols = st.columns([.6,.4])

        imgcols[0].write('Desearia agregar una imagen al producto?')
        no = imgcols[1].button('No',use_container_width=True)

        image = st.file_uploader('Imagen del producto',type=['jpg','png','jpeg'])

        if st.button('Guardar Imagen'):
            if image is not None:
                with st.spinner('Guardando Imagen...'):
                    try:
                        resultimg = xata.upload_file('Producto',result['id'],'imagenProducto',image.read(),content_type=image.type)
                        st.toast('Imagen Guardada',icon='🎉')
                        st.rerun()
                    except Exception as e:
                        st.error(f'Error al guardar la imagen: {e}')
                st.balloons()
        elif no:
            st.balloons()


    else:
        st.error('Error al guardar el producto')
