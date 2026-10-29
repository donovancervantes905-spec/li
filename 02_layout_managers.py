"""
02_layout_managers.py
---------------------
Muestra y compara en profundidad los 3 administradores de diseño (Geometry Managers) de Tkinter:
  1. pack()  - Empaquetador secuencial (top, bottom, left, right, fill, expand)
  2. grid()  - Cuadrícula matricial bidimensional (filas, columnas, sticky, weight)
  3. place() - Posicionamiento absoluto y relativo (x, y, relx, rely, relwidth, relheight)

Organizado mediante pestañas interactivas (ttk.Notebook) para facilitar el aprendizaje visual.
"""

import tkinter as tk
from tkinter import ttk


def pestaña_pack(parent):
    frame = tk.Frame(parent, bg="#ffffff", padx=15, pady=15)

    lbl_info = tk.Label(
        frame,
        text="El gestor pack() acomoda widgets contra los bordes (TOP, BOTTOM, LEFT, RIGHT).\n"
             "Usa 'fill' para rellenar ejes y 'expand=True' para reclamar el espacio sobrante.",
        font=("Segoe UI", 9),
        bg="#ecf0f1",
        fg="#2c3e50",
        relief=tk.SOLID,
        bd=1,
        padx=10,
        pady=8,
        justify=tk.LEFT
    )
    lbl_info.pack(fill=tk.X, pady=(0, 10))

    # Barra superior
    barra_sup = tk.Label(frame, text="pack(side=TOP, fill=X) -> Barra superior", bg="#3498db", fg="white", pady=8, font=("Segoe UI", 9, "bold"))
    barra_sup.pack(side=tk.TOP, fill=tk.X, pady=2)

    # Barra inferior
    barra_inf = tk.Label(frame, text="pack(side=BOTTOM, fill=X) -> Barra inferior / Footer", bg="#34495e", fg="white", pady=8, font=("Segoe UI", 9, "bold"))
    barra_inf.pack(side=tk.BOTTOM, fill=tk.X, pady=2)

    # Panel lateral izquierdo
    panel_izq = tk.Label(frame, text="pack(side=LEFT,\nfill=Y)\nPanel Lateral", bg="#2ecc71", fg="white", width=16, font=("Segoe UI", 9, "bold"))
    panel_izq.pack(side=tk.LEFT, fill=tk.Y, padx=2)

    # Contenido central expandible
    area_central = tk.Label(
        frame,
        text="pack(side=LEFT, fill=BOTH, expand=True)\nÁrea central que absorbe todo el espacio al redimensionar.",
        bg="#f39c12",
        fg="white",
        font=("Segoe UI", 10, "bold")
    )
    area_central.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=2)

    return frame


def pestaña_grid(parent):
    frame = tk.Frame(parent, bg="#ffffff", padx=15, pady=15)

    lbl_info = tk.Label(
        frame,
        text="El gestor grid() organiza en filas y columnas matemáticas.\n"
             "Es ideal para formularios estructurados. 'sticky' define la alineación (N, S, E, W).\n"
             "Con 'columnconfigure(i, weight=1)' logras que las columnas sean responsivas.",
        font=("Segoe UI", 9),
        bg="#ecf0f1",
        fg="#2c3e50",
        relief=tk.SOLID,
        bd=1,
        padx=10,
        pady=8,
        justify=tk.LEFT
    )
    lbl_info.grid(row=0, column=0, columnspan=3, sticky="ew", pady=(0, 15))

    # Configurar pesos de columnas para que crezcan
    frame.columnconfigure(1, weight=1)

    # Fila 1
    tk.Label(frame, text="Nombre:", bg="#ffffff", font=("Segoe UI", 9, "bold")).grid(row=1, column=0, sticky="w", pady=4)
    entry_nombre = tk.Entry(frame, relief=tk.SOLID, bd=1)
    entry_nombre.grid(row=1, column=1, columnspan=2, sticky="ew", pady=4)

    # Fila 2
    tk.Label(frame, text="Email:", bg="#ffffff", font=("Segoe UI", 9, "bold")).grid(row=2, column=0, sticky="w", pady=4)
    entry_email = tk.Entry(frame, relief=tk.SOLID, bd=1)
    entry_email.grid(row=2, column=1, columnspan=2, sticky="ew", pady=4)

    # Fila 3: Simulación de teclado numérico con grid
    tk.Label(frame, text="Cuadrícula Numérica (columnas y filas múltiples):", bg="#ffffff", font=("Segoe UI", 9, "italic")).grid(
        row=3, column=0, columnspan=3, sticky="w", pady=(15, 6)
    )

    frame_calc = tk.Frame(frame, bg="#e0e0e0", bd=1, relief=tk.SOLID, padx=5, pady=5)
    frame_calc.grid(row=4, column=0, columnspan=3, sticky="ew")

    botones = [
        ("7", 0, 0), ("8", 0, 1), ("9", 0, 2),
        ("4", 1, 0), ("5", 1, 1), ("6", 1, 2),
        ("1", 2, 0), ("2", 2, 1), ("3", 2, 2),
        ("0", 3, 0), (".", 3, 1), ("=", 3, 2),
    ]

    for c in range(3):
        frame_calc.columnconfigure(c, weight=1)

    for texto, f, c in botones:
        b = tk.Button(frame_calc, text=texto, font=("Segoe UI", 10, "bold"), relief=tk.GROOVE, padx=10, pady=8)
        b.grid(row=f, column=c, sticky="nsew", padx=2, pady=2)

    return frame


