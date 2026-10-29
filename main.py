"""
main.py
-------
Lanzador interactivo central (Showcase Hub).
Permite explorar y ejecutar todos los módulos de demostración de Tkinter
directamente desde una interfaz moderna sin necesidad de recurrir a la consola.
"""

import tkinter as tk
from tkinter import ttk, messagebox
import subprocess
import sys
import os

MODULOS = [
    {
        "archivo": "01_hola_mundo_y_widgets_basicos.py",
        "titulo": "01. Hola Mundo y Widgets Básicos",
        "descripcion": "Configuración de ventanas, StringVar/IntVar, Entry, Button, Checkbutton, Radiobutton, Spinbox y Text.",
        "icono": "🔤"
    },
    {
        "archivo": "02_layout_managers.py",
        "titulo": "02. Gestores de Posicionamiento (Layouts)",
        "descripcion": "Comparación interactiva de los 3 geometry managers: pack(), grid() y place().",
        "icono": "📐"
    },
    {
        "archivo": "03_ttk_widgets_y_estilos.py",
        "titulo": "03. Widgets Modernos TTK y Estilos",
        "descripcion": "Tablas con Treeview, menús desplegables Combobox, barras de progreso y selector de temas ttk.Style.",
        "icono": "🎨"
    },
    {
        "archivo": "04_canvas_y_dibujo.py",
        "titulo": "04. Gráficos, Canvas y Animación",
        "descripcion": "Pizarra de dibujo interactiva (Paint), primitivas 2D, animación de rebote y arrastrar/soltar.",
        "icono": "🖌️"
    },
    {
        "archivo": "05_dialogos_y_menus.py",
        "titulo": "05. Menús, Diálogos y Atajos",
        "descripcion": "Menú superior en cascada, menú contextual emergente (clic derecho), messagebox, filedialog y modales.",
        "icono": "📂"
    },
    {
        "archivo": "06_eventos_y_atajos_teclado.py",
        "titulo": "06. Eventos y Teclado en Tiempo Real",
        "descripcion": "Inspección en vivo de eventos de ratón, pulsación de teclas, combinaciones y ciclo de vida de la ventana.",
        "icono": "⚡"
    },
    {
        "archivo": "07_hilos_y_asincronia_after.py",
        "titulo": "07. Multihilos (Threading) y after()",
        "descripcion": "Evitar congelamiento de interfaz con procesos pesados en segundo plano mediante hilos y colas queue.Queue.",
        "icono": "🧵"
    },
    {
        "archivo": "08_proyecto_completo_gestor_tareas.py",
        "titulo": "08. Proyecto Completo: Gestor de Tareas",
        "descripcion": "Aplicación de escritorio terminada con persistencia JSON, filtros en vivo, exportación y POO.",
        "icono": "🚀"
    },
]


