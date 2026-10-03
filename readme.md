
# Sistema de Gestión para Restaurante (`restaurante_app`)

Aplicación desarrollada en **Python** orientada a consola, diseñada bajo los paradigmas de la **Programación Orientada a Objetos (POO)** y los principios **SOLID**. El sistema permite administrar de forma eficiente el catálogo de productos del restaurante, la gestión de clientes recurrentes y el control integral de ventas con descuento de inventario, optimizando el rendimiento mediante índices en memoria.

## Información del Estudiante
* **Nombre Completo:** Marco Julio Alcívar Chiriboga
* **Asignatura:** Programación Orientada a Objetos (Semana 12)
* **Institución:** Universidad Estatal Amazónica

## Arquitectura y Estructura Modular

El proyecto se encuentra estrictamente modularizado para separar las responsabilidades de datos, lógica de negocio e interacción con el usuario:

El proyecto se encuentra estrictamente modularizado para separar las responsabilidades de datos, lógica de negocio e interacción con el usuario mediante interfaz gráfica (GUI):

```text
restaurante_app/
│
├── assets/
│   ├── icons/
│   │   ├── home.png           # Icono para la vista general o inicio
│   │   ├── users.png          # Icono para la sección de clientes
│   │   ├── productos.png      # Icono para el catálogo de productos
│   │   ├── ventas.png         # Icono para el registro de ventas
│   │   ├── logout.png         # Icono para el botón de cerrar sesión
│   │   ├── add.png            # Icono para acciones de registro/agregar
│   │   ├── edit.png           # Icono para acciones de edición/actualización
│   │   ├── delete.png         # Icono para acciones de eliminación
│   │   └── clean.png          # Icono para limpiar formularios
│   └── logo/
│       ├── logo.png           # Identidad visual principal (Login y menú lateral)
│       └── icono.png          # Icono oficial para la ventana principal de Tkinter
│
├── datos/
│   ├── productos.json         # Persistencia de productos (JSON)
│   ├── usuarios.json          # Persistencia de clientes/usuarios (JSON)
│   └── ventas.json            # Persistencia de registros de ventas (JSON)
│
├── modelos/
│   ├── __init__.py            # Inicializador del paquete de modelos
│   ├── producto.py            # Clase base para la gestión de productos generales
│   ├── bebida.py              # Clase derivada con herencia y polimorfismo
│   ├── usuario.py             # Clase independiente para los clientes/usuarios
│   └── venta.py               # Clase para representar transacciones de venta
│
├── servicios/
│   ├── __init__.py            # Inicializador del paquete de servicios
│   ├── archivo_servicio.py    # Servicio responsable de la lectura y escritura de JSON
│   └── restaurante.py         # Capa de colecciones, índices en memoria y reglas de negocio
│
├── iu/                        # Capa de Interfaz de Usuario Gráfica (Tkinter GUI)
│   ├── __init__.py            # Inicializador del paquete visual
│   ├── login_view.py          # Frame para control de acceso, autenticación y logo
│   ├── main_view.py           # Frame principal estructurado con pestañas (Notebook) e iconos
│   └── utils.py               # Función auxiliar de carga segura de recursos gráficos
│
├── main.py                    # Controlador principal de la aplicación con icono de ventana
└── README.md                  # Documentación oficial y explicación de la arquitectura

Componentes y Principios Aplicados
1. Modelos de Datos (modelos/)
Producto (producto.py): Define la estructura base de los artículos del restaurante. Contiene atributos comunes como código, nombre, categoría y precio, además del método fundamental mostrar_informacion().

Bebida (bebida.py): Aplica herencia al extender de la clase Producto. Incorpora un atributo propio (tipo_envase) y aplica polimorfismo al sobrescribir mostrar_informacion() para complementar los datos heredados sin alterar la lógica general (Principio de Sustitución de Liskov).

Cliente (cliente.py): Modela la información personal del cliente (identificación, nombre y correo) manteniendo total independencia de la jerarquía de productos (Principio de Responsabilidad Única).

2. Capa de Servicios (servicios/)
Restaurante (restaurante.py): Actúa como el motor logístico de la aplicación. Administra una colección unificada de productos (donde conviven objetos tipo Producto y Bebida de manera transparente) y una lista independiente de clientes.

Incluye validaciones robustas para evitar duplicidad de códigos en productos/bebidas e identificaciones repetidas en los clientes.

3. Interfaz de Usuario (main.py)
Gestiona un bucle interactivo basado en consola impulsado por opciones numéricas (input()). Se encarga exclusivamente de capturar datos, instanciar objetos, invocar los métodos del servicio Restaurante y presentar los resultados formateados en pantalla.

Principios SOLID Implementados
S (Responsabilidad Única): Cada archivo y clase posee un propósito específico (las clases de modelos gestionan sus propios datos, el servicio administra colecciones y main.py maneja la interfaz).

O (Abierto/Cerrado): La clase Bebida amplía el comportamiento del sistema mediante herencia y polimorfismo sin necesidad de reescribir la lógica central del servicio.

L (Sustitución de Liskov): Los objetos de la clase derivada (Bebida) pueden utilizarse indistintamente en la colección de productos genéricos sin generar errores ni requerir validaciones repetitivas de tipo (isinstance).

# Semana 9
## Aplicacion de Estructuras de Datos 

| Estructura | Tipo en Python | Aplicacion en el Proyecto |
| **Listas** | list | Utilizadas para administrar las colecciones dinámicas de productos (`self.productos) y clientes (`self.clientes`). permiten realizar operaciones de registro, busqueda, actualizacion, eliminacion y listado.|
|**Tuplas** | `tuple` | Utilizadas para manejar informacion inmutable que debe mantenerse estable durante la ejecucion, como la tupla con la información general del negocio (nombre, RUC, direccion, teléfono) y las opciones fijas del menú.
| **Diccionarios** | `dict` | Utilizados para establecer relaciones de clave $\rigtarrow$ valor. Se aplica para mapear las opciones numéricas del menú interactivo con sus respectivas funciones de la interfaz de usuario. |
| **Conjuntos** | `set` | Utilizados para gestionar colecciones de elementos unicos sin duplicados. Se aplican en la funcion de obtencion de categorias para extraer y presentar unicamente las categorias unicas de los productosregistrados. | 

