class Venta:
    def __init__(self, id_venta: str, identificacion_usuario: str, codigo_producto: str, cantidad: int, total: float, fecha: str):
        self.id_venta = id_venta
        self.identificacion_usuario = identificacion_usuario
        self.codigo_producto = codigo_producto
        self.cantidad = int(cantidad)
        self.total = float(total)
        self.fecha = fecha

    def a_diccionario(self) -> dict:
        return {
            "id_venta": self.id_venta,
            "identificacion_usuario": self.identificacion_usuario,
            "codigo_producto": self.codigo_producto,
            "cantidad": self.cantidad,
            "total": self.total,
            "fecha": self.fecha
        }

    def to_dict(self) -> dict:
        return self.a_diccionario()

    @staticmethod
    def from_dict(datos: dict):
        return Venta(
            id_venta=datos.get("id_venta", ""),
            identificacion_usuario=datos.get("identificacion_usuario", datos.get("id_usuario", "")),
            codigo_producto=datos.get("codigo_producto", datos.get("isbn", "")),
            cantidad=datos.get("cantidad", 1),
            total=datos.get("total", 0.0),
            fecha=datos.get("fecha", "")
        )

    def mostrar_informacion(self) -> str:
        return f"ID Venta: {self.id_venta} | Cliente: {self.identificacion_usuario} | Producto: {self.codigo_producto} | Cantidad: {self.cantidad} | Total: ${self.total:.2f} | Fecha: {self.fecha}"

    def __str__(self) -> str:
        return self.mostrar_informacion()