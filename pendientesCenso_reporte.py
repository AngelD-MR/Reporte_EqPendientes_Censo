import streamlit as st
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

# Sidebar: botón para reiniciar filtros
st.sidebar.header("🔍 Filtros")
reset = st.sidebar.button("🔄 Resetear Filtros")

# Si se presiona el botón, no se guarda ninguna selección previa
if reset:
    subregiones_seleccionadas = []
    locaciones_seleccionadas = []
    mesas_seleccionadas = []
    rutas_seleccionadas = []
else:
    # Filtros dependientes (encadenados)
    subregiones_seleccionadas = st.sidebar.multiselect(
        "Sub-Región", df_original["Sub-Región"].dropna().unique()
    )

    df_filtrado = df_original.copy()
    if subregiones_seleccionadas:
        df_filtrado = df_filtrado[df_filtrado["Sub-Región"].isin(subregiones_seleccionadas)]

    locaciones_seleccionadas = st.sidebar.multiselect(
        "Locación Comercial", df_filtrado["Locación Comercial"].dropna().unique()
    )
    if locaciones_seleccionadas:
        df_filtrado = df_filtrado[df_filtrado["Locación Comercial"].isin(locaciones_seleccionadas)]

    mesas_seleccionadas = st.sidebar.multiselect(
        "Mesa Comercial", df_filtrado["Mesa Comercial"].dropna().unique()
    )
    if mesas_seleccionadas:
        df_filtrado = df_filtrado[df_filtrado["Mesa Comercial"].isin(mesas_seleccionadas)]

    rutas_seleccionadas = st.sidebar.multiselect(
        "Ruta", df_filtrado["Ruta"].dropna().unique()
    )
    if rutas_seleccionadas:
        df_filtrado = df_filtrado[df_filtrado["Ruta"].isin(rutas_seleccionadas)]
else:
    df_filtrado = df_original.copy()

# Mostrar resultados
st.markdown("### Resultados Filtrados")
st.dataframe(df_filtrado, use_container_width=True)

# Descargar como CSV
csv_bytes = df_filtrado.to_csv(index=False).encode("utf-8")
st.download_button(
    label="⬇️ Descargar CSV filtrado",
    data=csv_bytes,
    file_name="pendientes_filtrados.csv",
    mime="text/csv"
)