# Semana 10: Persistencia de Datos y Manejo de Excepciones

En esta etapa de desarrollo, el sistema evoluciona para incluir almacenamiento persistente mediante archivos JSON. Esto garantiza que el catálogo de productos y bebidas del restaurante "El Buen Sabor" no se pierda al cerrar la aplicación. Además, se incorpora un robusto manejo de excepciones para prevenir cierres inesperados.

### Nuevos Componentes y Modificaciones
* **`datos/productos.json`**: Archivo físico utilizado como medio de almacenamiento de la colección.
* **`servicios/archivo_servicio.py`**: Nuevo módulo de servicio dedicado exclusivamente a la lectura (`json.load()`) y escritura (`json.dump()`) del archivo. Cumple con el Principio de Responsabilidad Única al separar la persistencia de la lógica de negocio.
* **`modelos/producto.py` y `bebida.py`**: Se integró el método `a_diccionario()` para serializar los objetos a una estructura compatible con JSON, manteniendo intactos los atributos heredados (como el `tipo_de_envase`).
* **`main.py` (Actualización de Interfaz)**:
  * Se implementó una **tupla constante** (`INFO_RESTAURANTE`) que actúa como encabezado inmutable en la interfaz de consola, mostrando el nombre, RUC, dirección y teléfono.
  * Se expandió el menú a 12 opciones utilizando un despachador dinámico basado en un diccionario y funciones `lambda`, optimizando el flujo de ejecución sin abusar de condicionales `if/elif`.

### Manejo de Excepciones Implementado
El acceso a archivos y la captura de datos están protegidos rigurosamente con bloques `try-except`:
* **`FileNotFoundError`**: Permite que la aplicación inicie de manera controlada con una colección vacía si el archivo `productos.json` todavía no existe.
* **`json.JSONDecodeError`**: Protege la inicialización en caso de que el archivo exista pero su formato interno esté corrupto o no sea un JSON válido.
* **`PermissionError`**: Advierte al usuario de forma amigable si el sistema operativo deniega los permisos de lectura o escritura en el directorio `datos/`.
* **`KeyError`**: Mantiene la estabilidad al reconstruir los objetos durante la fase de carga si algún registro antiguo no posee las claves esperadas.
* **`ValueError`**: Empleado en los formularios de registro de la consola (ej. al pedir el precio) para impedir que el ingreso de letras o caracteres inválidos detenga la aplicación abruptamente.

