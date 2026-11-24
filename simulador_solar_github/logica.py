"""
=============================================================================
PROYECTO: Simulador Solar Fotovoltaico Residencial
CURSO: Fundamentos de Programación - Ingeniería Energética
MÓDULO: Lógica de Simulación y Cálculos Energéticos (logica.py)

RESTRICCIÓN PEDAGÓGICA:
Este módulo utiliza únicamente conceptos fundamentales vistos en clase:
- Funciones con parámetros y sentencia return.
- Listas y métodos básicos (append, len, indexación).
- Diccionarios (claves y valores).
- Ciclos iterativos (for con range o iteración directa).
- Condicionales (if, elif, else).
- Variables locales acumuladoras y de cálculo.
- Módulo nativo json para persistencia de datos.
=============================================================================
"""

import json
import os
from datetime import date


def cargar_datos_json(ruta_archivo):
    """
    Carga y retorna los datos de configuración desde un archivo JSON.
    Parámetro:
        ruta_archivo (str): Ruta al archivo JSON.
    Retorna:
        dict: Diccionario con la estructura de datos cargada.
    """
    with open(ruta_archivo, "r", encoding="utf-8") as archivo:
        datos = json.load(archivo)
    return datos


def guardar_escenarios_json(escenarios, ruta_archivo):
    """
    Guarda una lista de escenarios simulados en un archivo JSON.
    Parámetros:
        escenarios (list): Lista de diccionarios con los escenarios.
        ruta_archivo (str): Ruta de destino para guardar el archivo JSON.
    Retorna:
        bool: True si la operación fue exitosa.
    """
    with open(ruta_archivo, "w", encoding="utf-8") as archivo:
        json.dump(escenarios, archivo, indent=4, ensure_ascii=False)
    return True


FACTORES_ESTADO = {
    "operativo": 1.0,       # 100% de potencia nominal
    "sucio": 0.80,          # -20% de rendimiento por suciedad/polvo (soiling)
    "falla": 0.20,          # -80% de rendimiento por falla de bypass/celdas
    "mantenimiento": 0.0    # 0% desconectado temporalmente por mantenimiento
}


def calcular_potencia_efectiva(paneles, kw_panel, perdidas, estados=None):
    """
    Calcula la potencia neta o efectiva del sistema fotovoltaico
    considerando la potencia pico instalada, el factor de pérdidas
    y opcionalmente la condición o estado de salud de cada grupo de paneles.
    Fórmula:
        Factor_Rendimiento = 1.0 - perdidas
        Potencia_Efectiva = Suma(cantidad_i * kw_panel * Factor_Rendimiento * Factor_Estado_i)
    """
    factor_rendimiento = 1.0 - perdidas

    if estados is None:
        # Modo estándar: todos los paneles operativos al 100%
        potencia_pico = paneles * kw_panel
        potencia_efectiva = potencia_pico * factor_rendimiento
    else:
        # Modo con estados: acumulación ponderada por estado de salud
        potencia_efectiva = 0.0
        for clave, factor in FACTORES_ESTADO.items():
            cantidad = estados.get(clave, 0)
            potencia_efectiva = potencia_efectiva + (cantidad * kw_panel * factor_rendimiento * factor)

    return potencia_efectiva


def generar_matriz_paneles(estados, total_paneles):
    """
    Genera una lista de diccionarios con el estado y color de cada panel individual
    para renderizar la matriz visual del tejado (representación física).
    Utiliza listas, ciclos for y diccionarios básicos.
    """
    if estados is None:
        estados = {"operativo": total_paneles, "sucio": 0, "falla": 0, "mantenimiento": 0}

    matriz = []
    id_panel = 1

    orden_estados = [
        ("operativo", "Operativo", "#10B981", "🟢", 1.0),
        ("sucio", "Sucio (-20%)", "#F59E0B", "🟡", 0.80),
        ("falla", "Con Falla (-80%)", "#EF4444", "🔴", 0.20),
        ("mantenimiento", "Mantenimiento (0%)", "#94A3B8", "⚪", 0.0)
    ]

    for clave, nombre_est, color, icono, factor in orden_estados:
        cantidad = estados.get(clave, 0)
        for _ in range(cantidad):
            if len(matriz) < total_paneles:
                matriz.append({
                    "id": id_panel,
                    "estado": clave,
                    "etiqueta": nombre_est,
                    "color": color,
                    "icono": icono,
                    "factor": factor
                })
                id_panel = id_panel + 1

    # Relleno de seguridad si la suma es menor al total de paneles
    while len(matriz) < total_paneles:
        matriz.append({
            "id": id_panel,
            "estado": "operativo",
            "etiqueta": "Operativo",
            "color": "#10B981",
            "icono": "🟢",
            "factor": 1.0
        })
        id_panel = id_panel + 1

    return matriz


