import streamlit as st
import pandas as pd
st.write('Todo va bien')
"Hola que tal todo?"

mi_df = pd.DataFrame({'A':[1,2], 'B':[2,3]})
st.write(mi_df)

st.code("""
mi_df = pd.DataFrame({'A':[1,2], 'B':[2,3]})
st.write(mi_df)
class Miclase:
    def __init__(self):
        pass
""", language="python")

st.table(mi_df)

st.metric(label="Número de alumnnos", value=15, delta="2")

selected = st.checkbox("Haz click")
st.write(selected)
# Al pulsar cualquier  botón se recarga toda la página
if selected:
    st.write("Se ha pulsado el botón")
    contento = st.button("Haz click si estas contento")
    if contento:
        #El código nunca entrará aquí
        st.write("Estoy tela contento")
else:
    st.write("Estoy triste")

option = st.sidebar.selectbox('How would you like to be connected?', ('Email','Home Phone', 'Mobile Phone'))
st.write('You selected:', option)

col1, col2 = st.columns(2)

col1.write('Primera columna')
col2.write('Segunda columna')

with col1:
    st.write("Estamos en la primera columna")
    st.write(mi_df)

with col2:
    st.write("Estamos en la segunda columna")
    st.write(mi_df)