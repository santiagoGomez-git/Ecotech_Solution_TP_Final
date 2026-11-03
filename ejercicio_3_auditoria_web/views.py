from typing import Any
from django.http import HttpRequest, HttpResponse
from django.shortcuts import render
from auditoria_emisiones import obtener_metricas_consumo


# Simulación de datos realistas de prueba (según Especificaciones Generales de Entrega)
REGISTROS_CONSUMO_SIMULADOS: list[dict[str, Any]] = [
    {
        "planta": "Planta Ensamblaje Norte (Mendoza)",
        "ubicacion": "Parque Industrial Las Heras",
        "consumo_kwh": 14500.0,
        "factor_emision": 0.4,
    },
    {
        "planta": "Centro Logístico Andino",
        "ubicacion": "Luján de Cuyo",
        "consumo_kwh": 8200.5,
        "factor_emision": 0.4,
    },
    {
        "planta": "Planta Metalúrgica Sur",
        "ubicacion": "Godoy Cruz",
        "consumo_kwh": 23800.0,
        "factor_emision": 0.4,
    },
    {
        "planta": "Laboratorio I+D Solar",
        "ubicacion": "Ciudad de Mendoza",
        "consumo_kwh": 4150.0,
        "factor_emision": 0.4,
    },
]


def vista_panel_sustentabilidad(request: HttpRequest) -> HttpResponse:
    """
    Punto B: Vista Basada en Función (FBV) de Django que invoca el procesamiento
    de métricas de huella de carbono y renderiza la plantilla 'sustentabilidad/panel.html'.
    """
    metricas = obtener_metricas_consumo(REGISTROS_CONSUMO_SIMULADOS)

    contexto: dict[str, Any] = {
        "titulo_panel": "EcoTech Solutions - Panel de Auditoría y Sustentabilidad",
        "periodo_auditado": "Noviembre 2026",
        "total_emisiones_kg": metricas["total_emisiones_kg"],
        "total_consumo_kwh": metricas["total_consumo_kwh"],
        "planta_mayor_consumo": metricas["planta_mayor_consumo"],
        "max_consumo_kwh": metricas["max_consumo_kwh"],
        "cantidad_plantas": metricas["cantidad_plantas"],
        "detalle_plantas": metricas["detalle_plantas"],
    }

    return render(request, "sustentabilidad/panel.html", contexto)