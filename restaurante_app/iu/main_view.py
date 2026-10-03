import tkinter as tk
from pathlib import Path
from tkinter import messagebox, ttk
from modelos.producto import Producto
from modelos.usuario import Usuario  # Asegúrate de importar tu modelo Producto

class MainView(tk.Frame):
    def __init__(self, master, restaurante_servicio, usuario_actual, al_cerrar_sesion):
        super().__init__(master, bg="#f7fafc")
        # Actualizado de biblioteca_servicio a restaurante_servicio
        self.restaurante_servicio = restaurante_servicio
        self.usuario_actual = usuario_actual
        self.al_cerrar_sesion = al_cerrar_sesion

        self.contenido = None
        self.etiqueta_estado = None
        self.botones_menu = {}
        self.iconos = {}
        self.logo_sidebar = None

        # Variables para productos en lugar de libros
        self.producto_codigo_entry = None
        self.producto_nombre_entry = None
        self.producto_precio_entry = None
        self.producto_categoria_entry = None
        self.tabla_productos = None
        self.tabla_usuarios = None
        self.venta_usuario_combo = None
        self.venta_producto_combo = None
        self.venta_cantidad_entry = None
        self.venta_fecha_entry = None
        self.tabla_ventas = None

        self.definir_estilos()
        self.construir_interfaz()
        
        
    # -------------------------------------------------------------------------
    # Configuracion general: colores, estilos e iconos.
    # -------------------------------------------------------------------------
    def definir_estilos(self):
        self.color_fondo = "#f7fafc"
        self.color_panel = "#ffffff"
        self.color_encabezado = "#1f2a44"
        self.color_texto = "#243447"
        self.color_secundario = "#dbeafe"
        self.color_resaltado = "#2563eb"

        estilo = ttk.Style()
        estilo.theme_use("clam")
        estilo.configure(
            "MenuApp.TButton",
            background="#334155",
            foreground="#ffffff",
            font=("Arial", 10, "bold"),
            padding=(12, 10),
            borderwidth=0,
            anchor="w",
        )
        estilo.map("MenuApp.TButton", background=[("active", "#475569")])
        estilo.configure(
            "MenuActivo.TButton",
            background=self.color_resaltado,
            foreground="#ffffff",
            font=("Arial", 10, "bold"),
            padding=(12, 10),
            borderwidth=0,
            anchor="w",
        )
        estilo.map("MenuActivo.TButton", background=[("active", "#1d4ed8")])
        estilo.configure(
            "Secundario.TButton",
            background="#1f2a44",
            foreground="#ffffff",
            font=("Arial", 10, "bold"),
            padding=(10, 7),
            borderwidth=0,
        )
        estilo.map("Secundario.TButton", background=[("active", "#334155")])
        estilo.configure(
            "Accion.TButton",
            background=self.color_resaltado,
            foreground="#ffffff",
            font=("Arial", 10, "bold"),
            padding=(10, 7),
            borderwidth=0,
        )
        estilo.map("Accion.TButton", background=[("active", "#1d4ed8")])
        estilo.configure(
            "Eliminar.TButton",
            background="#e11d48",
            foreground="#ffffff",
            font=("Arial", 10, "bold"),
            padding=(10, 7),
            borderwidth=0,
        )
        estilo.map("Eliminar.TButton", background=[("active", "#be123c")])
        estilo.configure(
            "Treeview.Heading",
            background=self.color_secundario,
            foreground=self.color_encabezado,
            font=("Arial", 10, "bold"),
        )

    def cargar_icono(self, nombre_archivo):
        ruta_base = Path(__file__).resolve().parent.parent
        ruta_icono = ruta_base / "assets" / "icons" / nombre_archivo

        if not ruta_icono.exists():
            return None

        icono = tk.PhotoImage(file=str(ruta_icono))
        self.iconos[nombre_archivo] = icono
        return icono

    def crear_boton(self, contenedor, texto, comando, estilo, icono=None):
        imagen = self.cargar_icono(icono) if icono else None

        if imagen is not None:
            boton = ttk.Button(
                contenedor,
                text=texto,
                command=comando,
                style=estilo,
                image=imagen,
                compound="left",
            )
        else:
            boton = ttk.Button(
                contenedor,
                text=texto,
                command=comando,
                style=estilo,
            )

        return boton

    # -------------------------------------------------------------------------
    # Estructura principal: menu lateral + area de contenido.
    # -------------------------------------------------------------------------
    def construir_interfaz(self):
        frame_sidebar = tk.Frame(self, bg=self.color_encabezado, width=190, padx=16, pady=18)
        frame_sidebar.pack(side="left", fill="y")
        frame_sidebar.pack_propagate(False)

        tk.Label(
            frame_sidebar,
            text="RESTAURANTE",
            bg=self.color_encabezado,
            fg="#ffffff",
            font=("Arial", 16, "bold"),
        ).pack(anchor="w", pady=(0, 8))

        tk.Label(
            frame_sidebar,
            text=self.usuario_actual.nombre,
            bg=self.color_encabezado,
            fg="#dbeafe",
            font=("Arial", 10),
            wraplength=150,
            justify="left",
        ).pack(anchor="w", pady=(0, 24))

        self.crear_boton_menu(frame_sidebar, "Inicio", self.mostrar_inicio, "home.png")
        self.crear_boton_menu(frame_sidebar, "Usuarios", self.mostrar_usuarios, "users.png")
        self.crear_boton_menu(frame_sidebar, "Productos", self.mostrar_productos, "books.png") # Puedes cambiar el icono a products.png si lo tienes
        self.crear_boton_menu(frame_sidebar, "Ventas", self.mostrar_ventas, "ventas.png")
        
        tk.Frame(frame_sidebar, bg=self.color_encabezado).pack(fill="both", expand=True)

        self.crear_boton(
            frame_sidebar,
            "Cerrar sesion",
            self.cerrar_sesion,
            "Eliminar.TButton",
            "logout.png",
        ).pack(fill="x", pady=(16, 0))

        frame_principal = tk.Frame(self, bg=self.color_fondo)
        frame_principal.pack(side="left", fill="both", expand=True)

        self.contenido = tk.Frame(frame_principal, bg=self.color_fondo, padx=28, pady=24)
        self.contenido.pack(fill="both", expand=True)

        barra_estado = tk.Frame(frame_principal, bg=self.color_secundario, padx=18, pady=8)
        barra_estado.pack(fill="x", side="bottom")

        self.etiqueta_estado = tk.Label(
            barra_estado,
            bg=self.color_secundario,
            fg=self.color_texto,
            font=("Arial", 10),
        )
        self.etiqueta_estado.pack(side="left")

        self.mostrar_inicio()

    def crear_boton_menu(self, contenedor, texto, comando, icono):
        boton = self.crear_boton(contenedor, texto, comando, "MenuApp.TButton", icono)
        boton.pack(fill="x", pady=(0, 8))
        self.botones_menu[texto] = boton

    def marcar_seccion(self, seccion):
        for texto, boton in self.botones_menu.items():
            estilo = "MenuActivo.TButton" if texto == seccion else "MenuApp.TButton"
            boton.configure(style=estilo)

    def limpiar_contenido(self):
        assert self.contenido is not None

        for widget in self.contenido.winfo_children():
            widget.destroy()

    def actualizar_barra_estado(self):
        assert self.etiqueta_estado is not None
        
        # Obtenemos dinámicamente las cantidades actuales
        cantidad_productos = len(self.restaurante_servicio.obtener_todos_productos())
        cantidad_usuarios = len(self.restaurante_servicio.obtener_todos_usuarios())

        self.etiqueta_estado.config(
            text=(
                f"Productos: {cantidad_productos} | "
                f"Usuarios: {cantidad_usuarios} | "
                "Datos JSON locales"
            )
        )

    # -------------------------------------------------------------------------
    # Vista de inicio: resumen general del sistema.
    # -------------------------------------------------------------------------
    def mostrar_inicio(self):
        self.marcar_seccion("Inicio")
        self.limpiar_contenido()
        self.actualizar_barra_estado()

        assert self.contenido is not None

        tk.Label(
            self.contenido,
            text="Panel principal",
            bg=self.color_fondo,
            fg=self.color_encabezado,
            font=("Arial", 20, "bold"),
        ).pack(anchor="w", pady=(0, 8))

        tk.Label(
            self.contenido,
            text="Consulte usuarios y gestione productos desde el menú lateral.",
            bg=self.color_fondo,
            fg=self.color_texto,
            font=("Arial", 12),
        ).pack(anchor="w", pady=(0, 22))

        resumen = tk.Frame(self.contenido, bg=self.color_fondo)
        resumen.pack(fill="x")
        
        cantidad_usuarios = len(self.restaurante_servicio.obtener_todos_usuarios())
        cantidad_productos = len(self.restaurante_servicio.obtener_todos_productos())
        
        self.crear_tarjeta_resumen(resumen, "Usuarios registrados", cantidad_usuarios)
        self.crear_tarjeta_resumen(resumen, "Productos registrados", cantidad_productos)

    def crear_tarjeta_resumen(self, contenedor, titulo, valor):
        tarjeta = tk.Frame(contenedor, bg=self.color_panel, padx=18, pady=16)
        tarjeta.pack(side="left", fill="x", expand=True, padx=(0, 14))

        tk.Label(
            tarjeta,
            text=titulo,
            bg=self.color_panel,
            fg=self.color_texto,
            font=("Arial", 10, "bold"),
        ).pack(anchor="w")
        tk.Label(
            tarjeta,
            text=str(valor),
            bg=self.color_panel,
            fg=self.color_resaltado,
            font=("Arial", 24, "bold"),
        ).pack(anchor="w", pady=(8, 0))

    # -------------------------------------------------------------------------
    # Vista de usuarios: Gestión completa (CRUD) con roles y Treeview.
    # -------------------------------------------------------------------------
    def mostrar_usuarios(self):
        self.marcar_seccion("Usuarios")
        self.limpiar_contenido()

        assert self.contenido is not None

        self.crear_titulo_seccion("Gestión de Usuarios")

        cuerpo = tk.Frame(self.contenido, bg=self.color_fondo)
        cuerpo.pack(fill="both", expand=True)
        cuerpo.grid_columnconfigure(1, weight=1)
        cuerpo.grid_rowconfigure(0, weight=1)

        # Formulario de Usuario
        formulario = tk.LabelFrame(
            cuerpo,
            text="Datos del usuario",
            bg=self.color_panel,
            fg=self.color_encabezado,
            font=("Arial", 10, "bold"),
            padx=14,
            pady=14,
        )
        formulario.grid(row=0, column=0, sticky="n", padx=(0, 18))

        self.usuario_id_entry = self.crear_campo(formulario, "Identificador", 0)
        self.usuario_nombre_entry = self.crear_campo(formulario, "Nombre", 1)
        self.usuario_login_entry = self.crear_campo(formulario, "Usuario (Login)", 2)
        self.usuario_pass_entry = self.crear_campo(formulario, "Contraseña", 3)
        self.usuario_pass_entry.config(show="*")

        # Campo Rol (Combobox)
        tk.Label(
            formulario,
            text="Rol",
            bg=self.color_panel,
            fg=self.color_texto,
            font=("Arial", 10, "bold"),
        ).grid(row=4, column=0, sticky="w", pady=(0, 8), padx=(0, 10))
        
        self.usuario_rol_combo = ttk.Combobox(formulario, width=26, state="readonly")
        self.usuario_rol_combo['values'] = ["Cliente", "Empleado", "Administrador"]
        self.usuario_rol_combo.set("Cliente")
        self.usuario_rol_combo.grid(row=4, column=1, sticky="ew", pady=(0, 8))
        self.usuario_pass_entry.bind("<Return>", lambda event: self.registrar_usuario())
        self.winfo_toplevel().bind("<Escape>", lambda event: self.limpiar_formulario_usuario())
        self.usuario_rol_combo.bind("<<ComboboxSelected>>", self.al_seleccionar_rol)

        acciones = tk.Frame(formulario, bg=self.color_panel)
        acciones.grid(row=5, column=0, columnspan=2, sticky="ew", pady=(12, 0))

        botones = (
            ("Registrar", self.registrar_usuario, "Accion.TButton", "add.png"),
            ("Cargar por ID", self.cargar_usuario_en_formulario, "Secundario.TButton", "search.png"),
            ("Actualizar", self.actualizar_usuario, "Accion.TButton", "edit.png"),
            ("Eliminar", self.eliminar_usuario, "Eliminar.TButton", "delete.png"),
            ("Limpiar", self.limpiar_formulario_usuario, "Secundario.TButton", "clean.png"),
        )

        for texto, comando, estilo, icono in botones:
            self.crear_boton(acciones, texto, comando, estilo, icono).pack(fill="x", pady=(0, 7))

        listado = self.crear_listado(cuerpo, "Usuarios registrados", usar_grid=True)
        self.tabla_usuarios = self.crear_tabla(
            listado,
            ("identificador", "nombre", "usuario", "rol"),
            ("Identificador", "Nombre", "Usuario", "Rol"),
        )
        
        # Enlazar selección en el Treeview para autocompletar el formulario
        self.tabla_usuarios.bind("<<TreeviewSelect>>", self.seleccionar_usuario_tabla)
        self.refrescar_usuarios()

    def obtener_datos_usuario(self):
        return (
            self.usuario_id_entry.get().strip(),
            self.usuario_nombre_entry.get().strip(),
            self.usuario_login_entry.get().strip(),
            self.usuario_pass_entry.get().strip(),
            self.usuario_rol_combo.get()
        )

    def registrar_usuario(self):
        try:
            identificador, nombre, usuario, contrasena, rol = self.obtener_datos_usuario()
            if not identificador or not nombre or not usuario or not contrasena:
                messagebox.showerror("Error", "Todos los campos obligatorios deben estar llenos.")
                return

            nuevo_usuario = Usuario(
                identificador=identificador, 
                nombre=nombre, 
                usuario=usuario, 
                contrasena=contrasena, 
                rol=rol
            )
            exito = self.restaurante_servicio.registrar_usuario(nuevo_usuario)
            
            if exito:
                self.limpiar_formulario_usuario()
                self.refrescar_usuarios()
                messagebox.showinfo("Usuarios", "Usuario registrado correctamente.")
            else:
                messagebox.showwarning("Usuarios", "Ya existe un usuario con ese identificador.")
        except ValueError as e:
            messagebox.showerror("Error", str(e))

    def cargar_usuario_en_formulario(self):
        identificador = self.usuario_id_entry.get().strip()
        usuario = self.restaurante_servicio.buscar_usuario(identificador)
        if usuario is None:
            messagebox.showerror("Usuarios", "No existe un usuario con ese identificador.")
            return

        self.limpiar_formulario_usuario()
        self.usuario_id_entry.insert(0, usuario.identificador)
        self.usuario_nombre_entry.insert(0, usuario.nombre)
        self.usuario_login_entry.insert(0, usuario.usuario)
        self.usuario_pass_entry.insert(0, usuario.contrasena)
        self.usuario_rol_combo.set(getattr(usuario, 'rol', 'Cliente'))

    def seleccionar_usuario_tabla(self, event):
        seleccion = self.tabla_usuarios.selection()
        if not seleccion:
            return
        valores = self.tabla_usuarios.item(seleccion[0], "values")
        if valores:
            self.limpiar_formulario_usuario()
            self.usuario_id_entry.insert(0, valores[0])
            self.usuario_nombre_entry.insert(0, valores[1])
            self.usuario_login_entry.insert(0, valores[2])
            self.usuario_rol_combo.set(valores[3])
            
            usr = self.restaurante_servicio.buscar_usuario(valores[0])
            if usr:
                self.usuario_pass_entry.insert(0, usr.contrasena)

    def actualizar_usuario(self):
        try:
            identificador, nombre, usuario, contrasena, rol = self.obtener_datos_usuario()
            exito = self.restaurante_servicio.actualizar_usuario(identificador, nombre, usuario, contrasena, rol)
            
            if exito:
                self.refrescar_usuarios()
                messagebox.showinfo("Usuarios", "Usuario actualizado correctamente.")
            else:
                messagebox.showwarning("Usuarios", "No se encontró el usuario a actualizar.")
        except ValueError as e:
            messagebox.showerror("Error", str(e))

    def eliminar_usuario(self):
        identificador = self.usuario_id_entry.get().strip()
        if not identificador:
            messagebox.showwarning("Usuarios", "Ingrese o seleccione el identificador del usuario a eliminar.")
            return

        confirmacion = messagebox.askyesno("Confirmar eliminación", f"¿Está seguro de eliminar al usuario {identificador}?")
        if confirmacion:
            exito = self.restaurante_servicio.eliminar_usuario(identificador)
            if exito:
                self.limpiar_formulario_usuario()
                self.refrescar_usuarios()
                messagebox.showinfo("Usuarios", "Usuario eliminado correctamente.")
            else:
                messagebox.showwarning("Usuarios", "No se encontró el usuario a eliminar.")

    def limpiar_formulario_usuario(self):
        for entrada in (self.usuario_id_entry, self.usuario_nombre_entry, 
                        self.usuario_login_entry, self.usuario_pass_entry):
            if entrada:
                entrada.delete(0, tk.END)
        if self.usuario_rol_combo:
            self.usuario_rol_combo.set("Cliente")

    def refrescar_usuarios(self):
        assert self.tabla_usuarios is not None

        self.limpiar_tabla(self.tabla_usuarios)
        for usuario in self.restaurante_servicio.obtener_todos_usuarios():
            id_val = getattr(usuario, 'identificador', getattr(usuario, 'identificacion', ''))
            rol_val = getattr(usuario, 'rol', 'Cliente')
            self.tabla_usuarios.insert(
                "",
                tk.END,
                values=(id_val, usuario.nombre, usuario.usuario, rol_val),
            )

        self.actualizar_barra_estado()

    # -------------------------------------------------------------------------
    # Vista de productos: formulario + tabla + CRUD basico por botones.
    # -------------------------------------------------------------------------
    def mostrar_productos(self):
        self.marcar_seccion("Productos")
        self.limpiar_contenido()

        assert self.contenido is not None

        self.crear_titulo_seccion("Gestión de productos")

        cuerpo = tk.Frame(self.contenido, bg=self.color_fondo)
        cuerpo.pack(fill="both", expand=True)
        cuerpo.grid_columnconfigure(1, weight=1)
        cuerpo.grid_rowconfigure(0, weight=1)

        formulario = tk.LabelFrame(
            cuerpo,
            text="Datos del producto",
            bg=self.color_panel,
            fg=self.color_encabezado,
            font=("Arial", 10, "bold"),
            padx=14,
            pady=14,
        )
        formulario.grid(row=0, column=0, sticky="n", padx=(0, 18))

        self.producto_codigo_entry = self.crear_campo(formulario, "Código", 0)
        self.producto_nombre_entry = self.crear_campo(formulario, "Nombre", 1)
        self.producto_precio_entry = self.crear_campo(formulario, "Precio ($)", 2)
        self.producto_categoria_entry = self.crear_campo(formulario, "Categoría", 3)

        acciones = tk.Frame(formulario, bg=self.color_panel)
        acciones.grid(row=4, column=0, columnspan=2, sticky="ew", pady=(12, 0))

        botones = (
            ("Registrar", self.registrar_producto, "Accion.TButton", "add.png"),
            ("Cargar por código", self.cargar_producto_en_formulario, "Secundario.TButton", "search.png"),
            ("Actualizar", self.actualizar_producto, "Accion.TButton", "edit.png"),
            ("Eliminar", self.eliminar_producto, "Eliminar.TButton", "delete.png"),
            ("Limpiar", self.limpiar_formulario_producto, "Secundario.TButton", "clean.png"),
        )

        for texto, comando, estilo, icono in botones:
            self.crear_boton(acciones, texto, comando, estilo, icono).pack(fill="x", pady=(0, 7))

        listado = self.crear_listado(cuerpo, "Productos registrados", usar_grid=True)
        self.tabla_productos = self.crear_tabla(
            listado,
            ("codigo", "nombre", "precio", "categoria"),
            ("Código", "Nombre", "Precio", "Categoría"),
        )
        self.refrescar_productos()

    def obtener_datos_producto(self):
        assert self.producto_codigo_entry is not None
        assert self.producto_nombre_entry is not None
        assert self.producto_precio_entry is not None
        assert self.producto_categoria_entry is not None

        return (
            self.producto_codigo_entry.get(),
            self.producto_nombre_entry.get(),
            self.producto_precio_entry.get(),
            self.producto_categoria_entry.get()
        )

    def registrar_producto(self):
        try:
            codigo, nombre, precio, categoria = self.obtener_datos_producto()
            nuevo_producto = Producto(codigo=codigo, nombre=nombre, precio=float(precio), categoria=categoria)
            
            exito = self.restaurante_servicio.registrar_producto(nuevo_producto)
            if exito:
                self.limpiar_formulario_producto()
                self.refrescar_productos()
                messagebox.showinfo("Productos", "Producto registrado correctamente.")
            else:
                messagebox.showwarning("Productos", "Ya existe un producto con ese código.")
        except ValueError:
            messagebox.showerror("Error", "Asegúrese de llenar todos los campos y que el precio sea numérico.")

    def cargar_producto_en_formulario(self):
        assert self.producto_codigo_entry is not None
        codigo = self.producto_codigo_entry.get()
        
        producto = self.restaurante_servicio.buscar_producto(codigo)
        if producto is None:
            messagebox.showerror("Productos", "No existe un producto con ese código.")
            return

        self.limpiar_formulario_producto()
        self.producto_codigo_entry.insert(0, producto.codigo)
        self.producto_nombre_entry.insert(0, producto.nombre)
        self.producto_precio_entry.insert(0, str(producto.precio))
        
        # Maneja tanto atributo 'categoria' como 'tipo_producto'
        cat_val = getattr(producto, 'categoria', getattr(producto, 'tipo_producto', ''))
        self.producto_categoria_entry.insert(0, cat_val)

    def actualizar_producto(self):
        try:
            codigo, nombre, precio, categoria = self.obtener_datos_producto()
            exito = self.restaurante_servicio.actualizar_producto(codigo, nombre, float(precio), categoria)
            
            if exito:
                self.refrescar_productos()
                messagebox.showinfo("Productos", "Producto actualizado correctamente.")
            else:
                messagebox.showwarning("Productos", "No se encontró el producto a actualizar.")
        except ValueError:
            messagebox.showerror("Error", "El precio debe ser un número válido.")

    def eliminar_producto(self):
        assert self.producto_codigo_entry is not None
        codigo = self.producto_codigo_entry.get()

        exito = self.restaurante_servicio.eliminar_producto(codigo)
        if exito:
            self.limpiar_formulario_producto()
            self.refrescar_productos()
            messagebox.showinfo("Productos", "Producto eliminado correctamente.")
        else:
            messagebox.showwarning("Productos", "No se encontró el producto a eliminar.")

    def limpiar_formulario_producto(self):
        for entrada in (self.producto_codigo_entry, self.producto_nombre_entry, 
                        self.producto_precio_entry, self.producto_categoria_entry):
            assert entrada is not None
            entrada.delete(0, tk.END)

    def refrescar_productos(self):
        assert self.tabla_productos is not None

        self.limpiar_tabla(self.tabla_productos)
        for prod in self.restaurante_servicio.obtener_todos_productos():
            cat_val = getattr(prod, 'categoria', getattr(prod, 'tipo_producto', ''))
            self.tabla_productos.insert("", tk.END, values=(prod.codigo, prod.nombre, f"${prod.precio:.2f}", cat_val))

        self.actualizar_barra_estado()
    
