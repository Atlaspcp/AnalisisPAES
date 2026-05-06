import streamlit as st
import pandas as pd
import plotly.express as px

# --- CONFIGURACIÓN ---
st.set_page_config(page_title="Portal PAES Global", layout="wide")

# 1. DATOS ACTUALIZADOS (Se agregó la clave "Buenas")
DATABASE = {
    "Joel": {
        "M1 (Matemática)": {
            "Ensayos": ["Marzo", "Abril"],
            "Puntajes": [720, 750],
            "Buenas": [45, 48],  # <-- Nueva línea
            "Eje_Números": [80, 85],
            "Eje_Álgebra": [60, 70]
        },
        "Lenguaje": {
            "Ensayos": ["Marzo", "Abril"],
            "Puntajes": [600, 640],
            "Buenas": [38, 42],  # <-- Nueva línea
            "Eje_Rastreo": [50, 60],
            "Eje_Interpretación": [40, 55]
        }
    },
    "Kantar": {
        "M1 (Matemática)": {
            "Ensayos": ["Abril"],
            "Puntajes": [810],
            "Buenas": [52],
            "Eje_Números": [90],
            "Eje_Álgebra": [85]
        },
        "Historia": {
            "Ensayos": ["Febrero","Marzo","Abril"],
            "Puntajes": [810, 700, 900],
            "Buenas": [55, 48, 62],
            "Eje_Números": [90, 60, 86],
            "Eje_Álgebra": [85, 70, 83]
        },
        "Lenguaje": {
            "Ensayos": ["Abril"],
            "Puntajes": [810],
            "Buenas": [50],
            "Eje_Números": [90],
            "Eje_Álgebra": [85]
        }
    }
}

# --- 2. BARRA LATERAL ---
st.sidebar.header("Acceso Personal")
usuario_sel = st.sidebar.selectbox("Seleccionar un usuario", list(DATABASE.keys()))
asignaturas_disponibles = list(DATABASE[usuario_sel].keys())
asignatura_sel = st.sidebar.selectbox("Selecciona la Prueba", asignaturas_disponibles)

st.sidebar.divider()
st.sidebar.success(f"Perfil: {usuario_sel}")

# --- 3. PROCESAMIENTO ---
data_final = DATABASE[usuario_sel][asignatura_sel]
df = pd.DataFrame(data_final)

# --- 4. INTERFAZ PRINCIPAL ---
st.title(f"Evolución PAES: {asignatura_sel}")
st.subheader(f"Usuario: {usuario_sel}")

# Cálculos
ultimo_p = df['Puntajes'].iloc[-1]
# Verificamos si existen respuestas buenas en la data
tiene_buenas = "Buenas" in df.columns
ultima_b = df['Buenas'].iloc[-1] if tiene_buenas else "N/A"

col1, col2, col3, col4 = st.columns(4)
with col1:
    st.metric("Último Puntaje", f"{ultimo_p} pts")
with col2:
    st.metric("Respuestas Buenas", f"{ultima_b}", help="Aciertos en el último ensayo")
with col3:
    st.metric("Promedio General", f"{round(df['Puntajes'].mean(), 1)} pts")
with col4:
    st.metric("Total Ensayos", len(df))

st.divider()

# --- 5. GRÁFICOS DINÁMICOS ---
tab1, tab2, tab3 = st.tabs(["Progreso de Puntaje", "Análisis de Buenas", "Desempeño por Ejes"])

with tab1:
    fig_evolucion = px.line(df, x="Ensayos", y="Puntajes", markers=True, 
                            title="Evolución de Puntaje",
                            color_discrete_sequence=["#FF4B4B"])
    st.plotly_chart(fig_evolucion, use_container_width=True)

with tab2:
    if tiene_buenas:
        # Gráfico de barras para respuestas correctas
        fig_buenas = px.bar(df, x="Ensayos", y="Buenas", 
                            title="Cantidad de Respuestas Correctas por Ensayo",
                            text_auto=True,
                            color_discrete_sequence=["#00CC96"])
        st.plotly_chart(fig_buenas, use_container_width=True)
    else:
        st.warning("No hay datos de respuestas buenas para esta asignatura.")

with tab3:
    columnas_ejes = [c for c in df.columns if c.startswith("Eje_")]
    if columnas_ejes:
        fig_ejes = px.line(df, x="Ensayos", y=columnas_ejes, markers=True,
                          title="Rendimiento por Ejes (%)")
        fig_ejes.update_yaxes(range=[0, 105])
        st.plotly_chart(fig_ejes, use_container_width=True)
    else:
        st.warning("No hay datos de ejes temáticos.")

# --- 6. TABLA DE DATOS ---
with st.expander("Ver detalles de la planilla"):
    st.table(df)
