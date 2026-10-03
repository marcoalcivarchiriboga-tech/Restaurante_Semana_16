import json
import os

class ArchivoServicio:
    def __init__(self, ruta_archivo: str):
        self.ruta_archivo = ruta_archivo

    def cargar_datos(self) -> list:
        try:
            with open(self.ruta_archivo, 'r', encoding='utf-8') as archivo:
                return json.load(archivo)
        except FileNotFoundError:
            nombre_archivo = os.path.basename(self.ruta_archivo) if self.ruta_archivo else "archivo"
            print(f"Aviso: El archivo '{nombre_archivo}' todavía no existe. Se iniciará con una colección vacía.")
            return []
        except json.JSONDecodeError:
            print("Error: El contenido del archivo no posee un formato JSON válido. Iniciando vacío.")
            return []
        except PermissionError:
            print("Error: No existen permisos suficientes para leer el archivo.")
            return []

    def guardar_datos(self, datos: list) -> bool:
        try:
            directorio = os.path.dirname(self.ruta_archivo)
            if directorio:
                os.makedirs(directorio, exist_ok=True)

            with open(self.ruta_archivo, 'w', encoding='utf-8') as archivo:
                json.dump(datos, archivo, indent=4, ensure_ascii=False)
            return True
        except PermissionError:
            print("Error: No existen permisos suficientes para escribir en el archivo.")
            return False
        except Exception as e:
            print(f"Error inesperado al guardar: {e}")
            return False

    @staticmethod
    def cargar_json(ruta_archivo: str) -> list:
        """Método estático de apoyo para cargar JSON directamente por ruta."""
        servicio = ArchivoServicio(ruta_archivo)
        return servicio.cargar_datos()

    @staticmethod
    def guardar_json(ruta_archivo: str, datos: list) -> bool:
        """Método estático de apoyo para guardar JSON directamente por ruta."""
        servicio = ArchivoServicio(ruta_archivo)
        return servicio.guardar_datos(datos)
        