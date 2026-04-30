import streamlit as st
import pandas as pd
import plotly.express as px

# --- CONFIGURACIÓN ---
st.set_page_config(page_title="Portal PAES Global", layout="wide")

# Datos del programa
# Estudiante, Prueba, Info
DATABASE = {
    "Joel": {
        "M1 (Matemática)": {
            "Ensayos": ["Marzo", "Abril"],
            "Puntajes": [720, 750],
            "Eje_Números": [80, 85],
            "Eje_Álgebra": [60, 70]
        },
        "Lenguaje": {
            "Ensayos": ["Marzo", "Abril"],
            "Puntajes": [600, 640],
            "Eje_Rastreo": [50, 60],
            "Eje_Interpretación": [40, 55]
        }
    },
    "Kantar": {
        "M1 (Matemática)": {
            "Ensayos": ["Abril"],
            "Puntajes": [810],
            "Eje_Números": [90],
            "Eje_Álgebra": [85]
        },
        "Ciencias": {
            "Ensayos": ["Abril"],
            "Puntajes": [550],
            "Eje_Biología": [40],
            "Eje_Física": [30]
        },
        "Historia": {
            "Ensayos": ["Febrero","Marzo","Abril",],
            "Puntajes": [810,700,900],
            "Eje_Números": [90,60,86],
            "Eje_Álgebra": [85,70,83]
        },
        "Lenguaje": {
            "Ensayos": ["Abril"],
            "Puntajes": [810],
            "Eje_Números": [90],
            "Eje_Álgebra": [85]
        }
    }
}

# --- 2. BARRA LATERAL (Doble Filtro) ---
st.sidebar.header("Acceso Personal")

# Filtro 1: Usuario
usuario_lista = list(DATABASE.keys())
usuario_sel = st.sidebar.selectbox("Seleccionar un usuario", usuario_lista)

# Filtro 2: Asignatura (Se actualiza según el usuario elegido)
asignaturas_disponibles = list(DATABASE[usuario_sel].keys())
asignatura_sel = st.sidebar.selectbox("Selecciona la Prueba", asignaturas_disponibles)

st.sidebar.divider()
st.sidebar.success(f"Perfil: {usuario_sel}")
st.sidebar.info(f"Viendo: {asignatura_sel}")

# --- 3. PROCESAMIENTO ---
# Extraemos solo la info del usuario y asignatura elegida
data_final = DATABASE[usuario_sel][asignatura_sel]
df = pd.DataFrame(data_final)

# --- 4. INTERFAZ PRINCIPAL ---
st.title(f"Evolución Resultados ensayos PAES: {asignatura_sel}")
st.subheader(f"Usuario: {usuario_sel}")

# Métricas Dinámicas
col1, col2 = st.columns(2)
with col1:
    st.metric("Último Puntaje", f"{df['Puntajes'].iloc[-1]} pts")
with col2:
    st.metric("Total Ensayos", len(df))
with col3:
    st.metric("Promedio de los puntajes", len(df))
st.divider()

# --- 5. GRÁFICOS DINÁMICOS ---
tab1, tab2 = st.tabs(["Gráfico de Progreso", "Análisis por Ejes"])

with tab1:
    fig_evolucion = px.line(df, x="Ensayos", y="Puntajes", markers=True, 
                            title=f"Rendimiento en {asignatura_sel}",
                            color_discrete_sequence=["#FF4B4B"])
    st.plotly_chart(fig_evolucion, use_container_width=True)

with tab2:
    # El programa busca automáticamente cualquier columna que empiece con "Eje_"
    columnas_ejes = [c for c in df.columns if c.startswith("Eje_")]
    
    if columnas_ejes:
        fig_ejes = px.bar(df, x="Ensayos", y=columnas_ejes, barmode="group",
                          title="Comparativa de Ejes Temáticos")
        fig_ejes.update_yaxes(range=[0, 100])
        st.plotly_chart(fig_ejes, use_container_width=True)
    else:
        st.warning("No hay datos de ejes temáticos para esta asignatura.")

# --- 6. TABLA DE DATOS ---
with st.expander("Ver detalles de la planilla"):
    st.table(df)