def calcular_generacion_hora(perfil, paneles, kw_panel, perdidas, factor_clima=1.0, estados=None):
    """
    Calcula la generación solar hora a hora (kWh) a partir del perfil solar.
    Calcula tanto la generación real (con estados) como la generación óptima teórica.
    Parámetros:
        perfil (list): Lista con valores solares adimensionales (de 0 a 1).
        paneles (int): Número de paneles fotovoltaicos.
        kw_panel (float): Potencia nominal de cada panel en kW.
        perdidas (float): Fracción de pérdidas del sistema (ej: 0.20 para 20%).
        factor_clima (float): Factor de ajuste (1.0 = normal, 0.5 = día nublado).
        estados (dict): Opcional. Distribución de estados de los paneles.
    Retorna:
        tuple: (generacion_real, generacion_optima)
    """
    potencia_efectiva = calcular_potencia_efectiva(paneles, kw_panel, perdidas, estados)
    potencia_optima = (paneles * kw_panel) * (1.0 - perdidas)

    generacion_real = []
    generacion_optima = []

    for valor_solar in perfil:
        gen_hora = valor_solar * factor_clima * potencia_efectiva
        gen_opt = valor_solar * factor_clima * potencia_optima
        generacion_real.append(round(gen_hora, 4))
        generacion_optima.append(round(gen_opt, 4))

    return generacion_real, generacion_optima


def comparar_generacion_consumo(generacion, consumo):
    """
    Compara hora a hora la generación fotovoltaica contra la demanda de consumo.
    Calcula:
        - Autoconsumo: Energía solar usada directamente en la vivienda.
        - Excedente: Energía solar sobrante tras cubrir la demanda horaria.
        - Déficit: Energía faltante que debe comprarse a la red eléctrica.
    Parámetros:
        generacion (list): Generación por hora (kWh).
        consumo (list): Consumo por hora (kWh).
    Retorna:
        dict: Diccionario con tres listas: 'autoconsumo', 'excedente', 'deficit'.
    """
    autoconsumo = []
    excedente = []
    deficit = []

    total_horas = len(generacion)

    for i in range(total_horas):
        gen = generacion[i]
        con = consumo[i]

        if gen >= con:
            # La generación cubre toda la demanda de la hora
            auto_hora = con
            exc_hora = gen - con
            def_hora = 0.0
        else:
            # La generación es insuficiente; se autoconsume todo lo generado
            auto_hora = gen
            exc_hora = 0.0
            def_hora = con - gen

        autoconsumo.append(round(auto_hora, 4))
        excedente.append(round(exc_hora, 4))
        deficit.append(round(def_hora, 4))

    resultado = {
        "autoconsumo": autoconsumo,
        "excedente": excedente,
        "deficit": deficit
    }
    return resultado


def calcular_indicadores(generacion, consumo, balance, tarifa):
    """
    Calcula los totales energéticos diarios y los indicadores financieros.
    Parámetros:
        generacion (list): Lista de generación horaria.
        consumo (list): Lista de consumo horario.
        balance (dict): Diccionario retornado por comparar_generacion_consumo.
        tarifa (float): Costo de la energía eléctrica ($/kWh).
    Retorna:
        dict: Totales y métricas clave del día.
    """
    total_generacion = 0.0
    for g in generacion:
        total_generacion = total_generacion + g

    total_consumo = 0.0
    for c in consumo:
        total_consumo = total_consumo + c

    total_autoconsumo = 0.0
    for a in balance["autoconsumo"]:
        total_autoconsumo = total_autoconsumo + a

    total_excedente = 0.0
    for e in balance["excedente"]:
        total_excedente = total_excedente + e

    total_deficit = 0.0
    for d in balance["deficit"]:
        total_deficit = total_deficit + d

    # Porcentaje de la demanda total cubierto directamente por energía solar
    if total_consumo > 0.0:
        porcentaje_cubierto = (total_autoconsumo / total_consumo) * 100.0
    else:
        porcentaje_cubierto = 0.0

    # Ahorro del día: cada kWh autoconsumido es un kWh no comprado a la red
    ahorro_dia = total_autoconsumo * tarifa

    # Costos para contexto económico
    costo_sin_solar = total_consumo * tarifa
    costo_con_solar = total_deficit * tarifa

    indicadores = {
        "total_generacion": round(total_generacion, 2),
        "total_consumo": round(total_consumo, 2),
        "total_autoconsumo": round(total_autoconsumo, 2),
        "total_excedente": round(total_excedente, 2),
        "total_deficit": round(total_deficit, 2),
        "porcentaje_cubierto": round(porcentaje_cubierto, 2),
        "ahorro_dia": round(ahorro_dia, 2),
        "costo_sin_solar": round(costo_sin_solar, 2),
        "costo_con_solar": round(costo_con_solar, 2)
    }
    return indicadores


