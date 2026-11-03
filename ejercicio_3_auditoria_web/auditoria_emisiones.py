from typing import Any


def calcular_emisiones_carbono(consumo_kwh: float, factor_emision: float = 0.4) -> float:
    """
    Punto A: Calcula la huella de carbono industrial en kg de CO2eq.
    Eleva ValueError si el consumo eléctrico es negativo.
    """
    if consumo_kwh < 0:
        raise ValueError(
            f"El consumo eléctrico no puede ser negativo (valor recibido: {consumo_kwh} kWh)."
        )
    if factor_emision < 0:
        raise ValueError(
            f"El factor de emisión no puede ser negativo (valor recibido: {factor_emision})."
        )
    return round(float(consumo_kwh) * float(factor_emision), 2)


def obtener_metricas_consumo(registros: list[dict[str, Any]]) -> dict[str, Any]:
    """
    Punto B: Procesa un historial de consumos por planta industrial utilizando
    calcular_emisiones_carbono para determinar el total global de emisiones
    y la planta de mayor consumo energético.
    """
    if not registros:
        return {
            "total_emisiones_kg": 0.0,
            "total_consumo_kwh": 0.0,
            "planta_mayor_consumo": "Sin registros",
            "max_consumo_kwh": 0.0,
            "detalle_plantas": [],
        }

    total_emisiones: float = 0.0
    total_consumo: float = 0.0
    planta_max: str = ""
    consumo_max: float = -1.0
    detalle_procesado: list[dict[str, Any]] = []

    for reg in registros:
        nombre_planta = str(reg.get("planta", "Planta Desconocida")).strip()
        consumo = float(reg.get("consumo_kwh", 0.0))
        factor = float(reg.get("factor_emision", 0.4))

        # Invocación obligatoria al algoritmo auditado del Punto A
        emisiones = calcular_emisiones_carbono(consumo, factor)

        total_consumo += consumo
        total_emisiones += emisiones

        if consumo > consumo_max:
            consumo_max = consumo
            planta_max = nombre_planta

        detalle_procesado.append({
            "planta": nombre_planta,
            "ubicacion": str(reg.get("ubicacion", "No especificada")),
            "consumo_kwh": round(consumo, 2),
            "factor_emision": factor,
            "emisiones_kg": emisiones,
        })

    return {
        "total_emisiones_kg": round(total_emisiones, 2),
        "total_consumo_kwh": round(total_consumo, 2),
        "planta_mayor_consumo": planta_max,
        "max_consumo_kwh": round(consumo_max, 2),
        "cantidad_plantas": len(detalle_procesado),
        "detalle_plantas": detalle_procesado,
    }