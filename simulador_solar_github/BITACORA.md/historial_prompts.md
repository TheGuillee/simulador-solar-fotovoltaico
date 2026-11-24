# Bitácora de Prompts - Simulador Solar Fotovoltaico Residencial

Este directorio (`BITACORA.md`) almacena el registro cronológico de todos los prompts e instrucciones proporcionadas por el usuario para el desarrollo del proyecto de Fundamentos de Programación para Ingeniería Energética.

---

## Prompt 1
- **Fecha y Hora:** 2026-11-21 02:15:26
- **Rol:** Estudiante de Ingeniería Energética (Fundamentos de Programación)
- **Contenido del Prompt:**

```text
Voy a construir el proyecto "Simulador solar fotovoltaico residencial" para una clase de Fundamentos de Programación de Ingeniería Energética.(Quiero que sea una aplicacion visual, que se vea profesional y que cambie al instante cuando el usuario mueva los controles.) 

Crea una carpeta llamada BITACORA.md donde se guardara todos los promts que te de.

QUÉ DEBE HACER LA APLICACIÓN (OBLIGATORIO)
1. Elegir el número de paneles, la potencia de cada panel (kW) y las pérdidas del sistema.
2. Calcular la generación por hora a partir de un perfi l solar de 24 valores (de 0 a 1).
3. Comparar generación y consumo: energía autoconsumida y excedente. 
4. Calcular el ahorro del día con la tarifa y guardar los escenarios probados en JSON.

Te voy a agregar unos datos de entrada, la app debe cargar este archivo (datos/entrada.json)
al iniciar y debe poder cargar otro con la mismaestructura.

{ "vivienda": "Casa 12", 
"tarifa": 800, 
"perfil": [0, 0, 0, "... 24 valores entre 0 y 1"],
 "consumo": [0.4, 0.3, "... 24 valores (kWh por hora)"], 
"sistema": {"paneles": 4, "kw_panel": 0.5, "perdidas": 0.2}
}

Que debe poder verse en el diseño general
1. Gráfica de 24 h con excedente y déficit
   Eje horizontal con las24 horas; curva solar (amarillo) y curva de consumo (azul). Área verde donde sobra generación (excedente) y área roja donde falta (compra a la red). Leyenda y valor exacto al pasar el cursor.
2. Deslizadores que actualizan al instante
   Deslizadores para número de paneles, potencia por panel y pérdidas del sistema. Al moverlos, la gráfi ca y las tarjetas se actualizan al instante, sin botón de calcular. Botón «guardar escenario» y una lista lateral para compararlos.
3. Tarjetas de resultados
   Tarjetas con ícono: autoconsumo (kWh), excedente (kWh), % de la demanda cubierto por el sol yahorro del día ($). Colores con signifi cado (verde = bueno, rojo = alerta). Los valores cambian junto con los deslizadores.
4. Diseño general
   Jerarquía clara: se entiende qué es lo más importante con solo mirar la pantalla. Colores con signifi cado
   (no decorativos) y tema claro/oscuro. Textos y números legibles en proyector. Los controles responden al instante
   y no hay errores visuales ni textos cortados.
5. y como ultimo reto Comparar dos escenarios (por ejemplo 4 vs 8 paneles) y decir cuál ahorra más y por que

Construye la aplicación completa en Python con Streamlit: la lógica en un archivo aparte y la interfaz en app.py.Usa en la lógica solo lo visto en clase (funciones con return, listas, diccionarios, ciclos, condicionales, variables locales y JSON), para que yo pueda explicarla.Es un proyecto de DISEÑO: prioriza que se vea profesional, con jerarquía clara, colores con significado, tema claro/oscuro, textos legibles en proyector y controles que cambian todo al instante.Comprueba que el caso de verificación da exactamente esos resultados. Explícame cómo ejecutarla y no agregues librerías sin decírmelo.

luego de haberlo hecho te voy a dar un caso de verificacion y te debe mostrar exactamente los datos que te voy a dar 

Caso de verificación (la aplicación debe mostrar exactamente esto)
4 paneles de 0.5 kW, pérdidas 20 %, tarifa $800/kWh. Se prueba con solo 4 horas: perfi l solar [0, 0.5, 1,0.5]
y consumo de 1 kWh por hora.

lo que se mirara es lo siguiente, generacion por hora debe dar (0 · 0.8 · 1.6 · 0.8 kWh). 
el autoconsumo 2.6 kWh (65 % de la demanda)
Excedente 0.6 kWh
Ahorro del día $2 080
Día nublado (perfi l ×0.5) perfi l 0 · 0.25 · 0.5 · 0.25; autoconsumo 1.6 kWh y excedente 0
Escenarios guardados al guardar «4 paneles», aparece en la lista
```