class LauncherApp(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Tkinter Python Showcase - Explorador Central")
        self.geometry("780x680")
        self.minsize(680, 550)
        self.config(bg="#0f172a")

        self.directorio_base = os.path.dirname(os.path.abspath(__file__))
        self.procesos_activos = []

        self.construir_ui()

    def construir_ui(self):
        # Header
        frame_head = tk.Frame(self, bg="#0f172a", padx=25, pady=20)
        frame_head.pack(fill=tk.X)

        tk.Label(
            frame_head,
            text="🐍 Tkinter Python Showcase",
            font=("Segoe UI", 18, "bold"),
            fg="#38bdf8",
            bg="#0f172a"
        ).pack(anchor="w")

        tk.Label(
            frame_head,
            text="Colección completa de ejemplos prácticos y proyectos de la librería GUI estándar de Python.",
            font=("Segoe UI", 10),
            fg="#94a3b8",
            bg="#0f172a"
        ).pack(anchor="w", pady=(4, 0))

        # Contenedor con scroll para las tarjetas de módulos
        contenedor_scroll = tk.Frame(self, bg="#0f172a", padx=25)
        contenedor_scroll.pack(fill=tk.BOTH, expand=True)

        canvas = tk.Canvas(contenedor_scroll, bg="#0f172a", highlightthickness=0)
        scrollbar = ttk.Scrollbar(contenedor_scroll, orient="vertical", command=canvas.yview)
        self.frame_tarjetas = tk.Frame(canvas, bg="#0f172a")

        self.frame_tarjetas.bind(
            "<Configure>",
            lambda e: canvas.configure(scrollregion=canvas.bbox("all"))
        )

        canvas_window = canvas.create_window((0, 0), window=self.frame_tarjetas, anchor="nw")

        def al_redimensionar_canvas(event):
            canvas.itemconfig(canvas_window, width=event.width)

        canvas.bind("<Configure>", al_redimensionar_canvas)
        canvas.configure(yscrollcommand=scrollbar.set)

        canvas.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

        # Generar tarjetas de módulos
        for mod in MODULOS:
            self.crear_tarjeta_modulo(self.frame_tarjetas, mod)

        # Footer
        footer = tk.Frame(self, bg="#0f172a", padx=25, pady=12)
        footer.pack(fill=tk.X)

        tk.Label(
            footer,
            text="Listo para GitHub • Desarrollado en Python 3 puro (sin dependencias externas)",
            font=("Segoe UI", 9),
            fg="#64748b",
            bg="#0f172a"
        ).pack(side=tk.LEFT)

        btn_cerrar_todo = tk.Button(
            footer,
            text="Cerrar Todo",
            command=self.cerrar_aplicacion,
            bg="#334155",
            fg="#ffffff",
            relief=tk.FLAT,
            font=("Segoe UI", 8, "bold"),
            padx=10,
            pady=4,
            cursor="hand2"
        )
        btn_cerrar_todo.pack(side=tk.RIGHT)

    def crear_tarjeta_modulo(self, contenedor, mod):
        card = tk.Frame(contenedor, bg="#1e293b", padx=16, pady=12, bd=1, relief=tk.SOLID)
        card.pack(fill=tk.X, pady=6)

        # Lado izquierdo: Ícono y textos
        frame_textos = tk.Frame(card, bg="#1e293b")
        frame_textos.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

        header_fila = tk.Frame(frame_textos, bg="#1e293b")
        header_fila.pack(fill=tk.X)

        tk.Label(header_fila, text=mod["icono"], font=("Segoe UI", 13), bg="#1e293b").pack(side=tk.LEFT, padx=(0, 8))
        tk.Label(
            header_fila,
            text=mod["titulo"],
            font=("Segoe UI", 11, "bold"),
            fg="#f8fafc",
            bg="#1e293b"
        ).pack(side=tk.LEFT)

        tk.Label(
            frame_textos,
            text=mod["descripcion"],
            font=("Segoe UI", 9),
            fg="#94a3b8",
            bg="#1e293b",
            wraplength=480,
            justify=tk.LEFT
        ).pack(anchor="w", pady=(3, 0))

        # Lado derecho: Botón Ejecutar
        btn_run = tk.Button(
            card,
            text="Ejecutar ▶",
            command=lambda ruta=mod["archivo"]: self.ejecutar_script(ruta),
            bg="#0284c7",
            fg="#ffffff",
            activebackground="#0369a1",
            activeforeground="#ffffff",
            font=("Segoe UI", 9, "bold"),
            relief=tk.FLAT,
            padx=14,
            pady=6,
            cursor="hand2"
        )
        btn_run.pack(side=tk.RIGHT, padx=(12, 0))

    def ejecutar_script(self, nombre_archivo):
        ruta_completa = os.path.join(self.directorio_base, nombre_archivo)
        if not os.path.exists(ruta_completa):
            messagebox.showerror("Archivo No Encontrado", f"No se encontró el script:\n{ruta_completa}")
            return

        try:
            # Ejecuta el script en un subproceso independiente con el intérprete de Python actual
            p = subprocess.Popen([sys.executable, ruta_completa], cwd=self.directorio_base)
            self.procesos_activos.append(p)
        except Exception as e:
            messagebox.showerror("Error al Ejecutar", f"Error al iniciar {nombre_archivo}:\n{e}")

    def cerrar_aplicacion(self):
        # Limpiar procesos secundarios si es necesario
        for p in self.procesos_activos:
            if p.poll() is None:
                p.terminate()
        self.destroy()


if __name__ == "__main__":
    app = LauncherApp()
    app.mainloop()
