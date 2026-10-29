# 🐍 Tkinter Python Showcase — Guía Práctica y Repositorio de Ejemplos

![Python Version](https://img.shields.io/badge/python-3.8%2B-blue.svg)
![Tkinter](https://img.shields.io/badge/GUI-Tkinter%20%2F%20ttk-brightgreen.svg)
![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)
![Zero Dependencies](https://img.shields.io/badge/Dependencies-Standard%20Library%20Only-orange.svg)

Un repositorio pedagógico, moderno y estructurado que reúne las principales funcionalidades, widgets, administradores de diseño, eventos, hilos y patrones de desarrollo de interfaces gráficas de escritorio (**GUI**) utilizando la biblioteca estándar de Python: **`tkinter`** y **`tkinter.ttk`**.

Incluye un **Lanzador Visual (`main.py`)** para ejecutar y previsualizar cualquiera de las demostraciones interactivamente sin depender de la consola.

---

## 📋 Tabla de Contenidos

- [Características Principales](#-características-principales)
- [Estructura del Proyecto](#-estructura-del-proyecto)
- [Requisitos Previos](#-requisitos-previos)
- [Cómo Ejecutar los Ejemplos](#-cómo-ejecutar-los-ejemplos)
- [Detalle de los Archivos de Código](#-detalle-de-los-archivos-de-código)
  - [01. Hola Mundo y Widgets Básicos](#01_hola_mundo_y_widgets_basicospy)
  - [02. Gestores de Posicionamiento (Layouts)](#02_layout_managerspy)
  - [03. Widgets Modernos TTK y Estilos](#03_ttk_widgets_y_estilospy)
  - [04. Lienzo Canvas, Dibujo y Animaciones](#04_canvas_y_dibujopy)
  - [05. Menús, Diálogos y Modales](#05_dialogos_y_menuspy)
  - [06. Manejo de Eventos y Atajos de Teclado](#06_eventos_y_atajos_tecladopy)
  - [07. Multihilos (Threading) y Prevención de Congelamiento](#07_hilos_y_asincronia_afterpy)
  - [08. Proyecto Completo: Gestor de Tareas (TaskMaster Pro)](#08_proyecto_completo_gestor_tareaspy)
- [Cómo Subir este Repositorio a GitHub](#-cómo-subir-este-repositorio-a-github)
- [Licencia](#-licencia)

---

## ✨ Características Principales

- **Cero dependencias externas:** Funciona de inmediato con cualquier instalación estándar de Python 3.8+ (no requiere `pip install`).
- **De lo básico a lo avanzado:** Desde un `Label` interactivo hasta una arquitectura multihilo no bloqueante con `queue.Queue`.
- **Diseño limpio y moderno:** Aplicación de temas `ttk.Style`, espaciado consistente, paleta de colores cuidada y tipografía clara.
- **Lanzador interactivo central (`main.py`):** Explora y ejecuta cada módulo con un solo clic.
- **Proyecto final integrador:** Aplicación de escritorio funcional completa con persistencia en formato JSON.

---

## 📂 Estructura del Proyecto

```text
tkinter-showcase/
├── .gitignore                             # Archivos y carpetas ignorados por Git
├── LICENSE                                # Licencia MIT de código abierto
├── README.md                              # Documentación exhaustiva del proyecto
├── requirements.txt                       # Notas de entorno y dependencias del sistema
├── main.py                                # Lanzador interactivo central (Showcase Hub)
│
├── 01_hola_mundo_y_widgets_basicos.py     # Ventanas, entradas, botones y variables reactivas
├── 02_layout_managers.py                  # Comparativa de pack(), grid() y place()
├── 03_ttk_widgets_y_estilos.py            # Combobox, Treeview tabular, Progressbar y estilos
├── 04_canvas_y_dibujo.py                  # Pizarra tipo Paint, figuras 2D, animación y drag & drop
├── 05_dialogos_y_menus.py                 # Barra de menús, clic derecho, messagebox y filedialog
├── 06_eventos_y_atajos_teclado.py         # Inspector de eventos de ratón, teclado y ventana en vivo
├── 07_hilos_y_asincronia_after.py         # Concurrencia con threading.Thread y cola thread-safe
└── 08_proyecto_completo_gestor_tareas.py  # Aplicación de tareas completa con POO y persistencia JSON
```

---

## 🔧 Requisitos Previos

1. **Python 3.8 o superior** instalado en el sistema.
2. **Tkinter** (incluido por defecto en Windows y macOS).
   - *En distribuciones Linux (Ubuntu/Debian):* Si no lo tienes instalado, ejecuta:
     ```bash
     sudo apt-get install python3-tk
     ```

---

## 🚀 Cómo Ejecutar los Ejemplos

### Opción 1: Usando el Lanzador Gráfico Central (Recomendado)
Ejecuta el explorador interactivo para abrir cualquiera de los scripts con un solo clic:

```bash
python main.py
```

### Opción 2: Ejecutar los módulos individualmente por consola
Puedes ejecutar directamente cualquier archivo que desees estudiar:

```bash
python 01_hola_mundo_y_widgets_basicos.py
python 02_layout_managers.py
python 03_ttk_widgets_y_estilos.py
python 04_canvas_y_dibujo.py
python 05_dialogos_y_menus.py
python 06_eventos_y_atajos_teclado.py
python 07_hilos_y_asincronia_after.py
python 08_proyecto_completo_gestor_tareas.py
```

---

## 📖 Detalle de los Archivos de Código

### `01_hola_mundo_y_widgets_basicos.py`
Enseña el punto de partida indispensable para construir aplicaciones de escritorio.
- **Conceptos clave:**
  - Instanciación de la ventana principal con `tk.Tk()`, asignación de título con `.title()`, dimensiones con `.geometry()` y límites con `.minsize()`.
  - **Variables de control:** `tk.StringVar`, `tk.BooleanVar` y `tk.IntVar` para vincular el estado interno con la interfaz de forma reactiva.
  - **Widgets esenciales:**
    - `Label`: Texto informativo estático y reactivo.
    - `Entry`: Caja de entrada de texto de una sola línea.
    - `Button`: Botones de acción con eventos de callback (`command`).
    - `Checkbutton`: Casillas de verificación booleanas.
    - `Radiobutton`: Opciones de selección mutuamente excluyentes agrupadas por variable.
    - `Spinbox`: Selector de valores numéricos en un rango.
    - `Text`: Área de texto multilínea para comentarios o párrafos extensos.
    - `LabelFrame`: Agrupador visual con borde y título.

---

### `02_layout_managers.py`
Profundiza en los 3 gestores de geometría que determinan cómo se posicionan y redimensionan los elementos en pantalla:
- **`pack()`**: Posicionamiento cardinal secuencial. Explica el uso de `side=TOP/BOTTOM/LEFT/RIGHT`, `fill=X/Y/BOTH`, y la propiedad fundamental `expand=True` para permitir que un widget absorba el espacio disponible al maximizar la ventana.
- **`grid()`**: Sistema de rejilla matricial (filas y columnas). Demuestra el uso de `row`, `column`, `columnspan`, alineación con `sticky` (N, S, E, W) y la configuración de proporciones mediante `columnconfigure(col, weight=1)`.
- **`place()`**: Posicionamiento por coordenadas directas. Compara coordenadas absolutas en píxeles (`x`, `y`) frente a coordenadas relativas (`relx`, `rely`, `relwidth`, `relheight`).

---

### `03_ttk_widgets_y_estilos.py`
Presenta el submódulo `tkinter.ttk` (Themed Tkinter), diseñado para darle a las aplicaciones un aspecto nativo y moderno:
- **`ttk.Combobox`**: Selector desplegable con soporte de solo lectura (`state="readonly"`) y captura de selección mediante el evento `<<ComboboxSelected>>`.
- **`ttk.Treeview`**: Estructura de datos tabular completa con columnas, títulos de encabezado interactivos, scrollbars acoplados y selección de filas.
- **`ttk.Progressbar`**: Demostración de los dos modos de barra:
  - *Determinado (`mode="determinate"`):* Vinculado numéricamente a un control deslizante (`ttk.Scale`).
  - *Indeterminado (`mode="indeterminate"`):* Animación continua de carga que se puede iniciar o pausar.
- **`ttk.Style`**: Motor de estilos para personalizar paletas de colores, fuentes, tamaño de filas y cambio dinámico del tema global del sistema operativo (`clam`, `alt`, `default`, `classic`).

---

### `04_canvas_y_dibujo.py`
Explora el poderoso widget `Canvas` para renderizado de gráficos vectoriales 2D, interactividad táctil y animaciones:
- **Primitivas geométricas:** Creación de líneas (`create_line`), rectángulos (`create_rectangle`), círculos u óvalos (`create_oval`), polígonos (`create_polygon`) y textos renderizados (`create_text`).
- **Pizarra interactiva (Mini Paint):** Captura de trazos a mano alzada utilizando eventos `<Button-1>` y `<B1-Motion>` con selector dinámico de color (`colorchooser`) y grosor de pincel.
- **Arrastrar y soltar (Drag and Drop):** Manipulación de objetos visuales en tiempo real mediante tags (`gettags`, `find_withtag`, `canvas.move`).
- **Animación basada en fotogramas:** Simulación de una esfera rebotando contra los márgenes de la ventana con detección de límites y refresco constante a 60 FPS mediante `.after(16, callback)`.

---

### `05_dialogos_y_menus.py`
Muestra cómo integrar la navegación del sistema operativo y ventanas modales de interacción:
- **Barra de menús superior (`tk.Menu`):** Menús desplegables en cascada (Archivo, Opciones, Ayuda) con separadores, casillas de verificación y atajos de teclado (`accelerator`).
- **Menú contextual emergente:** Ventana emergente (Popup) activada al hacer clic derecho (`<Button-3>`).
- **Diálogos estándar integrados:**
  - `messagebox`: Alertas informativas (`showinfo`), advertencias (`showwarning`), errores (`showerror`) y preguntas de confirmación (`askyesno`, `askokcancel`).
  - `filedialog`: Explorador del sistema para abrir archivos (`askopenfilename`), guardar archivos con extensión automática (`asksaveasfilename`) y seleccionar carpetas (`askdirectory`).
  - `colorchooser`: Paleta nativa de selección de color con devolución de código hexadecimal.
  - `simpledialog`: Solicitud rápida de cadenas de texto (`askstring`) o valores numéricos validados (`askinteger`).
- **Modal personalizado:** Creación de una ventana secundaria (`tk.Toplevel`) con comportamiento modal estricto mediante `.transient()` y `.grab_set()`.

---

### `06_eventos_y_atajos_teclado.py`
Explica en detalle el sistema de propagación y escucha de eventos de Tkinter:
- **Sintaxis de enlace:** `widget.bind("<Secuencia>", manejador)` y `bind_all()`.
- **Eventos de ratón:** Clic simple (`<Button-1>`), doble clic (`<Double-Button-1>`), arrastre (`<B1-Motion>`), entrada y salida de límites (`<Enter>`, `<Leave>`) y desplazamiento con rueda (`<MouseWheel>`).
- **Eventos de teclado:** Captura de caracteres (`<Key>`), teclas especiales (`<Return>`, `<Escape>`) y combinaciones simultáneas (`<Control-Shift-A>`).
- **Eventos del ciclo de vida de la ventana:** Detección de redimensionamiento (`<Configure>`) e intercepción del botón de cierre de ventana (`protocol("WM_DELETE_WINDOW")`).
- **Inspector de telemetría:** Panel en vivo que desglosa los atributos del objeto `event` recibido (`event.x`, `event.y`, `event.keysym`, `event.keycode`, `event.widget`).

---

### `07_hilos_y_asincronia_after.py`
Aborda el desafío más crítico al construir aplicaciones de escritorio: **evitar que la interfaz se congele** durante procesos intensivos o llamadas de red.
- **El error común:** Explicación y botón interactivo que reproduce el congelamiento al usar `time.sleep()` o tareas pesadas directamente en el bucle principal (`mainloop()`).
- **Temporizadores con `after()`:** Ejecución diferida y periódica sin interrumpir la recepción de eventos del usuario.
- **Concurrencia segura con `threading.Thread`:** Ejecución de procesos pesados en un hilo paralelo de fondo (modo `daemon=True`).
- **Comunicación Thread-Safe:** Dado que Tkinter no es seguro para ser modificado directamente desde hilos secundarios, se implementa una cola sincronizada `queue.Queue` que envía mensajes desde el hilo trabajador hacia la UI, la cual consume los eventos de forma controlada periódicamente con `root.after()`.

---

### `08_proyecto_completo_gestor_tareas.py`
Proyecto integrador final que reúne las mejores prácticas de desarrollo en una aplicación completa: **TaskMaster Pro**.
- **Arquitectura:** Programación Orientada a Objetos basada en clases heredando de `tk.Tk`.
- **Persistencia de datos:** Lectura y escritura automática en formato JSON (`tareas_guardadas.json`) al iniciar y guardar.
- **Funcionalidades:**
  - Creación de tareas con título, categoría y nivel de prioridad visual.
  - Tabla de visualización con `ttk.Treeview`, ordenamiento e indicadores de estado (Pendiente ⏳ / Completada ✅).
  - Filtrado en vivo por texto de búsqueda y por categoría mediante `StringVar.trace_add`.
  - Exportación e importación de listas de tareas a cualquier ubicación mediante `filedialog`.
  - Eliminación con confirmación y barra de estadísticas en el pie de página.

---

## 🌐 Cómo Subir este Repositorio a GitHub

Sigue estos sencillos pasos para publicar este código en tu cuenta de GitHub:

### Método 1: Desde la Consola (Git CLI)

1. **Abre tu terminal** en la carpeta del proyecto:
   ```bash
   cd C:\Users\Donov\.gemini\antigravity\scratch\tkinter-showcase
   ```

2. **Inicializa el repositorio Git local:**
   ```bash
   git init
   ```

3. **Agrega todos los archivos y realiza el primer commit:**
   ```bash
   git add .
   git commit -m "feat: initial commit - tkinter python showcase repository"
   ```

4. **Crea un nuevo repositorio vacío en GitHub:**
   - Ve a [github.com/new](https://github.com/new).
   - Nómbralo (por ejemplo: `tkinter-python-showcase`).
   - Elígelo **Público** o **Privado** y **NO marques** la opción de agregar README, .gitignore o licencia (ya los tenemos creados aquí).

5. **Vincula tu repositorio remoto y haz push:**
   ```bash
   git branch -M main
   git remote add origin https://github.com/TU_USUARIO/tkinter-python-showcase.git
   git push -u origin main
   ```

---

### Método 2: Usando GitHub Desktop

1. Abre **GitHub Desktop**.
2. Ve a **File > Add Local Repository...** (o presiona `Ctrl + O`).
3. Selecciona la carpeta del proyecto:
   `C:\Users\Donov\.gemini\antigravity\scratch\tkinter-showcase`
4. Haz clic en **Create a repository** si te lo sugiere, o realiza el commit inicial.
5. Haz clic en el botón superior **Publish repository** para subirlo directamente a tu cuenta de GitHub.

---

### Método 3: Subida directa mediante la Web de GitHub

1. Crea un nuevo repositorio vacío en [github.com/new](https://github.com/new).
2. En la página de bienvenida, haz clic en el enlace **uploading an existing file** ("subir un archivo existente").
3. Arrastra todos los archivos de esta carpeta hacia el navegador.
4. Escribe un mensaje de commit (ej. `Initial commit`) y presiona **Commit changes**.

---

## 📄 Licencia

Este proyecto está bajo la Licencia [MIT](LICENSE). Eres libre de usarlo, modificarlo y compartirlo con fines personales, académicos o comerciales.