---

## Prompt 2
- **Fecha y Hora:** 2026-11-21 02:39:43
- **Rol:** Estudiante de Ingeniería Energética (Fundamentos de Programación)
- **Contenido del Prompt:**

```text
Revisando un poco a fondo, principalmente en el renombre de "SIMULADOR SOLAR FOTOVOLTAICO RESIDENCIAL" esta recortado, no se ve correctamente. Y puedes mejorar los colores para que no sea tan simple, dame ideas de colores, y cualquier cambio que vayas a hacer me lo consultas, me lo explicas y yo te digo si si o si no.

la grafica me gustaaria que en la parte de las horas se vea mas bonito, separados de una mejor manera y al lado derecho muestre una opcion que diga "Historial de dias" donde guarde un historial aprox de 1 semana.
```


---

## Prompt 3
- **Fecha y Hora:** 2026-11-21 02:42:06
- **Rol:** Estudiante de Ingeniería Energética (Fundamentos de Programación)
- **Contenido del Prompt:**

```text
En el 1 me gusta selecciona la opcion 2
en la propuesta de colores pon la opcion A
```
- **Decisiones Aprobadas por el Usuario:**
  1. Título: Banner institucional estilizado con tipografía escalable (`clamp`) y margen superior protegido para eliminar cualquier recorte visual.
  2. Paleta de Colores: Opción A («Solar Clean Tech») con estética moderna de ingeniería energética (azul marino petróleo, acentos dorado solar y azul eléctrico, áreas con gradientes suaves y tarjetas glassmorphism).
  3. Gráfica: Horas con formato estilizado y mejor separación.
  4. Historial de Días: Panel lateral derecho con historial de 7 días (1 semana) y persistencia.


---

## Prompt 4
- **Fecha y Hora:** 2026-11-21 02:43:20
- **Rol:** Estudiante de Ingeniería Energética (Fundamentos de Programación)
- **Contenido del Prompt:**

```text
En la mejora de las horas visuales si me gusta la opcion que me das 
el la opcion 4  tambien me gusta la idea
```
- **Confirmación del Usuario:**
  - Aprobación explícita de la mejora visual en el eje de horas de la gráfica (formato limpio y espaciado de marcas temporales).
  - Aprobación explícita de la Opción 4: Panel lateral derecho con el «Historial de Días (Semanal)» de 1 semana con persistencia, análisis de variabilidad meteorológica y botones de carga instantánea.


---

## Prompt 5
- **Fecha y Hora:** 2026-11-21 03:00:41
- **Rol:** Estudiante de Ingeniería Energética (Fundamentos de Programación)
- **Contenido del Prompt:**

