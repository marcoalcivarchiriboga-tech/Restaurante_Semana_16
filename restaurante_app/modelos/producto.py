class Producto:
    def __init__(self, codigo: str, nombre: str, precio: float, categoria: str, tipo: str = "CONSUMO_LOCAL", stock: int = 10):
        self.codigo = codigo
        self.nombre = nombre
        self.precio = float(precio) # Se espera un valor numérico
        self.categoria = categoria
        self.tipo = tipo.upper() if isinstance(tipo, str) else "CONSUMO_LOCAL"
        self.stock = int(stock)

    def mostrar_informacion(self) -> str:
        """Devuelve la representación legible del producto para consolas y servicios."""
        return f"[{self.tipo}] [{self.codigo}] {self.nombre} - ${self.precio:.2f} ({self.categoria}) | Stock: {self.stock}"

    def a_diccionario(self) -> dict:
        """Convierte la información del objeto a un diccionario para JSON."""
        return {
            "codigo": self.codigo,
            "nombre": self.nombre,
            "precio": self.precio,
            "categoria": self.categoria,
            "tipo": self.tipo,
            "stock": self.stock,
            "tipo_producto": "Producto"
        }

    def to_dict(self) -> dict:
        """Alias para mantener compatibilidad con la estructura general del proyecto."""
        return self.a_diccionario()

    @staticmethod
    def from_dict(datos: dict):
        """Crea una instancia de Producto a partir de un diccionario cargado desde JSON."""
        return Producto(
            codigo=datos.get("codigo", ""),
            nombre=datos.get("nombre", ""),
            precio=datos.get("precio", 0.0),
            categoria=datos.get("categoria", ""),
            tipo=datos.get("tipo", "CONSUMO_LOCAL"),
            stock=datos.get("stock", 10)
        )
    
    def __str__(self):
        return f"[{self.codigo}] {self.nombre} - ${self.precio:.2f} ({self.categoria})"