def pestaña_place(parent):
    frame = tk.Frame(parent, bg="#ffffff", padx=15, pady=15)

    lbl_info = tk.Label(
        frame,
        text="El gestor place() ubica widgets por coordenadas exactas (x, y) o relativas (relx, rely).\n"
             "Útil para superposiciones, badges flotantes o diseños de coordenadas fijas.",
        font=("Segoe UI", 9),
        bg="#ecf0f1",
        fg="#2c3e50",
        relief=tk.SOLID,
        bd=1,
        padx=10,
        pady=8,
        justify=tk.LEFT
    )
    lbl_info.pack(fill=tk.X, pady=(0, 10))

    # Canvas o contenedor para demostrar place
    lienzo = tk.Frame(frame, bg="#f8f9fa", bd=2, relief=tk.GROOVE, height=350)
    lienzo.pack(fill=tk.BOTH, expand=True)

    # 1. Posición absoluta en píxeles (x=30, y=30)
    lbl_abs = tk.Label(lienzo, text="Coordenada Fija\nx=30, y=30", bg="#9b59b6", fg="white", font=("Segoe UI", 8, "bold"), padx=8, pady=4)
    lbl_abs.place(x=30, y=30, width=130, height=50)

    # 2. Posición relativa al centro (relx=0.5, rely=0.5 con anchor=CENTER)
    lbl_centro = tk.Label(lienzo, text="Centro Relativo\nrelx=0.5, rely=0.5", bg="#e67e22", fg="white", font=("Segoe UI", 9, "bold"), padx=10, pady=6)
    lbl_centro.place(relx=0.5, rely=0.5, anchor=tk.CENTER)

    # 3. Widget de ancho relativo (relwidth=0.8) en la parte inferior
    lbl_relativo = tk.Label(
        lienzo,
        text="Barra Inferior Relativa: relx=0.1, rely=0.85, relwidth=0.8",
        bg="#1abc9c",
        fg="white",
        font=("Segoe UI", 8, "bold")
    )
    lbl_relativo.place(relx=0.1, rely=0.85, relwidth=0.8, height=35)

    return frame


def main():
    root = tk.Tk()
    root.title("02 - Geometry Managers: pack vs grid vs place")
    root.geometry("680x620")
    root.minsize(550, 480)

    style = ttk.Style(root)
    # Seleccionar tema disponible
    if "clam" in style.theme_names():
        style.theme_use("clam")

    notebook = ttk.Notebook(root)
    notebook.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)

    # Agregar pestañas
    notebook.add(pestaña_pack(notebook), text="  📦 pack()  ")
    notebook.add(pestaña_grid(notebook), text="  📐 grid()  ")
    notebook.add(pestaña_place(notebook), text="  📍 place()  ")

    root.mainloop()


if __name__ == "__main__":
    main()
