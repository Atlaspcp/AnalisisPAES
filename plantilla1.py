import streamlit as st
import pandas as pd
import plotly.express as px

# --- CONFIGURACIÓN DE LA PÁGINA ---
st.set_page_config(page_title="Mi Progreso PAES", layout="wide", page_icon="📈")

# --- 1. BASE DE DATOS (Aquí los alumnos agregan a sus amigos y datos) ---
# Instrucción para alumnos: Para agregar un amigo, copia un bloque entero y cambia los datos.
# Asegúrate de que todas las listas dentro de un nombre tengan el mismo largo.
DATABASE = {
    "Joel": {
        "Ensayos": ["Ensayo 1", "Ensayo 2", "Ensayo 3","Ensayo 4"],
        "Puntajes": [650, 680, 710,890],
        "Buenas": [40, 45, 50,65],
        "Eje Numeros": [70, 75, 80, 90],       # % de acierto
        "Eje Algebra": [50, 55, 65,20],       # % de acierto
        "Eje Geometria": [40, 42, 48, 65],     # % de acierto
        "Eje Probabilidad": [30, 40, 50, 32]   # % de acierto
    },
    "Eduardo Z.": {
        "Ensayos": ["Ensayo 1", "Ensayo 2"],
        "Puntajes": [580, 610],
        "Buenas": [30, 35],
        "Eje Numeros": [60, 65],
        "Eje Algebra": [40, 45],
        "Eje Geometria": [30, 35],
        "Eje Probabilidad": [20, 30]
    }
    
}

# --- 2. BARRA LATERAL (Navegación) ---
st.sidebar.header("Panel de Acceso")
usuario = st.sidebar.selectbox("Selecciona tu perfil:", list(DATABASE.keys()))

st.sidebar.divider()
st.sidebar.markdown(f"**Usuario actual:** {usuario}")
st.sidebar.info("Para actualizar tus datos, edita el código en GitHub y guarda los cambios.")

# --- 3. PROCESAMIENTO DE DATOS ---
# Convertimos el diccionario del usuario seleccionado en una tabla (DataFrame)
datos_dict = DATABASE[usuario]
df = pd.DataFrame(datos_dict)

# --- 4. INTERFAZ PRINCIPAL ---
st.title(f"Preparación PAES: {usuario}")
st.write("Visualiza tu evolución y detecta en qué ejes necesitas reforzar.")

# Métricas destacadas
col1, col2, col3 = st.columns(3)
ultimo_puntaje = df["Puntajes"].iloc[-1]
primer_puntaje = df["Puntajes"].iloc[0]
mejor_puntaje = df["Puntajes"].max()

col1.metric("Último Puntaje", f"{ultimo_puntaje} pts", delta=int(ultimo_puntaje - primer_puntaje))
col2.metric("Mejor Puntaje", f"{mejor_puntaje} pts")
col3.metric("Ensayos Realizados", len(df))

st.divider()

# --- 5. GRÁFICOS ---
tab1, tab2, tab3 = st.tabs(["Evolución General", "Análisis por Ejes", "Resultados"])

with tab1:
    st.subheader("Progreso de Puntaje")
    fig_progreso = px.line(df, x="Ensayos", y="Puntajes", markers=True, 
                          text="Puntajes", title="Puntaje por Ensayo")
    fig_progreso.update_traces(textposition="top center", line_color="#00CC96")
    st.plotly_chart(fig_progreso, use_container_width=True)

with tab2:
    st.subheader("Rendimiento Detallado por Contenido")
    # Seleccionamos las columnas que empiezan con "Eje_" para graficar
    columnas_ejes = [col for col in df.columns if col.startswith("Eje_")]
    
    fig_ejes = px.line(df, x="Ensayos", y=columnas_ejes, markers=True,
                       title="Porcentaje de Logro por Eje Temático")
    fig_ejes.update_yaxes(range=[0, 100]) # El porcentaje es de 0 a 100
    st.plotly_chart(fig_ejes, use_container_width=True)
    
    st.info("Consejo: Los ejes con líneas más bajas son tu prioridad de estudio para esta semana.")

with tab3:
    st.subheader("Tus Datos")
    st.dataframe(df, use_container_width=True)
    
    # Botón para descargar
    csv = df.to_csv(index=False).encode('utf-8')
    st.download_button("Descargar mi planilla (CSV)", data=csv, file_name=f"progreso_{usuario}.csv")

# --- 6. PIE DE PÁGINA ---
st.caption("Programa creado para fines educativos - Preparación PAES 2026")
