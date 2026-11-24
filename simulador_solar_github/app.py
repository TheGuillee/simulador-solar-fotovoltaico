"""
=============================================================================
PROYECTO: Simulador Solar Fotovoltaico Residencial
CURSO: Fundamentos de Programación - Ingeniería Energética
INTERFAZ: Dashboard Integral con Monitoreo, Estado de Paneles,
          Moneda en Pesos Colombianos (COP), Selección de Vivienda y
          Base de Datos con Calendario e Historial Anual (app.py)

ESTRUCTURA Y DISTRIBUCIÓN:
1. Navegación Superior con Pestañas Muy Próximas:
   - ☀️ Simulador Solar Fotovoltaico
   - 📅 Historial Energético y Base de Datos Anual
2. Pestaña Simulador:
   - Encabezado con Vivienda y Tarifa Eléctrica en COP ($/kWh).
   - Barra de Acciones (Modo claro/oscuro, Caso de verificación, Restablecer, Exportar JSON).
   - Selector directo de Vivienda ("Vivienda 1", "Vivienda 2", "Vivienda 3", "Casa 12", etc.).
   - Modificación dinámica de Tarifa en Pesos Colombianos.
   - Tarjetas KPI con moneda en COP.
   - Controles de paneles, potencia, pérdidas, día nublado y salud de paneles.
   - Matriz visual del tejado digital.
   - Integración: Guardar simulación actual en el Historial Energético (con protección anti-duplicados).
   - Gráfica interactiva 24h con curvas real, óptima, consumo, excedente y déficit.
   - Comparador 4 vs 8 paneles, Historial semanal y Tabla horaria estilizada.
3. Pestaña Historial Energético:
   - Organización jerárquica por Vivienda y Fecha (YYYY-MM-DD).
   - Navegación por Años y Meses (Enero a Diciembre).
   - Calendario mensual en cuadrícula de 7 columnas (Lunes a Domingo).
   - Identificación visual: 🟢 Día Óptimo, 🟡 Día Afectado, ⚪ Día Vacío.
   - Inspección completa de día: 14 métricas, curva horaria, carga al simulador y eliminación.
   - Analítica energética: Resumen mensual, resumen anual, gráfico de 12 meses y comparativa Laborables vs Fin de semana.
=============================================================================
"""

import os
import json
from datetime import date, datetime
import streamlit as st
import plotly.graph_objects as go

# Lógica pura construida exclusivamente con fundamentos de programación
from logica import (
    cargar_datos_json,
    guardar_escenarios_json,
    ejecutar_simulacion_completa,
    comparar_dos_escenarios,
    generar_historial_semanal_inicial,
    agregar_dia_al_historial,
    calcular_resumen_semanal,
    generar_matriz_paneles,
    FACTORES_ESTADO,
    # Funciones de Calendario, Historial y Base de Datos
    MESES_NOMBRES,
    DIAS_SEMANA_CORTOS,
    DIAS_SEMANA_LARGOS,
    es_anio_bisiesto,
    obtener_dias_del_mes,
    obtener_dia_semana_indice,
    obtener_dia_semana_nombre,
    generar_grilla_calendario_mes,
    cargar_base_datos_historial,
    guardar_base_datos_historial,
    obtener_viviendas_registradas,
    obtener_fechas_vivienda,
    existe_registro_dia,
    obtener_registro_dia,
    crear_registro_dia,
    guardar_registro_dia,
    eliminar_registro_dia,
    vaciar_historial_vivienda,
    obtener_ultimos_dias_registrados,
    obtener_resumen_mensual_historial,
    obtener_resumen_anual_historial,
    obtener_estadisticas_dias_semana,
    comparar_anios_historial
)

