import pandas as pd
import streamlit as st
from PIL import Image
import numpy as np
from datetime import datetime
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots

# Page configuration
st.set_page_config(
    page_title="Análisis de Sensores - Mi Ciudad",
    page_icon="🌿",
    layout="wide"
)

# Custom CSS for natural theme (greens and blues)
st.markdown("""
    <style>
    .main {
        padding: 2rem;
        background: linear-gradient(135deg, #E8F6F3 0%, #D5F4E6 50%, #FDEBD0 100%);
        min-height: 100vh;
    }
    
    .stApp {
        background: linear-gradient(135deg, #E8F6F3 0%, #D5F4E6 50%, #FDEBD0 100%);
    }
    
    .stAlert {
        margin-top: 1rem;
        background-color: rgba(46, 125, 50, 0.1);
        border-left: 4px solid #2E7D32;
    }
    
    h1, h2, h3 {
        color: #1B4332;
        text-shadow: 1px 1px 2px rgba(0,0,0,0.1);
    }
    
    h1 {
        background: linear-gradient(90deg, #1B4332, #2D6A4F, #40916C);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        background-clip: text;
    }
    
    .stButton>button {
        background: linear-gradient(45deg, #2D6A4F, #40916C);
        color: white;
        border-radius: 15px;
        border: none;
        box-shadow: 0 4px 15px rgba(45, 106, 79, 0.3);
        transition: all 0.3s ease;
    }
    
    .stButton>button:hover {
        background: linear-gradient(45deg, #1B4332, #2D6A4F);
        transform: translateY(-2px);
        box-shadow: 0 6px 20px rgba(45, 106, 79, 0.4);
    }
    
    .stSelectbox>div>div {
        background: rgba(255, 255, 255, 0.9);
        border-radius: 10px;
        border: 2px solid #74C69D;
        backdrop-filter: blur(10px);
    }
    
    .stSlider>div>div>div {
        background-color: #74C69D;
    }
    
    .stRadio>div {
        background: rgba(255, 255, 255, 0.8);
        border-radius: 10px;
        padding: 1rem;
        border: 1px solid #74C69D;
    }
    
    .stTabs [data-baseweb="tab"] {
        background: rgba(255, 255, 255, 0.7);
        color: #1B4332;
        border-radius: 10px 10px 0 0;
        margin-right: 5px;
        font-weight: bold;
    }
    
    .stTabs [data-baseweb="tab"][aria-selected="true"] {
        background: linear-gradient(135deg, #74C69D, #95D5B2);
        color: #1B4332;
        border-bottom: 3px solid #2D6A4F;
    }
    
    .stDataFrame {
        background: rgba(255, 255, 255, 0.9);
        border-radius: 10px;
        border: 1px solid #74C69D;
        backdrop-filter: blur(5px);
    }
    
    .metric-card {
        background: rgba(255, 255, 255, 0.9);
        border-radius: 15px;
        padding: 1rem;
        margin: 0.5rem 0;
        border-left: 4px solid #40916C;
        box-shadow: 0 4px 15px rgba(0,0,0,0.1);
        backdrop-filter: blur(10px);
    }
    
    .info-box {
        background: linear-gradient(135deg, rgba(116, 198, 157, 0.2), rgba(149, 213, 178, 0.2));
        border-radius: 15px;
        padding: 1.5rem;
        border: 1px solid #74C69D;
        margin: 1rem 0;
        backdrop-filter: blur(5px);
    }
    
    .stCheckbox>label {
        background: rgba(255, 255, 255, 0.8);
        border-radius: 8px;
        padding: 0.5rem;
        border: 1px solid #95D5B2;
    }
    
    .sidebar .stSelectbox>div>div {
        background: rgba(255, 255, 255, 0.95);
    }
    
    /* Custom scrollbar */
    ::-webkit-scrollbar {
        width: 8px;
    }
    
    ::-webkit-scrollbar-track {
        background: rgba(116, 198, 157, 0.1);
        border-radius: 10px;
    }
    
    ::-webkit-scrollbar-thumb {
        background: linear-gradient(45deg, #74C69D, #40916C);
        border-radius: 10px;
    }
    
    ::-webkit-scrollbar-thumb:hover {
        background: linear-gradient(45deg, #40916C, #2D6A4F);
    }
    </style>
""", unsafe_allow_html=True)

