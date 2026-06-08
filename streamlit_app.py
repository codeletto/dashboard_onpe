import requests
import pandas as pd
import streamlit as st

# --- Configuración de la página ---
st.set_page_config(page_title="Resultados Segunda Vuelta 2026", layout="centered")

URL = "https://resultadosegundavuelta.onpe.gob.pe/presentacion-backend/eleccion-presidencial/participantes-ubicacion-geografica-nombre?idEleccion=10&tipoFiltro=eleccion"

HEADERS = {
    "accept": "*/*",
    "accept-language": "es-ES,es;q=0.9,en;q=0.8",
    "content-type": "application/json",
    "priority": "u=1, i",
    "referer": "https://resultadosegundavuelta.onpe.gob.pe/main/presidenciales",
    "sec-ch-ua": '"Google Chrome";v="149", "Chromium";v="149", "Not)A;Brand";v="24"',
    "sec-ch-ua-mobile": "?0",
    "sec-ch-ua-platform": '"Windows"',
    "sec-fetch-dest": "empty",
    "sec-fetch-mode": "cors",
    "sec-fetch-site": "same-origin",
    "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/149.0.0.0 Safari/537.36",
}

# --- Función que trae los datos ---
# @st.cache_data guarda el resultado por 60 segundos (ttl=60) para no
# pedirle a la ONPE en cada clic; pasados los 60s, vuelve a traer datos frescos.
@st.cache_data(ttl=60)
def traer_datos():
    respuesta = requests.get(URL, headers=HEADERS)
    df = pd.DataFrame(respuesta.json()["data"])
    df = df.rename(columns={
        "nombreAgrupacionPolitica": "Agrupacion",
        "nombreCandidato": "Candidato",
        "totalVotosValidos": "Votos",
        "porcentajeVotosValidos": "Pct_Validos",
        "porcentajeVotosEmitidos": "Pct_Emitidos",
    })
    return df

# --- Título ---
st.title("🗳️ Segunda Vuelta Presidencial 2026")
st.caption("Datos en tiempo real desde la API pública de la ONPE")

# --- Botón para actualizar manualmente ---
if st.button("🔄 Actualizar datos"):
    st.cache_data.clear()   # borra la caché para forzar una petición nueva

df = traer_datos()

# Separamos a los candidatos de los votos nulos/blancos
candidatos = df[df["Candidato"] != ""].sort_values("Votos", ascending=False)

# --- Tarjetas con el resultado de cada candidato ---
col1, col2 = st.columns(2)
for col, (_, fila) in zip([col1, col2], candidatos.iterrows()):
    col.metric(
        label=fila["Agrupacion"],
        value=f"{fila['Pct_Validos']:.3f} %",
        delta=f"{int(fila['Votos']):,} votos",
    )

# --- Gráfico de barras ---
st.subheader("Votos válidos por candidato")
st.bar_chart(candidatos, x="Agrupacion", y="Votos")

# --- Tabla completa ---
st.subheader("Detalle")
st.dataframe(df, hide_index=True)