### Flujo de Ejecución (Carga y Guardado)
1. **Inicio y Carga:** Al iniciar `main.py`, se crea el `ArchivoServicio` y se intenta leer los datos. Cada registro válido recuperado del JSON se utiliza para instanciar nuevamente objetos `Producto` o `Bebida`, los cuales se cargan en la memoria del `RestauranteServicio`.
2. **Operación en Memoria:** El sistema interactúa con el usuario trabajando netamente con los objetos en memoria para garantizar un alto rendimiento.
3. **Guardado Automático:** Inmediatamente después de que el usuario registra, actualiza o elimina un producto con éxito, `main.py` solicita la colección actualizada, los objetos se convierten a lista de diccionarios, y el servicio sobrescribe el archivo físico, manteniendo la información siempre sincronizada.

SEMANA 11

En esta etapa, el sistema consolida la interacción entre múltiples entidades del dominio (Usuarios - Préstamos/Ventas - Productos) y perfecciona la persistencia bidireccional en formato JSON.

Nuevas Funcionalidades e Integraciones
Persistencia Multi-Archivo: Se integró el guardado y carga automática para 4 colecciones independientes (productos.json, usuarios.json, prestamos.json y ventas.json).

Deserialización Inteligente (from_dict): Métodos estáticos implementados en las clases de modelo (Producto, Bebida, Usuario, Prestamo, Venta) que permiten reconstruir las instancias originales a partir de los diccionarios cargados desde JSON.

Control de Inventario y Tipos de Uso: Verificación de stock disponible antes de procesar préstamos o ventas, descontando automáticamente las unidades al confirmar transacciones.

Flujo de Ejecución Integrado
Inicio y Carga Automatizada: main.py inicializa las instancias de ArchivoServicio. Carga los JSON existentes y reconstruye las listas de objetos Producto, Bebida, Usuario, Prestamo y Venta en la memoria de RestauranteServicio.

Operación en Memoria y Validación: El usuario interactúa con las opciones de consola. El servicio ejecuta las operaciones CRUD y de negocio aplicando verificaciones de existencia, stock y tipo de consumo.

Sincronización Automática: Tras cada modificación exitosa, main.py invoca los métodos de guardado correspondientes, convirtiendo los objetos a diccionarios y actualizando los archivos físicos en la carpeta datos/.

Semana 12: Optimización de Rendimiento e Índices en Memoria:

En esta etapa se incorporaron optimizaciones clave de rendimiento:

Índices en Memoria con Diccionarios: Se crearon índices internos (self.productos_dict y self.usuarios_dict) para realizar búsquedas frecuentes por clave única en tiempo constante O(1), evitando recorrer secuencialmente las listas.

Optimización de Consultas de Ventas por Usuario: Se implementó una estructura auxiliar indexada (self.ventas_por_usuario) para consultar el historial de compras de un cliente de forma directa sin escanear toda la colección de ventas.

Sincronización Automática: Los índices se mantienen rigurosamente sincronizados cada vez que se registran, actualizan o eliminan datos en memoria y en los archivos JSON.

Reconstrucción de Índices: Al iniciar la aplicación, los índices se reconstruyen automáticamente a partir de los objetos recuperados desde el almacenamiento persistente.

Semana 13:Interfaz Gráfica de Usuario (GUI con Tkinter) y Navegación de Ventana Única

En esta etapa final se migró la interacción por consola hacia una Interfaz Gráfica de Usuario (GUI) construida con tkinter y ttk, aplicando un patrón desacoplado y orientado a eventos.

Componentes Desarrollados e Integrados
Patrón de Ventana Única (Single Window Architecture en main.py):

Se creó la clase AplicacionRestaurante, la cual inicializa la ventana principal self.root = tk.Tk().

Administra el método cambiar_vista(nueva_vista), encargado de destruir el contenedor actual (self.vista_actual.destroy()) e incrustar la nueva vista (pack(fill="both", expand=True)), evitando la apertura de múltiples ventanas flotantes.

Vista de Inicio de Sesión (iu/login_view.py):

Hereda de ttk.Frame y se incrusta en el root principal.

Proporciona los campos para ingresar usuario y contraseña con enmascaramiento (show="*").

Al autenticarse correctamente, ejecuta la función callback on_login_success para notificar al controlador principal y dar paso a la ventana de trabajo.

Vista Principal por Pestañas (iu/main_view.py):

Encabezado y Gestión de Sesión: Presenta la barra superior con el usuario activo y el botón Cerrar Sesión. Al presionarlo, invoca el callback on_logout, que destruye la vista actual y retorna a la pantalla de login dentro de la misma ventana.

Contenedor por Pestañas (ttk.Notebook): Organiza el sistema en 4 pestañas interactivas:

Productos: Formulario CRUD para registrar/actualizar y tabla ttk.Treeview sincronizada.

Clientes: Formulario de registro/actualización de usuarios y tabla ttk.Treeview.

Ventas: Registro directo de ventas con actualización en tiempo real del stock de productos.

Categorías e Informes: Presentación de las categorías únicas extraídas mediante la estructura de datos set.

Desacoplamiento Estricto:

Ninguna vista gráfica interactúa directamente con los archivos JSON físicos. Toda lectura o modificación de información se realiza solicitando operaciones a RestauranteServicio, preservando la integridad de las reglas de negocio y los índices en memoria.

Estructura y Navegación de la Interfaz Gráfica (GUI)

El sistema opera bajo una Arquitectura de Ventana Única, alternando dinámicamente entre las siguientes vistas:  Pantalla de Acceso (LoginView):  
Control de autenticación mediante usuario (admin) y contraseña (admin123).  
Ventana Principal (MainView):  Encabezado Superior: Muestra el usuario activo y contiene el botón Cerrar Sesión para retornar al login sin destruir la ventana principal.  
Pestaña Productos: Formulario de registro y actualización, junto con la tabla interactiva de catálogo.  Pestaña Clientes: Formulario para registrar y editar clientes con tabla desplegable.  
Pestaña Ventas: Formulario de procesamiento de ventas directas con actualización automática de stock.  Pestaña Categorías e Informes: Consulta en tiempo real de las categorías únicas extraídas mediante la estructura

Semana 14: 
El objetivo principal de esta iteración es evolucionar la Interfaz Gráfica de Usuario (GUI) desarrollada en la Semana 13, integrando identidad visual corporativa (logos e iconos) y mejorando la organización del espacio de trabajo. Todo esto se realiza conservando intacta la arquitectura modular del sistema (Modelos, Servicios, IU) y la persistencia de datos en formato JSON.

## 2. Nueva Estructura de Recursos (Assets)
Para separar el código fuente de los elementos visuales, se implementó un nuevo directorio llamado `assets/`. Esta carpeta aloja todos los gráficos necesarios para renderizar la interfaz:

Se enriqueció la experiencia de usuario (UX) integrando imágenes a través de la clase tk.PhotoImage:

Icono de la Aplicación: En el controlador main.py, se implementó el método root.iconphoto(True, icono) para reemplazar el ícono por defecto de Tkinter por el logotipo del restaurante en la barra de tareas y el marco de la ventana.

Logo Corporativo (LoginView y MainView): Se integró el logo del restaurante en la pantalla de inicio de sesión. Para garantizar que la imagen encaje perfectamente sin distorsionar la interfaz, se empleó el método .subsample(2, 2), el cual reduce la escala de la imagen de forma nativa.

Carga Segura de Iconografía: Se desarrolló una función utilitaria (cargar_icono()) que verifica la existencia del archivo gráfico antes de intentar cargarlo. Si el archivo .png no se encuentra, la función retorna None. Gracias a esto, los botones (ttk.Button) pueden mostrar el icono mediante la propiedad compound=tk.LEFT, pero si el icono falta, la aplicación no colapsa y sigue funcionando mostrando únicamente el texto.

La interfaz se reestructuró para ser más limpia y profesional empleando los siguientes contenedores y componentes:

Contenedores de Agrupación:

Tk: Mantiene el control de la ventana principal de renderizado.

ttk.Frame: Se utiliza para seccionar grandes áreas de la pantalla (ej. separar la barra de navegación del área de contenido de las pestañas).

ttk.LabelFrame: Implementado para agrupar visualmente los formularios de "Registro de Platos/Bebidas" y "Gestión de Clientes", añadiendo un borde y un título descriptivo que mejora la comprensión de la interfaz.

Componentes de Interacción:

ttk.Treeview: Tablas de datos interactivas utilizadas para mostrar el menú del restaurante y el directorio de clientes registrados.

ttk.Scrollbar: Acoplado dinámicamente a los Treeview para permitir la navegación cuando el menú de platos supera el espacio visual de la tabla.

messagebox: Sistema de retroalimentación para notificar al usuario sobre ventas exitosas, errores de validación de campos vacíos o falta de stock.

Gestión de Geometría (pack y grid)

Se respetó la regla de diseño de Tkinter de no mezclar gestores de geometría dentro del mismo contenedor padre:

pack(): Se utilizó para el maquetado principal (Header, Contenedor de Pestañas Notebook), permitiendo que las vistas se expandan y adapten al redimensionar la ventana (fill="both", expand=True).

grid(): Se implementó exclusivamente dentro de los LabelFrame de los formularios. Esto permitió alinear perfectamente las etiquetas (Label) con sus respectivos cuadros de texto (Entry) en un formato de cuadrícula (filas y columnas).

Semana 15: Implementación de la Sección de Ventas

Durante esta iteración, se consolidó la funcionalidad principal del restaurante mediante la creación e integración de una interfaz gráfica completa para el registro de ventas.

Integración del Modelo de Venta: Se adaptó y utilizó la clase Venta existente, la cual representa transacciones que asocian un usuario específico, un producto y una fecha.

Persistencia Consolidada: Se configuró el archivo ventas.json dentro de la carpeta datos/ para almacenar de forma persistente cada transacción generada, asegurando la sincronización entre los datos en memoria y el almacenamiento físico.

Interfaz de Registro Optimizada (Tkinter/ttk):

Se diseñó un nuevo formulario dentro de la interfaz principal que facilita la entrada de datos.

Se implementaron componentes ttk.Combobox configurados en modo readonly para permitir la selección exclusiva de clientes y productos que ya existen en el sistema, evitando errores de entrada manual.

Gestión de Lógica en la Capa de Servicios: Toda la validación de inventario y procesamiento lógico de la venta se delegó al método vender_producto de la clase RestauranteServicio. Esta arquitectura asegura que la interfaz de usuario (main_view.py) permanezca completamente desacoplada de la manipulación directa de archivos JSON, garantizando un flujo seguro y ordenado.

Visualización en Tiempo Real: Las ventas registradas se presentan inmediatamente al usuario en un componente Treeview, el cual se refresca dinámicamente (refrescar_ventas()) tras cada operación exitosa.

Adaptación de Terminología: Se realizó una refactorización de código para alinear los nombres de variables, mensajes y referencias visuales al contexto exclusivo de un restaurante, reemplazando terminología residual de proyectos anteriores (como referencias a bibliotecas).

**Consolidación de Identidad Visual (Assets):** Se dio cumplimiento al requerimiento obligatorio de integrar recursos gráficos locales. Se añadieron y vincularon los íconos definitivos en formato `.png` dentro del directorio `assets/icons/` (ej. `add.png`, `home.png`, `users.png`) y el logotipo oficial en `assets/logo/`. Esto garantiza que el nuevo menú de Ventas y todas las acciones del sistema cuenten con su respectiva representación visual, mejorando significativamente la experiencia de usuario (UX) sin deformar la geometría de la interfaz.

---

## Nuevas Funcionalidades de la Semana 16

En esta versión se ha evolucionado el módulo de **Usuarios** para convertirlo en un **CRUD completo e interactivo**, integrando además un sistema avanzado de manejo de eventos, atajos de teclado y roles de usuario.

### ✨ Características principales implementadas:
* **Gestión completa de usuarios (CRUD):** 
  * Registro de nuevos usuarios y clientes.
  * Consulta general en tiempo real reflejada en un componente `ttk.Treeview`.
  * Actualización de datos existentes.
  * Eliminación de registros con ventana de confirmación previa (`messagebox`).
  * Limpieza y cancelación de selección de formularios.
* **Roles de Usuario:** 
  * Integración del atributo de roles en el modelo: `Administrador`, `Empleado` y `Cliente`.
* **Manejo Avanzado de Eventos y Atajos de Teclado:**
  * Uso de **`<<TreeviewSelect>>`** para cargar automáticamente los datos del usuario seleccionado desde la tabla hacia el formulario.
  * Uso de **`<<ComboboxSelected>>`** en el selector de roles con callbacks informativos en la barra de estado.
  * Atajo de teclado **`<Return>` (Enter)** para realizar el inicio de sesión o registrar usuarios directamente desde las casillas de texto.
  * Atajo de teclado global **`<Escape>`** implementado mediante `winfo_toplevel()` para limpiar los campos de los formularios instantáneamente desde cualquier posición.
* **Persistencia Local:** Sincronización automática de altas, modificaciones y bajas con el archivo `usuarios.json`.
* **Diseño e Interfaz Gráfica:** Mantenimiento de la línea visual corporativa, colores estructurados, barra de estado dinámica e incorporación de iconos desde la carpeta `assets/`.


Ejecución
Desde la carpeta raíz restaurante_app, ejecutar en el archivo main.py:
