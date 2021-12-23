import streamlit as st
import pandas as pd

click = st.button("Haz click")
st.write(click)
# Al pulsar cualquier  botón se recarga toda la página
if click:
    st.write("Se ha pulsado el botón")
    contento = st.button("Haz click si estas contento")
    if contento:
        #El código nunca entrará aquí
        st.write("Estoy tela contento")
else:
    st.write("Estoy triste")


