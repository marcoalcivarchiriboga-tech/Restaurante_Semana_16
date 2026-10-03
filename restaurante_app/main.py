import tkinter as tk
from pathlib import Path

# Eliminamos la importacion de ArchivoServicio, ya no se usa aquí.
from servicios.restaurante import RestauranteServicio
from iu.login_view import LoginView
from iu.main_view import MainView

class AplicacionRestaurante:
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("Restaurante - Tkinter")
        self.root.geometry("920x560")
        self.root.minsize(780, 500)
        self.icono_app = None

        # Prepara los servicios que usaran las vistas.
        ruta_base = Path(__file__).resolve().parent
        self.configurar_icono_ventana(ruta_base)
        
        # CORRECCIÓN AQUÍ: Pasamos la ruta de la carpeta "datos" como texto (str)
        ruta_datos = str(ruta_base / "datos")
        self.restaurante_servicio = RestauranteServicio(ruta_datos)

        self.vista_actual = None
        self.mostrar_login()

    def configurar_icono_ventana(self, ruta_base):
        # Usa un PNG pequeno como icono de la ventana.
        ruta_icono = ruta_base / "assets" / "logo" / "icono.png"
        if not ruta_icono.exists():
            return

        try:
            self.icono_app = tk.PhotoImage(file=str(ruta_icono))
            self.root.iconphoto(True, self.icono_app)
        except tk.TclError:
            pass

    def cambiar_vista(self, nueva_vista):
        # Reemplaza la vista actual dentro de la misma ventana.
        if self.vista_actual is not None:
            self.vista_actual.destroy()

        self.vista_actual = nueva_vista
        self.vista_actual.pack(fill="both", expand=True)

    def mostrar_login(self):
        # Muestra la primera pantalla de la aplicacion.
        vista = LoginView(
            self.root,
            self.restaurante_servicio,
            self.mostrar_interfaz_principal,
        )
        self.cambiar_vista(vista)

    def mostrar_interfaz_principal(self, usuario_actual):
        # Abre la interfaz principal despues de un acceso correcto.
        vista = MainView(
            self.root,
            self.restaurante_servicio,
            usuario_actual,
            self.mostrar_login,
        )
        self.cambiar_vista(vista)

    def ejecutar(self):
        self.root.mainloop()

if __name__ == "__main__":
    app = AplicacionRestaurante()
    app.ejecutar()