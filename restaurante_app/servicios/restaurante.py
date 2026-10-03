import os
from modelos.producto import Producto
from modelos.usuario import Usuario
from modelos.venta import Venta
from servicios.archivo_servicio import ArchivoServicio

class RestauranteServicio:
    def __init__(self, ruta_carpeta_datos: str):
        # 1. Crear un ArchivoServicio para cada archivo JSON
        self.archivo_productos = ArchivoServicio(os.path.join(ruta_carpeta_datos, "productos.json"))
        self.archivo_usuarios = ArchivoServicio(os.path.join(ruta_carpeta_datos, "usuarios.json"))
        self.archivo_ventas = ArchivoServicio(os.path.join(ruta_carpeta_datos, "ventas.json"))
        
        # 2. Cargar los datos (vienen como diccionarios desde el JSON)
        dict_productos = self.archivo_productos.cargar_datos()
        dict_usuarios = self.archivo_usuarios.cargar_datos()
        dict_ventas = self.archivo_ventas.cargar_datos()
        
        # 3. Convertir los diccionarios en objetos de forma segura (mapeo manual)
        self.productos = []
        if dict_productos:
            for p in dict_productos:
                if isinstance(p, dict):
                    # Mapeamos 'tipo_producto' a 'categoria' para evitar el TypeError
                    categoria_val = p.get('categoria') or p.get('tipo_producto', 'General')
                    prod = Producto(
                        codigo=p.get('codigo', ''),
                        nombre=p.get('nombre', ''),
                        precio=float(p.get('precio', 0.0)),
                        categoria=categoria_val
                    )
                    # Restaurar atributos extra como el stock si existen
                    if 'stock' in p:
                        prod.stock = int(p.get('stock', 0))
                    if 'tipo_producto' in p:
                        # Si tu sistema necesita explícitamente tipo_producto
                        setattr(prod, 'tipo_producto', p.get('tipo_producto'))
                        
                    self.productos.append(prod)
                else:
                    self.productos.append(p)
        self.usuarios = []
        if dict_usuarios:
            for u in dict_usuarios:
                if isinstance(u, dict):
                    # Adaptamos las claves del JSON a los parámetros requeridos por usuario.py
                    id_val = u.get('identificador') or u.get('identificacion') or u.get('id', '')
                    usr_val = u.get('usuario') or u.get('correo', '') # Si no hay 'usuario', usar correo
                    
                    usr = Usuario(
                        identificador=id_val,
                        nombre=u.get('nombre', ''),
                        usuario=usr_val,
                        contrasena=u.get('contrasena', '1234'),
                        rol=u.get('rol', 'Cliente') # Añadido para soportar el rol
                    )
                    
                    # Para mantener compatibilidad con métodos antiguos que buscan por 'identificacion'
                    if not hasattr(usr, 'identificacion'):
                        setattr(usr, 'identificacion', id_val)
                        
                    self.usuarios.append(usr)
                else:
                    self.usuarios.append(u)

        self.ventas = []
        if dict_ventas:
            for v in dict_ventas:
                if isinstance(v, dict):
                    # Manejo flexible de las claves del JSON para ventas
                    id_venta = v.get('id_venta') or v.get('codigo_venta', '')
                    id_usuario = v.get('identificacion_usuario') or v.get('id_usuario', '')
                    cod_producto = v.get('codigo_producto') or v.get('id_producto', '')
                    
                    venta = Venta(
                        id_venta=id_venta,
                        identificacion_usuario=id_usuario,
                        codigo_producto=cod_producto,
                        cantidad=int(v.get('cantidad', 1)),
                        total=float(v.get('total', 0.0)),
                        fecha=v.get('fecha', '')
                    )
                    self.ventas.append(venta)
                else:
                    self.ventas.append(v)
        
        # 4. Inicializar índices en memoria (Semana 12)
        self.productos_dict = {}
        self.usuarios_dict = {}
        self.ventas_por_usuario = {}
        
        self._reconstruir_indices()

    def guardar_todo(self) -> None:
        """Guarda las listas actuales en sus respectivos archivos JSON limpiando los atributos privados."""
        self.archivo_productos.guardar_datos([p.__dict__ for p in self.productos])
        
        # Limpiar guiones bajos de los atributos de usuario
        usuarios_limpios = []
        for u in self.usuarios:
            diccionario_limpio = {clave.lstrip('_'): valor for clave, valor in u.__dict__.items()}
            usuarios_limpios.append(diccionario_limpio)
            
        self.archivo_usuarios.guardar_datos(usuarios_limpios)
        self.archivo_ventas.guardar_datos([v.__dict__ for v in self.ventas])

    def _reconstruir_indices(self) -> None:
        """Reconstruye los índices en memoria a partir de las colecciones cargadas desde JSON."""
        self.productos_dict = {p.codigo: p for p in self.productos}
        self.usuarios_dict = {u.identificador: u for u in self.usuarios}
        
        self.ventas_por_usuario = {}
        for v in self.ventas:
            # CORRECCIÓN AQUÍ: Cambiar a identificacion_usuario
            if v.identificacion_usuario not in self.ventas_por_usuario:
                self.ventas_por_usuario[v.identificacion_usuario] = []
            self.ventas_por_usuario[v.identificacion_usuario].append(v)

    # --- MÉTODOS DE PRODUCTOS ---
    def registrar_producto(self, producto: Producto) -> bool:
        if producto.codigo in self.productos_dict:
            return False
        self.productos.append(producto)
        self.productos_dict[producto.codigo] = producto  # Sincronizar índice
        self.guardar_todo()  # Persistencia en JSON
        return True

    def buscar_producto(self, codigo: str) -> Producto | None:
        """Búsqueda eficiente usando el diccionario índice en O(1)."""
        return self.productos_dict.get(codigo)

    def actualizar_producto(self, codigo: str, nuevo_nombre: str, nuevo_precio: float, nueva_categoria: str) -> bool:
        producto = self.buscar_producto(codigo)
        if producto:
            producto.nombre = nuevo_nombre
            producto.precio = float(nuevo_precio)
            producto.categoria = nueva_categoria
            self.guardar_todo()  # Persistencia en JSON
            return True
        return False

    def eliminar_producto(self, codigo: str) -> bool:
        producto = self.buscar_producto(codigo)
        if producto:
            self.productos.remove(producto)
            del self.productos_dict[codigo]  # Sincronizar índice
            self.guardar_todo()  # Persistencia en JSON
            return True
        return False

    def obtener_todos_productos(self) -> list:
        return self.productos

    # --- MÉTODOS DE USUARIOS (CLIENTES) ---
    def registrar_usuario(self, usuario: Usuario) -> bool:
        if usuario.identificador in self.usuarios_dict:
            return False
        self.usuarios.append(usuario)
        self.usuarios_dict[usuario.identificador] = usuario  # Sincronizar índice
        self.guardar_todo()  # Persistencia en JSON
        return True

    def buscar_usuario(self, identificador: str) -> Usuario | None:
        """Búsqueda eficiente usando el diccionario índice en O(1)."""
        return self.usuarios_dict.get(identificador)

    def actualizar_usuario(self, identificador: str, nuevo_nombre: str, nuevo_usuario: str, nueva_contrasena: str, nuevo_rol: str) -> bool:
        usuario = self.buscar_usuario(identificador)
        if usuario:
            usuario.nombre = nuevo_nombre
            usuario.usuario = nuevo_usuario
            if nueva_contrasena:
                usuario.contrasena = nueva_contrasena
            usuario.rol = nuevo_rol
            self.guardar_todo()
            return True
        return False

    def eliminar_usuario(self, identificador: str) -> bool:
        usuario = self.buscar_usuario(identificador)
        if usuario:
            self.usuarios.remove(usuario)
            if identificador in self.usuarios_dict:
                del self.usuarios_dict[identificador]
            self.guardar_todo()
            return True
        return False

    def obtener_todos_usuarios(self) -> list:
        return self.usuarios

    # --- MÉTODOS DE VENTAS ---
    def vender_producto(self, identificador_usuario: str, codigo_producto: str, cantidad: int, fecha: str) -> tuple[bool, str]:
        if identificador_usuario not in self.usuarios_dict:
            return False, "Cliente no encontrado."

        producto = self.buscar_producto(codigo_producto)
        if not producto:
            return False, "Producto no encontrado."

        stock_actual = getattr(producto, 'stock', cantidad)
        if stock_actual < cantidad:
            return False, f"Stock insuficiente. Disponible: {stock_actual}"

        if hasattr(producto, 'stock'):
            producto.stock -= cantidad

        total = producto.precio * cantidad
        id_v = f"V{len(self.ventas) + 1:03d}"
        nueva_venta = Venta(id_v, identificador_usuario, codigo_producto, cantidad, total, fecha)
        
        self.ventas.append(nueva_venta)
        
        # Sincronizar índice auxiliar de ventas por usuario
        if identificador_usuario not in self.ventas_por_usuario:
            self.ventas_por_usuario[identificador_usuario] = []
        self.ventas_por_usuario[identificador_usuario].append(nueva_venta)
        
        # Guardar cambios en los archivos JSON
        self.guardar_todo()
        
        return True, f"Venta registrada. Total: ${total:.2f} (ID Venta: {id_v})"

    def obtener_todas_ventas(self) -> list:
        return self.ventas

    # --- CONSULTAS Y ESTRUCTURAS DE DATOS ---
    def obtener_historial_ventas_usuario(self, identificador_usuario: str) -> list:
        """Consulta eficiente de ventas por usuario consultando directamente el índice en memoria."""
        return self.ventas_por_usuario.get(identificador_usuario, [])

    def obtener_categorias_unicas(self) -> set:
        """Uso de set para extraer categorías únicas."""
        return set(getattr(p, 'categoria', getattr(p, 'tipo_producto', 'General')) for p in self.productos)
    
    # --- MÉTODOS DE AUTENTICACIÓN ---
    def validar_acceso(self, usuario: str, contrasena: str) -> Usuario | None:
        """Verifica las credenciales del usuario para iniciar sesión en LoginView."""
        for u in self.usuarios:
            # Compara el nombre de usuario (o correo/identificador) y la contraseña
            usr_nombre = getattr(u, 'usuario', getattr(u, 'identificador', ''))
            usr_clave = getattr(u, 'contrasena', '')
            
            if usr_nombre == usuario and usr_clave == contrasena:
                return u
        return None