def ejecutar_simulacion_completa(perfil, consumo, paneles, kw_panel, perdidas, tarifa, factor_clima=1.0, estados=None):
    """
    Función orquestadora que integra todo el flujo de simulación.
    Retorna un diccionario completo con entradas, perfiles horarios e indicadores,
    incluyendo la generación óptima teórica y pérdidas por estado de los paneles.
    """
    generacion_real, generacion_optima = calcular_generacion_hora(
        perfil, paneles, kw_panel, perdidas, factor_clima, estados
    )
    balance = comparar_generacion_consumo(generacion_real, consumo)
    indicadores = calcular_indicadores(generacion_real, consumo, balance, tarifa)

    # Cálculo de energía teórica y mermas por fallas o suciedad
    total_gen_optima = 0.0
    for g in generacion_optima:
        total_gen_optima = total_gen_optima + g

    energia_perdida = round(max(0.0, total_gen_optima - indicadores["total_generacion"]), 2)
    dinero_perdido = round(energia_perdida * tarifa, 2)

    pot_optima = round((paneles * kw_panel) * (1.0 - perdidas), 3)
    pot_efectiva = round(calcular_potencia_efectiva(paneles, kw_panel, perdidas, estados), 3)
    eficiencia_tejado = round((pot_efectiva / pot_optima * 100.0), 1) if pot_optima > 0 else 100.0

    # Perfil solar efectivo considerando factor climático
    perfil_efectivo = []
    for p in perfil:
        perfil_efectivo.append(round(p * factor_clima, 4))

    resultado_completo = {
        "parametros": {
            "paneles": paneles,
            "kw_panel": kw_panel,
            "perdidas": perdidas,
            "tarifa": tarifa,
            "factor_clima": factor_clima,
            "estados": estados if estados is not None else {"operativo": paneles, "sucio": 0, "falla": 0, "mantenimiento": 0},
            "potencia_pico": round(paneles * kw_panel, 2),
            "potencia_efectiva": pot_efectiva,
            "potencia_optima": pot_optima,
            "eficiencia_tejado": eficiencia_tejado,
            "energia_perdida_fallas": energia_perdida,
            "dinero_perdido_fallas": dinero_perdido
        },
        "perfiles": {
            "perfil_solar": perfil_efectivo,
            "generacion": generacion_real,
            "generacion_optima": generacion_optima,
            "consumo": consumo,
            "autoconsumo": balance["autoconsumo"],
            "excedente": balance["excedente"],
            "deficit": balance["deficit"]
        },
        "indicadores": indicadores
    }
    return resultado_completo


def comparar_dos_escenarios(escenario_a, escenario_b):
    """
    Reto: Compara dos escenarios técnicos y económicos (ej. 4 vs 8 paneles).
    Determina cuál ahorra más y genera una explicación analítica de ingeniería energética.
    Parámetros:
        escenario_a (dict): Diccionario del primer escenario.
        escenario_b (dict): Diccionario del segundo escenario.
    Retorna:
        dict: Métricas comparativas y explicación técnica del por qué.
    """
    nombre_a = escenario_a.get("nombre", "Escenario A")
    nombre_b = escenario_b.get("nombre", "Escenario B")

    ind_a = escenario_a["indicadores"]
    ind_b = escenario_b["indicadores"]

    ahorro_a = ind_a["ahorro_dia"]
    ahorro_b = ind_b["ahorro_dia"]
    diff_ahorro = round(ahorro_b - ahorro_a, 2)

    auto_a = ind_a["total_autoconsumo"]
    auto_b = ind_b["total_autoconsumo"]
    diff_auto = round(auto_b - auto_a, 2)

    exc_a = ind_a["total_excedente"]
    exc_b = ind_b["total_excedente"]
    diff_exc = round(exc_b - exc_a, 2)

    paneles_a = escenario_a["parametros"]["paneles"]
    paneles_b = escenario_b["parametros"]["paneles"]

    # Determinar ganador y redacción pedagógica
    if ahorro_b > ahorro_a:
        ganador = nombre_b
        pct_mejora = round(((ahorro_b - ahorro_a) / ahorro_a) * 100.0, 1) if ahorro_a > 0 else 100.0
        explicacion = (
            f"El {nombre_b} ahorra ${diff_ahorro:,.0f} más al día (+{pct_mejora}%) que el {nombre_a}. "
            f"Al contar con más paneles ({paneles_b} vs {paneles_a}), genera mayor energía instantánea. "
        )
        if diff_exc > diff_auto:
            explicacion += (
                f"Sin embargo, nota que el autoconsumo solo subió {diff_auto} kWh mientras que el excedente "
                f"creció {diff_exc} kWh. Esto ocurre por la curva de saturación solar: en las horas de mayor "
                f"irradiancia la potencia supera el consumo del hogar, por lo que la energía extra se vierte "
                f"a la red y no incrementa el ahorro directo a menos que se instalen baterías o exista balance neto."
            )
        else:
            explicacion += (
                f"La energía adicional fue aprovechada eficientemente por los consumos diurnos del hogar, "
                f"aumentando la cobertura solar al {ind_b['porcentaje_cubierto']}% de la demanda."
            )
    elif ahorro_a > ahorro_b:
        ganador = nombre_a
        pct_mejora = round(((ahorro_a - ahorro_b) / ahorro_b) * 100.0, 1) if ahorro_b > 0 else 100.0
        explicacion = (
            f"El {nombre_a} genera mayor ahorro (${abs(diff_ahorro):,.0f} adicionales, +{pct_mejora}%) "
            f"en comparación con el {nombre_b}."
        )
    else:
        ganador = "Empate en Ahorro"
        explicacion = (
            f"Ambos escenarios generan el mismo ahorro económico (${ahorro_a:,.0f}/día). "
            f"Esto indica que el consumo del hogar ya estaba cubierto al 100% en las horas de sol y "
            f"cualquier panel adicional solo produce excedentes sin incrementar el autoconsumo."
        )

    comparacion = {
        "ganador": ganador,
        "nombre_a": nombre_a,
        "nombre_b": nombre_b,
        "ahorro_a": ahorro_a,
        "ahorro_b": ahorro_b,
        "diferencia_ahorro": diff_ahorro,
        "autoconsumo_a": auto_a,
        "autoconsumo_b": auto_b,
        "diferencia_autoconsumo": diff_auto,
        "excedente_a": exc_a,
        "excedente_b": exc_b,
        "diferencia_excedente": diff_exc,
        "cobertura_a": ind_a["porcentaje_cubierto"],
        "cobertura_b": ind_b["porcentaje_cubierto"],
        "explicacion": explicacion
    }
    return comparacion