```text
Elimina esa opcion de "Cargar un Json" un usuario normal no haria eso.

# REDISEÑO VISUAL DEL SIMULADOR SOLAR FOTOVOLTAICO

Quiero que realices un rediseño completo de la interfaz gráfica de mi proyecto Simulador solar fotovoltaico residencial.

Te adjunto una imagen que debes utilizar como REFERENCIA VISUAL PRINCIPAL. Quiero que mi aplicación tenga una apariencia muy similar a la de esa imagen. No quiero que inventes un diseño diferente ni que simplemente cambies algunos colores: quiero que reproduzcas su estilo visual, distribución, jerarquía y organización de los elementos.

IMPORTANTE: Este encargo se centra en el diseño visual. El simulador ya tiene sus requisitos funcionales definidos anteriormente. No elimines, simplifiques ni dañes ninguna funcionalidad existente.

## 1. ESTILO VISUAL
- Fondo general azul marino muy oscuro (#0B1220 aproximadamente).
- Paneles y tarjetas en azul oscuro (#18243D aproximadamente).
- Bordes sutiles en azul grisáceo.
- Texto principal blanco.
- Texto secundario azul grisáceo claro.
- Verde brillante para representar resultados positivos y ahorro.
- Amarillo o dorado para representar generación solar y excedentes.
- Azul para representar consumo eléctrico.
- Rojo para representar déficit o energía comprada a la red.

## 2. DISTRIBUCIÓN DE LA PANTALLA
A. Encabezado superior (Icono de sol, título grande "Simulador solar fotovoltaico residencial", información secundaria con vivienda, tarifa y horas simuladas).
B. Barra de acciones (Modo oscuro/claro, Caso de verificación, Restablecer configuración).
C. Mensaje de resultados (Barra horizontal con resumen destacado en verde: "El sol cubre el X% de la demanda y te ahorra $Y en el día").
D. Tarjetas principales (4 tarjetas horizontales: AUTOCONSUMO, EXCEDENTE, DEMANDA CUBIERTA en fondo #18243D con bordes sutiles, y AHORRO DEL DÍA destacada con fondo verde brillante y texto oscuro).
E. Área principal de trabajo:
   - COLUMNA IZQUIERDA: CONTROLES (panel vertical "Controles" con deslizadores de paneles, potencia, pérdidas, checkbox día nublado, potencia total instalada, nombre y botón guardar escenario).
   - COLUMNA DERECHA: GRÁFICA (panel "Generación vs. consumo por hora" con línea amarilla solar, azul consumo, área verde excedente, área roja déficit, leyenda superior y fondo azul oscuro).
```


---

## Prompt 6
- **Fecha y Hora:** 2026-11-22 16:06:39
- **Rol:** Estudiante de Ingeniería Energética (Fundamentos de Programación)
- **Contenido del Prompt:**

```text
NUEVA FUNCIONALIDAD: ESTADO, FALLAS Y MANTENIMIENTO DE LOS PANELES SOLARES

Quiero ampliar mi proyecto Simulador solar fotovoltaico residencial con una nueva funcionalidad que permita representar situaciones reales que pueden afectar el rendimiento de los paneles solares.

IMPORTANTE: En esta primera etapa NO QUIERO QUE IMPLEMENTES NADA. Primero quiero que analices el funcionamiento actual del programa, estudies las posibilidades y me presentes diferentes propuestas. Yo elegiré cuál considero más conveniente antes de autorizar cualquier modificación.

1. NUEVO SISTEMA DE ESTADO DE LOS PANELES (Operativo, Sucio, En mantenimiento, Con falla, etc.)
2. PROPÓN DIFERENTES ALTERNATIVAS (Alternativa A: por panel/grupo, B: por rendimiento/matriz, C: por fallas y mantenimiento horario).
3. INTEGRACIÓN CON LA GRÁFICA PRINCIPAL (curva real vs teórica, paneles afectados).
4. REDISEÑO DE LA TABLA DE HORARIO DETALLADO (estilo propio #0B1220 y #18243D, colores semánticos, indicadores de horas con merma).
5. COHERENCIA CON EL DISEÑO ACTUAL
6. RESTRICCIONES IMPORTANTES (No librerías nuevas, compatibilidad JSON, fundamentos de programación).
```

---

## Prompt 7
- **Fecha y Hora:** 2026-11-22 16:11:57
- **Rol:** Estudiante de Ingeniería Energética (Fundamentos de Programación)
- **Contenido del Prompt:**

```text
1. me gusta la opcion A pero puedes agregarle la matriz visual de la B
2. esa opcion de la linea me gusta, agregala
3. Si apruebo el diseño para la tabla horaria detallada
```
- **Decisiones Aprobadas por el Usuario:**
  1. Estado de los paneles: Alternativa A enriquecida con la Matriz Visual de la B (selectores de cantidad por estado: Operativos 100%, Sucios 80%, Con Falla 20%, En Mantenimiento 0%, más la cuadrícula visual de los módulos en el tejado con sus respectivos estados de color).
  2. Gráfica horaria: Integración de la línea punteada dorada de «Generación Teórica Óptima (Sin fallas)» contrastada con la línea sólida de «Generación Solar Real» para visibilizar la energía perdida por suciedad o averías.
  3. Tabla horaria detallada: Rediseño completo en HTML/CSS nativo integrado con el tema del dashboard, con colores semánticos (amarillo generación, azul consumo, verde autoconsumo, verde brillante excedente, rojo déficit) y badges de estado horario.


---