# -----------------------------------------------------------------------------
# 1. CONFIGURACIÓN DE PÁGINA Y ESTILOS GLOBALES
# -----------------------------------------------------------------------------
st.set_page_config(
    page_title="Simulador solar fotovoltaico residencial",
    page_icon="☀️",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# Inyección de estilos CSS para dashboard de monitoreo energético profesional
st.markdown("""
<style>
    /* 1. Fondo General y Tipografía */
    .stApp {
        background-color: #0B1220 !important;
        color: #FFFFFF !important;
        font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, "Helvetica Neue", Arial, sans-serif;
    }
    
    .block-container {
        padding-top: 4.2rem !important;
        padding-bottom: 2.5rem !important;
        max-width: 96% !important;
    }
    
    /* 2. Pestañas de Navegación Principal Superiores - MUY JUNTAS Y DESPEJADAS */
    div[data-baseweb="tab-list"] {
        gap: 6px !important;
        border-bottom: 2px solid #233354 !important;
        margin-top: 8px !important;
        margin-bottom: 18px !important;
        padding-bottom: 0px !important;
    }
    button[data-baseweb="tab"] {
        padding: 8px 20px !important;
        margin-right: 4px !important;
        border-radius: 8px 8px 0 0 !important;
        font-weight: 700 !important;
        font-size: 0.96rem !important;
        background-color: #141E33 !important;
        color: #94A3B8 !important;
        border: 1px solid #233354 !important;
        border-bottom: none !important;
        transition: all 0.2s ease !important;
    }
    button[data-baseweb="tab"]:hover {
        background-color: #1F2D4A !important;
        color: #38BDF8 !important;
    }
    button[data-baseweb="tab"][aria-selected="true"] {
        background-color: #18243D !important;
        color: #38BDF8 !important;
        border: 1px solid #38BDF8 !important;
        border-bottom: 2px solid #18243D !important;
    }

    /* 3. Encabezado Superior (A) */
    .header-box {
        margin-bottom: 12px;
    }
    .header-title-text {
        font-size: 2.15rem;
        font-weight: 800;
        color: #FFFFFF;
        letter-spacing: -0.5px;
        margin: 0;
        padding: 0;
        display: flex;
        align-items: center;
        gap: 12px;
    }
    .header-sub-text {
        font-size: 0.95rem;
        color: #8B9CB8;
        margin-top: 4px;
        font-weight: 500;
    }
    .header-sub-text b {
        color: #E2E8F0;
    }

    /* 4. Barra de Acciones y Botones */
    .stButton > button {
        background-color: #18243D !important;
        color: #FFFFFF !important;
        border: 1px solid #2A3859 !important;
        border-radius: 8px !important;
        font-weight: 600 !important;
        font-size: 0.88rem !important;
        padding: 6px 14px !important;
        transition: all 0.2s ease !important;
        white-space: nowrap !important;
    }
    .stButton > button:hover {
        background-color: #233354 !important;
        border-color: #38BDF8 !important;
        color: #38BDF8 !important;
        transform: translateY(-1px);
    }
    
    /* 5. Barra Horizontal de Resumen */
    .summary-bar {
        background-color: #18243D;
        border: 1px solid #233354;
        border-left: 5px solid #10B981;
        border-radius: 8px;
        padding: 12px 18px;
        margin-top: 10px;
        margin-bottom: 16px;
        font-size: 1.08rem;
        font-weight: 600;
        color: #F8FAFC;
        display: flex;
        align-items: center;
        gap: 10px;
        box-shadow: 0 4px 14px rgba(0, 0, 0, 0.25);
    }
    .highlight-green-val {
        color: #10B981;
        font-weight: 800;
        font-size: 1.15rem;
    }

    /* 6. Tarjetas Principales (D) */
    .kpi-grid-card {
        background-color: #18243D;
        border: 1px solid #233354;
        border-radius: 12px;
        padding: 16px 18px;
        min-height: 125px;
        display: flex;
        flex-direction: column;
        justify-content: space-between;
        box-shadow: 0 4px 16px rgba(0, 0, 0, 0.25);
        transition: transform 0.15s ease, border-color 0.15s ease;
    }
    .kpi-grid-card:hover {
        transform: translateY(-2px);
        border-color: #38BDF8;
    }
    .kpi-top-row {
        display: flex;
        align-items: center;
        gap: 8px;
        margin-bottom: 4px;
    }
    .kpi-icon-symbol {
        font-size: 1.25rem;
    }
    .kpi-label-text {
        font-size: 0.78rem;
        font-weight: 700;
        text-transform: uppercase;
        letter-spacing: 0.6px;
        color: #94A3B8;
    }
    .kpi-main-number {
        font-size: 1.85rem;
        font-weight: 800;
        color: #FFFFFF;
        line-height: 1.15;
    }
    .kpi-unit-symbol {
        font-size: 0.92rem;
        font-weight: 600;
        color: #94A3B8;
    }
    .kpi-desc-text {
        font-size: 0.78rem;
        color: #64748B;
        font-weight: 500;
        margin-top: 4px;
    }

    /* Tarjeta Especial de Ahorro: Verde Radiante */
    .kpi-savings-highlight {
        background: linear-gradient(135deg, #10B981 0%, #059669 100%) !important;
        border: 1px solid #34D399 !important;
        border-radius: 12px;
        padding: 16px 18px;
        min-height: 125px;
        display: flex;
        flex-direction: column;
        justify-content: space-between;
        box-shadow: 0 6px 22px rgba(16, 185, 129, 0.32);
        transition: transform 0.15s ease;
    }
    .kpi-savings-highlight:hover {
        transform: translateY(-2px);
    }
    .kpi-savings-highlight .kpi-label-text {
        color: #064E3B !important;
        font-weight: 800;
    }
    .kpi-savings-highlight .kpi-main-number {
        color: #0B1220 !important;
        font-weight: 900;
    }
    .kpi-savings-highlight .kpi-desc-text {
        color: #044332 !important;
        font-weight: 600;
    }

    /* 7. Paneles de Trabajo (E) */
    .panel-container {
        background-color: #18243D;
        border: 1px solid #233354;
        border-radius: 14px;
        padding: 18px 20px;
        box-shadow: 0 4px 20px rgba(0, 0, 0, 0.25);
    }
    .panel-headline {
        font-size: 1.22rem;
        font-weight: 800;
        color: #FFFFFF;
        margin-bottom: 16px;
        display: flex;
        align-items: center;
        gap: 8px;
    }

    .slider-title-row {
        display: flex;
        justify-content: space-between;
        align-items: center;
        font-weight: 600;
        font-size: 0.92rem;
        color: #E2E8F0;
        margin-bottom: -6px;
    }
    .slider-value-pill {
        color: #38BDF8;
        font-weight: 700;
        font-size: 0.95rem;
    }

    /* Contenedor del Estado de Paneles */
    .health-section-box {
        background-color: rgba(11, 18, 32, 0.7);
        border: 1px solid #2A3859;
        border-radius: 10px;
        padding: 14px 16px;
        margin-top: 14px;
        margin-bottom: 14px;
    }
    .health-header-row {
        display: flex;
        justify-content: space-between;
        align-items: center;
        margin-bottom: 10px;
    }
    .health-title-label {
        font-weight: 700;
        font-size: 0.92rem;
        color: #F1F5F9;
        display: flex;
        align-items: center;
        gap: 6px;
    }
    .health-badge-pill {
        font-size: 0.82rem;
        font-weight: 800;
        padding: 3px 10px;
        border-radius: 12px;
    }

    /* Matriz Visual del Techo (Techo Digital) */
    .roof-grid-container {
        display: grid;
        grid-template-columns: repeat(auto-fill, minmax(44px, 1fr));
        gap: 6px;
        margin-top: 10px;
        margin-bottom: 8px;
    }
    .panel-tile {
        background: #0F172A;
        border: 1.5px solid;
        border-radius: 6px;
        padding: 4px 2px;
        text-align: center;
        font-size: 0.72rem;
        font-weight: 700;
        color: #F8FAFC;
        box-shadow: 0 2px 6px rgba(0, 0, 0, 0.2);
        transition: transform 0.15s ease;
    }
    .panel-tile:hover {
        transform: scale(1.08);
    }

    .installed-power-banner {
        background-color: rgba(11, 18, 32, 0.65);
        border: 1px solid #2A3859;
        border-radius: 8px;
        padding: 12px 14px;
        margin-top: 12px;
        margin-bottom: 14px;
        display: flex;
        justify-content: space-between;
        align-items: center;
    }
    .installed-power-label {
        font-size: 0.88rem;
        font-weight: 600;
        color: #94A3B8;
    }
    .installed-power-val {
        font-size: 1.2rem;
        font-weight: 800;
        color: #FBBF24;
    }

    /* TABLA HORARIA ESTILIZADA NATIVA */
    .styled-table-wrap {
        border-radius: 10px;
        overflow: hidden;
        border: 1px solid #233354;
        background-color: #18243D;
        box-shadow: 0 4px 16px rgba(0, 0, 0, 0.25);
    }
    .styled-energy-table {
        width: 100%;
        border-collapse: collapse;
        font-size: 0.88rem;
        text-align: right;
    }
    .styled-energy-table th {
        background-color: #0E1729;
        color: #8B9CB8;
        font-weight: 700;
        font-size: 0.78rem;
        letter-spacing: 0.5px;
        text-transform: uppercase;
        padding: 12px 14px;
        border-bottom: 2px solid #233354;
    }
    .styled-energy-table td {
        padding: 10px 14px;
        border-bottom: 1px solid rgba(35, 51, 84, 0.6);
        color: #E2E8F0;
        font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, monospace;
    }
    .styled-energy-table tr:nth-child(even) {
        background-color: #141E33;
    }
    .styled-energy-table tr:hover {
        background-color: rgba(56, 189, 248, 0.08);
    }
    .badge-diag {
        display: inline-block;
        padding: 3px 8px;
        border-radius: 12px;
        font-size: 0.74rem;
        font-weight: 700;
        text-transform: uppercase;
        letter-spacing: 0.3px;
        white-space: nowrap;
    }

    /* ESTILOS EXCLUSIVOS PARA EL CALENDARIO E HISTORIAL */
    .cal-day-card {
        border-radius: 8px;
        padding: 8px 6px;
        min-height: 82px;
        text-align: center;
        display: flex;
        flex-direction: column;
        justify-content: space-between;
        box-shadow: 0 2px 8px rgba(0,0,0,0.25);
        transition: transform 0.15s ease, border-color 0.15s ease;
    }
    .cal-day-card:hover {
        transform: translateY(-2px);
    }
    .cal-day-optimal {
        background-color: #122822;
        border: 1.5px solid #10B981;
    }
    .cal-day-affected {
        background-color: #2D2311;
        border: 1.5px solid #F59E0B;
    }
    .cal-day-empty {
        background-color: #121A2C;
        border: 1px dashed #233354;
        opacity: 0.85;
    }
    .cal-header-weekday {
        text-align: center;
        font-weight: 800;
        font-size: 0.82rem;
        color: #94A3B8;
        padding: 8px 4px;
        background: #0E1729;
        border-radius: 6px;
        letter-spacing: 0.5px;
    }
    .cal-day-number {
        font-size: 0.95rem;
        font-weight: 800;
        color: #FFFFFF;
    }
    .cal-metric-snippet {
        font-size: 0.76rem;
        font-weight: 700;
        margin-top: 2px;
    }
    .cal-badge-pill-sm {
        display: inline-block;
        font-size: 0.68rem;
        font-weight: 700;
        padding: 1px 6px;
        border-radius: 8px;
    }

    [data-testid="collapsedControl"] {
        display: none;
    }
</style>
""", unsafe_allow_html=True)


# -----------------------------------------------------------------------------
# 2. GESTIÓN DEL ESTADO Y BASE DE DATOS
# -----------------------------------------------------------------------------
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
RUTA_ENTRADA_DEFAULT = os.path.join(BASE_DIR, "datos", "entrada.json")
RUTA_CASO_VERIF = os.path.join(BASE_DIR, "datos", "caso_verificacion.json")
RUTA_HISTORIAL_DB = os.path.join(BASE_DIR, "datos", "historial_energetico.json")

if "tema_modo" not in st.session_state:
    st.session_state.tema_modo = "oscuro"

if "escenarios_guardados" not in st.session_state:
    st.session_state.escenarios_guardados = []

# Carga de datos base de entrada
if "datos_actuales" not in st.session_state:
    if os.path.exists(RUTA_ENTRADA_DEFAULT):
        st.session_state.datos_actuales = cargar_datos_json(RUTA_ENTRADA_DEFAULT)
    else:
        st.session_state.datos_actuales = {
            "vivienda": "Casa 12",
            "tarifa": 800.0,
            "perfil": [0.0]*6 + [0.05, 0.2, 0.45, 0.7, 0.9, 1.0, 0.95, 0.85, 0.65, 0.4, 0.15, 0.02] + [0.0]*6,
            "consumo": [0.4, 0.3, 0.3, 0.3, 0.3, 0.4, 0.8, 1.2, 0.9, 0.6, 0.5, 0.7, 1.1, 0.8, 0.6, 0.7, 0.9, 1.3, 1.6, 1.5, 1.2, 0.8, 0.5, 0.4],
            "sistema": {"paneles": 4, "kw_panel": 0.5, "perdidas": 0.2}
        }

# Carga de la Base de Datos Histórica Anual
if "db_historial" not in st.session_state:
    st.session_state.db_historial = cargar_base_datos_historial(RUTA_HISTORIAL_DB)

# Variables de selección activa
if "vivienda_activa" not in st.session_state:
    st.session_state.vivienda_activa = st.session_state.datos_actuales.get("vivienda", "Casa 12")

if "tarifa_activa_cop" not in st.session_state:
    st.session_state.tarifa_activa_cop = float(st.session_state.datos_actuales.get("tarifa", 800.0))

if "cal_anio_seleccionado" not in st.session_state:
    st.session_state.cal_anio_seleccionado = 2026

if "cal_mes_seleccionado" not in st.session_state:
    st.session_state.cal_mes_seleccionado = 11

if "dia_inspeccionado_fecha" not in st.session_state:
    st.session_state.dia_inspeccionado_fecha = "2026-11-22"

# Carga diferida de un día histórico hacia el simulador (evita StreamlitWidgetAlreadyInstantiatedError)
if "_dia_a_cargar_en_simulador" in st.session_state:
    fecha_cargar = st.session_state.pop("_dia_a_cargar_en_simulador")
    reg_a_cargar = obtener_registro_dia(st.session_state.db_historial, st.session_state.vivienda_activa, fecha_cargar)
    if reg_a_cargar and "perfiles" in reg_a_cargar:
        st.session_state.datos_actuales["perfil"] = reg_a_cargar["perfiles"]["perfil_solar"]
        st.session_state.datos_actuales["consumo"] = reg_a_cargar["perfiles"]["consumo"]
        st.session_state["slider_paneles"] = int(reg_a_cargar["paneles"])
        st.session_state["slider_kw_panel"] = float(reg_a_cargar["kw_panel"])
        st.session_state["slider_perdidas"] = int(reg_a_cargar["perdidas_porcentaje"])
        st.session_state["tarifa_activa_cop"] = float(reg_a_cargar["tarifa_cop"])
        st.session_state["chk_dia_nublado"] = bool(reg_a_cargar.get("es_dia_nublado", False))
        estados_c = reg_a_cargar.get("estados_paneles", {})
        st.session_state["input_sucios"] = int(estados_c.get("sucio", 0))
        st.session_state["input_fallas"] = int(estados_c.get("falla", 0))
        st.session_state["input_mantenimiento"] = int(estados_c.get("mantenimiento", 0))
        st.toast(f"¡Configuración de {fecha_cargar} cargada en el Simulador!", icon="☀️")

# Lectura de parámetros de simulación
datos = st.session_state.datos_actuales
sist_data = datos.get("sistema", {})
paneles_base = int(sist_data.get("paneles", 4))
kw_base = float(sist_data.get("kw_panel", 0.5))
perd_raw = sist_data.get("perdidas", 0.2)
perdidas_base = int(perd_raw * 100) if perd_raw <= 1.0 else int(perd_raw)
perfil_raw = datos.get("perfil", [])
consumo_raw = datos.get("consumo", [])
horas_totales = len(perfil_raw)

# Captura de valores actuales de controles de simulación
val_paneles = st.session_state.get("slider_paneles", paneles_base)
val_kw = st.session_state.get("slider_kw_panel", kw_base)
val_perd = st.session_state.get("slider_perdidas", perdidas_base)
val_nublado = st.session_state.get("chk_dia_nublado", False)

# Captura y acotamiento de estados de salud
num_sucios = st.session_state.get("input_sucios", 0)
num_fallas = st.session_state.get("input_fallas", 0)
num_mantenimiento = st.session_state.get("input_mantenimiento", 0)

total_afectados = num_sucios + num_fallas + num_mantenimiento
if total_afectados > val_paneles:
    cupo = val_paneles
    num_mantenimiento = min(num_mantenimiento, cupo)
    cupo -= num_mantenimiento
    num_fallas = min(num_fallas, cupo)
    cupo -= num_fallas
    num_sucios = min(num_sucios, cupo)
    
    st.session_state["input_mantenimiento"] = num_mantenimiento
    st.session_state["input_fallas"] = num_fallas
    st.session_state["input_sucios"] = num_sucios

num_operativos = max(0, val_paneles - (num_sucios + num_fallas + num_mantenimiento))
estados_dict = {
    "operativo": num_operativos,
    "sucio": num_sucios,
    "falla": num_fallas,
    "mantenimiento": num_mantenimiento
}

factor_clima_actual = 0.5 if val_nublado else 1.0
perdidas_fraccion_actual = val_perd / 100.0

# Ejecutamos la simulación considerando estados de salud y potencia óptima
simulacion_actual = ejecutar_simulacion_completa(
    perfil=perfil_raw,
    consumo=consumo_raw,
    paneles=val_paneles,
    kw_panel=val_kw,
    perdidas=perdidas_fraccion_actual,
    tarifa=float(st.session_state.tarifa_activa_cop),
    factor_clima=factor_clima_actual,
    estados=estados_dict
)

ind = simulacion_actual["indicadores"]
perfiles = simulacion_actual["perfiles"]
params = simulacion_actual["parametros"]
potencia_total_kwp = round(val_paneles * val_kw, 2)


# =============================================================================
# 3. NAVEGACIÓN SUPERIOR CON PESTAÑAS (MUY JUNTAS POR CSS)
# =============================================================================
tab_simulador, tab_historial = st.tabs([
    "☀️ Simulador Solar Fotovoltaico",
    "📅 Historial Energético y Base de Datos"
])


# =============================================================================
# =============================================================================
# PESTAÑA 1: SIMULADOR SOLAR FOTOVOLTAICO RESIDENCIAL
# =============================================================================
# =============================================================================
with tab_simulador:
    # -------------------------------------------------------------------------
    # A. ENCABEZADO SUPERIOR DEL SIMULADOR
    # -------------------------------------------------------------------------
    st.markdown(f"""
    <div class="header-box">
        <div class="header-title-text">
            <span>☀️</span> Simulador solar fotovoltaico residencial
        </div>
        <div class="header-sub-text">
            Vivienda activa: <b>{st.session_state.vivienda_activa}</b> &nbsp;&bull;&nbsp; 
            Tarifa eléctrica: <b>${st.session_state.tarifa_activa_cop:,.0f} COP/kWh</b> &nbsp;&bull;&nbsp; 
            <b>{horas_totales} horas simuladas</b>
        </div>
    </div>
    """, unsafe_allow_html=True)

    # -------------------------------------------------------------------------
    # B. BARRA DE ACCIONES Y CONFIGURACIÓN RÁPIDA (VIVIENDA Y TARIFA EN COP)
    # -------------------------------------------------------------------------
    col_b1, col_b2, col_b3, col_b4 = st.columns([1.6, 2.3, 2.0, 1.8], gap="small")
    with col_b1:
        btn_txt_tema = "☀️ Modo claro" if st.session_state.tema_modo == "oscuro" else "🌙 Modo oscuro"
        if st.button(f"🌓 {btn_txt_tema}", use_container_width=True):
            st.session_state.tema_modo = "claro" if st.session_state.tema_modo == "oscuro" else "oscuro"
            st.rerun()

    with col_b2:
        if st.button("🎓 Caso de verificación", use_container_width=True, help="Cargar caso de verificación 4 horas"):
            if os.path.exists(RUTA_CASO_VERIF):
                st.session_state.datos_actuales = cargar_datos_json(RUTA_CASO_VERIF)
                st.session_state.slider_paneles = 4
                st.session_state.slider_kw_panel = 0.50
                st.session_state.slider_perdidas = 20
                st.session_state.chk_dia_nublado = False
                st.session_state.input_sucios = 0
                st.session_state.input_fallas = 0
                st.session_state.input_mantenimiento = 0
                st.session_state.tarifa_activa_cop = 800.0
                st.toast("Caso de verificación de 4 horas cargado.", icon="🎓")
                st.rerun()

    with col_b3:
        if st.button("🔄 Restablecer", use_container_width=True, help="Restablecer a datos/entrada.json"):
            if os.path.exists(RUTA_ENTRADA_DEFAULT):
                st.session_state.datos_actuales = cargar_datos_json(RUTA_ENTRADA_DEFAULT)
                st.session_state.slider_paneles = 4
                st.session_state.slider_kw_panel = 0.50
                st.session_state.slider_perdidas = 20
                st.session_state.chk_dia_nublado = False
                st.session_state.input_sucios = 0
                st.session_state.input_fallas = 0
                st.session_state.input_mantenimiento = 0
                st.session_state.tarifa_activa_cop = 800.0
                st.toast("Configuración inicial restablecida.", icon="🔄")
                st.rerun()

    with col_b4:
        if len(st.session_state.escenarios_guardados) > 0:
            json_export_str = json.dumps(st.session_state.escenarios_guardados, indent=4, ensure_ascii=False)
            st.download_button(
                label="📥 Exportar JSON",
                data=json_export_str,
                file_name="escenarios_guardados.json",
                mime="application/json",
                use_container_width=True,
                help="Descargar escenarios en formato JSON"
            )
        else:
            st.button("📥 Exportar JSON", disabled=True, use_container_width=True, help="Guarda un escenario primero")

    # -------------------------------------------------------------------------
    # SELECTOR DIRECTO DE VIVIENDA ("Vivienda 1 o 2 o 3") Y TARIFA EN COP
    # -------------------------------------------------------------------------
    st.markdown("<div style='height: 6px;'></div>", unsafe_allow_html=True)
    with st.expander("🏠 Configurar Nombre de Vivienda y Tarifa Eléctrica (Pesos Colombianos - COP)", expanded=False):
        col_viv_input, col_tar_input = st.columns([2.5, 2.5])
        with col_viv_input:
            opciones_preset = ["Casa 12", "Vivienda 1", "Vivienda 2", "Vivienda 3", "➕ Escribir otro nombre..."]
            sel_preset = st.selectbox(
                "Seleccionar o escribir vivienda:",
                opciones_preset,
                index=0 if st.session_state.vivienda_activa not in ["Vivienda 1", "Vivienda 2", "Vivienda 3"] else (1 if st.session_state.vivienda_activa == "Vivienda 1" else (2 if st.session_state.vivienda_activa == "Vivienda 2" else 3)),
                key="sb_vivienda_preset"
            )
            if sel_preset == "➕ Escribir otro nombre...":
                nuevo_nom = st.text_input("Escribe el nombre de la vivienda:", value=st.session_state.vivienda_activa, key="txt_viv_personalizada")
                if nuevo_nom and nuevo_nom != st.session_state.vivienda_activa:
                    st.session_state.vivienda_activa = nuevo_nom
                    st.rerun()
            else:
                if sel_preset != st.session_state.vivienda_activa:
                    st.session_state.vivienda_activa = sel_preset
                    st.rerun()

        with col_tar_input:
            nueva_tarifa = st.number_input(
                "Tarifa eléctrica ($ COP/kWh):",
                min_value=50.0,
                max_value=5000.0,
                value=float(st.session_state.tarifa_activa_cop),
                step=50.0,
                format="%.0f",
                key="num_tarifa_cop_input"
            )
            if nueva_tarifa != st.session_state.tarifa_activa_cop:
                st.session_state.tarifa_activa_cop = nueva_tarifa
                st.rerun()

    # -------------------------------------------------------------------------
    # C. MENSAJE DE RESULTADOS (BARRA HORIZONTAL EN COP)
    # -------------------------------------------------------------------------
    st.markdown(f"""
    <div class="summary-bar">
        <span>💡</span>
        <span>El sol cubre el <span class="highlight-green-val">{ind['porcentaje_cubierto']} %</span> de la demanda y te ahorra <span class="highlight-green-val">${ind['ahorro_dia']:,.0f} COP</span> en el día.</span>
    </div>
    """, unsafe_allow_html=True)

    # -------------------------------------------------------------------------
    # D. CUATRO TARJETAS PRINCIPALES (CON MONEDA EN COP)
    # -------------------------------------------------------------------------
    c_card1, c_card2, c_card3, c_card4 = st.columns(4, gap="medium")

    with c_card1:
        st.markdown(f"""
        <div class="kpi-grid-card" style="border-top: 3px solid #10B981;">
            <div class="kpi-top-row">
                <span class="kpi-icon-symbol">🔋</span>
                <span class="kpi-label-text">AUTOCONSUMO</span>
            </div>
            <div class="kpi-main-number">{ind['total_autoconsumo']} <span class="kpi-unit-symbol">kWh</span></div>
            <div class="kpi-desc-text">Energía solar utilizada en la vivienda</div>
        </div>
        """, unsafe_allow_html=True)

    with c_card2:
        st.markdown(f"""
        <div class="kpi-grid-card" style="border-top: 3px solid #F59E0B;">
            <div class="kpi-top-row">
                <span class="kpi-icon-symbol">🔄</span>
                <span class="kpi-label-text">EXCEDENTE</span>
            </div>
            <div class="kpi-main-number">{ind['total_excedente']} <span class="kpi-unit-symbol">kWh</span></div>
            <div class="kpi-desc-text">Energía sobrante no consumida</div>
        </div>
        """, unsafe_allow_html=True)

    with c_card3:
        st.markdown(f"""
        <div class="kpi-grid-card" style="border-top: 3px solid #38BDF8;">
            <div class="kpi-top-row">
                <span class="kpi-icon-symbol">🎯</span>
                <span class="kpi-label-text">DEMANDA CUBIERTA</span>
            </div>
            <div class="kpi-main-number">{ind['porcentaje_cubierto']} <span class="kpi-unit-symbol">%</span></div>
            <div class="kpi-desc-text">Porcentaje cubierto por el sistema solar</div>
        </div>
        """, unsafe_allow_html=True)

    with c_card4:
        st.markdown(f"""
        <div class="kpi-savings-highlight">
            <div class="kpi-top-row">
                <span class="kpi-icon-symbol">💰</span>
                <span class="kpi-label-text">AHORRO DEL DÍA (COP)</span>
            </div>
            <div class="kpi-main-number">${ind['ahorro_dia']:,.0f} <span style="font-size:1.0rem; font-weight:800;">COP</span></div>
            <div class="kpi-desc-text">Dinero ahorrado en pesos colombianos</div>
        </div>
        """, unsafe_allow_html=True)

    st.markdown("<div style='height: 18px;'></div>", unsafe_allow_html=True)

    # -------------------------------------------------------------------------
    # E. ÁREA PRINCIPAL: CONTROLES Y GRÁFICA 24H
    # -------------------------------------------------------------------------
    col_izq, col_der = st.columns([3.6, 6.4], gap="medium")

    with col_izq:
        st.markdown('<div class="panel-container">', unsafe_allow_html=True)
        st.markdown('<div class="panel-headline">⚙️ Controles</div>', unsafe_allow_html=True)
        
        # 1. Número de paneles
        st.markdown(f"""
        <div class="slider-title-row">
            <span>Número de paneles</span>
            <span class="slider-value-pill">{val_paneles}</span>
        </div>
        """, unsafe_allow_html=True)
        slider_paneles = st.slider(
            label="Número de paneles slider",
            min_value=1,
            max_value=24,
            value=val_paneles,
            step=1,
            label_visibility="collapsed",
            key="slider_paneles"
        )
        
        st.markdown("<div style='height: 12px;'></div>", unsafe_allow_html=True)

        # 2. Potencia por panel (kW)
        st.markdown(f"""
        <div class="slider-title-row">
            <span>Potencia por panel (kW)</span>
            <span class="slider-value-pill">{val_kw:.2f} kW</span>
        </div>
        """, unsafe_allow_html=True)
        slider_kw = st.slider(
            label="Potencia por panel slider",
            min_value=0.10,
            max_value=1.00,
            value=val_kw,
            step=0.05,
            format="%.2f kW",
            label_visibility="collapsed",
            key="slider_kw_panel"
        )

        st.markdown("<div style='height: 12px;'></div>", unsafe_allow_html=True)

        # 3. Pérdidas del sistema (%)
        st.markdown(f"""
        <div class="slider-title-row">
            <span>Pérdidas del sistema</span>
            <span class="slider-value-pill">{val_perd} %</span>
        </div>
        """, unsafe_allow_html=True)
        slider_perd = st.slider(
            label="Pérdidas del sistema slider",
            min_value=0,
            max_value=50,
            value=val_perd,
            step=1,
            format="%d %%",
            label_visibility="collapsed",
            key="slider_perdidas"
        )

        st.markdown("<div style='height: 10px;'></div>", unsafe_allow_html=True)

        # 4. Día nublado
        chk_nublado = st.checkbox(
            "Día nublado (perfil × 0.5)",
            value=val_nublado,
            key="chk_dia_nublado"
        )

        # 5. Estado y Salud del Parque Solar
        eficiencia_val = params.get("eficiencia_tejado", 100.0)
        badge_bg = "#064E3B" if eficiencia_val >= 90 else ("#78350F" if eficiencia_val >= 70 else "#7F1D1D")
        badge_color = "#34D399" if eficiencia_val >= 90 else ("#FBBF24" if eficiencia_val >= 70 else "#F87171")

        st.markdown(f"""
        <div class="health-section-box">
            <div class="health-header-row">
                <span class="health-title-label">🛠️ Estado de los Paneles</span>
                <span class="health-badge-pill" style="background:{badge_bg}; color:{badge_color};">
                    {eficiencia_val}% Salud
                </span>
            </div>
        """, unsafe_allow_html=True)

        col_st1, col_st2 = st.columns(2)
        with col_st1:
            color_op = "#10B981" if num_operativos > 0 else "#EF4444"
            st.markdown(f"<span style='font-size:0.8rem; color:{color_op}; font-weight:700;'>🟢 Operativos: {num_operativos}</span>", unsafe_allow_html=True)
            nuevo_sucios = st.number_input(
                "🟡 Sucios (-20%):",
                min_value=0,
                max_value=val_paneles,
                value=num_sucios,
                step=1,
                key="input_sucios"
            )
        with col_st2:
            nuevo_fallas = st.number_input(
                "🔴 Con Falla (-80%):",
                min_value=0,
                max_value=val_paneles,
                value=num_fallas,
                step=1,
                key="input_fallas"
            )
            nuevo_mant = st.number_input(
                "⚪ Mantenimiento (0%):",
                min_value=0,
                max_value=val_paneles,
                value=num_mantenimiento,
                step=1,
                key="input_mantenimiento"
            )

        if num_operativos == 0:
            st.markdown("<div style='font-size:0.75rem; color:#EF4444; font-weight:700; margin-top:2px;'>⚠️ 0 paneles operativos (parque totalmente afectado)</div>", unsafe_allow_html=True)

        st.markdown("<div style='font-size:0.78rem; font-weight:700; color:#8B9CB8; margin-top:8px;'>Matriz Visual del Techo:</div>", unsafe_allow_html=True)
        matriz_modulos = generar_matriz_paneles(estados_dict, val_paneles)
        
        html_matriz = '<div class="roof-grid-container">'
        for p in matriz_modulos:
            html_matriz += f'<div class="panel-tile" style="border-color:{p["color"]};" title="Panel {p["id"]}: {p["etiqueta"]}">P{p["id"]}<br>{p["icono"]}</div>'
        html_matriz += '</div>'
        st.markdown(html_matriz, unsafe_allow_html=True)

        if params.get("energia_perdida_fallas", 0.0) > 0:
            st.markdown(f"""
            <div style="font-size:0.78rem; color:#FBBF24; margin-top:4px; font-weight:600;">
                ⚠️ Merma por fallas/suciedad: -{params['energia_perdida_fallas']} kWh/día (-${params['dinero_perdido_fallas']:,.0f} COP)
            </div>
            """, unsafe_allow_html=True)

        st.markdown('</div>', unsafe_allow_html=True)

        # 6. Potencia instalada
        st.markdown(f"""
        <div class="installed-power-banner">
            <span class="installed-power-label">⚡ Potencia total instalada:</span>
            <span class="installed-power-val">{potencia_total_kwp} kWp</span>
        </div>
        """, unsafe_allow_html=True)

        # 7. Guardar Escenario
        nom_esc_val = st.text_input(
            "Nombre del escenario:",
            value=f"{val_paneles} paneles ({potencia_total_kwp} kWp)",
            key="input_nom_esc"
        )
        if st.button("💾 Guardar escenario", use_container_width=True):
            esc_nuevo = {
                "id": len(st.session_state.escenarios_guardados) + 1,
                "nombre": nom_esc_val,
                "vivienda": st.session_state.vivienda_activa,
                "parametros": params,
                "indicadores": ind
            }
            st.session_state.escenarios_guardados.append(esc_nuevo)
            st.toast(f"¡Escenario '{nom_esc_val}' guardado!", icon="✅")

        # ---------------------------------------------------------------------
        # 8. INTEGRACIÓN CON HISTORIAL: GUARDAR DÍA EN LA BASE DE DATOS
        # ---------------------------------------------------------------------
        st.markdown("<div style='height: 10px;'></div>", unsafe_allow_html=True)
        with st.expander("📅 Guardar Simulación en Historial Anual", expanded=False):
            st.caption("Almacena este día con todos sus perfiles e indicadores en la base de datos.")
            fecha_guardar = st.date_input("Fecha del registro:", value=date(2026, 11, 22), key="fecha_guardar_sim")
            fecha_str = fecha_guardar.strftime("%Y-%m-%d")
            dia_sem_detectado = obtener_dia_semana_nombre(fecha_guardar.year, fecha_guardar.month, fecha_guardar.day)
            
            st.markdown(f"<span style='font-size:0.82rem; color:#94A3B8;'>Día de la semana: <b style='color:#38BDF8;'>{dia_sem_detectado}</b></span>", unsafe_allow_html=True)
            
            ya_existe = existe_registro_dia(st.session_state.db_historial, st.session_state.vivienda_activa, fecha_str)
            if ya_existe:
                st.warning(f"⚠️ Ya existe un registro para {fecha_str} en '{st.session_state.vivienda_activa}'. Al guardar se actualizará.")
            
            nota_reg = st.text_input("Nota u observación (opcional):", value="Simulación residencial", key="nota_guardar_sim")
            
            btn_add_label = "🔄 Actualizar Día en Historial" if ya_existe else "➕ Agregar Día al Historial"
            if st.button(btn_add_label, use_container_width=True, type="primary", key="btn_guardar_sim_ctrl"):
                reg_nuevo = crear_registro_dia(
                    fecha=fecha_str,
                    vivienda=st.session_state.vivienda_activa,
                    simulacion=simulacion_actual,
                    nota=nota_reg
                )
                db_act, es_act = guardar_registro_dia(st.session_state.db_historial, reg_nuevo)
                guardar_base_datos_historial(db_act, RUTA_HISTORIAL_DB)
                st.session_state.db_historial = db_act
                st.session_state.dia_inspeccionado_fecha = fecha_str
                msg_toast = f"¡Día {fecha_str} ({dia_sem_detectado}) actualizado con éxito!" if es_act else f"¡Día {fecha_str} ({dia_sem_detectado}) guardado en el historial!"
                st.toast(msg_toast, icon="🎉")
                st.rerun()

        st.markdown('</div>', unsafe_allow_html=True)

    # --- COLUMNA DERECHA: PANEL DE GRÁFICA ---
    with col_der:
        st.markdown('<div class="panel-container">', unsafe_allow_html=True)
        st.markdown('<div class="panel-headline">📊 Generación vs. consumo por hora</div>', unsafe_allow_html=True)
        
        total_h = len(perfil_raw)
        if total_h == 24:
            horas_labels = [f"{h:02d}:00" for h in range(24)]
            tick_pos = [f"{h:02d}:00" for h in range(0, 24, 3)]
            tick_textos = [f"{h:02d}:00" for h in range(0, 24, 3)]
        else:
            horas_labels = [f"H{h}" for h in range(total_h)]
            tick_pos = horas_labels
            tick_textos = horas_labels

        gen_serie = perfiles["generacion"]
        gen_optima_serie = perfiles.get("generacion_optima", gen_serie)
        con_serie = perfiles["consumo"]

        fig = go.Figure()

        fig.add_trace(go.Scatter(
            x=horas_labels,
            y=con_serie,
            mode='lines',
            line=dict(width=0),
            hoverinfo='skip',
            showlegend=False
        ))

        max_gen_curva = [max(g, c) for g, c in zip(gen_serie, con_serie)]
        fig.add_trace(go.Scatter(
            x=horas_labels,
            y=max_gen_curva,
            mode='lines',
            fill='tonexty',
            fillcolor='rgba(16, 185, 129, 0.35)',
            line=dict(width=0),
            hoverinfo='skip',
            name='Excedente (Sobra generación)',
            showlegend=True
        ))

        fig.add_trace(go.Scatter(
            x=horas_labels,
            y=gen_serie,
            mode='lines',
            line=dict(width=0),
            hoverinfo='skip',
            showlegend=False
        ))

        max_def_curva = [max(g, c) for g, c in zip(gen_serie, con_serie)]
        fig.add_trace(go.Scatter(
            x=horas_labels,
            y=max_def_curva,
            mode='lines',
            fill='tonexty',
            fillcolor='rgba(239, 68, 68, 0.28)',
            line=dict(width=0),
            hoverinfo='skip',
            name='Déficit (Compra a red)',
            showlegend=True
        ))

        fig.add_trace(go.Scatter(
            x=horas_labels,
            y=gen_optima_serie,
            mode='lines',
            name='Generación Óptima (Sin fallas)',
            line=dict(color='rgba(251, 191, 36, 0.50)', width=2.2, dash='dot'),
            hovertemplate="✨ Gen. Óptima: <b>%{y:.2f} kWh</b><extra></extra>"
        ))

        fig.add_trace(go.Scatter(
            x=horas_labels,
            y=gen_serie,
            mode='lines+markers',
            name='Generación Solar Real',
            line=dict(color='#F59E0B', width=3.5),
            marker=dict(size=7, color='#FBBF24', symbol='circle'),
            hovertemplate="☀️ Gen. Solar Real: <b>%{y:.2f} kWh</b><extra></extra>"
        ))

        fig.add_trace(go.Scatter(
            x=horas_labels,
            y=con_serie,
            mode='lines+markers',
            name='Consumo Eléctrico',
            line=dict(color='#3B82F6', width=3.5),
            marker=dict(size=7, color='#60A5FA', symbol='diamond'),
            hovertemplate="⚡ Consumo Eléctrico: <b>%{y:.2f} kWh</b><extra></extra>"
        ))

        es_oscuro = (st.session_state.tema_modo == "oscuro")
        bg_grafica = "#18243D" if es_oscuro else "#FFFFFF"
        color_txt = "#F8FAFC" if es_oscuro else "#0F172A"
        color_rejilla = "rgba(255, 255, 255, 0.08)" if es_oscuro else "rgba(0, 0, 0, 0.08)"

        fig.update_layout(
            plot_bgcolor=bg_grafica,
            paper_bgcolor=bg_grafica,
            margin=dict(l=35, r=20, t=45, b=35),
            height=430,
            hovermode="x unified",
            legend=dict(
                orientation="h",
                yanchor="bottom",
                y=1.02,
                xanchor="right",
                x=1,
                font=dict(size=11, color=color_txt),
                bgcolor="rgba(24, 36, 61, 0.75)" if es_oscuro else "rgba(255,255,255,0.75)"
            ),
            xaxis=dict(
                title=dict(text="<b>Hora del día</b>", font=dict(color=color_txt, size=12)),
                gridcolor=color_rejilla,
                tickmode='array',
                tickvals=tick_pos,
                ticktext=tick_textos,
                tickfont=dict(color=color_txt, size=11),
                zeroline=False
            ),
            yaxis=dict(
                title=dict(text="<b>Energía (kWh)</b>", font=dict(color=color_txt, size=12)),
                gridcolor=color_rejilla,
                tickfont=dict(color=color_txt, size=11),
                zeroline=True,
                zerolinecolor=color_rejilla
            )
        )

        st.plotly_chart(fig, use_container_width=True)
        st.markdown('</div>', unsafe_allow_html=True)

    # -------------------------------------------------------------------------
    # F. PESTAÑAS INFERIORES DEL SIMULADOR: COMPARADOR, HISTORIAL SEMANAL Y TABLA
    # -------------------------------------------------------------------------
    st.markdown("<div style='height: 18px;'></div>", unsafe_allow_html=True)
    tab_comp, tab_hist_sem, tab_datos = st.tabs([
        "⚖️ Comparador de Escenarios (4 vs 8 Paneles)",
        "📅 Historial Semanal (7 Días)",
        "📋 Tabla Horaria Detallada"
    ])

    with tab_comp:
        st.markdown('<div class="panel-container">', unsafe_allow_html=True)
        col_c_sel, col_c_res = st.columns([1, 2], gap="medium")
        
        with col_c_sel:
            st.markdown("#### Selección de Escenarios")
            if len(st.session_state.escenarios_guardados) < 2:
                st.info("💡 Pulsa el botón para cargar el preset 4 vs 8 paneles:")
                if st.button("➕ Cargar Preset: 4 Paneles vs 8 Paneles", use_container_width=True):
                    sim_4 = ejecutar_simulacion_completa(perfil_raw, consumo_raw, 4, val_kw, perdidas_fraccion_actual, float(st.session_state.tarifa_activa_cop), factor_clima_actual)
                    esc_1 = {
                        "id": 1,
                        "nombre": "4 Paneles (2.0 kWp)",
                        "vivienda": st.session_state.vivienda_activa,
                        "parametros": sim_4["parametros"],
                        "indicadores": sim_4["indicadores"]
                    }
                    sim_8 = ejecutar_simulacion_completa(perfil_raw, consumo_raw, 8, val_kw, perdidas_fraccion_actual, float(st.session_state.tarifa_activa_cop), factor_clima_actual)
                    esc_2 = {
                        "id": 2,
                        "nombre": "8 Paneles (4.0 kWp)",
                        "vivienda": st.session_state.vivienda_activa,
                        "parametros": sim_8["parametros"],
                        "indicadores": sim_8["indicadores"]
                    }
                    st.session_state.escenarios_guardados = [esc_1, esc_2]
                    st.rerun()

            nombres_esc = [e["nombre"] for e in st.session_state.escenarios_guardados]
            if len(nombres_esc) >= 2:
                esc_a_sel = st.selectbox("Escenario A:", nombres_esc, index=0)
                esc_b_sel = st.selectbox("Escenario B:", nombres_esc, index=1 if len(nombres_esc) > 1 else 0)

        with col_c_res:
            if len(st.session_state.escenarios_guardados) >= 2 and 'esc_a_sel' in locals() and 'esc_b_sel' in locals():
                obj_a = next(e for e in st.session_state.escenarios_guardados if e["nombre"] == esc_a_sel)
                obj_b = next(e for e in st.session_state.escenarios_guardados if e["nombre"] == esc_b_sel)

                res_comparacion = comparar_dos_escenarios(obj_a, obj_b)
                
                st.markdown(f"#### Mayor Ahorro Económico ➔ <span style='color: #10B981;'>{res_comparacion['ganador']}</span>", unsafe_allow_html=True)
                
                m1, m2, m3 = st.columns(3)
                with m1:
                    st.metric(
                        label="Diferencia de Ahorro",
                        value=f"${abs(res_comparacion['diferencia_ahorro']):,.0f} COP/día",
                        delta=f"{'+' if res_comparacion['diferencia_ahorro'] >= 0 else ''}${res_comparacion['diferencia_ahorro']:,.0f} COP"
                    )
                with m2:
                    st.metric(
                        label="Autoconsumo Escenario B",
                        value=f"{res_comparacion['autoconsumo_b']} kWh",
                        delta=f"{res_comparacion['diferencia_autoconsumo']:+.2f} kWh"
                    )
                with m3:
                    st.metric(
                        label="Excedente Escenario B",
                        value=f"{res_comparacion['excedente_b']} kWh",
                        delta=f"{res_comparacion['diferencia_excedente']:+.2f} kWh"
                    )

                st.markdown(f"""
                <div style="background: rgba(16, 185, 129, 0.1); border-left: 4px solid #10B981; padding: 12px 16px; border-radius: 8px; margin-top: 10px;">
                    <b style="color: #34D399;">📘 Diagnóstico Técnico de Saturación Solar:</b>
                    <p style="margin-top: 4px; font-size: 0.93rem; color: #E2E8F0; line-height: 1.5;">{res_comparacion['explicacion']}</p>
                </div>
                """, unsafe_allow_html=True)

                tabla_comp_data = [
                    {"Métrica": "Número de Paneles", esc_a_sel: obj_a["parametros"]["paneles"], esc_b_sel: obj_b["parametros"]["paneles"]},
                    {"Métrica": "Potencia Pico", esc_a_sel: f"{obj_a['parametros']['potencia_pico']} kWp", esc_b_sel: f"{obj_b['parametros']['potencia_pico']} kWp"},
                    {"Métrica": "Autoconsumo", esc_a_sel: f"{obj_a['indicadores']['total_autoconsumo']} kWh", esc_b_sel: f"{obj_b['indicadores']['total_autoconsumo']} kWh"},
                    {"Métrica": "Excedente", esc_a_sel: f"{obj_a['indicadores']['total_excedente']} kWh", esc_b_sel: f"{obj_b['indicadores']['total_excedente']} kWh"},
                    {"Métrica": "Cobertura Demanda", esc_a_sel: f"{obj_a['indicadores']['porcentaje_cubierto']}%", esc_b_sel: f"{obj_b['indicadores']['porcentaje_cubierto']}%"},
                    {"Métrica": "Ahorro Económico (COP)", esc_a_sel: f"${obj_a['indicadores']['ahorro_dia']:,.0f} COP", esc_b_sel: f"${obj_b['indicadores']['ahorro_dia']:,.0f} COP"}
                ]
                st.dataframe(tabla_comp_data, use_container_width=True)
        st.markdown('</div>', unsafe_allow_html=True)

    with tab_hist_sem:
        st.markdown('<div class="panel-container">', unsafe_allow_html=True)
        st.markdown(f"#### 📅 Historial de Días Registrados — {st.session_state.vivienda_activa}")
        st.caption("Base de datos unificada: agrega los días reales configurados en el simulador y consúltalos tanto aquí como en el calendario.")

        # 1. Widget directo para agregar el día actual al historial
        with st.container():
            col_add_f1, col_add_f2, col_add_f3 = st.columns([2.2, 2.5, 3.3], gap="small")
            with col_add_f1:
                f_sem_val = st.date_input("Fecha a registrar:", value=date(2026, 11, 22), key="fecha_input_tab_semanal")
                f_sem_str = f_sem_val.strftime("%Y-%m-%d")
            with col_add_f2:
                dia_nom_sem = obtener_dia_semana_nombre(f_sem_val.year, f_sem_val.month, f_sem_val.day)
                st.markdown(f"<div style='padding-top:28px; font-weight:700; color:#38BDF8; font-size:0.95rem;'>🗓️ {dia_nom_sem}</div>", unsafe_allow_html=True)
            with col_add_f3:
                st.markdown("<div style='height:24px;'></div>", unsafe_allow_html=True)
                existe_f_sem = existe_registro_dia(st.session_state.db_historial, st.session_state.vivienda_activa, f_sem_str)
                btn_txt_sem = "🔄 Actualizar este Día" if existe_f_sem else "➕ Agregar Día al Historial"
                if st.button(btn_txt_sem, use_container_width=True, type="primary", key="btn_add_tab_sem"):
                    reg_nuevo = crear_registro_dia(
                        fecha=f_sem_str,
                        vivienda=st.session_state.vivienda_activa,
                        simulacion=simulacion_actual,
                        nota="Registro manual desde pestaña semanal"
                    )
                    db_act, es_act = guardar_registro_dia(st.session_state.db_historial, reg_nuevo)
                    guardar_base_datos_historial(db_act, RUTA_HISTORIAL_DB)
                    st.session_state.db_historial = db_act
                    st.session_state.dia_inspeccionado_fecha = f_sem_str
                    msg_toast = f"¡Día {f_sem_str} ({dia_nom_sem}) actualizado con éxito!" if es_act else f"¡Día {f_sem_str} ({dia_nom_sem}) guardado en el historial!"
                    st.toast(msg_toast, icon="🎉")
                    st.rerun()

        st.markdown("<div style='height: 12px;'></div>", unsafe_allow_html=True)

        # 2. Consulta de los días reales registrados para esta vivienda
        dias_hist_reales = obtener_ultimos_dias_registrados(
            st.session_state.db_historial,
            st.session_state.vivienda_activa,
            limite=7
        )

        if len(dias_hist_reales) == 0:
            st.info(f"💡 No hay días registrados en el historial para '{st.session_state.vivienda_activa}'. Configura los controles a tu gusto, selecciona la fecha arriba y pulsa '➕ Agregar Día al Historial' para registrar tu primer día.")
        else:
            res_semana = calcular_resumen_semanal(dias_hist_reales)
            
            col_h_m1, col_h_m2, col_h_m3 = st.columns(3)
            with col_h_m1:
                st.metric("Ahorro Acumulado (COP)", f"${res_semana['total_ahorro_semana']:,.0f} COP")
            with col_h_m2:
                st.metric("Ahorro Promedio Diario", f"${res_semana['promedio_ahorro_dia']:,.0f} COP/día")
            with col_h_m3:
                st.metric("Autoconsumo Acumulado", f"{res_semana['total_autoconsumo_semana']} kWh")

            st.markdown("<div style='height: 10px;'></div>", unsafe_allow_html=True)
            st.markdown(f"##### Días Registrados ({len(dias_hist_reales)} días en historial)")
            
            num_cols = min(7, max(1, len(dias_hist_reales)))
            cols_dias = st.columns(num_cols)
            for idx, dia in enumerate(dias_hist_reales):
                col_target = cols_dias[idx % num_cols]
                with col_target:
                    es_afectado = "Merma" in dia["clima"]
                    border_color = "#F59E0B" if es_afectado else "#10B981"
                    badge_color = "#FBBF24" if es_afectado else "#34D399"
                    
                    st.markdown(f"""
                    <div style="background: #0B1220; border: 1.5px solid {border_color}; border-radius: 8px; padding: 10px; text-align: center;">
                        <b style="color: #FFFFFF; font-size: 0.9rem;">{dia['dia']}</b><br>
                        <span style="font-size: 0.74rem; color: #8B9CB8;">{dia['fecha']}</span><br>
                        <span style="font-size: 0.78rem; font-weight:700; color: {badge_color};">{dia['clima']}</span><br>
                        <span style="font-size: 1.05rem; font-weight: 800; color: #10B981;">${dia['ahorro']:,.0f} COP</span><br>
                        <span style="font-size: 0.75rem; color: #64748B;">{dia['autoconsumo']} kWh</span>
                    </div>
                    """, unsafe_allow_html=True)
                    
                    c_btn1, c_btn2 = st.columns(2)
                    with c_btn1:
                        if st.button("🔄 Cargar", key=f"btn_cargar_sem_{dia['fecha']}", use_container_width=True, help="Restaurar este día al simulador"):
                            st.session_state["_dia_a_cargar_en_simulador"] = dia["fecha"]
                            st.rerun()
                    with c_btn2:
                        if st.button("🗑️", key=f"btn_del_sem_{dia['fecha']}", use_container_width=True, help="Eliminar este día"):
                            eliminar_registro_dia(st.session_state.db_historial, st.session_state.vivienda_activa, dia["fecha"])
                            guardar_base_datos_historial(st.session_state.db_historial, RUTA_HISTORIAL_DB)
                            st.toast(f"Día {dia['fecha']} eliminado del historial.", icon="🗑️")
                            st.rerun()
        st.markdown('</div>', unsafe_allow_html=True)

    with tab_datos:
        st.markdown('<div class="panel-container">', unsafe_allow_html=True)
        st.markdown("#### 📋 Balance Energético Detallado Hora a Hora")
        st.caption("Valores horarios con codificación de colores según el vector de energía y diagnóstico de estado del sistema.")

        filas_html = []
        auto_serie = perfiles["autoconsumo"]
        exc_serie = perfiles["excedente"]
        def_serie = perfiles["deficit"]
        perfil_serie = perfiles["perfil_solar"]

        for i in range(total_h):
            h_str = horas_labels[i]
            p_val = perfil_serie[i]
            g_opt = gen_optima_serie[i]
            g_real = gen_serie[i]
            c_val = con_serie[i]
            a_val = auto_serie[i]
            e_val = exc_serie[i]
            d_val = def_serie[i]

            exc_str = f"<span style='color:#34D399; font-weight:700;'>{e_val:.2f} kWh</span>" if e_val > 0 else "<span style='color:#64748B;'>—</span>"
            def_str = f"<span style='color:#F43F5E; font-weight:700;'>{d_val:.2f} kWh</span>" if d_val > 0 else "<span style='color:#64748B;'>—</span>"
            
            merma_detectada = (g_opt - g_real) > 0.05
            if g_real >= c_val and c_val > 0:
                diag_html = '<span class="badge-diag" style="background:rgba(16,185,129,0.18); color:#10B981; border:1px solid #10B981;">🟢 100% Solar</span>'
            elif g_real > 0 and g_real < c_val:
                if merma_detectada:
                    diag_html = '<span class="badge-diag" style="background:rgba(245,158,11,0.22); color:#FBBF24; border:1px solid #F59E0B;">⚠️ Merma / Red</span>'
                else:
                    diag_html = '<span class="badge-diag" style="background:rgba(56,189,248,0.18); color:#38BDF8; border:1px solid #38BDF8;">🟡 Parcial Solar</span>'
            else:
                diag_html = '<span class="badge-diag" style="background:rgba(239,68,68,0.18); color:#EF4444; border:1px solid #EF4444;">🔴 Red Pura</span>'

            fila_str = f"<tr><td style='text-align: left; font-weight: 700; color: #FFFFFF;'>{h_str}</td><td style='color: #94A3B8;'>{p_val:.2f}</td><td style='color: #FDE68A;'>{g_opt:.2f} kWh</td><td style='color: #FBBF24; font-weight: 700;'>{g_real:.2f} kWh</td><td style='color: #38BDF8; font-weight: 700;'>{c_val:.2f} kWh</td><td style='color: #10B981; font-weight: 700;'>{a_val:.2f} kWh</td><td>{exc_str}</td><td>{def_str}</td><td style='text-align: center;'>{diag_html}</td></tr>"
            filas_html.append(fila_str)

        html_tabla = '<div class="styled-table-wrap"><table class="styled-energy-table"><thead><tr><th style="text-align: left;">Hora</th><th>Perfil Solar</th><th>Gen. Óptima</th><th>Gen. Real</th><th>Consumo</th><th>Autoconsumo</th><th>Excedente</th><th>Déficit Red</th><th style="text-align: center;">Diagnóstico</th></tr></thead><tbody>' + "".join(filas_html) + '</tbody></table></div>'
        st.markdown(html_tabla, unsafe_allow_html=True)
        st.markdown('</div>', unsafe_allow_html=True)


# =============================================================================
# =============================================================================
# PESTAÑA 2: HISTORIAL ENERGÉTICO Y BASE DE DATOS ANUAL (ALTERNATIVA A)
# =============================================================================
# =============================================================================
with tab_historial:
    db = st.session_state.db_historial
    viviendas_disponibles = obtener_viviendas_registradas(db)
    if st.session_state.vivienda_activa not in viviendas_disponibles:
        viviendas_disponibles.append(st.session_state.vivienda_activa)
        viviendas_disponibles.sort()

    # Barra Superior de Control de la Base de Datos
    col_h_top1, col_h_top2, col_h_top3 = st.columns([3.0, 2.0, 2.0], gap="medium")
    with col_h_top1:
        st.markdown(f"""
        <div style="font-size:1.4rem; font-weight:800; color:#FFFFFF; display:flex; align-items:center; gap:8px;">
            <span>📅</span> Historial Energético y Calendario
        </div>
        <div style="font-size:0.86rem; color:#8B9CB8;">
            Base de datos de registros diarios por vivienda y fecha (YYYY-MM-DD).
        </div>
        """, unsafe_allow_html=True)

    with col_h_top2:
        viv_sel_hist = st.selectbox(
            "🏠 Consultar Vivienda:",
            viviendas_disponibles,
            index=viviendas_disponibles.index(st.session_state.vivienda_activa) if st.session_state.vivienda_activa in viviendas_disponibles else 0,
            key="sb_viv_historial"
        )
        if viv_sel_hist != st.session_state.vivienda_activa:
            st.session_state.vivienda_activa = viv_sel_hist

    with col_h_top3:
        fechas_viv = obtener_fechas_vivienda(db, st.session_state.vivienda_activa)
        st.markdown(f"""
        <div style="background:#141E33; border:1px solid #233354; border-radius:8px; padding:10px 14px; text-align:right;">
            <span style="font-size:0.78rem; color:#8B9CB8; text-transform:uppercase; font-weight:700;">Días Registrados</span><br>
            <span style="font-size:1.35rem; font-weight:800; color:#10B981;">{len(fechas_viv)} días</span>
        </div>
        """, unsafe_allow_html=True)

    with st.expander("⚙️ Opciones avanzadas de base de datos", expanded=False):
        col_opt1, col_opt2 = st.columns([3, 2])
        with col_opt1:
            st.caption(f"Gestión de registros almacenados para **{st.session_state.vivienda_activa}**.")
        with col_opt2:
            if st.button("🗑️ Vaciar todos los registros de esta vivienda", use_container_width=True, type="secondary"):
                vaciar_historial_vivienda(db, st.session_state.vivienda_activa)
                guardar_base_datos_historial(db, RUTA_HISTORIAL_DB)
                st.session_state.db_historial = db
                st.toast(f"Se han eliminado todos los registros de {st.session_state.vivienda_activa}.", icon="🗑️")
                st.rerun()

    if len(fechas_viv) == 0:
        st.info(f"💡 No hay días registrados en el historial para '{st.session_state.vivienda_activa}'. Configura los controles en la pestaña '☀️ Simulador Solar Fotovoltaico' y agrega tu primer día, o haz clic en '➕ Crear' en cualquier día del calendario.")

    st.markdown("<div style='height: 12px;'></div>", unsafe_allow_html=True)

    # -------------------------------------------------------------------------
    # NAVEGADOR DE AÑO Y MESES
    # -------------------------------------------------------------------------
    col_nav_y1, col_nav_y2, col_nav_y3 = st.columns([1, 3, 1], gap="small")
    with col_nav_y1:
        if st.button("◀ Año Anterior", use_container_width=True):
            st.session_state.cal_anio_seleccionado -= 1
            st.rerun()
    with col_nav_y2:
        es_bis = es_anio_bisiesto(st.session_state.cal_anio_seleccionado)
        texto_bis = " (Bisiesto - 366 días)" if es_bis else ""
        st.markdown(f"""
        <div style="text-align:center; font-size:1.35rem; font-weight:800; color:#38BDF8; padding-top:4px;">
            AÑO {st.session_state.cal_anio_seleccionado} <span style="font-size:0.85rem; color:#94A3B8;">{texto_bis}</span>
        </div>
        """, unsafe_allow_html=True)
    with col_nav_y3:
        if st.button("Año Siguiente ▶", use_container_width=True):
            st.session_state.cal_anio_seleccionado += 1
            st.rerun()

    # Barra horizontal de los 12 meses
    st.markdown("<div style='height: 6px;'></div>", unsafe_allow_html=True)
    cols_m = st.columns(12, gap="small")
    for m_idx in range(1, 13):
        m_nom = MESES_NOMBRES[m_idx - 1]
        m_corto = m_nom[:3]
        # Conteo de días registrados en ese mes
        pref = f"{st.session_state.cal_anio_seleccionado:04d}-{m_idx:02d}-"
        dias_en_m = sum(1 for f in fechas_viv if f.startswith(pref))
        es_mes_sel = (m_idx == st.session_state.cal_mes_seleccionado)
        
        btn_label = f"{m_corto} ({dias_en_m})" if dias_en_m > 0 else f"{m_corto}"
        with cols_m[m_idx - 1]:
            tipo_btn = "primary" if es_mes_sel else "secondary"
            if st.button(btn_label, key=f"btn_mes_sel_{m_idx}", use_container_width=True, type=tipo_btn):
                st.session_state.cal_mes_seleccionado = m_idx
                st.rerun()

    # -------------------------------------------------------------------------
    # CALENDARIO MENSUAL EN CUADRÍCULA DE 7 COLUMNAS (LUNES A DOMINGO)
    # -------------------------------------------------------------------------
    anio_sel = st.session_state.cal_anio_seleccionado
    mes_sel = st.session_state.cal_mes_seleccionado
    nom_mes_sel = MESES_NOMBRES[mes_sel - 1]

    st.markdown(f"""
    <div style="margin-top:14px; margin-bottom:10px; display:flex; justify-content:space-between; align-items:center;">
        <span style="font-size:1.15rem; font-weight:800; color:#FFFFFF;">
            📅 Calendario de {nom_mes_sel} de {anio_sel}
        </span>
        <span style="font-size:0.82rem; color:#94A3B8;">
            Leyenda: <span style="color:#10B981; font-weight:700;">🟢 Óptimo (100% Salud)</span> &nbsp;&bull;&nbsp; 
            <span style="color:#F59E0B; font-weight:700;">🟡 Afectado / Sucio / Merma</span> &nbsp;&bull;&nbsp; 
            <span style="color:#64748B;">⚪ Sin Registro</span>
        </span>
    </div>
    """, unsafe_allow_html=True)

    grilla_mes = generar_grilla_calendario_mes(anio_sel, mes_sel)

    # Cabecera de días de la semana (Lunes a Domingo)
    cols_dias_cab = st.columns(7, gap="small")
    for idx_d, dia_nom_corto in enumerate(DIAS_SEMANA_CORTOS):
        with cols_dias_cab[idx_d]:
            st.markdown(f'<div class="cal-header-weekday">{dia_nom_corto}</div>', unsafe_allow_html=True)

    st.markdown("<div style='height: 4px;'></div>", unsafe_allow_html=True)

    # Renderizado de semanas del mes
    for sem_idx, semana in enumerate(grilla_mes):
        cols_sem = st.columns(7, gap="small")
        for d_idx, dia_num in enumerate(semana):
            with cols_sem[d_idx]:
                if dia_num is None:
                    # Espacio fuera del mes
                    st.markdown('<div style="min-height:82px; background:rgba(18,26,44,0.3); border-radius:8px; border:1px dashed #1A2538;"></div>', unsafe_allow_html=True)
                else:
                    fecha_str = f"{anio_sel:04d}-{mes_sel:02d}-{dia_num:02d}"
                    reg = obtener_registro_dia(db, st.session_state.vivienda_activa, fecha_str)
                    
                    if reg is not None:
                        # Día registrado
                        es_opt = (reg.get("estado_general") == "optimo")
                        clase_card = "cal-day-optimal" if es_opt else "cal-day-affected"
                        badge_txt = "🟢 Óptimo" if es_opt else "🟡 Afectado"
                        badge_color = "#10B981" if es_opt else "#F59E0B"
                        
                        ahorro_val = reg.get("ahorro_cop", 0.0)
                        auto_val = reg.get("autoconsumo_kwh", 0.0)
                        
                        st.markdown(f"""
                        <div class="cal-day-card {clase_card}">
                            <div style="display:flex; justify-content:space-between; align-items:center;">
                                <span class="cal-day-number">{dia_num}</span>
                                <span style="font-size:0.68rem; font-weight:800; color:{badge_color};">{badge_txt}</span>
                            </div>
                            <div class="cal-metric-snippet" style="color:#FFFFFF;">
                                ${ahorro_val:,.0f} COP
                            </div>
                            <div style="font-size:0.70rem; color:#94A3B8;">
                                {auto_val} kWh
                            </div>
                        </div>
                        """, unsafe_allow_html=True)
                        if st.button("👁️ Ver", key=f"btn_ver_{fecha_str}", use_container_width=True):
                            st.session_state.dia_inspeccionado_fecha = fecha_str
                            st.rerun()
                    else:
                        # Día sin información registrada
                        st.markdown(f"""
                        <div class="cal-day-card cal-day-empty">
                            <div style="text-align:left;">
                                <span class="cal-day-number" style="color:#64748B;">{dia_num}</span>
                            </div>
                            <div style="font-size:0.75rem; color:#475569; margin: 6px 0;">
                                Sin datos
                            </div>
                            <div style="font-size:0.68rem; color:#334155;">—</div>
                        </div>
                        """, unsafe_allow_html=True)
                        if st.button("➕ Crear", key=f"btn_crear_{fecha_str}", use_container_width=True):
                            st.session_state.dia_inspeccionado_fecha = fecha_str
                            st.rerun()

        st.markdown("<div style='height: 4px;'></div>", unsafe_allow_html=True)

    # -------------------------------------------------------------------------
    # TARJETA DE INSPECCIÓN DETALLADA DEL DÍA SELECCIONADO
    # -------------------------------------------------------------------------
    st.markdown("<div style='height: 18px;'></div>", unsafe_allow_html=True)
    dia_target = st.session_state.dia_inspeccionado_fecha
    reg_target = obtener_registro_dia(db, st.session_state.vivienda_activa, dia_target)

    st.markdown(f"""
    <div class="panel-container" style="border-left: 5px solid #38BDF8;">
        <div class="panel-headline">
            <span>🔍 Inspección Detallada del Día: {dia_target}</span>
        </div>
    """, unsafe_allow_html=True)

    if reg_target is not None:
        p_anio = reg_target.get("anio", 2026)
        p_mes = reg_target.get("mes", 11)
        p_dia = reg_target.get("dia", 22)
        dia_sem_nom = reg_target.get("dia_semana", obtener_dia_semana_nombre(p_anio, p_mes, p_dia))
        estados_reg = reg_target.get("estados_paneles", {})
        salud_reg = reg_target.get("salud_porcentaje", 100.0)
        es_opt_reg = (reg_target.get("estado_general") == "optimo")
        badge_header = "🟢 100% Salud Operativa" if es_opt_reg else f"🟡 {salud_reg}% Salud (Afectaciones Detectadas)"
        badge_hdr_color = "#10B981" if es_opt_reg else "#F59E0B"

        st.markdown(f"""
        <div style="display:flex; justify-content:space-between; align-items:center; margin-bottom:14px; background:#0F172A; padding:10px 14px; border-radius:8px; border:1px solid #233354;">
            <div>
                <b style="font-size:1.15rem; color:#FFFFFF;">{dia_sem_nom}, {p_dia} de {MESES_NOMBRES[p_mes - 1]} de {p_anio}</b> &nbsp;&bull;&nbsp; 
                <span style="color:#38BDF8; font-weight:600;">{reg_target.get('vivienda', st.session_state.vivienda_activa)}</span>
            </div>
            <div style="font-size:0.92rem; font-weight:800; color:{badge_hdr_color};">
                {badge_header}
            </div>
        </div>
        """, unsafe_allow_html=True)

        # Métricas de energía
        c_m1, c_m2, c_m3, c_m4 = st.columns(4, gap="medium")
        with c_m1:
            st.metric("Generación Solar", f"{reg_target.get('generacion_total_kwh', 0.0)} kWh")
        with c_m2:
            st.metric("Autoconsumo", f"{reg_target.get('autoconsumo_kwh', 0.0)} kWh")
        with c_m3:
            st.metric("Excedente", f"{reg_target.get('excedente_kwh', 0.0)} kWh")
        with c_m4:
            st.metric("Déficit / Red", f"{reg_target.get('deficit_kwh', 0.0)} kWh")

        # Métricas económicas y de sistema
        st.markdown("<div style='height: 10px;'></div>", unsafe_allow_html=True)
        c_f1, c_f2, c_f3, c_f4 = st.columns(4, gap="medium")
        with c_f1:
            st.metric("Ahorro Económico (COP)", f"${reg_target.get('ahorro_cop', 0.0):,.0f} COP")
        with c_f2:
            st.metric("Demanda Cubierta", f"{reg_target.get('demanda_cubierta_pct', 0.0)} %")
        with c_f3:
            st.metric("Tarifa Aplicada", f"${reg_target.get('tarifa_cop', 800.0):,.0f} COP/kWh")
        with c_f4:
            st.metric("Costo Factura Red", f"${reg_target.get('costo_con_solar_cop', 0.0):,.0f} COP")

        # Desglose del sistema y paneles
        st.markdown(f"""
        <div style="background:#121A2C; border:1px solid #233354; border-radius:8px; padding:12px 14px; margin-top:12px; margin-bottom:12px;">
            <div style="font-size:0.85rem; color:#8B9CB8; margin-bottom:6px;">
                <b>Configuración Técnica:</b> {reg_target.get('paneles', 4)} paneles &times; {reg_target.get('kw_panel', 0.5)} kWp ({reg_target.get('potencia_total_kwp', 2.0)} kWp) &nbsp;&bull;&nbsp; 
                Pérdidas: {reg_target.get('perdidas_porcentaje', 20)}% &nbsp;&bull;&nbsp; 
                Clima: {'🌧️ Día Nublado' if reg_target.get('es_dia_nublado') else '☀️ Normal'} &nbsp;&bull;&nbsp; 
                Observación: <i>{reg_target.get('nota', 'Sin notas')}</i>
            </div>
            <div style="font-size:0.84rem; font-weight:700;">
                Estado del Parque: 
                <span style="color:#10B981;">🟢 {estados_reg.get('operativo', 0)} Operativos</span> &nbsp;|&nbsp; 
                <span style="color:#F59E0B;">🟡 {estados_reg.get('sucio', 0)} Sucios (-20%)</span> &nbsp;|&nbsp; 
                <span style="color:#EF4444;">🔴 {estados_reg.get('falla', 0)} Fallas (-80%)</span> &nbsp;|&nbsp; 
                <span style="color:#94A3B8;">⚪ {estados_reg.get('mantenimiento', 0)} Mantenimiento</span>
            </div>
        </div>
        """, unsafe_allow_html=True)

        # Mini gráfica horaria si perfiles están disponibles
        if "perfiles" in reg_target:
            p_gen = reg_target["perfiles"].get("generacion", [])
            p_con = reg_target["perfiles"].get("consumo", [])
            tot_h_reg = len(p_gen)
            if tot_h_reg > 0:
                h_labs_reg = [f"{h:02d}:00" for h in range(tot_h_reg)] if tot_h_reg == 24 else [f"H{h}" for h in range(tot_h_reg)]
                fig_mini = go.Figure()
                fig_mini.add_trace(go.Scatter(x=h_labs_reg, y=p_gen, mode='lines+markers', name='Generación Solar', line=dict(color='#F59E0B', width=2.5)))
                fig_mini.add_trace(go.Scatter(x=h_labs_reg, y=p_con, mode='lines+markers', name='Consumo Eléctrico', line=dict(color='#3B82F6', width=2.5)))
                fig_mini.update_layout(
                    height=260,
                    plot_bgcolor="#121A2C",
                    paper_bgcolor="#121A2C",
                    margin=dict(l=30, r=20, t=30, b=30),
                    hovermode="x unified",
                    legend=dict(orientation="h", y=1.1, x=1, xanchor="right", font=dict(color="#FFFFFF", size=10)),
                    xaxis=dict(gridcolor="rgba(255,255,255,0.06)", tickfont=dict(color="#FFFFFF", size=10)),
                    yaxis=dict(title="kWh", gridcolor="rgba(255,255,255,0.06)", tickfont=dict(color="#FFFFFF", size=10))
                )
                st.plotly_chart(fig_mini, use_container_width=True)

        # Acciones para este día registrado
        col_acc1, col_acc2, col_acc3 = st.columns([2.5, 2.5, 3.0], gap="small")
        with col_acc1:
            if st.button("🔄 Cargar en el Simulador", use_container_width=True, help="Copiar perfiles y configuración al simulador"):
                if "perfiles" in reg_target:
                    st.session_state["_dia_a_cargar_en_simulador"] = dia_target
                    st.rerun()
        with col_acc2:
            if st.button("🗑️ Eliminar este Día", use_container_width=True, type="secondary"):
                eliminar_registro_dia(db, st.session_state.vivienda_activa, dia_target)
                guardar_base_datos_historial(db, RUTA_HISTORIAL_DB)
                st.session_state.db_historial = db
                st.toast(f"Día {dia_target} eliminado.", icon="🗑️")
                st.rerun()

    else:
        st.info(f"💡 No hay información registrada para la fecha **{dia_target}** en **{st.session_state.vivienda_activa}**.")
        st.markdown("<p style='font-size:0.88rem; color:#94A3B8;'>Puedes simular este día en la pestaña <b>☀️ Simulador Solar</b> y pulsar <b>'Guardar Simulación en Historial Anual'</b>, o registrarlo manualmente a continuación.</p>", unsafe_allow_html=True)
        if st.button(f"➕ Registrar {dia_target} con la simulación activa actual", type="primary"):
            reg_nuevo = crear_registro_dia(
                fecha=dia_target,
                vivienda=st.session_state.vivienda_activa,
                simulacion=simulacion_actual,
                nota="Registro rápido desde calendario"
            )
            db_act, _ = guardar_registro_dia(db, reg_nuevo)
            guardar_base_datos_historial(db_act, RUTA_HISTORIAL_DB)
            st.session_state.db_historial = db_act
            st.toast(f"¡Día {dia_target} guardado exitosamente!", icon="🎉")
            st.rerun()

    st.markdown('</div>', unsafe_allow_html=True)

    # -------------------------------------------------------------------------
    # ANALÍTICA Y ESTADÍSTICAS DEL HISTORIAL
    # -------------------------------------------------------------------------
    st.markdown("<div style='height: 18px;'></div>", unsafe_allow_html=True)
    st.markdown("### 📊 Estadísticas y Analítica Energética Anual")

    tab_an_mes, tab_an_ano, tab_an_habitos = st.tabs([
        "📆 Resumen Mensual",
        "📈 Balance Anual (12 Meses)",
        "🔄 Análisis Días Laborables vs Fin de Semana"
    ])

    with tab_an_mes:
        st.markdown('<div class="panel-container">', unsafe_allow_html=True)
        res_m = obtener_resumen_mensual_historial(db, st.session_state.vivienda_activa, anio_sel, mes_sel)
        
        st.markdown(f"#### Balance de {nom_mes_sel} {anio_sel} — {st.session_state.vivienda_activa}")
        
        c_rm1, c_rm2, c_rm3, c_rm4 = st.columns(4, gap="medium")
        with c_rm1:
            st.metric("Días Registrados", f"{res_m['dias_registrados']} días", delta=f"{res_m['dias_optimos']} óptimos / {res_m['dias_afectados']} afectados")
        with c_rm2:
            st.metric("Generación Total", f"{res_m['total_generacion_kwh']} kWh")
        with c_rm3:
            st.metric("Autoconsumo Total", f"{res_m['total_autoconsumo_kwh']} kWh")
        with c_rm4:
            st.metric("Ahorro Acumulado (COP)", f"${res_m['total_ahorro_cop']:,.0f} COP")

        st.markdown("<div style='height: 8px;'></div>", unsafe_allow_html=True)
        c_rm5, c_rm6, c_rm7 = st.columns(3)
        with c_rm5:
            st.metric("Cobertura Solar Media", f"{res_m['promedio_cobertura_pct']} %")
        with c_rm6:
            st.metric("Ahorro Promedio Diario", f"${res_m['promedio_ahorro_dia_cop']:,.0f} COP/día")
        with c_rm7:
            st.metric("Excedente Vertido Total", f"{res_m['total_excedente_kwh']} kWh")

        st.markdown('</div>', unsafe_allow_html=True)

    with tab_an_ano:
        st.markdown('<div class="panel-container">', unsafe_allow_html=True)
        res_a = obtener_resumen_anual_historial(db, st.session_state.vivienda_activa, anio_sel)
        
        st.markdown(f"#### Balance Acumulado del Año {anio_sel} — {st.session_state.vivienda_activa}")
        
        col_ra1, col_ra2, col_ra3 = st.columns(3)
        with col_ra1:
            st.metric("Total Días Monitoreados", f"{res_a['total_dias_registrados']} días")
        with col_ra2:
            st.metric("Generación Anual Total", f"{res_a['total_generacion_kwh']} kWh")
        with col_ra3:
            st.metric("Ahorro Anual Total (COP)", f"${res_a['total_ahorro_cop']:,.0f} COP")

        col_ra4, col_ra5 = st.columns(2)
        with col_ra4:
            st.info(f"🏆 **Mes con Mayor Ahorro:** {res_a['mejor_mes_ahorro']['mes']} (${res_a['mejor_mes_ahorro']['ahorro']:,.0f} COP)")
        with col_ra5:
            st.warning(f"📉 **Mes con Menor Generación:** {res_a['menor_mes_generacion']['mes']} ({res_a['menor_mes_generacion']['generacion']} kWh)")

        # Gráfico comparativo de los 12 meses
        nombres_12 = [m["nombre_mes"][:3] for m in res_a["meses"]]
        ahorros_12 = [m["total_ahorro_cop"] for m in res_a["meses"]]
        gen_12 = [m["total_generacion_kwh"] for m in res_a["meses"]]

        fig_anual = go.Figure()
        fig_anual.add_trace(go.Bar(x=nombres_12, y=ahorros_12, name="Ahorro ($ COP)", marker_color="#10B981", yaxis="y1"))
        fig_anual.add_trace(go.Scatter(x=nombres_12, y=gen_12, name="Generación (kWh)", mode="lines+markers", line=dict(color="#F59E0B", width=3), yaxis="y2"))
        
        fig_anual.update_layout(
            height=320,
            plot_bgcolor="#141E33",
            paper_bgcolor="#141E33",
            margin=dict(l=35, r=35, t=30, b=30),
            hovermode="x unified",
            legend=dict(orientation="h", y=1.1, x=1, xanchor="right", font=dict(color="#FFFFFF", size=10)),
            xaxis=dict(gridcolor="rgba(255,255,255,0.06)", tickfont=dict(color="#FFFFFF")),
            yaxis=dict(title="Ahorro ($ COP)", gridcolor="rgba(255,255,255,0.06)", tickfont=dict(color="#10B981")),
            yaxis2=dict(title="Generación (kWh)", overlaying="y", side="right", tickfont=dict(color="#F59E0B"))
        )
        st.plotly_chart(fig_anual, use_container_width=True)
        st.markdown('</div>', unsafe_allow_html=True)

    with tab_an_habitos:
        st.markdown('<div class="panel-container">', unsafe_allow_html=True)
        stats_sem = obtener_estadisticas_dias_semana(db, st.session_state.vivienda_activa)
        
        st.markdown(f"#### Comparativa de Patrones Energéticos: Lunes a Domingo ({st.session_state.vivienda_activa})")
        st.markdown(f"""
        <div style="background:rgba(56, 189, 248, 0.12); border-left:4px solid #38BDF8; padding:12px 16px; border-radius:8px; margin-bottom:14px;">
            <b style="color:#38BDF8;">📘 Diagnóstico de Hábitos de Consumo:</b>
            <p style="margin-top:4px; font-size:0.92rem; color:#E2E8F0; line-height:1.5;">{stats_sem['diagnostico_patron']}</p>
        </div>
        """, unsafe_allow_html=True)

        col_hab1, col_hab2 = st.columns(2)
        with col_hab1:
            st.metric("Promedio Días Laborables (Lun-Vie)", f"{stats_sem['promedio_laborable_kwh']} kWh/día")
        with col_hab2:
            st.metric("Promedio Fines de Semana (Sáb-Dom)", f"{stats_sem['promedio_fin_de_semana_kwh']} kWh/día")

        # Tabla por cada día de la semana
        tabla_dias_list = []
        for d in stats_sem["dias"]:
            tabla_dias_list.append({
                "Día": d["dia"],
                "Registros": d["cantidad"],
                "Consumo Promedio": f"{d['promedio_consumo_kwh']} kWh",
                "Gen. Promedio": f"{d['promedio_generacion_kwh']} kWh",
                "Autoconsumo Promedio": f"{d['promedio_autoconsumo_kwh']} kWh",
                "Ahorro Promedio": f"${d['promedio_ahorro_cop']:,.0f} COP"
            })
        st.dataframe(tabla_dias_list, use_container_width=True)
        st.markdown('</div>', unsafe_allow_html=True)
