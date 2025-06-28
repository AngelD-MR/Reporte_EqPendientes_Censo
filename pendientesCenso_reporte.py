import streamlit as st
import pandas as pd

# Configuración de la página
st.set_page_config(page_title="Reporte Pendientes de Censo", layout="wide")
st.title("📋 Reporte de Clientes - Pendientes de Censo")

# Carga y limpieza de datos
@st.cache_data
def load_data():
    df = pd.read_csv("pendientesCenso.csv", encoding="utf-8")
    # Asegurarnos de que 'Serie' sea string y quitar espacios
    df["Serie"] = df["Serie"].astype(str).str.strip()
    return df

df = load_data()

# Sidebar de filtros
st.sidebar.header("🔍 Filtros")
subregiones = st.sidebar.multiselect("Sub-Región", df["Sub-Región"].dropna().unique())
locaciones  = st.sidebar.multiselect("Locación Comercial", df["Locación Comercial"].dropna().unique())
mesas       = st.sidebar.multiselect("Mesa Comercial", df["Mesa Comercial"].dropna().unique())
rutas       = st.sidebar.multiselect("Ruta", df["Ruta"].dropna().unique())

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

# Botón para descargar
csv_bytes = df_filtrado.to_csv(index=False).encode("utf-8")
st.download_button(
    label="⬇️ Descargar CSV filtrado",
    data=csv_bytes,
    file_name="pendientes_filtrados.csv",
    mime="text/csv"
)