def generar_historial_semanal_inicial(perfil, consumo, paneles, kw_panel, perdidas, tarifa):
    """
    Genera un historial simulado de 1 semana (7 días consecutivos) con
    variaciones meteorológicas realistas (días despejados, parciales y nublados).
    Utiliza únicamente listas, ciclos for, diccionarios y condicionales.
    """
    dias_nombres = ["Lunes", "Martes", "Miércoles", "Jueves", "Viernes", "Sábado", "Domingo"]
    factores_clima = [1.0, 0.85, 1.0, 0.50, 0.75, 1.0, 0.65]
    etiquetas_clima = [
        "☀️ Despejado",
        "⛅ Parcial",
        "☀️ Radiante",
        "🌧️ Nublado",
        "⛅ Parcial",
        "☀️ Despejado",
        "⛅ Variable"
    ]

    historial = []

    for i in range(len(dias_nombres)):
        dia_nom = dias_nombres[i]
        factor = factores_clima[i]
        clima_str = etiquetas_clima[i]

        sim_dia = ejecutar_simulacion_completa(
            perfil=perfil,
            consumo=consumo,
            paneles=paneles,
            kw_panel=kw_panel,
            perdidas=perdidas,
            tarifa=tarifa,
            factor_clima=factor
        )

        ind = sim_dia["indicadores"]

        registro_dia = {
            "id": i + 1,
            "dia": dia_nom,
            "clima": clima_str,
            "factor_clima": factor,
            "autoconsumo": ind["total_autoconsumo"],
            "excedente": ind["total_excedente"],
            "cobertura": ind["porcentaje_cubierto"],
            "ahorro": ind["ahorro_dia"],
            "costo_red": ind["costo_con_solar"],
            "simulacion": sim_dia
        }
        historial.append(registro_dia)

    return historial


def agregar_dia_al_historial(historial, nuevo_registro, limite_dias=7):
    """
    Agrega un nuevo registro diario al historial de días.
    Mantiene una ventana móvil de máximo 7 días (1 semana).
    """
    if len(historial) >= limite_dias:
        # Eliminamos el día más antiguo con pop(0)
        historial.pop(0)

    # Reindexamos los días restantes
    historial.append(nuevo_registro)
    for idx in range(len(historial)):
        historial[idx]["id"] = idx + 1

    return historial


def calcular_resumen_semanal(historial):
    """
    Calcula los totales y promedios de la semana a partir de la lista de días.
    Utiliza acumuladores locales y ciclos for.
    """
    total_ahorro = 0.0
    total_autoconsumo = 0.0
    total_excedente = 0.0
    cantidad_dias = len(historial)

    for dia in historial:
        total_ahorro = total_ahorro + dia["ahorro"]
        total_autoconsumo = total_autoconsumo + dia["autoconsumo"]
        total_excedente = total_excedente + dia["excedente"]

    if cantidad_dias > 0:
        promedio_ahorro = total_ahorro / cantidad_dias
        promedio_autoconsumo = total_autoconsumo / cantidad_dias
    else:
        promedio_ahorro = 0.0
        promedio_autoconsumo = 0.0

    resumen = {
        "cantidad_dias": cantidad_dias,
        "total_ahorro_semana": round(total_ahorro, 2),
        "total_autoconsumo_semana": round(total_autoconsumo, 2),
        "total_excedente_semana": round(total_excedente, 2),
        "promedio_ahorro_dia": round(promedio_ahorro, 2),
        "promedio_autoconsumo_dia": round(promedio_autoconsumo, 2)
    }
    return resumen


# =============================================================================
# MÓDULO DE CALENDARIO, BASE DE DATOS E HISTORIAL ANUAL (ALTERNATIVA A)
# =============================================================================

MESES_NOMBRES = [
    "Enero", "Febrero", "Marzo", "Abril", "Mayo", "Junio",
    "Julio", "Agosto", "Septiembre", "Octubre", "Noviembre", "Diciembre"
]

DIAS_SEMANA_CORTOS = ["Lun", "Mar", "Mié", "Jue", "Vie", "Sáb", "Dom"]
DIAS_SEMANA_LARGOS = ["Lunes", "Martes", "Miércoles", "Jueves", "Viernes", "Sábado", "Domingo"]


def es_anio_bisiesto(anio):
    """
    Determina si un año es bisiesto aplicando la regla del calendario gregoriano:
    Un año es bisiesto si es divisible por 4, excepto el fin de siglo,
    a menos que sea divisible por 400.
    Parámetro:
        anio (int): Año a evaluar (ej: 2024, 2026).
    Retorna:
        bool: True si es bisiesto, False en caso contrario.
    """
    if (anio % 4 == 0 and anio % 100 != 0) or (anio % 400 == 0):
        return True
    return False