## Prompt 8
- **Fecha y Hora:** 2026-11-22 16:30:27
- **Rol:** Estudiante de Ingeniería Energética (Fundamentos de Programación)
- **Contenido del Prompt:**

```text
Encontre un error en el momento de elegir el tipo de operativo del panel, cuando pongo todos con falla y de igual forma sucios automaticamente sale con que "Tienen 100% de salud" y sale funcional, arregla eso
```
- **Diagnóstico y Corrección:**
  - **Causa Raíz:** Cuando la suma de paneles no operativos (sucios + con falla + mantenimiento) superaba el número total de paneles instalados, existía una condición de reinicio que forzaba a cero todas las fallas (`num_sucios = 0; num_fallas = 0; num_mantenimiento = 0`), lo que provocaba que el sistema considerara erróneamente que todos los paneles volvían a estar 100% operativos.
  - **Solución:** Se implementó una lógica de acotamiento inteligente (*cap / clamping*) que nunca resetea a cero los estados seleccionados por el usuario. Si la suma intenta exceder el total de paneles, se asigna el cupo máximo real preservando las fallas y suciedad configuradas, calculando con exactitud la caída de salud (20% si todos tienen falla, 80% si todos están sucios, o 0% si están en mantenimiento), actualizando en tiempo real la matriz del tejado, la gráfica y los balances energéticos.


---

## Prompt 10 (Aprobación e Implementación Inmediata)
- **Fecha y Hora:** 2026-11-22 17:30:54
- **Rol:** Estudiante de Ingeniería Energética (Fundamentos de Programación)
- **Contenido del Prompt:**

```text
1. aprueba la alternativa A y que este organizado por vivienda y fecha
2. me gusta la idea de la navergacion superior mediante pestaña, pero trata de que esten bastante cerca
3. antes de que hagas todo eso quiero que hagas lo siguiente, el precio y costo total de la pagina es en pesos colombianos y quiero ponerle la opcion donde yo pueda escrbir "vivienda 1 o 2 o 3" y tambien poner la tarifa

agrega eso enseguida, no me preguntes
```

- **Resumen de Arquitectura e Implementación Realizada:**
  1. **Moneda en Pesos Colombianos (COP):**
     - Se unificó toda la interfaz para formatear las tarifas, costos y ahorros en pesos colombianos (`$ X.XXX COP`, `$ X.XXX COP/kWh`).
     - Se aplicó tanto en el encabezado, mensaje resumen en barra horizontal, tarjeta radiante de ahorro (`AHORRO DEL DÍA (COP)`), comparadores de escenarios y en cada celda del historial energético y calendario.
  2. **Configuración de Vivienda y Tarifa:**
     - Se integró un expander y selector directo para alternar entre "Casa 12", "Vivienda 1", "Vivienda 2", "Vivienda 3" o ingresar libremente cualquier nombre de vivienda personalizada.
     - Se agregó un control numérico directo para ajustar la tarifa eléctrica en tiempo real ($/kWh COP), recalculando de inmediato los balances y ahorros de la simulación.
  3. **Navegación Superior con Pestañas Contiguas:**
     - Se crearon las pestañas superiores `[ ☀️ Simulador Solar Fotovoltaico ]` y `[ 📅 Historial Energético y Base de Datos ]`.
     - Mediante CSS personalizado (`div[data-baseweb="tab-list"] { gap: 6px; }`, `button[data-baseweb="tab"]`), se garantizó que queden muy juntas, modernas y fáciles de alternar.
  4. **Base de Datos del Historial Anual (Alternativa A - `datos/historial_energetico.json`):**
     - Estructura jerárquica: `base_datos[vivienda][fecha]` (formato ISO `YYYY-MM-DD`).
     - Verificación de duplicados en tiempo constante $O(1)$ (`existe_registro_dia`).
     - Almacena los 14 parámetros clave: fecha, día de la semana, vivienda, número de paneles, potencia pico (kWp), pérdidas (%), generación total (kWh), autoconsumo (kWh), excedente (kWh), déficit red (kWh), cobertura (%), ahorro ($ COP), tarifa ($ COP/kWh), estado de paneles (operativo, sucio, falla, mantenimiento, % salud), perfiles horarios completos y notas.
  5. **Módulo Pedagógico en `logica.py` (Fundamentos de Programación):**
     - Regla del año bisiesto (`es_anio_bisiesto`).
     - Días por mes (`obtener_dias_del_mes`).
     - Día de la semana en español (`obtener_dia_semana_nombre`).
     - Generador de matriz/grilla de 7 columnas (`generar_grilla_calendario_mes`).
     - CRUD: `cargar_base_datos_historial`, `guardar_base_datos_historial`, `crear_registro_dia`, `guardar_registro_dia`, `eliminar_registro_dia`.
     - Analítica: `obtener_resumen_mensual_historial`, `obtener_resumen_anual_historial`, `obtener_estadisticas_dias_semana` (con diagnóstico de hábitos de consumo laborables vs fin de semana), `comparar_anios_historial`.
  6. **Calendario Mensual e Inspección en `app.py`:**
     - Selector de año con botones `◀ Año Anterior` y `Año Siguiente ▶`.
     - Selector de 12 meses (Ene a Dic) con indicador de cantidad de días registrados.
     - Cuadrícula de 7 columnas (Lun a Dom) con códigos de color: 🟢 Óptimo (100% salud), 🟡 Afectado (suciedad/falla/merma) y ⚪ Vacío (con botón para crear registro).
     - Tarjeta de inspección con desglose de 14 métricas, curva horaria Plotly mini de 24h, botón de eliminación y botón `🔄 Cargar en el Simulador` con carga diferida libre de errores.
     - Analítica anual con gráfico de barras Plotly de los 12 meses (Ahorro $ COP y Generación kWh) y comparación entre días laborables y fines de semana.
  7. **Pruebas y Verificación:**
     - `test_caso_verificacion.py`: 100% de precisión matemática (2.6 kWh autoconsumo, 65% cobertura, 0.6 kWh excedente, $2,080 COP de ahorro).
 ---

