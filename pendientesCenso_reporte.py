mport streamlit as st
import pandas as pd

st.set_page_config(page_title="Reporte Pendientes de Censo", layout="wide")
st.title("📋 Reporte de Clientes - Pendientes de Censo")

# Cargar archivo CSV
@st.cache_data
def load_data():
    return pd.read_csv("pendientesCenso.csv", encoding="utf-8")

df = load_data()

# Normalizar nombres de columnas (elimina espacios, baja a minúsculas, reemplaza tildes)
df.columns = df.columns.str.strip().str.lower().str.replace(" ", "").str.replace("-", "")
df["serie"] = df["serie"].astype(str).str.strip()
# Filtros desde la barra lateral
st.sidebar.header("🔍 Filtros")
subregiones = st.sidebar.multiselect("Sub-Región", df["sub_región"].unique())
locaciones = st.sidebar.multiselect("Locación Comercial", df["locación_comercial"].unique())
mesas = st.sidebar.multiselect("Mesa Comercial", df["mesa_comercial"].unique())
rutas = st.sidebar.multiselect("Ruta", df["ruta"].unique())

# Aplicar filtros
df_filtrado = df.copy()
if subregiones:
    df_filtrado = df_filtrado[df_filtrado["sub_región"].isin(subregiones)]
if locaciones:
    df_filtrado = df_filtrado[df_filtrado["locación_comercial"].isin(locaciones)]
if mesas:
    df_filtrado = df_filtrado[df_filtrado["mesa_comercial"].isin(mesas)]
if rutas:
    df_filtrado = df_filtrado[df_filtrado["ruta"].isin(rutas)]

# Mostrar resultados
st.markdown("### Resultados Filtrados")
st.dataframe(df_filtrado, use_container_width=True)

# Descargar como CSV
csv = df_filtrado.to_csv(index=False).encode("utf-8")
st.download_button("⬇️ Descargar CSV filtrado", csv, "pendientes_filtrados.csv", "text/csv")