def obtener_dias_del_mes(anio, mes):
    """
    Retorna la cantidad exacta de días para un mes determinado (1 a 12),
    considerando 29 días en febrero para años bisiestos.
    Parámetros:
        anio (int): Año (ej: 2026).
        mes (int): Mes del 1 al 12.
    Retorna:
        int: Días del mes (28, 29, 30 o 31).
    """
    dias_por_mes = [31, 28, 31, 30, 31, 30, 31, 31, 30, 31, 30, 31]
    if mes == 2 and es_anio_bisiesto(anio):
        return 29
    return dias_por_mes[mes - 1]


def obtener_dia_semana_indice(anio, mes, dia):
    """
    Retorna el índice del día de la semana para una fecha dada.
    Convención ISO estándar:
        0: Lunes, 1: Martes, 2: Miércoles, 3: Jueves,
        4: Viernes, 5: Sábado, 6: Domingo.
    """
    return date(anio, mes, dia).weekday()


def obtener_dia_semana_nombre(anio, mes, dia):
    """
    Retorna el nombre formal en español del día de la semana.
    Ejemplo: 'Lunes', 'Martes', ..., 'Domingo'.
    """
    idx = obtener_dia_semana_indice(anio, mes, dia)
    return DIAS_SEMANA_LARGOS[idx]


def generar_grilla_calendario_mes(anio, mes):
    """
    Genera una matriz (lista de semanas) para estructurar el calendario mensual.
    Cada semana es una lista de 7 elementos correspondiente a Lunes..Domingo.
    Los espacios sin día (relleno al inicio y al final) se representan con None.
    """
    total_dias = obtener_dias_del_mes(anio, mes)
    primer_dia_sem = obtener_dia_semana_indice(anio, mes, 1)

    grilla = []
    semana_actual = [None] * primer_dia_sem

    for d in range(1, total_dias + 1):
        semana_actual.append(d)
        if len(semana_actual) == 7:
            grilla.append(semana_actual)
            semana_actual = []

    if len(semana_actual) > 0:
        while len(semana_actual) < 7:
            semana_actual.append(None)
        grilla.append(semana_actual)

    return grilla


def cargar_base_datos_historial(ruta_archivo):
    """
    Carga la base de datos completa del historial energético desde un archivo JSON.
    Estructura jerárquica: base_datos[vivienda][fecha_str] -> dict_registro
    Si el archivo no existe o está corrupto, retorna un diccionario vacío {}.
    """
    if not os.path.exists(ruta_archivo):
        return {}
    try:
        with open(ruta_archivo, "r", encoding="utf-8") as f:
            datos = json.load(f)
            return datos if isinstance(datos, dict) else {}
    except Exception:
        return {}


def guardar_base_datos_historial(base_datos, ruta_archivo):
    """
    Guarda la base de datos completa en formato JSON legible.
    """
    directorio = os.path.dirname(ruta_archivo)
    if directorio and not os.path.exists(directorio):
        os.makedirs(directorio, exist_ok=True)
    with open(ruta_archivo, "w", encoding="utf-8") as f:
        json.dump(base_datos, f, indent=4, ensure_ascii=False)
    return True


def obtener_viviendas_registradas(base_datos):
    """
    Retorna la lista ordenada de todas las viviendas registradas en la base de datos.
    """
    viviendas = list(base_datos.keys())
    viviendas.sort()
    return viviendas


def obtener_fechas_vivienda(base_datos, vivienda):
    """
    Retorna la lista ordenada cronológicamente de fechas (YYYY-MM-DD) para una vivienda.
    """
    if vivienda not in base_datos:
        return []
    fechas = list(base_datos[vivienda].keys())
    fechas.sort()
    return fechas


def existe_registro_dia(base_datos, vivienda, fecha):
    """
    Verifica en tiempo constante O(1) si ya existe un registro para una vivienda y fecha.
    """
    if vivienda in base_datos and fecha in base_datos[vivienda]:
        return True
    return False


def obtener_registro_dia(base_datos, vivienda, fecha):
    """
    Obtiene el diccionario con los datos energéticos de un día específico, o None si no existe.
    """
    if existe_registro_dia(base_datos, vivienda, fecha):
        return base_datos[vivienda][fecha]
    return None