# Title and description with nature emojis
st.title('🌿 Análisis de Datos de Sensores Ambientales 🌍')
st.markdown("""
    <div class="info-box">
    🌱 Esta aplicación permite analizar datos de temperatura y humedad
    recolectados por sensores ESP32 en diferentes puntos de la ciudad.
    Explora los patrones ambientales de tu entorno natural. 🍃
    </div>
""", unsafe_allow_html=True)

# Create map data for EAFIT
eafit_location = pd.DataFrame({
    'lat': [6.2479],
    'lon': [-75.6081],
    'location': ['🌿 Sensor Ambiental']
})

# Display map with nature styling
st.subheader("🗺️ Ubicación de los Sensores Ambientales")
st.map(eafit_location, zoom=15)

# File uploader with natural styling
uploaded_file = st.file_uploader('🌱 Seleccione archivo CSV con datos ambientales', type=['csv'])

if uploaded_file is not None:
    try:
        # Load and process data
        df1 = pd.read_csv(uploaded_file)
        
        # Renombrar columnas para simplificar
        column_mapping = {
            'temperatura {device="ESP32", name="Final_IOT"}': 'temperatura',
            'humedad {device="ESP32", name="Final_IOT"}': 'humedad'
        }
        df1 = df1.rename(columns=column_mapping)
        
        df1['Time'] = pd.to_datetime(df1['Time'])
        df1 = df1.set_index('Time')

        # Create tabs for different analyses
        tab1, tab2, tab3, tab4, tab5 = st.tabs([
            "📈 Visualización", 
            "📊 Estadísticas", 
            "🔍 Filtros", 
            "🧠 Análisis Avanzado",
            "🗺️ Información del Sitio"
        ])

        with tab1:
            st.subheader('🌊 Visualización de Datos Ambientales')
            
            col1, col2 = st.columns(2)
            
            with col1:
                # Variable selector
                variable = st.selectbox(
                    "🌿 Seleccione variable a visualizar",
                    ["temperatura", "humedad", "Ambas variables", "Humedad < 30%"]
                )
            
            with col2:
                # Chart type selector
                chart_type = st.selectbox(
                    "📊 Seleccione tipo de gráfico",
                    ["Línea", "Área", "Barra", "Interactivo (Plotly)"]
                )
            
            # Create plot based on selection
            if variable == "Ambas variables":
                if chart_type == "Interactivo (Plotly)":
                    fig = make_subplots(
                        rows=2, cols=1,
                        subplot_titles=('🌡️ Temperatura', '💧 Humedad'),
                        vertical_spacing=0.08
                    )
                    
                    fig.add_trace(
                        go.Scatter(x=df1.index, y=df1["temperatura"], 
                                 name="Temperatura", line=dict(color='#FF6B6B')),
                        row=1, col=1
                    )
                    
                    fig.add_trace(
                        go.Scatter(x=df1.index, y=df1["humedad"], 
                                 name="Humedad", line=dict(color='#4ECDC4')),
                        row=2, col=1
                    )
                    
                    fig.update_layout(height=600, showlegend=True,
                                    paper_bgcolor='rgba(0,0,0,0)',
                                    plot_bgcolor='rgba(255,255,255,0.9)')
                    st.plotly_chart(fig, use_container_width=True)
                else:
                    st.write("### 🌡️ Temperatura")
                    if chart_type == "Línea":
                        st.line_chart(df1["temperatura"])
                    elif chart_type == "Área":
                        st.area_chart(df1["temperatura"])
                    else:
                        st.bar_chart(df1["temperatura"])
                        
                    st.write("### 💧 Humedad")
                    if chart_type == "Línea":
                        st.line_chart(df1["humedad"])
                    elif chart_type == "Área":
                        st.area_chart(df1["humedad"])
                    else:
                        st.bar_chart(df1["humedad"])
                        
            elif variable == "Humedad < 30%":
                st.write("### 🏜️ Condiciones de Baja Humedad (< 30%)")
                low_humidity_df = df1[df1["humedad"] < 30]
                if low_humidity_df.empty:
                    st.warning("🌿 ¡Excelente! No hay registros con humedad crítica menor a 30%")
                else:
                    if chart_type == "Interactivo (Plotly)":
                        fig = px.line(x=low_humidity_df.index, y=low_humidity_df["humedad"],
                                    title="Períodos de Baja Humedad",
                                    color_discrete_sequence=['#FF6B6B'])
                        fig.update_layout(paper_bgcolor='rgba(0,0,0,0)',
                                        plot_bgcolor='rgba(255,255,255,0.9)')
                        st.plotly_chart(fig, use_container_width=True)
                    elif chart_type == "Línea":
                        st.line_chart(low_humidity_df["humedad"])
                    elif chart_type == "Área":
                        st.area_chart(low_humidity_df["humedad"])
                    else:
                        st.bar_chart(low_humidity_df["humedad"])
            else:
                if chart_type == "Interactivo (Plotly)":
                    color = '#FF6B6B' if variable == 'temperatura' else '#4ECDC4'
                    title = f"{'🌡️ Temperatura' if variable == 'temperatura' else '💧 Humedad'} - Serie Temporal"
                    
                    fig = px.line(x=df1.index, y=df1[variable], 
                                title=title,
                                color_discrete_sequence=[color])
                    fig.update_layout(paper_bgcolor='rgba(0,0,0,0)',
                                    plot_bgcolor='rgba(255,255,255,0.9)')
                    st.plotly_chart(fig, use_container_width=True)
                elif chart_type == "Línea":
                    st.line_chart(df1[variable])
                elif chart_type == "Área":
                    st.area_chart(df1[variable])
                else:
                    st.bar_chart(df1[variable])

            # Raw data display with toggle
            if st.checkbox('🗂️ Mostrar datos crudos'):
                st.write(df1)

        with tab2:
            st.subheader('📊 Análisis Estadístico Ambiental')
            
            # Variable selector for statistics
            stat_variable = st.radio(
                "🌿 Seleccione variable para estadísticas",
                ["temperatura", "humedad"]
            )
            
            # Statistical summary
            stats_df = df1[stat_variable].describe()
            
            col1, col2, col3 = st.columns(3)
            
            with col1:
                st.write("### 📈 Estadísticas Descriptivas")
                st.dataframe(stats_df)
            
            with col2:
                # Additional statistics
                if stat_variable == "temperatura":
                    st.markdown('<div class="metric-card">', unsafe_allow_html=True)
                    st.metric("🌡️ Temperatura Promedio", f"{stats_df['mean']:.2f}°C")
                    st.metric("🔥 Temperatura Máxima", f"{stats_df['max']:.2f}°C")
                    st.metric("❄️ Temperatura Mínima", f"{stats_df['min']:.2f}°C")
                    st.metric("📏 Desviación Estándar", f"{stats_df['std']:.2f}°C")
                    st.markdown('</div>', unsafe_allow_html=True)
                else:
                    st.markdown('<div class="metric-card">', unsafe_allow_html=True)
                    st.metric("💧 Humedad Promedio", f"{stats_df['mean']:.2f}%")
                    st.metric("🌊 Humedad Máxima", f"{stats_df['max']:.2f}%")
                    st.metric("🏜️ Humedad Mínima", f"{stats_df['min']:.2f}%")
                    st.metric("📏 Desviación Estándar", f"{stats_df['std']:.2f}%")
                    st.markdown('</div>', unsafe_allow_html=True)
                    
            with col3:
                # Histogram
                fig = px.histogram(df1, x=stat_variable, nbins=20,
                                title=f"Distribución de {'Temperatura' if stat_variable == 'temperatura' else 'Humedad'}",
                                color_discrete_sequence=['#74C69D'])
                fig.update_layout(paper_bgcolor='rgba(0,0,0,0)',
                                plot_bgcolor='rgba(255,255,255,0.9)')
                st.plotly_chart(fig, use_container_width=True)

        with tab3:
            st.subheader('🔍 Filtros y Análisis de Rangos')
            
            # Variable selector for filtering
            filter_variable = st.selectbox(
                "🌿 Seleccione variable para filtrar",
                ["temperatura", "humedad"]
            )
            
            col1, col2 = st.columns(2)
            
            with col1:
                # Minimum value filter
                min_val = st.slider(
                    f'🔽 Valor mínimo de {filter_variable}',
                    float(df1[filter_variable].min()),
                    float(df1[filter_variable].max()),
                    float(df1[filter_variable].mean()),
                    key="min_val"
                )
                
                filtrado_df_min = df1[df1[filter_variable] > min_val]
                st.write(f"📊 Registros con {filter_variable} superior a", 
                        f"{min_val}{'°C' if filter_variable == 'temperatura' else '%'}:")
                st.dataframe(filtrado_df_min)
                
            with col2:
                # Maximum value filter
                max_val = st.slider(
                    f'🔼 Valor máximo de {filter_variable}',
                    float(df1[filter_variable].min()),
                    float(df1[filter_variable].max()),
                    float(df1[filter_variable].mean()),
                    key="max_val"
                )
                
                filtrado_df_max = df1[df1[filter_variable] < max_val]
                st.write(f"📊 Registros con {filter_variable} inferior a",
                        f"{max_val}{'°C' if filter_variable == 'temperatura' else '%'}:")
                st.dataframe(filtrado_df_max)

            # Download filtered data
            if st.button('💾 Descargar datos filtrados'):
                csv = filtrado_df_min.to_csv().encode('utf-8')
                st.download_button(
                    label="📁 Descargar CSV",
                    data=csv,
                    file_name='datos_ambientales_filtrados.csv',
                    mime='text/csv',
                )

        with tab4:
            st.subheader('🧠 Análisis Avanzado y Correlaciones')
            
            # Correlation analysis
            st.write("### 🔗 Análisis de Correlación")
            correlation = df1['temperatura'].corr(df1['humedad'])
            
            col1, col2 = st.columns(2)
            
            with col1:
                st.metric("🔗 Correlación Temperatura-Humedad", f"{correlation:.3f}")
                
                if abs(correlation) > 0.7:
                    st.success("🟢 Correlación fuerte detectada")
                elif abs(correlation) > 0.3:
                    st.warning("🟡 Correlación moderada")
                else:
                    st.info("🔵 Correlación débil")
                    
                # Scatter plot
                fig = px.scatter(df1, x='temperatura', y='humedad',
                               title="Relación Temperatura vs Humedad",
                               trendline="ols",
                               color_discrete_sequence=['#40916C'])
                fig.update_layout(paper_bgcolor='rgba(0,0,0,0)',
                                plot_bgcolor='rgba(255,255,255,0.9)')
                st.plotly_chart(fig, use_container_width=True)
            
            with col2:
                # Time-based analysis
                st.write("### ⏰ Análisis Temporal")
                
                # Add hour column for analysis
                df_temp = df1.copy()
                df_temp['hora'] = df_temp.index.hour
                df_temp['dia_semana'] = df_temp.index.dayofweek
                df_temp['mes'] = df_temp.index.month
                
                # Hourly patterns
                hourly_avg = df_temp.groupby('hora')[['temperatura', 'humedad']].mean()
                
                fig = go.Figure()
                fig.add_trace(go.Scatter(x=hourly_avg.index, y=hourly_avg['temperatura'],
                                       mode='lines+markers', name='Temperatura',
                                       line=dict(color='#FF6B6B')))
                fig.add_trace(go.Scatter(x=hourly_avg.index, y=hourly_avg['humedad'],
                                       mode='lines+markers', name='Humedad',
                                       line=dict(color='#4ECDC4'), yaxis='y2'))
                
                fig.update_layout(
                    title="Patrones Horarios Promedio",
                    xaxis_title="Hora del día",
                    yaxis_title="Temperatura (°C)",
                    yaxis2=dict(title="Humedad (%)", overlaying='y', side='right'),
                    paper_bgcolor='rgba(0,0,0,0)',
                    plot_bgcolor='rgba(255,255,255,0.9)'
                )
                st.plotly_chart(fig, use_container_width=True)
            
            # Anomaly detection
            st.write("### 🚨 Detección de Anomalías")
            
            col1, col2 = st.columns(2)
            
            with col1:
                # Temperature anomalies
                temp_mean = df1['temperatura'].mean()
                temp_std = df1['temperatura'].std()
                temp_anomalies = df1[
                    (df1['temperatura'] > temp_mean + 2*temp_std) | 
                    (df1['temperatura'] < temp_mean - 2*temp_std)
                ]
                
                st.metric("🌡️ Anomalías de Temperatura", len(temp_anomalies))
                if len(temp_anomalies) > 0:
                    st.write("Valores anómalos de temperatura:")
                    st.dataframe(temp_anomalies[['temperatura']])
            
            with col2:
                # Humidity anomalies
                hum_mean = df1['humedad'].mean()
                hum_std = df1['humedad'].std()
                hum_anomalies = df1[
                    (df1['humedad'] > hum_mean + 2*hum_std) | 
                    (df1['humedad'] < hum_mean - 2*hum_std)
                ]
                
                st.metric("💧 Anomalías de Humedad", len(hum_anomalies))
                if len(hum_anomalies) > 0:
                    st.write("Valores anómalos de humedad:")
                    st.dataframe(hum_anomalies[['humedad']])
            
            # Environmental comfort analysis
            st.write("### 🌿 Análisis de Confort Ambiental")
            
            # Define comfort zones
            comfort_temp_min, comfort_temp_max = 18, 26
            comfort_hum_min, comfort_hum_max = 30, 70
            
            df1['confort_temp'] = (df1['temperatura'] >= comfort_temp_min) & (df1['temperatura'] <= comfort_temp_max)
            df1['confort_hum'] = (df1['humedad'] >= comfort_hum_min) & (df1['humedad'] <= comfort_hum_max)
            df1['confort_total'] = df1['confort_temp'] & df1['confort_hum']
            
            comfort_percentage = (df1['confort_total'].sum() / len(df1)) * 100
            
            col1, col2, col3 = st.columns(3)
            
            with col1:
                st.metric("🌡️ Confort Térmico", f"{(df1['confort_temp'].sum() / len(df1)) * 100:.1f}%")
            
            with col2:
                st.metric("💧 Confort de Humedad", f"{(df1['confort_hum'].sum() / len(df1)) * 100:.1f}%")
            
            with col3:
                st.metric("🌿 Confort Total", f"{comfort_percentage:.1f}%")
            
            # Comfort zone visualization
            fig = px.scatter(df1, x='temperatura', y='humedad',
                           color='confort_total',
                           title="Zona de Confort Ambiental",
                           color_discrete_map={True: '#40916C', False: '#FF6B6B'})
            
            # Add comfort zone rectangle
            fig.add_shape(
                type="rect",
                x0=comfort_temp_min, y0=comfort_hum_min,
                x1=comfort_temp_max, y1=comfort_hum_max,
                line=dict(color="green", width=2, dash="dash"),
                fillcolor="rgba(64, 145, 108, 0.1)"
            )
            
            fig.update_layout(paper_bgcolor='rgba(0,0,0,0)',
                            plot_bgcolor='rgba(255,255,255,0.9)')
            st.plotly_chart(fig, use_container_width=True)

        with tab5:
            st.subheader("🌍 Información del Sitio de Medición")
            
            col1, col2 = st.columns(2)
            
            with col1:
                st.markdown("""
                <div class="info-box">
                <h3>📍 Ubicación del Sensor</h3>
                <p><strong>🔒 CLASIFICADO</strong></p>
                <p>🌍 <strong>Latitud:</strong> 6.2479</p>
                <p>🌍 <strong>Longitud:</strong> -75.6081</p>
                <p>⛰️ <strong>Altitud:</strong> ~1,495 metros sobre el nivel del mar</p>
                <p>🏞️ <strong>Ecosistema:</strong> Bosque húmedo montano bajo</p>
                <p>🌡️ <strong>Clima:</strong> Tropical de montaña</p>
                </div>
                """, unsafe_allow_html=True)
            
            with col2:
                st.markdown("""
                <div class="info-box">
                <h3>📱 Detalles del Sensor</h3>
                <p>🔧 <strong>Tipo:</strong> ESP32</p>
                <p>📊 <strong>Variables medidas:</strong></p>
                <ul>
                <li>🌡️ Temperatura (°C)</li>
                <li>💧 Humedad relativa (%)</li>
                </ul>
                <p>⏱️ <strong>Frecuencia:</strong> Según configuración</p>
                <p>🏫 <strong>Ubicación:</strong> Campus universitario</p>
                <p>🌿 <strong>Entorno:</strong> Zona verde urbana</p>
                <p>🔋 <strong>Alimentación:</strong> Solar/Batería</p>
                </div>
                """, unsafe_allow_html=True)
            
            # Environmental context
            st.markdown("""
            <div class="info-box">
            <h3>🌱 Contexto Ambiental</h3>
            <p>El sensor está ubicado en un entorno que representa las condiciones microclimáticas 
            típicas de un ecosistema urbano en la región andina colombiana. Los datos recolectados 
            contribuyen al monitoreo de la calidad ambiental y el confort climático en espacios verdes urbanos.</p>
            
            <p><strong>🌿 Características del sitio:</strong></p>
            <ul>
            <li>🌳 Presencia de vegetación nativa y ornamental</li>
            <li>🏢 Influencia de infraestructura urbana</li>
            <li>💨 Circulación de aire natural</li>
            <li>☀️ Exposición solar variable por cobertura arbórea</li>
            </ul>
            </div>
            """, unsafe_allow_html=True)

    except Exception as e:
        st.error(f'❌ Error al procesar el archivo: {str(e)}')
        st.info("🔧 Verifique que el archivo CSV tenga el formato correcto y las columnas esperadas.")
else:
    st.markdown("""
    <div class="info-box">
    <h3>🌱 ¡Bienvenido al Análisis Ambiental!</h3>
    <p>Por favor, carga un archivo CSV con datos de sensores para comenzar el análisis.</p>
    <p>📁 El archivo debe contener columnas de tiempo, temperatura y humedad.</p>
    </div>
    """, unsafe_allow_html=True)
    
# Footer with nature theme
st.markdown("""
    ---
    <div style="text-align: center; color: #1B4332; padding: 2rem;">
    🌿 <strong>Desarrollado para el análisis de datos de sensores ambientales</strong> 🌿<br>
    📍 <strong>Ubicación:</strong> CLASIFICADO, Medellín, Colombia 🇨🇴<br>
    🌍 <em>Monitoreando nuestro entorno natural para un futuro sostenible</em> 🌱
    </div>
""", unsafe_allow_html=True)
