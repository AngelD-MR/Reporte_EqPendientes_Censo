import streamlit as st
import pandas as pd

st.set_page_config(page_title="Reporte Comercial", layout="wide")
st.title("📊 Reporte de Equipos pendientes de censo")

@st.cache_data
def load_data():
    return pd.read_csv("pendientesCenso.csv", encoding="utf-8")

df = load_data()

st.sidebar.header("🔍 Filtros")
subregiones = st.sidebar.multiselect("Sub-región", df["subregión"].unique())
locaciones = st.sidebar.multiselect("Locación Comercial", df["locación comercial"].unique())
mesas = st.sidebar.multiselect("Mesa Comercial", df["Mesa Comercial"].unique())
rutas = st.sidebar.multiselect("Ruta", df["ruta"].unique())

df_filtrado = df.copy()
if subregiones:
    df_filtrado = df_filtrado[df_filtrado["subregión"].isin(subregiones)]
if locaciones:
    df_filtrado = df_filtrado[df_filtrado["locación comercial"].isin(locaciones)]
if mesas:
    df_filtrado = df_filtrado[df_filtrado["mesa comercial"].isin(mesas)]
if rutas:
    df_filtrado = df_filtrado[df_filtrado["ruta"].isin(rutas)]

st.markdown("### 📋 Resultados Filtrados")
st.dataframe(df_filtrado, use_container_width=True)

csv = df_filtrado.to_csv(index=False).encode("utf-8")
st.download_button("⬇️ Descargar resultados filtrados", csv, "PendientesCenso_filtrados.csv", "text/csv")
