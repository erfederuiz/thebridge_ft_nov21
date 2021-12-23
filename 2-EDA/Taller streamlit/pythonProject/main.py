import streamlit as st
import functions as ft
import pandas as pd


ft.configuracion()

csv_name = 'red_recarga_acceso_publico_2021.csv'
datos_propios = st.sidebar.file_uploader("¿Tienes otros datos?", type=['csv'])
df = ft.cargar_datos(csv_name, datos_propios)
df.rename(columns={'Nº CARGADORES': 'cantidad'}, inplace=True)

option = st.sidebar.selectbox('Visualizar', ('Home','Datos'))
st.sidebar.text('Filtros:')
filtro_distrito = st.sidebar.selectbox('Distritos', ft.lista_columna(df, 'DISTRITO'))
selected_filtro_distrito = st.sidebar.checkbox("Filtrar distrito")

filtro_operador = st.sidebar.selectbox('Operadores', ft.lista_columna(df, 'OPERADOR'))
selected_filtro_operador = st.sidebar.checkbox("Filtrar operador")

num_cargadores = list(ft.lista_columna(df, 'cantidad'))
filtro_cargadores = st.sidebar.slider('Nº Cargadores', num_cargadores[0], num_cargadores[-1])
selected_filtro_cargadores = st.sidebar.checkbox("Filtrar por nº cargadores")

texto_filtro = ft.get_filtro(selected_filtro_distrito, 'DISTRITO', filtro_distrito, False)
texto_filtro += ft.get_filtro(selected_filtro_operador, 'OPERADOR', filtro_operador, False)
texto_filtro += ft.get_filtro(selected_filtro_cargadores, 'cantidad', filtro_cargadores, True)


st.sidebar.text(texto_filtro[:-1])

if option == 'Home':
    ft.home(df)
else:
    if selected_filtro_distrito or selected_filtro_operador or selected_filtro_cargadores:
        filtro = texto_filtro[:-1]
        df = df[df.eval(filtro)]
    if df.shape[0] > 0:
        with st.echo():
            st.write(df)
        col1, col2 = st.columns([3,2])
        with col1:
            ft.crear_mapa(df, zoom_mapa=11 if not selected_filtro_distrito else 13)
        with col2:
            if not selected_filtro_distrito:
                ft.cargadores_distrito(df)
                ft.bar_chart_variable(df, 'DISTRITO')
            if not selected_filtro_operador:
                ft.cargadores_operador(df)
                ft.bar_chart_variable(df, 'OPERADOR')

    else:
        st.warning('El filtro no produce resultados!!')