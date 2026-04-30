import streamlit as st
import pandas as pd
import plotly.express as px

# 1. CONFIGURACIÓN DE LA PÁGINA
st.set_page_config(page_title="Mi Evolución PAES", layout="wide")

st.title("📈 Tracker de Ensayos PAES")
st.markdown("""
Esta aplicación te permite monitorear tu progreso. 
**Instrucciones:** Edita la tabla de abajo con tus resultados y los gráficos se actualizarán solos.
""")

# 2. CONFIGURACIÓN ADAPTABLE (Lo que los alumnos pueden cambiar)
# Aquí definimos los ejes temáticos. Si quieren cambiar a "Ciencias", solo editan esta lista.
EJES_TEMATICOS = ["Números", "Álgebra y Funciones", "Geometría", "Probabilidad y Estadística"]

# 3. DATOS INICIALES (Para que no aparezca vacío)
if 'df_resultados' not in st.session_state:
    data = {
        "Ensayo": ["Ensayo 1", "Ensayo 2"],
        "Fecha": ["2026-03-01", "2026-04-01"],
        "Puntaje": [650, 720],
        "Buenas": [40, 48],
        "Malas": [20, 12],
        "Números (%)": [70, 85],
        "Álgebra (%)": [50, 60],
        "Geometría (%)": [40, 55],
        "Probabilidad (%)": [30, 45]
    }
    st.session_state.df_resultados = pd.DataFrame(data)

# 4. EDITOR DE DATOS (La "Planilla")
st.subheader("📝 Ingresa tus resultados")
df_editado = st.data_editor(
    st.session_state.df_resultados, 
    num_rows="dynamic", 
    use_container_width=True
)

# Guardar cambios
st.session_state.df_resultados = df_editado

# 5. VISUALIZACIÓN DE MÉTRICAS CLAVE
col1, col2, col3 = st.columns(3)
with col1:
    ultimo_puntaje = df_editado["Puntaje"].iloc[-1]
    st.metric("Último Puntaje", f"{ultimo_puntaje} pts")
with col2:
    promedio_buenas = round(df_editado["Buenas"].mean(), 1)
    st.metric("Promedio Buenas", promedio_buenas)
with col3:
    progreso = ultimo_puntaje - df_editado["Puntaje"].iloc[0]
    st.metric("Progreso Total", f"{progreso} pts", delta=int(progreso))

# 6. GRÁFICOS DE EVOLUCIÓN
st.divider()
tab1, tab2 = st.tabs(["Evolución General", "Análisis por Ejes"])

with tab1:
    st.subheader("Puntaje a través del tiempo")
    fig_puntaje = px.line(df_editado, x="Ensayo", y="Puntaje", markers=True, 
                          line_shape="linear", title="Evolución del Puntaje")
    st.plotly_chart(fig_puntaje, use_container_width=True)

with tab2:
    st.subheader("Porcentaje de acierto por Eje Temático")
    # Filtramos las columnas que terminan en (%) para graficarlas
    columnas_ejes = [c for c in df_editado.columns if "%" in c]
    fig_ejes = px.line(df_editado, x="Ensayo", y=columnas_ejes, markers=True,
                       title="Rendimiento por Contenido")
    fig_ejes.update_yaxes(range=[0, 100])
    st.plotly_chart(fig_ejes, use_container_width=True)
