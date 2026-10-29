"""
04_canvas_y_dibujo.py
---------------------
Demuestra las capacidades gráficas del widget Canvas de Tkinter:
  - Dibujo de primitivas geométricas: rectángulos, círculos (óvalos), líneas, polígonos y texto
  - Pizarra de dibujo interactiva (Paint básico con selección de color y grosor)
  - Animación en tiempo real (pelota que rebota contra los bordes usando after())
  - Arrastrar y soltar (Drag and Drop) de objetos visuales en el lienzo
"""

import tkinter as tk
from tkinter import ttk, colorchooser


class DemoCanvas(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("04 - Canvas Gráfico, Dibujo y Animaciones")
        self.geometry("860x650")
        self.minsize(700, 500)
        self.config(bg="#f1f5f9")

        # Variables de dibujo
        self.color_actual = "#2563eb"
        self.grosor_pincel = tk.IntVar(value=3)
        self.ultimo_x = None
        self.ultimo_y = None

        # Variables de animación
        self.animando = False
        self.pelota = None
        self.vel_x = 4
        self.vel_y = 3

        # Variables de drag & drop
        self.item_arrastrado = None
        self.arrastre_x = 0
        self.arrastre_y = 0

        self.construir_ui()

    def construir_ui(self):
        # Barra de herramientas superior
        toolbar = tk.Frame(self, bg="#ffffff", padx=10, pady=8, bd=1, relief=tk.SOLID)
        toolbar.pack(fill=tk.X, side=tk.TOP)

        tk.Label(toolbar, text="🎨 Pincel:", bg="#ffffff", font=("Segoe UI", 9, "bold")).pack(side=tk.LEFT, padx=(5, 2))

        # Indicador de color
        self.btn_color = tk.Button(
            toolbar, bg=self.color_actual, width=3, height=1, relief=tk.GROOVE, command=self.seleccionar_color
        )
        self.btn_color.pack(side=tk.LEFT, padx=4)

        tk.Label(toolbar, text="Grosor:", bg="#ffffff", font=("Segoe UI", 9)).pack(side=tk.LEFT, padx=(10, 2))
        spin_grosor = tk.Spinbox(toolbar, from_=1, to=25, textvariable=self.grosor_pincel, width=3)
        spin_grosor.pack(side=tk.LEFT, padx=4)

        btn_limpiar = tk.Button(toolbar, text="Borrar Lienzo", command=self.limpiar_lienzo, bg="#ef4444", fg="white", font=("Segoe UI", 9), relief=tk.FLAT, padx=8)
        btn_limpiar.pack(side=tk.LEFT, padx=12)

        tk.Label(toolbar, text="|", bg="#ffffff", fg="#cbd5e1").pack(side=tk.LEFT, padx=6)

        # Botón para iniciar/detener animación
        self.btn_anim = tk.Button(toolbar, text="Iniciar Rebote", command=self.toggle_animacion, bg="#10b981", fg="white", font=("Segoe UI", 9, "bold"), relief=tk.FLAT, padx=10)
        self.btn_anim.pack(side=tk.LEFT, padx=4)

        tk.Label(
            toolbar,
            text="Tip: Arrastra el cuadrado morado o dibuja con clic izquierdo.",
            bg="#ffffff",
            fg="#64748b",
            font=("Segoe UI", 9, "italic")
        ).pack(side=tk.RIGHT, padx=10)

        # Lienzo (Canvas)
        self.canvas = tk.Canvas(self, bg="#ffffff", cursor="cross")
        self.canvas.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)

        # Dibujar elementos iniciales
        self.inicializar_figuras()

        # Enlazar eventos de dibujo libre
        self.canvas.bind("<Button-1>", self.al_presionar_raton)
        self.canvas.bind("<B1-Motion>", self.al_arrastrar_raton)
        self.canvas.bind("<ButtonRelease-1>", self.al_soltar_raton)

    def inicializar_figuras(self):
        # Dibujar cuadrícula de fondo decorativa
        for x in range(0, 900, 50):
            self.canvas.create_line(x, 0, x, 700, fill="#f8fafc", tags="fondo")
        for y in range(0, 700, 50):
            self.canvas.create_line(0, y, 900, y, fill="#f8fafc", tags="fondo")

        # Texto ilustrativo
        self.canvas.create_text(
            160, 30,
            text="Canvas 2D Interactivo",
            font=("Segoe UI", 14, "bold"),
            fill="#334155"
        )

        # Figura arrastrable (cuadrado con tag "arrastrable")
        self.caja_movible = self.canvas.create_rectangle(
            50, 70, 160, 160,
            fill="#8b5cf6", outline="#6d28d9", width=2,
            tags=("arrastrable", "forma")
        )
        self.canvas.create_text(105, 115, text="¡Arrástrame!", fill="white", font=("Segoe UI", 9, "bold"), tags="arrastrable")

        # Polígono decorativo (estrella o triángulo)
        self.canvas.create_polygon(
            220, 160, 260, 80, 300, 160,
            fill="#fbbf24", outline="#d97706", width=2
        )

        # Pelota para la animación
        self.pelota = self.canvas.create_oval(340, 70, 380, 110, fill="#ef4444", outline="#b91c1c", width=2)

    def seleccionar_color(self):
        color = colorchooser.askcolor(self.color_actual, title="Elige un color para el pincel")[1]
        if color:
            self.color_actual = color
            self.btn_color.config(bg=color)

    def limpiar_lienzo(self):
        self.canvas.delete("all")
        self.inicializar_figuras()

    def al_presionar_raton(self, event):
        # Verificar si se hizo clic en un objeto con tag "arrastrable"
        items_cercanos = self.canvas.find_withtag("current")
        if items_cercanos and "arrastrable" in self.canvas.gettags(items_cercanos[0]):
            self.item_arrastrado = "arrastrable"
            self.arrastre_x = event.x
            self.arrastre_y = event.y
        else:
            self.item_arrastrado = None
            self.ultimo_x = event.x
            self.ultimo_y = event.y

    def al_arrastrar_raton(self, event):
        if self.item_arrastrado:
            # Mover todas las partes con tag arrastrable
            dx = event.x - self.arrastre_x
            dy = event.y - self.arrastre_y
            self.canvas.move(self.item_arrastrado, dx, dy)
            self.arrastre_x = event.x
            self.arrastre_y = event.y
        else:
            # Dibujo de pincel libre
            if self.ultimo_x and self.ultimo_y:
                self.canvas.create_line(
                    self.ultimo_x, self.ultimo_y, event.x, event.y,
                    fill=self.color_actual,
                    width=self.grosor_pincel.get(),
                    capstyle=tk.ROUND,
                    smooth=True,
                    tags="trazos"
                )
            self.ultimo_x = event.x
            self.ultimo_y = event.y

    def al_soltar_raton(self, event):
        self.ultimo_x = None
        self.ultimo_y = None
        self.item_arrastrado = None

    def toggle_animacion(self):
        if self.animando:
            self.animando = False
            self.btn_anim.config(text="Iniciar Rebote", bg="#10b981")
        else:
            self.animando = True
            self.btn_anim.config(text="Detener Rebote", bg="#f59e0b")
            self.animar_bucle()

    def animar_bucle(self):
        if not self.animando:
            return

        # Obtener coordenadas de la pelota
        coords = self.canvas.coords(self.pelota)
        if coords:
            x1, y1, x2, y2 = coords
            ancho_canvas = self.canvas.winfo_width()
            alto_canvas = self.canvas.winfo_height()

            # Rebote en límites horizontales
            if x2 >= ancho_canvas or x1 <= 0:
                self.vel_x = -self.vel_x
            # Rebote en límites verticales
            if y2 >= alto_canvas or y1 <= 0:
                self.vel_y = -self.vel_y

            self.canvas.move(self.pelota, self.vel_x, self.vel_y)

        # Reprogramar siguiente fotograma cada 16ms (~60 FPS)
        self.after(16, self.animar_bucle)


if __name__ == "__main__":
    app = DemoCanvas()
    app.mainloop()
