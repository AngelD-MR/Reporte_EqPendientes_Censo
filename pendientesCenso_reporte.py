mport streamlit as st
import pandas as pd

# Configuración de la página
st.set_page_config(page_title="Reporte Pendientes de Censo", layout="wide")
st.title("📋 Reporte de Clientes - Pendientes de Censo")

# Cargar datos
@st.cache_data
def load_data():
    df = pd.read_csv("pendientesCenso.csv", encoding="utf-8")
    df["Serie"] = df["Serie"].astype(str).str.strip()
    return df

df_original = load_data()

# Sidebar de filtros
st.sidebar.header("🔍 Filtros")
if st.sidebar.button("🔄 Resetear filtros"):
    st.experimental_rerun()  # Reinicia la app para limpiar selección

# Filtro 1: Sub-Región
subregiones = st.sidebar.multiselect(
    "Sub-Región",
    options=sorted(df_original["Sub-Región"].dropna().unique()),
    key="subregiones"
)

# Filtrar después de Sub-Región
df_filtrado = df_original.copy()
if subregiones:
    df_filtrado = df_filtrado[df_filtrado["Sub-Región"].isin(subregiones)]

# Filtro 2: Locación Comercial
locaciones = st.sidebar.multiselect(
    "Locación Comercial",
    options=sorted(df_filtrado["Locación Comercial"].dropna().unique()),
    key="locaciones"
)
if locaciones:
    df_filtrado = df_filtrado[df_filtrado["Locación Comercial"].isin(locaciones)]

# Filtro 3: Mesa Comercial
mesas = st.sidebar.multiselect(
    "Mesa Comercial",
    options=sorted(df_filtrado["Mesa Comercial"].dropna().unique()),
    key="mesas"
)
if mesas:
    df_filtrado = df_filtrado[df_filtrado["Mesa Comercial"].isin(mesas)]

# Filtro 4: Ruta
rutas = st.sidebar.multiselect(
    "Ruta",
    options=sorted(df_filtrado["Ruta"].dropna().unique()),
    key="rutas"
)
if rutas:
    df_filtrado = df_filtrado[df_filtrado["Ruta"].isin(rutas)]

# Mostrar resultados
st.markdown("### 📊 Resultados Filtrados")
st.dataframe(df_filtrado, use_container_width=True)

# Descargar CSV filtrado
csv = df_filtrado.to_csv(index=False).encode("utf-8")
st.download_button(
    "⬇️ Descargar CSV filtrado",
    csv,
    "pendientes_filtrados.csv",
    "text/csv"
)