# -------------------------------------------------------------------------
    # Vista de Ventas: Formulario con Combobox + Tabla Treeview
    # -------------------------------------------------------------------------
    def mostrar_ventas(self):
        self.marcar_seccion("Ventas")
        self.limpiar_contenido()

        self.crear_titulo_seccion("Gestión de Ventas")

        cuerpo = tk.Frame(self.contenido, bg=self.color_fondo)
        cuerpo.pack(fill="both", expand=True)
        cuerpo.grid_columnconfigure(1, weight=1)
        cuerpo.grid_rowconfigure(0, weight=1)

        # Formulario
        formulario = tk.LabelFrame(cuerpo, text="Registrar Nueva Venta", bg=self.color_panel, fg=self.color_encabezado, font=("Arial", 10, "bold"), padx=14, pady=14)
        formulario.grid(row=0, column=0, sticky="n", padx=(0, 18))

        # Combobox para Usuarios
        tk.Label(formulario, text="Usuario", bg=self.color_panel, fg=self.color_texto, font=("Arial", 10, "bold")).grid(row=0, column=0, sticky="w", pady=(0, 8), padx=(0, 10))
        self.venta_usuario_combo = ttk.Combobox(formulario, width=26, state="readonly")
        lista_usuarios = [f"[{getattr(u, 'identificador', getattr(u, 'identificacion', ''))}] {u.nombre}" for u in self.restaurante_servicio.obtener_todos_usuarios()]
        self.venta_usuario_combo['values'] = lista_usuarios
        self.venta_usuario_combo.grid(row=0, column=1, sticky="ew", pady=(0, 8))

        # Combobox para Productos
        tk.Label(formulario, text="Producto", bg=self.color_panel, fg=self.color_texto, font=("Arial", 10, "bold")).grid(row=1, column=0, sticky="w", pady=(0, 8), padx=(0, 10))
        self.venta_producto_combo = ttk.Combobox(formulario, width=26, state="readonly")
        lista_productos = [f"[{p.codigo}] {p.nombre} - ${p.precio}" for p in self.restaurante_servicio.obtener_todos_productos()]
        self.venta_producto_combo['values'] = lista_productos
        self.venta_producto_combo.grid(row=1, column=1, sticky="ew", pady=(0, 8))

        self.venta_cantidad_entry = self.crear_campo(formulario, "Cantidad", 2)
        self.venta_fecha_entry = self.crear_campo(formulario, "Fecha (DD/MM/AAAA)", 3)

        # Botón de registro
        acciones = tk.Frame(formulario, bg=self.color_panel)
        acciones.grid(row=4, column=0, columnspan=2, sticky="ew", pady=(12, 0))
        self.crear_boton(acciones, "Registrar venta", self.registrar_venta, "Accion.TButton", "venta.png").pack(fill="x", pady=(0, 7))

        # Treeview de ventas
        listado = self.crear_listado(cuerpo, "Historial de Ventas", usar_grid=True)
        self.tabla_ventas = self.crear_tabla(listado, ("id", "usuario", "producto", "cantidad", "total", "fecha"), ("ID", "ID Usuario", "Cód. Producto", "Cant.", "Total", "Fecha"))
        self.refrescar_ventas()

    def registrar_venta(self):
        seleccion_usuario = self.venta_usuario_combo.get()
        seleccion_producto = self.venta_producto_combo.get()
        cantidad_str = self.venta_cantidad_entry.get()
        fecha = self.venta_fecha_entry.get()

        if not seleccion_usuario or not seleccion_producto or not cantidad_str or not fecha:
            messagebox.showerror("Error", "Todos los campos son obligatorios.")
            return

        try:
            cantidad = int(cantidad_str)
            # Extraer el ID de entre los corchetes "[001] Nombre" -> "001"
            id_usuario = seleccion_usuario.split("]")[0].replace("[", "")
            cod_producto = seleccion_producto.split("]")[0].replace("[", "")

            exito, mensaje = self.restaurante_servicio.vender_producto(id_usuario, cod_producto, cantidad, fecha)

            if exito:
                messagebox.showinfo("Venta Exitosa", mensaje)
                self.venta_cantidad_entry.delete(0, tk.END)
                self.venta_fecha_entry.delete(0, tk.END)
                self.venta_usuario_combo.set('')
                self.venta_producto_combo.set('')
                self.refrescar_ventas()
            else:
                messagebox.showwarning("Error en Venta", mensaje)
                
        except ValueError:
            messagebox.showerror("Error", "La cantidad debe ser un número entero.")

    def refrescar_ventas(self):
        if self.tabla_ventas:
            self.limpiar_tabla(self.tabla_ventas)
            for venta in self.restaurante_servicio.obtener_todas_ventas():
                self.tabla_ventas.insert("", tk.END, values=(venta.id_venta, venta.identificacion_usuario, venta.codigo_producto, venta.cantidad, f"${venta.total:.2f}", venta.fecha))

    # -------------------------------------------------------------------------
    # Utilidades de interfaz compartidas por las vistas.
    # -------------------------------------------------------------------------
    def crear_titulo_seccion(self, texto):
        assert self.contenido is not None

        tk.Label(
            self.contenido,
            text=texto,
            bg=self.color_fondo,
            fg=self.color_encabezado,
            font=("Arial", 20, "bold"),
        ).pack(anchor="w", pady=(0, 16))

    def crear_campo(self, contenedor, etiqueta, fila):
        tk.Label(
            contenedor,
            text=etiqueta,
            bg=self.color_panel,
            fg=self.color_texto,
            font=("Arial", 10, "bold"),
        ).grid(row=fila, column=0, sticky="w", pady=(0, 8), padx=(0, 10))

        entrada = tk.Entry(contenedor, width=28, font=("Arial", 10))
        entrada.grid(row=fila, column=1, sticky="ew", pady=(0, 8))
        return entrada

    def crear_listado(self, contenedor, titulo, usar_grid=False):
        listado = tk.LabelFrame(
            contenedor,
            text=titulo,
            bg=self.color_panel,
            fg=self.color_encabezado,
            font=("Arial", 10, "bold"),
            padx=12,
            pady=12,
        )

        if usar_grid:
            listado.grid(row=0, column=1, sticky="nsew")
        else:
            listado.pack(fill="both", expand=True)

        return listado

    def crear_tabla(self, contenedor, columnas, encabezados):
        frame_tabla = tk.Frame(contenedor, bg=self.color_panel)
        frame_tabla.pack(fill="both", expand=True)

        tabla = ttk.Treeview(frame_tabla, columns=columnas, show="headings", height=12)
        barra = ttk.Scrollbar(frame_tabla, orient="vertical", command=tabla.yview)
        tabla.configure(yscrollcommand=barra.set)

        for columna, encabezado in zip(columnas, encabezados):
            tabla.heading(columna, text=encabezado)
            tabla.column(columna, width=150, anchor="w")

        tabla.pack(side="left", fill="both", expand=True)
        barra.pack(side="right", fill="y")
        return tabla

    def limpiar_tabla(self, tabla):
        for item in tabla.get_children():
            tabla.delete(item)

    def cerrar_sesion(self):
        self.al_cerrar_sesion()
    
    def al_seleccionar_rol(self, event):
        rol_seleccionado = self.usuario_rol_combo.get()
        if self.etiqueta_estado:
            self.etiqueta_estado.config(text=f"Rol seleccionado: {rol_seleccionado}")