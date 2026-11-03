import json
from pathlib import Path
from typing import Any


class StockInvalidoError(Exception):
    """Excepción personalizada que se lanza ante intentos de asignar un stock negativo."""
    pass


class DispositivoEcologico:
    """
    Punto A: Clase base del dominio del catálogo sustentable.
    Aplica encapsulamiento explícito para proteger la integridad del stock.
    """

    def __init__(self, codigo: str, nombre: str, precio: float, stock: int) -> None:
        self.codigo: str = codigo.strip()
        self.nombre: str = nombre.strip()
        self.precio: float = float(precio)
        self._stock: int = 0
        # Asignamos mediante la propiedad para disparar la validación desde el __init__
        self.stock = stock

    @property
    def stock(self) -> int:
        """Getter del atributo encapsulado _stock."""
        return self._stock

    @stock.setter
    def stock(self, valor: int) -> None:
        """Setter que valida que el stock nunca sea negativo."""
        if valor < 0:
            raise StockInvalidoError(
                f"Operación rechazada en '{self.nombre}' ({self.codigo}): "
                f"El stock no puede ser negativo (se intentó asignar: {valor})."
            )
        self._stock = int(valor)

    def emitir_ficha_tecnica(self) -> str:
        """Retorna la ficha técnica comercial base del dispositivo."""
        return (
            f"[{self.codigo}] {self.nombre} | "
            f"Precio: ${self.precio:,.2f} | Stock disponible: {self.stock} u."
        )

    def to_dict(self) -> dict[str, Any]:
        """Convierte la instancia en un diccionario serializable a JSON."""
        return {
            "tipo": self.__class__.__name__,
            "codigo": self.codigo,
            "nombre": self.nombre,
            "precio": self.precio,
            "stock": self.stock,
        }


class PanelSolar(DispositivoEcologico):
    """
    Punto A: Clase especializada que hereda de DispositivoEcologico.
    Incorpora atributos propios y aplica polimorfismo en su ficha técnica.
    """

    def __init__(
        self,
        codigo: str,
        nombre: str,
        precio: float,
        stock: int,
        potencia_watts: int,
        eficiencia: float,
    ) -> None:
        super().__init__(codigo, nombre, precio, stock)
        self.potencia_watts: int = int(potencia_watts)
        self.eficiencia: float = float(eficiencia)

    def emitir_ficha_tecnica(self) -> str:
        """Polimorfismo: extiende la ficha técnica comercial con especificaciones solares."""
        ficha_base = super().emitir_ficha_tecnica()
        return (
            f"{ficha_base} | Potencia: {self.potencia_watts}W | "
            f"Eficiencia: {self.eficiencia:.1f}%"
        )

    def to_dict(self) -> dict[str, Any]:
        """Polimorfismo en serialización: agrega los atributos específicos del panel."""
        datos = super().to_dict()
        datos["potencia_watts"] = self.potencia_watts
        datos["eficiencia"] = self.eficiencia
        return datos


class GestorInventario:
    """Punto B: Gestiona la persistencia del catálogo de dispositivos en formato JSON."""

    @staticmethod
    def guardar_catalogo_json(
        lista_dispositivos: list[DispositivoEcologico],
        ruta_archivo: str | Path,
    ) -> None:
        """Serializa y almacena la lista de dispositivos en el archivo JSON indicado."""
        datos_exportables: list[dict[str, Any]] = [
            dispositivo.to_dict() for dispositivo in lista_dispositivos
        ]
        ruta_destino = Path(ruta_archivo)
        with open(ruta_destino, mode="w", encoding="utf-8") as archivo:
            json.dump(datos_exportables, archivo, indent=4, ensure_ascii=False)


# =====================================================================
# BLOQUE DE PRUEBA (Verificación de Excepciones, Polimorfismo y JSON)
# =====================================================================
if __name__ == "__main__":
    print("=" * 75)
    print("  ECOTECH SOLUTIONS - CATÁLOGO DE PRODUCTOS Y PERSISTENCIA")
    print("=" * 75)

    # 1. Instanciación de productos válidos
    bateria = DispositivoEcologico(
        codigo="ECO-BAT-100",
        nombre="Banco de Baterías Litio Ferrofosfato",
        precio=1850.00,
        stock=15,
    )
    panel_mono = PanelSolar(
        codigo="ECO-SOL-550",
        nombre="Panel Solar Monocristalino Tier-1",
        precio=295.50,
        stock=40,
        potencia_watts=550,
        eficiencia=21.6,
    )
    panel_bifacial = PanelSolar(
        codigo="ECO-SOL-660",
        nombre="Panel Solar Bifacial Industrial",
        precio=380.00,
        stock=25,
        potencia_watts=660,
        eficiencia=22.9,
    )

    catalogo_activo: list[DispositivoEcologico] = [bateria, panel_mono, panel_bifacial]

    print("\n[A] FICHAS TÉCNICAS COMERCIALES (Polimorfismo):")
    print("-" * 75)
    for item in catalogo_activo:
        print(f"• {item.emitir_ficha_tecnica()}")

    # 2. Verificación de captura controlada de StockInvalidoError
    print("\n[B] PRUEBA DE VALIDACIÓN DE INVENTARIO (StockInvalidoError):")
    print("-" * 75)

    # Prueba 2.1: Intento de asignar stock negativo mediante el setter
    try:
        print("-> Intentando modificar el stock de 'ECO-BAT-100' a -8 unidades...")
        bateria.stock = -8
    except StockInvalidoError as err:
        print(f"   [ALERTA CAPTURADA]: {err}")
        print(f"   [ESTADO SEGURO]   : El stock de '{bateria.codigo}' se mantuvo en {bateria.stock} u.")

    # Prueba 2.2: Intento de crear un PanelSolar con stock inicial negativo
    try:
        print("\n-> Intentando registrar un nuevo PanelSolar con stock inicial de -5...")
        panel_invalido = PanelSolar(
            codigo="ECO-SOL-ERR",
            nombre="Panel Solar Prueba Fallida",
            precio=210.00,
            stock=-5,
            potencia_watts=450,
            eficiencia=19.0,
        )
    except StockInvalidoError as err:
        print(f"   [ALERTA CAPTURADA]: {err}")

    # 3. Exportación de productos válidos a catalogo_ecotech.json
    ruta_json = Path(__file__).parent / "catalogo_ecotech.json"
    GestorInventario.guardar_catalogo_json(catalogo_activo, ruta_json)

    print("\n[C] PERSISTENCIA EN DISCO:")
    print("-" * 75)
    print(f"• Archivo generado exitosamente : {ruta_json.name}")
    print(f"• Ubicación                     : {ruta_json}")
    print(f"• Productos válidos exportados  : {len(catalogo_activo)}")
    print("=" * 75)