## Prompt 11
- **Fecha y Hora:** 2026-11-22 17:51:14
- **Rol:** Estudiante de Ingeniería Energética (Fundamentos de Programación)
- **Contenido del Prompt:**

```text
UNIFICACIÓN DE HISTORIAL MANUAL CON CALENDARIO + CORRECCIÓN DE MARGEN SUPERIOR

Registra este prompt en BITACORA.md/historial_prompts.md siguiendo el mismo formato cronológico de los anteriores.

Necesito realizar dos ajustes importantes en la aplicación:

1. CORRECCIÓN VISUAL: PESTAÑAS SUPERIORES RECORTADAS

Actualmente, las pestañas superiores ("☀️ Simulador Solar Fotovoltaico" y "📅 Historial Energético y Base de Datos") quedaron demasiado arriba y se cortan debajo de la barra superior de Streamlit (donde aparece "Deploy").
- Ajusta el CSS en app.py (por ejemplo, aumentando el `padding-top` de `.block-container` de `1.2rem` a `3.8rem` o `4.2rem`, y dando margen superior limpio a las pestañas) para que las pestañas superiores bajen y se vean completas, claras y sin solaparse con la barra de Streamlit.


2. HISTORIAL DE DÍAS 100% MANUAL Y UNIFICADO CON EL CALENDARIO

NO quiero días simulados ni precargados automáticamente. Quiero que el "Historial Semanal (7 Días)" y la pestaña "📅 Historial Energético y Base de Datos (Calendario)" trabajen completamente juntos sobre la MISMA base de datos (`datos/historial_energetico.json`), y que sea el usuario quien vaya agregando cada día uno por uno.

QUÉ DEBE HACER:
1. Inicio limpio (sin días simulados):
   - Elimina la generación automática de días ficticios al iniciar (`generar_historial_semanal_inicial` ya no debe llenar la semana con datos inventados).
   - Deja limpia la base de datos inicial (`datos/historial_energetico.json` vacía `{}` o con un botón visible para vaciar registros de prueba si hubiera) para que solo aparezcan los días que el usuario registre manualmente.
   - Si no hay días registrados para la vivienda activa, muestra un mensaje claro indicando al usuario que configure los controles y agregue su primer día.

2. Registro manual día a día (sincronizado con Controles y Calendario):
   - Tanto en el panel de Controles como en la pestaña "📅 Historial Semanal (7 Días)", el usuario debe poder elegir una fecha (mostrando automáticamente qué día de la semana corresponde: Lunes, Martes, Miércoles, etc.) y pulsar un botón "➕ Agregar día al historial".
   - Al agregarlo, debe guardar en `datos/historial_energetico.json` EXACTAMENTE la configuración y resultados actuales de los Controles:
     * Vivienda activa y tarifa eléctrica ($ COP/kWh).
     * Número de paneles, potencia por panel (kW), potencia total instalada (kWp) y pérdidas (%).
     * Condición climática (Normal o Día nublado).
     * Estado y salud de los paneles (operativos, sucios, con falla, mantenimiento y % de salud).
     * Resultados calculados (generación, consumo, autoconsumo, excedente, déficit, % cobertura, ahorro en COP) y los perfiles horarios de 24h.

3. Todo conectado (una sola fuente de verdad):
   - Cada día que el usuario agregue debe aparecer AL INSTANTE tanto en la pestaña "📅 Historial Semanal (7 Días)" como en su casilla exacta del **Calendario mensual** (con su color 🟢 Óptimo o 🟡 Afectado) y sumarse automáticamente a las estadísticas mensuales, anuales y de días laborables vs. fin de semana.
   - La pestaña "📅 Historial Semanal (7 Días)" debe mostrar los días reales registrados por el usuario para la vivienda activa (por ejemplo, los últimos 7 días registrados o los días de la semana seleccionada, ordenados cronológicamente), con su resumen semanal calculado únicamente sobre los días reales agregados.
   - Si el usuario vuelve a registrar una fecha ya existente para la misma vivienda, debe actualizar ese día (sin duplicarlo) y avisar con una notificación (`st.toast`).
   - Al cargar un día guardado hacia el simulador (desde el historial semanal o desde el calendario), debe restaurar todos los controles exactos de ese día (paneles, kW, pérdidas, tarifa, día nublado y estados de salud).
   - Si el usuario elimina un día desde el historial semanal o desde el calendario, debe eliminarse de la base de datos y desaparecer de ambas vistas al instante.

RESTRICCIONES:
- Mantén toda la lógica en `logica.py` usando únicamente conceptos de Fundamentos de Programación (funciones con return, listas, diccionarios, ciclos, condicionales, variables locales y JSON).
- No agregues librerías nuevas.
- Conserva el diseño oscuro actual (#0B1220 y #18243D), la moneda en Pesos Colombianos (COP) y no dañes el Caso de Verificación ni el Comparador de escenarios.
```

