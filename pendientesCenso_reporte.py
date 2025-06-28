import streamlit as st
import pandas as pd
import unicodedata

st.set_page_config(page_title="Reporte Pendientes de Censo", layout="wide")
st.title("📋 Reporte de Clientes - Pendientes de Censo")

# Función para limpiar tildes
def normalizar_columna(col):
    col = col.strip()
    col = unicodedata.normalize("NFKD", col).encode("ascii", errors="ignore").decode("utf-8")
    return col

# Cargar archivo CSV
@st.cache_data
def load_data():
    df = pd.read_csv("pendientesCenso.csv", encoding="utf-8")
    df.columns = [normalizar_columna(col) for col in df.columns]
    return df

df = load_data()

# Mostrar columnas en pantalla (debug opcional)
# st.write("🧠 Columnas normalizadas:", df.columns.tolist())

# Asegurar que la columna 'Serie' exista y esté limpia
if "Serie" in df.columns:
    df["Serie"] = df["Serie"].astype(str).str.strip()
else:
    st.error("La columna 'Serie' no se encontró en el archivo.")
    st.stop()

# Filtros desde la barra lateral
st.sidebar.header("🔍 Filtros")

# Nos aseguramos de usar los nombres ya normalizados
subregiones = st.sidebar.multiselect("Sub-Región", df["Sub-Region"].unique() if "Sub-Region" in df.columns else [])
locaciones = st.sidebar.multiselect("Locación Comercial", df["Locacion Comercial"].unique() if "Locacion Comercial" in df.columns else [])
mesas = st.sidebar.multiselect("Mesa Comercial", df["Mesa Comercial"].unique() if "Mesa Comercial" in df.columns else [])
rutas = st.sidebar.multiselect("Ruta", df["Ruta"].unique() if "Ruta" in df.columns else [])

# Aplicar filtros
df_filtrado = df.copy()
if subregiones:
    df_filtrado = df_filtrado[df_filtrado["Sub-Region"].isin(subregiones)]
if locaciones:
    df_filtrado = df_filtrado[df_filtrado["Locacion Comercial"].isin(locaciones)]
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
