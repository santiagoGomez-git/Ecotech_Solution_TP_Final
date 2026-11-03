import unittest
from auditoria_emisiones import calcular_emisiones_carbono, obtener_metricas_consumo


class TestCalculoEmisiones(unittest.TestCase):
    """
    Punto A: Suite de pruebas unitarias para certificar la precisión del algoritmo
    calcular_emisiones_carbono y el procesamiento de métricas industriales.
    """

    def test_calculo_nominal_factor_por_defecto(self) -> None:
        """Valida el cálculo exacto con un consumo estándar y el factor por defecto (0.4)."""
        resultado = calcular_emisiones_carbono(1000.0)
        self.assertAlmostEqual(resultado, 400.00, places=2)

    def test_calculo_nominal_factor_personalizado(self) -> None:
        """Valida el cálculo con valores decimales y un factor de emisión específico."""
        resultado = calcular_emisiones_carbono(250.5, factor_emision=0.52)
        self.assertAlmostEqual(resultado, 130.26, places=2)

    def test_calculo_consumo_cero(self) -> None:
        """Valida el caso límite donde la planta registra 0 kWh de consumo."""
        resultado = calcular_emisiones_carbono(0.0)
        self.assertEqual(resultado, 0.0)

    def test_excepcion_consumo_negativo(self) -> None:
        """Verifica que se eleve ValueError ante un consumo eléctrico negativo."""
        with self.assertRaises(ValueError):
            calcular_emisiones_carbono(-150.0)

    def test_obtener_metricas_consumo_correcto(self) -> None:
        """Verifica la integración del cálculo de emisiones en el resumen de plantas."""
        historial_prueba = [
            {"planta": "Planta Norte", "consumo_kwh": 1000.0},
            {"planta": "Planta Sur", "consumo_kwh": 2500.0},
        ]
        metricas = obtener_metricas_consumo(historial_prueba)
        self.assertEqual(metricas["total_emisiones_kg"], 1400.0)
        self.assertEqual(metricas["planta_mayor_consumo"], "Planta Sur")


if __name__ == "__main__":
    unittest.main(verbosity=2)