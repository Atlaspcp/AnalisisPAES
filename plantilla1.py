import streamlit as st
import pandas as pd
import plotly.express as px

# Nombre que aparecerá en el navegador, el titulo se puede cambiar
st.set_page_config(page_title="Analisis resultados PAES", layout="wide")

# Base de datos, nombre de una persona, asociada a una prueba, cada prueba asociada a ciertos criterios.
#Cuidado con los parentesis de llaves, todo debe mantenerse dentro de ellos para no desconfigurar las "listas", en estricto rigor son diccionarios
DATABASE = {
    "Joel": {
        "M1": {
            "Ensayos": ["Marzo", "Abril"],
            "Puntajes": [720, 750],
            "Buenas": [45, 48],
            "Eje Números": [80, 85],
            "Eje Álgebra": [60, 70],
            "Eje Geomtría": [65, 79],
            "Eje Probabilidades": [20, 90]
        },
        "Lenguaje": {
            "Ensayos": ["Marzo", "Abril"],
            "Puntajes": [600, 640],
            "Buenas": [38, 42], 
            "Eje_Rastreo": [50, 60],
            "Eje_Interpretación": [40, 55]
        }
    },
    "Kantar": {
        "M1": {
            "Ensayos": ["Abril"],
            "Puntajes": [810],
            "Buenas": [52],
            "Eje Números": [90],
            "Eje Álgebra": [85]
        },
        "Historia": {
            "Ensayos": ["Febrero","Marzo","Abril"],
            "Puntajes": [810, 700, 900],
            "Buenas": [55, 48, 62],
            "Eje Números": [90, 60, 86],
            "Eje Álgebra": [85, 70, 83]
        },
        "Lenguaje": {
            "Ensayos": ["Abril"],
            "Puntajes": [810],
            "Buenas": [50],
            "Eje Números": [90],
            "Eje Álgebra": [85]
        }
    }
}

# Configuración de barra lateral izquierda, pide un nombre, dependiendo del usuario, se vén las pruebas que tiene agregadas en la base de datos. Acá no se debe mover nada.
st.sidebar.header("Acceso Personal")
usuario_sel = st.sidebar.selectbox("Seleccionar un usuario", list(DATABASE.keys()))
asignaturas_disponibles = list(DATABASE[usuario_sel].keys())
asignatura_sel = st.sidebar.selectbox("Selecciona la Prueba", asignaturas_disponibles)

st.sidebar.divider()
st.sidebar.success(f"Perfil: {usuario_sel}")

#Muestra la información del ususario y la prueba seleccionada
data_final = DATABASE[usuario_sel][asignatura_sel]
df = pd.DataFrame(data_final)

#Vista principal, el titulo se puede cambiar
st.title(f"Analisis PAES: {asignatura_sel}")
st.subheader(f"Usuario: {usuario_sel}")

# Calculos matematicos, cantidad de buenas, ultimos puntajes, promedio y cantidad de ensayos. Primero se comprueba que
ultimo_p = df['Puntajes'].iloc[-1]
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

# Acá se configuran los parametros de los gráficos, los nombres son modificables.
tab1, tab2, tab3 = st.tabs(["Progreso de Puntaje", "Análisis de Buenas", "Desempeño por Ejes"])

with tab1:
    fig_evolucion = px.line(df, x="Ensayos", y="Puntajes", markers=True, 
                            title="Evolución de Puntaje",
                            color_discrete_sequence=["#FF4B4B"])
    st.plotly_chart(fig_evolucion, use_container_width=True)

with tab2:
    if tiene_buenas:
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

# Muestra una tabla similar a excel con la información resumida que ha sido ingresada.
with st.expander("Ver detalles de la planilla"):
    st.table(df)