def crear_registro_dia(fecha, vivienda, simulacion, nota=""):
    """
    Construye el registro estandarizado de un día a partir de una simulación energética.
    Empaqueta los 14 parámetros clave requeridos por el proyecto.
    """
    partes = fecha.split("-")
    anio = int(partes[0])
    mes = int(partes[1])
    dia = int(partes[2])

    dia_semana = obtener_dia_semana_nombre(anio, mes, dia)
    params = simulacion["parametros"]
    ind = simulacion["indicadores"]
    perfiles = simulacion["perfiles"]
    estados = params.get("estados", {"operativo": params["paneles"], "sucio": 0, "falla": 0, "mantenimiento": 0})
    salud = params.get("eficiencia_tejado", 100.0)

    # Identificación del indicador visual:
    # 🟢 'optimo': 100% operativo sin afecciones
    # 🟡 'afectado': paneles sucios, con fallas, en mantenimiento o salud reducida
    es_afectado = (estados.get("sucio", 0) > 0 or 
                   estados.get("falla", 0) > 0 or 
                   estados.get("mantenimiento", 0) > 0 or 
                   salud < 99.0)
    estado_general = "afectado" if es_afectado else "optimo"

    registro = {
        "fecha": fecha,
        "anio": anio,
        "mes": mes,
        "dia": dia,
        "dia_semana": dia_semana,
        "vivienda": vivienda,
        "paneles": params["paneles"],
        "kw_panel": params["kw_panel"],
        "potencia_total_kwp": params.get("potencia_pico", round(params["paneles"] * params["kw_panel"], 2)),
        "perdidas_porcentaje": int(params["perdidas"] * 100) if params["perdidas"] <= 1.0 else int(params["perdidas"]),
        "tarifa_cop": params["tarifa"],
        "factor_clima": params.get("factor_clima", 1.0),
        "es_dia_nublado": (params.get("factor_clima", 1.0) < 0.9),
        "generacion_total_kwh": ind["total_generacion"],
        "consumo_total_kwh": ind["total_consumo"],
        "autoconsumo_kwh": ind["total_autoconsumo"],
        "excedente_kwh": ind["total_excedente"],
        "deficit_kwh": ind["total_deficit"],
        "demanda_cubierta_pct": ind["porcentaje_cubierto"],
        "ahorro_cop": ind["ahorro_dia"],
        "costo_sin_solar_cop": ind["costo_sin_solar"],
        "costo_con_solar_cop": ind["costo_con_solar"],
        "estados_paneles": estados,
        "salud_porcentaje": salud,
        "estado_general": estado_general,
        "nota": nota,
        "perfiles": perfiles
    }
    return registro


def guardar_registro_dia(base_datos, registro):
    """
    Inserta o actualiza un registro de día en la base de datos.
    Retorna una tupla: (base_datos, es_actualizacion).
    """
    vivienda = registro["vivienda"]
    fecha = registro["fecha"]

    if vivienda not in base_datos:
        base_datos[vivienda] = {}

    es_actualizacion = (fecha in base_datos[vivienda])
    base_datos[vivienda][fecha] = registro

    return base_datos, es_actualizacion


def eliminar_registro_dia(base_datos, vivienda, fecha):
    """
    Elimina un registro de día de la base de datos.
    Retorna True si fue eliminado, False si no existía.
    """
    if existe_registro_dia(base_datos, vivienda, fecha):
        del base_datos[vivienda][fecha]
        return True
    return False


def vaciar_historial_vivienda(base_datos, vivienda):
    """
    Elimina todos los registros de una vivienda en la base de datos.
    Retorna la base de datos actualizada.
    """
    if vivienda in base_datos:
        base_datos[vivienda] = {}
    return base_datos


def obtener_ultimos_dias_registrados(base_datos, vivienda, limite=7):
    """
    Retorna la lista de los últimos registros diarios reales (hasta un máximo de `limite`)
    para la vivienda seleccionada, ordenados cronológicamente.
    Cada elemento adapta los datos reales para alimentar la pestaña semanal y mantener
    una única fuente de verdad con el calendario.
    """
    if vivienda not in base_datos:
        return []

    fechas = list(base_datos[vivienda].keys())
    fechas.sort()

    ultimas_fechas = fechas[-limite:] if len(fechas) > limite else fechas

    lista_dias = []
    for idx, f in enumerate(ultimas_fechas):
        reg = base_datos[vivienda][f]
        es_nub = reg.get("es_dia_nublado", False)
        clima_str = "🌧️ Nublado" if es_nub else "☀️ Despejado"
        if reg.get("estado_general") == "afectado":
            clima_str = clima_str + " (Merma)"

        item = {
            "id": idx + 1,
            "fecha": f,
            "dia": reg.get("dia_semana", "Día"),
            "clima": clima_str,
            "factor_clima": reg.get("factor_clima", 1.0),
            "autoconsumo": reg.get("autoconsumo_kwh", 0.0),
            "excedente": reg.get("excedente_kwh", 0.0),
            "cobertura": reg.get("demanda_cubierta_pct", 0.0),
            "ahorro": reg.get("ahorro_cop", 0.0),
            "costo_red": reg.get("costo_con_solar_cop", 0.0),
            "simulacion": {
                "perfiles": reg.get("perfiles", {}),
                "parametros": {
                    "paneles": reg.get("paneles", 4),
                    "kw_panel": reg.get("kw_panel", 0.5),
                    "perdidas": reg.get("perdidas_porcentaje", 20) / 100.0,
                    "tarifa": reg.get("tarifa_cop", 800.0),
                    "estados": reg.get("estados_paneles", {}),
                    "es_dia_nublado": es_nub
                },
                "indicadores": {
                    "total_generacion": reg.get("generacion_total_kwh", 0.0),
                    "total_consumo": reg.get("consumo_total_kwh", 0.0),
                    "total_autoconsumo": reg.get("autoconsumo_kwh", 0.0),
                    "total_excedente": reg.get("excedente_kwh", 0.0),
                    "total_deficit": reg.get("deficit_kwh", 0.0),
                    "porcentaje_cubierto": reg.get("demanda_cubierta_pct", 0.0),
                    "ahorro_dia": reg.get("ahorro_cop", 0.0),
                    "costo_sin_solar": reg.get("costo_sin_solar_cop", 0.0),
                    "costo_con_solar": reg.get("costo_con_solar_cop", 0.0)
                }
            },
            "registro_completo": reg
        }
        lista_dias.append(item)

    return lista_dias


