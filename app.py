import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px

# Configuración de la página
st.set_page_config(page_title="Simulador de Secado - Equipo Mango", layout="wide")

st.title("🍎 Simulador de Secado por Aire Caliente (SC)")
st.markdown("""
Esta simulación recrea el proceso de obtención de **Mango en Polvo** a 50°C, basado en el estudio de Estrada et al. (2018).
""")

# --- SIDEBAR (Controles) ---
st.sidebar.header("Parámetros del Proceso")
temp = st.sidebar.selectbox("Temperatura de Secado (°C)", [50], help="Temperatura fija según el artículo.")
tiempo_input = st.sidebar.slider("Tiempo de Secado (Horas)", 0, 12, 12)

# --- LÓGICA DE SIMULACIÓN (Basada en datos del artículo) ---
# Datos iniciales y finales del artículo
h_inicial = 73.94  # 
h_final_objetivo = 6.44  # 

# Generar curva exponencial de secado (cinética teórica que ajusta a los datos)
t = np.linspace(0, 12, 100)
# Constante de secado calculada para llegar de 73.94 a 6.44 en 12h
k = -np.log(h_final_objetivo / h_inicial) / 12
h_t = h_inicial * np.exp(-k * t)

df_cinetica = pd.DataFrame({"Tiempo (h)": t, "Humedad (%)": h_t})
df_filtrado = df_cinetica[df_cinetica["Tiempo (h)"] <= tiempo_input]

# --- VISUALIZACIÓN ---
col1, col2 = st.columns(2)

with col1:
    st.subheader("Curva de Cinética de Secado")
    fig = px.line(df_filtrado, x="Tiempo (h)", y="Humedad (%)", 
                  title=f"Pérdida de Humedad del Mango a {temp}°C",
                  range_y=[0, 80], range_x=[0, 12])
    fig.add_hline(y=10, line_dash="dash", line_color="red", annotation_text="Límite Humedad Baja (<10%)")
    st.plotly_chart(fig, use_container_width=True)

with col2:
    st.subheader("Concentración de Vitamina C")
    # Datos de Vit C: Fresco (44.09) vs Polvo (87.21) 
    datos_vit = pd.DataFrame({
        "Estado": ["Fresco", "Polvo (Final)"],
        "Vitamina C (mg/100g)": [44.09, 87.21]
    })
    fig_bar = px.bar(datos_vit, x="Estado", y="Vitamina C (mg/100g)", 
                     color="Estado", text_auto=True)
    st.plotly_chart(fig_bar, use_container_width=True)

# --- MÉTRICAS FINALES ---
st.divider()
st.subheader("Indicadores Finales de Calidad (al completar 12h)")
m1, m2, m3 = st.columns(3)
m1.metric("Humedad Final", f"{h_final_objetivo}%", "-67.5% Δ")
m2.metric("Actividad de Agua (aw)", "0.345", "Estable")
m3.metric("Fibra Dietaria", "10.98%", "Ingrediente Funcional")

st.info("Nota: La simulación muestra cómo el aire caliente concentra nutrientes y reduce la actividad de agua para prevenir el crecimiento bacteriano.")
