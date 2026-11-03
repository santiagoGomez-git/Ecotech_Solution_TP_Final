# 🌱 EcoTech Solutions – Evaluación Técnica de Desarrollo

Resolución integral de la evaluación técnica estructurada en tres módulos independientes bajo buenas prácticas de **Python 3**, **Programación Orientada a Objetos (POO)**, **Testing Automatizado (`unittest` / `pytest`)** y **Django**.

---

## 📂 Estructura del Proyecto

```text
Ecotech_Solution_TP_Final/
├── ejercicio_1_sensores/
│   └── procesador_sensores.py         # Sanitización de telemetría y reporte estadístico
├── ejercicio_2_productos/
│   ├── modelos_catalogo.py            # POO, encapsulamiento, StockInvalidoError y polimorfismo
│   └── catalogo_ecotech.json          # Persistencia generada del catálogo de productos válidos
├── ejercicio_3_auditoria_web/
│   ├── __init__.py
│   ├── auditoria_emisiones.py         # Algoritmo de huella de carbono y métricas por planta
│   ├── test_emisiones.py              # Suite de pruebas unitarias (unittest / pytest)
│   ├── views.py                       # Vista FBV en Django (vista_panel_sustentabilidad)
│   ├── manage.py                      # Micro-servidor Django autónomo para visualización en vivo
│   └── templates/
│       └── sustentabilidad/
│           └── panel.html             # Interfaz web del Panel de Sustentabilidad
├── pyproject.toml                     # Gestión de dependencias y configuración con uv
└── README.md
```

---

## ⚙️ Instalación y Activación del Entorno

El proyecto fue configurado utilizando el gestor de paquetes y entornos **`uv`**:

```powershell
# 1. Crear y activar el entorno virtual
uv venv
.\.venv\Scripts\Activate.ps1

# 2. Sincronizar dependencias (Django y Pytest)
uv sync
```

---

## 🚀 Ejecución por Ejercicio

### 1. Ejercicio 1: Sanitización y Análisis Estadístico de Sensores (20 pts)
Normaliza lecturas térmicas crudas (`limpiar_registro_sensor`), evalúa umbrales críticos (`generar_resumen_sensores`) y emite el reporte consolidado por consola:

```powershell
python ejercicio_1_sensores\procesador_sensores.py
```

### 2. Ejercicio 2: Modelo de Productos, Excepciones y Persistencia (40 pts)
Ejecuta la jerarquía POO (`DispositivoEcologico` y `PanelSolar`), demuestra el polimorfismo en fichas técnicas, verifica la captura controlada de `StockInvalidoError` mediante encapsulamiento (`@property`) y exporta los dispositivos válidos a `catalogo_ecotech.json`:

```powershell
python ejercicio_2_productos\modelos_catalogo.py
```

### 3. Ejercicio 3: Auditoría con Tests Unitarios e Integración Web (40 pts)

* **Punto A – Ejecutar la suite de pruebas unitarias (`TestCalculoEmisiones`):**
  ```powershell
  pytest ejercicio_3_auditoria_web\test_emisiones.py -v
  ```
  *(También ejecutable con `unittest` nativo: `python ejercicio_3_auditoria_web\test_emisiones.py`)*

* **Punto B – Visualizar el Panel Web en Django (Nota de Arquitectura):**
  Además de los módulos requeridos por la consigna (`auditoria_emisiones.py`, `views.py` y `templates/sustentabilidad/panel.html`), se incluyó un script `manage.py` autocontenido para que el equipo docente pueda levantar el servidor y visualizar en vivo el renderizado de `vista_panel_sustentabilidad(request)` en el navegador con un único comando, manteniendo la carpeta 100% independiente:
  ```powershell
  python ejercicio_3_auditoria_web\manage.py runserver
  ```
  Luego abrir en el navegador: **http://127.0.0.1:8000/**