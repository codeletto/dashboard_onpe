import json
import requests
import pandas as pd
import streamlit as st

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

def normalizar(registros):
    df = pd.DataFrame(registros)
    return df.rename(columns={
        "nombreAgrupacionPolitica": "Agrupacion",
        "nombreCandidato": "Candidato",
        "totalVotosValidos": "Votos",
        "porcentajeVotosValidos": "Pct_Validos",
        "porcentajeVotosEmitidos": "Pct_Emitidos",
    })

@st.cache_data(ttl=60)
def cargar_datos():
    # Intentamos datos en vivo; si la API no responde JSON, usamos el snapshot.
    try:
        respuesta = requests.get(URL, headers=HEADERS, timeout=10)
        registros = respuesta.json()["data"]
        return normalizar(registros), "vivo"
    except Exception:
        with open("data_snapshot.json", "r", encoding="utf-8") as f:
            registros = json.load(f)["data"]
        return normalizar(registros), "snapshot"

st.title("🗳️ Segunda Vuelta Presidencial 2026")
st.caption("Datos desde la API pública de la ONPE")

if st.button("🔄 Actualizar datos"):
    st.cache_data.clear()

df, fuente = cargar_datos()

if fuente == "vivo":
    st.success("🟢 Datos en vivo desde la ONPE")
else:
    st.warning("🟡 Mostrando datos guardados — la API de la ONPE solo responde "
               "a accesos desde Perú. Ejecuta la app localmente para verla en vivo.")

candidatos = df[df["Candidato"] != ""].sort_values("Votos", ascending=False)

col1, col2 = st.columns(2)
for col, (_, fila) in zip([col1, col2], candidatos.iterrows()):
    col.metric(
        label=fila["Agrupacion"],
        value=f"{fila['Pct_Validos']:.3f} %",
        delta=f"{int(fila['Votos']):,} votos",
    )

st.subheader("Votos válidos por candidato")
st.bar_chart(candidatos, x="Agrupacion", y="Votos")

st.subheader("Detalle")
st.dataframe(df, hide_index=True)