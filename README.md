# 🗳️ Dashboard Segunda Vuelta Presidencial 2026 — Perú

Dashboard interactivo que consume en tiempo real la API pública de la ONPE
para visualizar los resultados de la segunda vuelta presidencial 2026.

## 🔗 Demo en vivo

[Ver dashboard](URL_PENDIENTE)

## 🛠️ Tecnologías

- **Python**
- **Requests** — consumo de la API de la ONPE
- **Pandas** — limpieza y transformación de datos
- **Streamlit** — visualización e interfaz del dashboard

## 📊 ¿Qué hace?

- Se conecta a la API oficial de resultados de la ONPE.
- Transforma la respuesta JSON en una tabla estructurada.
- Muestra porcentajes, total de votos y un gráfico comparativo.
- Permite actualizar los datos en tiempo real.

## 🚀 Cómo ejecutarlo localmente

```bash
git clone https://github.com/[TU_USUARIO]/dashboard-onpe.git
cd dashboard-onpe
python -m venv venv
venv\Scripts\activate
pip install -r requirements.txt
streamlit run streamlit_app.py
```

## 👤 Autor

Adrian Aybar Medina — [tu LinkedIn]
