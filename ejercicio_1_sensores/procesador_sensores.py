from typing import Any


def limpiar_registro_sensor(registro_raw: dict[str, Any]) -> dict[str, Any]:
    """
    Punto A: Normaliza un diccionario con datos crudos de un sensor térmico.
    - 'sensor_id': string sin espacios sobrantes en los extremos.
    - 'temperatura': float sin sufijos de unidad (ej. 'C', '°C').
    - 'ubicacion': string limpio o valor por defecto seguro si falta o está vacío.
    """
    # 1. Limpieza de sensor_id sin espacios sobrantes
    raw_id = str(registro_raw.get("sensor_id", "ID-DESCONOCIDO"))
    sensor_id_limpio = raw_id.strip() or "ID-DESCONOCIDO"

    # 2. Conversión de temperatura a float eliminando sufijos de unidad
    raw_temp = registro_raw.get("temperatura", 0.0)
    if isinstance(raw_temp, (int, float)):
        temperatura_limpia = float(raw_temp)
    else:
        temp_str = str(raw_temp).strip().upper()
        for sufijo in ("°C", "C", "°F", "F", "°"):
            temp_str = temp_str.replace(sufijo, "")
        temperatura_limpia = float(temp_str.strip())

    # 3. Validación de ubicación con valor por defecto seguro
    raw_ubicacion = registro_raw.get("ubicacion")
    if raw_ubicacion is None or not str(raw_ubicacion).strip():
        ubicacion_limpia = "Sin ubicación registrada"
    else:
        ubicacion_limpia = str(raw_ubicacion).strip()

    return {
        "sensor_id": sensor_id_limpio,
        "temperatura": temperatura_limpia,
        "ubicacion": ubicacion_limpia,
    }


def generar_resumen_sensores(
    lista_sensores_limpios: list[dict[str, Any]], 
    umbral_temperatura: float
) -> tuple[list[str], float]:
    """
    Punto B: Recibe registros sanitizados y un valor límite.
    Retorna la tupla (lista_sensores_alerta, promedio_temperatura).
    """
    if not lista_sensores_limpios:
        return ([], 0.0)

    lista_sensores_alerta: list[str] = []
    suma_temperaturas: float = 0.0

    for sensor in lista_sensores_limpios:
        temp = sensor["temperatura"]
        suma_temperaturas += temp

        if temp > umbral_temperatura:
            lista_sensores_alerta.append(sensor["sensor_id"])

    promedio_temperatura = round(suma_temperaturas / len(lista_sensores_limpios), 2)

    return (lista_sensores_alerta, promedio_temperatura)


if __name__ == "__main__":
    # Lote de prueba con los casos exigidos en la consigna
    datos_crudos: list[dict[str, Any]] = [
        {"sensor_id": " SENSOR-001 ", "temperatura": "24.5C", "ubicacion": "Planta Norte"},
        {"sensor_id": "SENSOR-002   ", "temperatura": " 31.2 °C ", "ubicacion": "Sector Calderas"},
        {"sensor_id": "  SENSOR-003", "temperatura": "28.9c", "ubicacion": ""},
        {"sensor_id": "SENSOR-004", "temperatura": "19.5C"},
        {"sensor_id": " SENSOR-005 ", "temperatura": 34.0, "ubicacion": "  Sala de Servidores  "},
    ]

    UMBRAL = 28.0

    print("=" * 65)
    print("  ECOTECH SOLUTIONS - REPORTE CONSOLIDADO DE SENSORES")
    print("=" * 65)

    # 1. Sanitización de registros (Punto A)
    sensores_limpios = [limpiar_registro_sensor(reg) for reg in datos_crudos]

    print("\n[A] LECTURAS NORMALIZADAS:")
    print(f"{'ID SENSOR':<14} | {'TEMP (°C)':<10} | {'UBICACIÓN'}")
    print("-" * 65)
    for s in sensores_limpios:
        print(f"{s['sensor_id']:<14} | {s['temperatura']:<10.2f} | {s['ubicacion']}")

    # 2. Monitoreo y resumen estadístico (Punto B)
    alertas, promedio = generar_resumen_sensores(sensores_limpios, UMBRAL)

    print("\n[B] ESTADÍSTICAS Y ALERTAS TÉRMICAS:")
    print("-" * 65)
    print(f"• Sensores analizados      : {len(sensores_limpios)}")
    print(f"• Promedio térmico global  : {promedio:.2f} °C")
    print(f"• Umbral de alerta fijado  : {UMBRAL:.2f} °C")
    print(f"• IDs en estado de alerta  : {', '.join(alertas) if alertas else 'Ninguno'}")
    print("=" * 65)