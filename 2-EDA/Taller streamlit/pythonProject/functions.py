import streamlit as st
import pandas as pd
from streamlit_folium import folium_static
import folium

titulo = "Cargatron"


def configuracion():

    st.set_page_config(page_title=titulo, page_icon=':electric_plug', layout="wide", initial_sidebar_state="auto",
                       menu_items=None)


def home(df):
    st.title(titulo)
    st.subheader('Lista de cargadores de coches eléctricos en Madrid')
    with st.expander("About..."):
        st.write("""
            Aunque a Julia no le guste el rollo cargadores...\n
            Lorem Ipsum is simply dummy text of the printing and typesetting industry. Lorem Ipsum has been the industry's standard dummy text ever since the 1500s, when an unknown printer took a galley of type and scrambled it to make a type specimen book. It has survived not only five centuries, but also the leap into electronic typesetting, remaining essentially unchanged. It was popularised in the 1960s with the release of Letraset sheets containing Lorem Ipsum passages, and more recently with desktop publishing software like Aldus PageMaker including versions of Lorem Ipsum.
        """)
    st.image('cargador-de-cable-gordo.jpg')


@st.cache()
def cargar_datos(csv_path, datos_propios):
    datos_cargar = csv_path

    if datos_propios != None:
        datos_cargar = datos_propios

    df = pd.read_csv(datos_cargar, sep=';')

    return df


def crear_mapa(df, zoom_mapa):
    st.header("Ubicación de cargadores")
    df_map = df[['latidtud', 'longitud']].copy()
    df_map.rename(columns={'latidtud': 'lat', 'longitud': 'lon'}, inplace=True)
    st.map(df_map, zoom=zoom_mapa)


def cargadores_distrito(df):
    st.header("Cargadores por distrito")
    df_bar1 = df[['DISTRITO', 'cantidad']].copy()
    df_bar1.rename(columns={'DISTRITO': 'distrito'}, inplace=True)
    df_bar1 = df_bar1.groupby('distrito').sum()
    #st.write(df_bar1)
    st.bar_chart(df_bar1)

def cargadores_operador(df):
    st.header("Cargadores por operador")
    df_bar2 = df[['OPERADOR', 'cantidad']].copy()
    df_bar2.rename(columns={ 'OPERADOR': 'operador'}, inplace=True)
    df_bar2 = df_bar2.groupby('operador').sum()
    #st.write(df_bar2)
    st.bar_chart(df_bar2)

def bar_chart_variable(df, column):
    columna_group = 'DISTRITO' if column == 'OPERADOR' else 'OPERADOR'
    cargadores_por_ope = df.groupby(column)['cantidad'].count()
    st.bar_chart(cargadores_por_ope)


def lista_columna(df, columna):
    lista = df[columna].tolist()
    return set(lista)


def get_filtro(chequeado, columna, valor, isint):
    if chequeado and not isint:
        return f' {columna} == \'{valor}\'' + ' &'
    elif chequeado and isint:
        return f' {columna} == {valor}' + ' &'
    else:
        return ""

#def generar_eval(filtro_distrito, filtro_operador, filtro_cargadores):
