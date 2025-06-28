import streamlit as st
import pandas as pd

st.set_page_config(page_title="Reporte Pendientes de Censo", layout="wide")
st.title("📋 Reporte de Clientes - Pendientes de Censo")

# Cargar archivo CSV
@st.cache_data
def load_data():
    return pd.read_csv("pendientesCenso.csv", encoding="utf-8")

df = load_data()

# Normalizar nombres de columnas (elimina espacios, baja a minúsculas, reemplaza tildes)

# Filtros desde la barra lateral
st.sidebar.header("🔍 Filtros")
subregiones = st.sidebar.multiselect("Sub-Región", df["Sub-Región"].unique())
locaciones = st.sidebar.multiselect("Locación Comercial", df["Locación Comercial"].unique())
mesas = st.sidebar.multiselect("Mesa Comercial", df["Mesa Comercial"].unique())
rutas = st.sidebar.multiselect("Ruta", df["Ruta"].unique())

# Aplicar filtros
df_filtrado = df.copy()
if subregiones:
    df_filtrado = df_filtrado[df_filtrado["Sub-Región"].isin(subregiones)]
if locaciones:
    df_filtrado = df_filtrado[df_filtrado["Locación Comercial"].isin(locaciones)]
if mesas:
    df_filtrado = df_filtrado[df_filtrado["Mesa Comercial"].isin(mesas)]
if rutas:
    df_filtrado = df_filtrado[df_filtrado["Ruta"].isin(rutas)]

# Mostrar resultados
st.markdown("### Resultados Filtrados")
st.dataframe(df_filtrado, use_container_width=True)

# Descargar como CSV
csv = df_filtrado.to_csv(index=False).encode("utf-8")
st.download_button("⬇️ Descargar CSV filtrado", csv, "pendientes_filtrados.csv", "text/csv")