- **Plan de Acción y Decisiones:**
  1. Aumentar `padding-top` de `.block-container` a `4.2rem` en `app.py` y otorgar separación superior adecuada para garantizar que las pestañas principales nunca queden recortadas bajo la barra de herramientas de Streamlit.
  2. Unificar el Historial Semanal y el Calendario sobre una única fuente de verdad: `datos/historial_energetico.json`.
  3. Eliminar la generación de días ficticios/simulados; inicializar la base de datos limpia (`{}`) para poblarla 100% de manera manual por el usuario.
  4. Proveer controles de registro manual ("➕ Agregar día al historial") sincronizados con los parámetros activos en ambos paneles, con detección de día de la semana y actualización reactiva.
  5. Sincronizar acciones de carga (`🔄 Cargar en el Simulador`) y eliminación (`🗑️ Eliminar`) en ambas vistas sin duplicados.

- **Resultados de Verificación Automatizada (100% Éxito):**
  - **Margen Superior:** Pestañas visualizadas limpiamente con separación total respecto a la barra nativa de Streamlit.
  - **Estado Inicial:** Inicio 100% limpio sin registros ficticios, mostrando mensaje orientador al usuario.
  - **Registro Manual Sincronizado:** Se agregaron días reales (2026-11-22 en verde óptimo y 2026-11-23 en amarillo por merma del 10%), reflejándose inmediatamente en ambas vistas (tarjetas semanales y casillas de calendario) y actualizando métricas acumuladas en COP.
  - **Acciones y Vaciado:** El botón `🔄 Cargar` restaura fielmente perfiles y controles sin errores de ciclo de vida; el botón de vaciado limpia de forma instantánea ambas vistas y el archivo JSON.
  - **Caso de Verificación:** `test_caso_verificacion.py` superado con 100% de precisión matemática (2.6 kWh autoconsumo, 65% cobertura, 0.6 kWh excedente, $2,080 COP de ahorro).

