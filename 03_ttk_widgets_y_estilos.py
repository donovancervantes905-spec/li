"""
03_ttk_widgets_y_estilos.py
----------------------------
Explora la biblioteca moderna tkinter.ttk (Themed Tkinter):
  - Combobox con autocompletado y selección de eventos
  - Treeview como tabla de datos tabular con columnas, encabezados y ordenamiento
  - Progressbar en modo determinado e indeterminado
  - Scale (deslizador) con enlace dinámico
  - Separator
  - Personalización visual mediante ttk.Style() y cambio de temas globales
"""

import tkinter as tk
from tkinter import ttk, messagebox


class DemoTTK(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("03 - Widgets Modernos con tkinter.ttk y Estilos")
        self.geometry("750x700")
        self.minsize(650, 550)

        self.style = ttk.Style(self)
        self.configurar_estilos()
        self.construir_ui()

    def configurar_estilos(self):
        # Usar clam como base si está disponible para mayor consistencia visual
        if "clam" in self.style.theme_names():
            self.style.theme_use("clam")

        self.style.configure("Header.TLabel", font=("Segoe UI", 14, "bold"), foreground="#1e293b")
        self.style.configure("Sub.TLabel", font=("Segoe UI", 9), foreground="#64748b")
        self.style.configure("Accent.TButton", font=("Segoe UI", 9, "bold"))
        self.style.configure("Treeview.Heading", font=("Segoe UI", 9, "bold"))
        self.style.configure("Treeview", rowheight=24, font=("Segoe UI", 9))

    def construir_ui(self):
        # Header
        frame_head = ttk.Frame(self, padding=(15, 12))
        frame_head.pack(fill=tk.X)

        ttk.Label(frame_head, text="Componentes Avanzados TTK", style="Header.TLabel").pack(anchor="w")
        ttk.Label(frame_head, text="Aprovecha temas nativos, tablas jerárquicas y barras de progreso.", style="Sub.TLabel").pack(anchor="w")

        ttk.Separator(self, orient=tk.HORIZONTAL).pack(fill=tk.X, padx=15, pady=5)

        # Contenedor con 2 columnas: Izquierda (Controles) y Derecha/Abajo (Treeview)
        frame_central = ttk.Frame(self, padding=15)
        frame_central.pack(fill=tk.BOTH, expand=True)

        # --- SECCIÓN 1: Combobox y Selector de Temas ---
        sec_tema = ttk.LabelFrame(frame_central, text="Selector de Temas TTK y Combobox", padding=10)
        sec_tema.pack(fill=tk.X, pady=(0, 10))

        ttk.Label(sec_tema, text="Tema global del sistema:").grid(row=0, column=0, sticky="w", padx=5, pady=5)
        self.combo_temas = ttk.Combobox(sec_tema, values=self.style.theme_names(), state="readonly", width=18)
        self.combo_temas.set(self.style.theme_use())
        self.combo_temas.grid(row=0, column=1, sticky="w", padx=5, pady=5)
        self.combo_temas.bind("<<ComboboxSelected>>", self.al_cambiar_tema)

        ttk.Label(sec_tema, text="Combobox de Categoría:").grid(row=0, column=2, sticky="w", padx=(15, 5), pady=5)
        self.combo_cat = ttk.Combobox(sec_tema, values=["Desarrollo Web", "Ciencia de Datos", "DevOps", "Diseño UX/UI"], state="readonly", width=18)
        self.combo_cat.current(0)
        self.combo_cat.grid(row=0, column=3, sticky="w", padx=5, pady=5)

        # --- SECCIÓN 2: Progressbar y Scale (Slider) ---
        sec_progreso = ttk.LabelFrame(frame_central, text="Barras de Progreso y Sliders", padding=10)
        sec_progreso.pack(fill=tk.X, pady=(0, 10))

        # Slider conectado a la barra de progreso
        ttk.Label(sec_progreso, text="Control Manual (0-100):").grid(row=0, column=0, sticky="w", padx=5, pady=5)
        self.var_slider = tk.DoubleVar(value=40)
        self.slider = ttk.Scale(sec_progreso, from_=0, to=100, variable=self.var_slider, command=self.al_mover_slider)
        self.slider.grid(row=0, column=1, sticky="ew", padx=10, pady=5)

        self.lbl_valor_slider = ttk.Label(sec_progreso, text="40%")
        self.lbl_valor_slider.grid(row=0, column=2, padx=5, pady=5)

        sec_progreso.columnconfigure(1, weight=1)

        # Barra de progreso determinada
        ttk.Label(sec_progreso, text="Barra Determinada:").grid(row=1, column=0, sticky="w", padx=5, pady=5)
        self.bar_determinada = ttk.Progressbar(sec_progreso, orient="horizontal", mode="determinate", maximum=100, value=40)
        self.bar_determinada.grid(row=1, column=1, columnspan=2, sticky="ew", padx=10, pady=5)

        # Barra de progreso indeterminada (animación continua)
        ttk.Label(sec_progreso, text="Barra Indeterminada:").grid(row=2, column=0, sticky="w", padx=5, pady=5)
        self.bar_indeterminada = ttk.Progressbar(sec_progreso, orient="horizontal", mode="indeterminate")
        self.bar_indeterminada.grid(row=2, column=1, sticky="ew", padx=10, pady=5)

        btn_toggle = ttk.Button(sec_progreso, text="Iniciar/Pausar", command=self.toggle_indeterminada)
        btn_toggle.grid(row=2, column=2, padx=5, pady=5)
        self.indeterminada_activa = False

        # --- SECCIÓN 3: Treeview (Tabla de datos interactiva) ---
        sec_tabla = ttk.LabelFrame(frame_central, text="Treeview: Tabla de Datos con Selección y Scroll", padding=10)
        sec_tabla.pack(fill=tk.BOTH, expand=True)

        columnas = ("id", "nombre", "lenguaje", "estrellas")
        self.tree = ttk.Treeview(sec_tabla, columns=columnas, show="headings", selectmode="browse")

        self.tree.heading("id", text="ID")
        self.tree.heading("nombre", text="Proyecto")
        self.tree.heading("lenguaje", text="Lenguaje")
        self.tree.heading("estrellas", text="Estrellas ⭐")

        self.tree.column("id", width=50, anchor="center")
        self.tree.column("nombre", width=220, anchor="w")
        self.tree.column("lenguaje", width=140, anchor="center")
        self.tree.column("estrellas", width=90, anchor="center")

        # Scrollbar vertical para el Treeview
        scroll = ttk.Scrollbar(sec_tabla, orient=tk.VERTICAL, command=self.tree.yview)
        self.tree.configure(yscrollcommand=scroll.set)

        self.tree.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        scroll.pack(side=tk.RIGHT, fill=tk.Y)

        self.tree.bind("<<TreeviewSelect>>", self.al_seleccionar_fila)

        # Cargar datos de prueba
        datos_ejemplo = [
            (1, "Tkinter Showcase", "Python", 450),
            (2, "Django REST Core", "Python", 1200),
            (3, "FastAPI Service", "Python", 3100),
            (4, "React Dashboard", "JavaScript", 2800),
            (5, "Go Microservice", "Go", 1950),
            (6, "Flutter Mobile Client", "Dart", 1600),
            (7, "Rust CLI Utility", "Rust", 4200),
        ]
        for fila in datos_ejemplo:
            self.tree.insert("", tk.END, values=fila)

    def al_cambiar_tema(self, event):
        nuevo_tema = self.combo_temas.get()
        self.style.theme_use(nuevo_tema)

    def al_mover_slider(self, val):
        valor_flotante = float(val)
        self.bar_determinada["value"] = valor_flotante
        self.lbl_valor_slider.config(text=f"{int(valor_flotante)}%")

    def toggle_indeterminada(self):
        if self.indeterminada_activa:
            self.bar_indeterminada.stop()
            self.indeterminada_activa = False
        else:
            self.bar_indeterminada.start(10)
            self.indeterminada_activa = True

    def al_seleccionar_fila(self, event):
        seleccion = self.tree.selection()
        if seleccion:
            item = self.tree.item(seleccion[0])
            valores = item["values"]
            print(f"Fila seleccionada: ID={valores[0]}, Proyecto={valores[1]}")


if __name__ == "__main__":
    app = DemoTTK()
    app.mainloop()