def obtener_resumen_mensual_historial(base_datos, vivienda, anio, mes):
    """
    Calcula totales, promedios y estado de paneles para un mes y año seleccionados.
    Utiliza acumuladores locales y ciclos for nativos.
    """
    prefijo_mes = f"{anio:04d}-{mes:02d}-"
    dias_registrados = 0
    dias_optimos = 0
    dias_afectados = 0

    tot_gen = 0.0
    tot_con = 0.0
    tot_auto = 0.0
    tot_exc = 0.0
    tot_def = 0.0
    tot_ahorro = 0.0
    suma_cobertura = 0.0

    registros_mes = []

    if vivienda in base_datos:
        for fecha, reg in base_datos[vivienda].items():
            if fecha.startswith(prefijo_mes):
                dias_registrados = dias_registrados + 1
                registros_mes.append(reg)

                if reg.get("estado_general") == "optimo":
                    dias_optimos = dias_optimos + 1
                else:
                    dias_afectados = dias_afectados + 1

                tot_gen = tot_gen + reg.get("generacion_total_kwh", 0.0)
                tot_con = tot_con + reg.get("consumo_total_kwh", 0.0)
                tot_auto = tot_auto + reg.get("autoconsumo_kwh", 0.0)
                tot_exc = tot_exc + reg.get("excedente_kwh", 0.0)
                tot_def = tot_def + reg.get("deficit_kwh", 0.0)
                tot_ahorro = tot_ahorro + reg.get("ahorro_cop", 0.0)
                suma_cobertura = suma_cobertura + reg.get("demanda_cubierta_pct", 0.0)

    prom_cob = round(suma_cobertura / dias_registrados, 2) if dias_registrados > 0 else 0.0
    prom_ahorro = round(tot_ahorro / dias_registrados, 2) if dias_registrados > 0 else 0.0
    prom_auto = round(tot_auto / dias_registrados, 2) if dias_registrados > 0 else 0.0

    return {
        "anio": anio,
        "mes": mes,
        "nombre_mes": MESES_NOMBRES[mes - 1],
        "dias_registrados": dias_registrados,
        "dias_optimos": dias_optimos,
        "dias_afectados": dias_afectados,
        "total_generacion_kwh": round(tot_gen, 2),
        "total_consumo_kwh": round(tot_con, 2),
        "total_autoconsumo_kwh": round(tot_auto, 2),
        "total_excedente_kwh": round(tot_exc, 2),
        "total_deficit_kwh": round(tot_def, 2),
        "total_ahorro_cop": round(tot_ahorro, 2),
        "promedio_cobertura_pct": prom_cob,
        "promedio_ahorro_dia_cop": prom_ahorro,
        "promedio_autoconsumo_dia_kwh": prom_auto,
        "registros": registros_mes
    }


def obtener_resumen_anual_historial(base_datos, vivienda, anio):
    """
    Calcula el balance y métricas anuales acumuladas a lo largo de los 12 meses.
    Identifica el mejor mes de ahorro y el de menor generación.
    """
    resumen_meses = []
    tot_dias = 0
    tot_gen = 0.0
    tot_auto = 0.0
    tot_exc = 0.0
    tot_ahorro = 0.0

    mejor_mes_ahorro = {"mes": "Sin datos", "ahorro": 0.0}
    menor_mes_gen = {"mes": "Sin datos", "generacion": 999999999.0}

    for m in range(1, 13):
        res_m = obtener_resumen_mensual_historial(base_datos, vivienda, anio, m)
        resumen_meses.append(res_m)

        tot_dias = tot_dias + res_m["dias_registrados"]
        tot_gen = tot_gen + res_m["total_generacion_kwh"]
        tot_auto = tot_auto + res_m["total_autoconsumo_kwh"]
        tot_exc = tot_exc + res_m["total_excedente_kwh"]
        tot_ahorro = tot_ahorro + res_m["total_ahorro_cop"]

        if res_m["dias_registrados"] > 0:
            if res_m["total_ahorro_cop"] > mejor_mes_ahorro["ahorro"]:
                mejor_mes_ahorro = {"mes": res_m["nombre_mes"], "ahorro": res_m["total_ahorro_cop"]}
            if res_m["total_generacion_kwh"] < menor_mes_gen["generacion"]:
                menor_mes_gen = {"mes": res_m["nombre_mes"], "generacion": res_m["total_generacion_kwh"]}

    if menor_mes_gen["generacion"] == 999999999.0:
        menor_mes_gen = {"mes": "Sin datos", "generacion": 0.0}

    return {
        "anio": anio,
        "total_dias_registrados": tot_dias,
        "total_generacion_kwh": round(tot_gen, 2),
        "total_autoconsumo_kwh": round(tot_auto, 2),
        "total_excedente_kwh": round(tot_exc, 2),
        "total_ahorro_cop": round(tot_ahorro, 2),
        "mejor_mes_ahorro": mejor_mes_ahorro,
        "menor_mes_generacion": menor_mes_gen,
        "meses": resumen_meses
    }


