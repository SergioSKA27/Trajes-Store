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

# Invetory Dashboard

navcols = st.columns([0.4,0.2,0.2,0.1,0.1])
navcols[0].title('Inventario')
navcols[2].page_link('pages/ProductosMain.py',label='Gestion de Productos',icon='🩱',help='Modifica, elimina y busca productos en el inventario',use_container_width=True)
navcols[3].page_link('pages/Ventas.py',label='Ventas',icon='💰',help='Registra las ventas de productos en la tienda',use_container_width=True)
navcols[4].page_link('Main.py',label='Inicio',icon='🏠',help='Regresa a la pagina principal',use_container_width=True)
