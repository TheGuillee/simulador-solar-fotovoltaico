# ☀️ Simulador Solar Fotovoltaico Residencial
**Asignatura:** Fundamentos de Programación — Ingeniería Energética  
**Autor:** Proyecto de Aplicación Práctica, Visual y de Gestión Energética  
**Tecnología:** Python + Streamlit + Plotly  

---

## 📋 Descripción del Proyecto

Aplicación interactiva y visual de ingeniería energética diseñada con la estética de un **Dashboard de Monitoreo Energético Profesional** (SCADA residencial). Permite simular el comportamiento horario de un sistema solar fotovoltaico residencial, contrastando la producción fotovoltaica con la demanda horaria del hogar, calculando balances energéticos (autoconsumo, excedente e inyección a la red), evaluando el impacto de **fallas, suciedad y mantenimiento de módulos** y cuantificando el ahorro económico diario según la tarifa eléctrica.

---

## 🗂️ Estructura del Proyecto

```text
simulador_solar/
│
├── BITACORA.md/                     # Carpeta de registro de prompts
│   └── historial_prompts.md         # Registro cronológico de todos los prompts e instrucciones
│
├── datos/
│   ├── entrada.json                 # Configuración residencial estándar (perfil 24 horas)
│   └── caso_verificacion.json       # Caso de prueba de verificación de clase (4 horas)
│
├── logica.py                        # Lógica pura de cálculo (solo conceptos vistos en clase)
├── app.py                           # Dashboard visual interactivo (Streamlit + Plotly + HTML/CSS nativo)
├── test_caso_verificacion.py        # Suite de pruebas unitarias automatizadas
└── README.md                        # Documentación y guía pedagógica
```

---

## 🛠️ Nueva Funcionalidad: Salud y Estado de los Paneles Solares

El simulador incorpora la gestión cuantitativa y física del estado de salud del parque solar:

1. **Estados Soportados:**
   - 🟢 **Operativo (100%):** Módulo en condiciones ideales.
   - 🟡 **Sucio (-20% de rendimiento):** Pérdidas ópticas por polvo, polen o excrementos de aves (*soiling*).
   - 🔴 **Con Falla (-80% de rendimiento):** Módulo con diodo bypass averiado, microfisuras o *hotspots*.
   - ⚪ **En Mantenimiento (0% de rendimiento):** Módulo desconectado temporalmente por reparación.

2. **Matriz Visual del Techo (Techo Digital):**
   - Representación gráfica de cada módulo instalado (`[P1 🟢]`, `[P2 🟢]`, `[P3 🟡]`, `[P4 🔴]...`) con colores dinámicos de estado.
   - Badge de salud del parque solar: `Eficiencia del Tejado: X %`.
   - Cálculo automático de la **Merma Energética y Económica por Fallas**:  
     Muestra cuántos kWh y dinero al día se pierden por no limpiar o reparar los módulos.

3. **Gráfica Solar con Generación Teórica Óptima:**
   - **Línea Dorada Punteada:** Generación Teórica Óptima (como si no hubiera fallas).
   - **Línea Amarilla Sólida:** Generación Real Efectiva.
   - Permite visualizar de forma inmediata la brecha de pérdida de energía generada por averías o suciedad.

---

## 📋 Rediseño Integral de la Tabla Horaria Detallada

La sección de balance horario fue reconstruida como una **Tabla HTML/CSS Nativa** integrada con el tema `#0B1220` y `#18243D`:
- **Encabezados:** Tipografía nítida en mayúsculas sobre fondo azul oscuro.
- **Colores Semánticos por Vector Energético:**
  - ☀️ Generación Real: Amarillo solar (`#FBBF24`).
  - ✨ Generación Óptima: Dorado suave (`#FDE68A`).
  - ⚡ Consumo Vivienda: Azul eléctrico (`#38BDF8`).
  - 🔋 Autoconsumo: Verde esmeralda (`#10B981`).
  - 🔄 Excedente: Verde brillante (`#34D399`) o guion (`—`).
  - 🔌 Déficit Red: Rojo coral (`#F43F5E`) o guion (`—`).
- **Columna de Diagnóstico con Badges:**
  - `🟢 100% Solar` (Generación cubre el 100% de la demanda).
  - `🟡 Parcial Solar` (Autoconsumo parcial + compra a red).
  - `🔴 Red Pura` (Horas sin sol o con paneles desconectados).
  - `⚠️ Merma / Red` (Horas con sol donde se pierde energía por suciedad o fallas).

---

## 🔬 Comprobación del Caso de Verificación del Examen

- **Parámetros:** 4 paneles de 0.5 kW, pérdidas 20%, tarifa $800/kWh, 4 horas: perfil `[0, 0.5, 1, 0.5]` y consumo `[1, 1, 1, 1]` kWh.
- **Resultados:**
  - Generación horaria: `[0.0, 0.8, 1.6, 0.8] kWh`
  - Autoconsumo: `2.6 kWh` (65.0% de la demanda)
  - Excedente: `0.6 kWh`
  - Ahorro del día: `$2,080`
  - Día nublado (perfil $\times 0.5$): Autoconsumo `1.6 kWh` y Excedente `0.0 kWh`
  - Reto comparador: 8 paneles vs 4 paneles explica el fenómeno de saturación solar residencial.

---

## 🚀 Cómo Ejecutar la Aplicación

1. **Abrir PowerShell o terminal en la carpeta:**
   ```powershell
   cd C:\Users\Jason\.gemini\antigravity\scratch\simulador_solar
   ```

2. **Ejecutar pruebas unitarias de lógica:**
   ```powershell
   python test_caso_verificacion.py
   ```

3. **Iniciar la aplicación interactiva:**
   ```powershell
   python -m streamlit run app.py
   ```

4. **Abrir en tu navegador:** [http://localhost:8501](http://localhost:8501)
