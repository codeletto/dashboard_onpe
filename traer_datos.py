import requests
import pandas as pd

url = "https://resultadosegundavuelta.onpe.gob.pe/presentacion-backend/eleccion-presidencial/participantes-ubicacion-geografica-nombre?idEleccion=10&tipoFiltro=eleccion"

headers = {
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

respuesta = requests.get(url, headers=headers)
datos = respuesta.json()

# 1. Excavamos hasta la lista de registros
registros = datos["data"]

# 2. La lista de registros se convierte en tabla en UNA línea
df = pd.DataFrame(registros)

# 3. Nos quedamos solo con las columnas útiles
df = df[[
    "nombreAgrupacionPolitica",
    "nombreCandidato",
    "totalVotosValidos",
    "porcentajeVotosValidos",
    "porcentajeVotosEmitidos",
]]

# 4. Les ponemos nombres legibles
df = df.rename(columns={
    "nombreAgrupacionPolitica": "Agrupacion",
    "nombreCandidato": "Candidato",
    "totalVotosValidos": "Votos",
    "porcentajeVotosValidos": "Pct_Validos",
    "porcentajeVotosEmitidos": "Pct_Emitidos",
})

# 5. Lo mostramos en la terminal
print(df)