def obtener_estadisticas_dias_semana(base_datos, vivienda):
    """
    Agrupa todos los registros por día de la semana (Lunes a Domingo)
    y evalúa el patrón de hábitos de consumo entre días laborales y fin de semana.
    """
    dias_stats = {}
    for d in DIAS_SEMANA_LARGOS:
        dias_stats[d] = {
            "nombre": d,
            "cantidad": 0,
            "total_consumo": 0.0,
            "total_generacion": 0.0,
            "total_autoconsumo": 0.0,
            "total_ahorro": 0.0
        }

    if vivienda in base_datos:
        for fecha, reg in base_datos[vivienda].items():
            dia_sem = reg.get("dia_semana")
            if dia_sem in dias_stats:
                dias_stats[dia_sem]["cantidad"] = dias_stats[dia_sem]["cantidad"] + 1
                dias_stats[dia_sem]["total_consumo"] = dias_stats[dia_sem]["total_consumo"] + reg.get("consumo_total_kwh", 0.0)
                dias_stats[dia_sem]["total_generacion"] = dias_stats[dia_sem]["total_generacion"] + reg.get("generacion_total_kwh", 0.0)
                dias_stats[dia_sem]["total_autoconsumo"] = dias_stats[dia_sem]["total_autoconsumo"] + reg.get("autoconsumo_kwh", 0.0)
                dias_stats[dia_sem]["total_ahorro"] = dias_stats[dia_sem]["total_ahorro"] + reg.get("ahorro_cop", 0.0)

    lista_dias = []
    tot_laborable_con = 0.0
    cant_laborable = 0
    tot_finde_con = 0.0
    cant_finde = 0

    for d in DIAS_SEMANA_LARGOS:
        item = dias_stats[d]
        c = item["cantidad"]
        prom_con = round(item["total_consumo"] / c, 2) if c > 0 else 0.0
        prom_gen = round(item["total_generacion"] / c, 2) if c > 0 else 0.0
        prom_auto = round(item["total_autoconsumo"] / c, 2) if c > 0 else 0.0
        prom_ahorro = round(item["total_ahorro"] / c, 2) if c > 0 else 0.0

        elem = {
            "dia": d,
            "cantidad": c,
            "promedio_consumo_kwh": prom_con,
            "promedio_generacion_kwh": prom_gen,
            "promedio_autoconsumo_kwh": prom_auto,
            "promedio_ahorro_cop": prom_ahorro
        }
        lista_dias.append(elem)

        if d in ["Lunes", "Martes", "Miércoles", "Jueves", "Viernes"]:
            tot_laborable_con = tot_laborable_con + item["total_consumo"]
            cant_laborable = cant_laborable + c
        else:
            tot_finde_con = tot_finde_con + item["total_consumo"]
            cant_finde = cant_finde + c

    prom_lab = round(tot_laborable_con / cant_laborable, 2) if cant_laborable > 0 else 0.0
    prom_finde = round(tot_finde_con / cant_finde, 2) if cant_finde > 0 else 0.0

    if prom_finde > prom_lab and prom_lab > 0:
        diff_pct = round(((prom_finde - prom_lab) / prom_lab) * 100.0, 1)
        patron_texto = f"El consumo en fin de semana ({prom_finde} kWh/día) es un {diff_pct}% superior a los días laborables ({prom_lab} kWh/día), indicando mayor ocupación en el hogar durante el sábado y domingo."
    elif prom_lab > prom_finde and prom_finde > 0:
        diff_pct = round(((prom_lab - prom_finde) / prom_finde) * 100.0, 1)
        patron_texto = f"El consumo en días laborables ({prom_lab} kWh/día) supera en {diff_pct}% al fin de semana ({prom_finde} kWh/día)."
    else:
        patron_texto = "El consumo promedio se mantiene equilibrado entre días laborables y fines de semana."

    return {
        "dias": lista_dias,
        "promedio_laborable_kwh": prom_lab,
        "promedio_fin_de_semana_kwh": prom_finde,
        "total_registros": cant_laborable + cant_finde,
        "diagnostico_patron": patron_texto
    }


def comparar_anios_historial(base_datos, vivienda, anio_1, anio_2):
    """
    Compara el desempeño anual de dos años para la misma vivienda.
    """
    res_1 = obtener_resumen_anual_historial(base_datos, vivienda, anio_1)
    res_2 = obtener_resumen_anual_historial(base_datos, vivienda, anio_2)

    diff_gen = round(res_2["total_generacion_kwh"] - res_1["total_generacion_kwh"], 2)
    diff_ahorro = round(res_2["total_ahorro_cop"] - res_1["total_ahorro_cop"], 2)

    return {
        "anio_1": anio_1,
        "anio_2": anio_2,
        "resumen_anio_1": res_1,
        "resumen_anio_2": res_2,
        "diferencia_generacion_kwh": diff_gen,
        "diferencia_ahorro_cop": diff_ahorro
    }


