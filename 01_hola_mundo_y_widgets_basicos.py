"""
01_hola_mundo_y_widgets_basicos.py
-----------------------------------
Demuestra los fundamentos de Tkinter:
  - Creación y configuración de la ventana principal (Tk)
  - Variables de control reactivas (StringVar, BooleanVar, IntVar)
  - Widgets esenciales: Label, Entry, Button, Checkbutton, Radiobutton, Spinbox y Text
  - Manejo básico del layout con pack() y frames organizadores
"""

import tkinter as tk
from tkinter import messagebox


def crear_interfaz():
    # 1. Ventana principal
    ventana = tk.Tk()
    ventana.title("01 - Fundamentos y Widgets Básicos de Tkinter")
    ventana.geometry("620x720")
    ventana.minsize(500, 600)
    ventana.config(bg="#f4f6f9")

    # 2. Variables de control de Tkinter (Reactividad básica)
    var_nombre = tk.StringVar(value="Mundo")
    var_notificaciones = tk.BooleanVar(value=True)
    var_nivel = tk.StringVar(value="Intermedio")
    var_edad = tk.IntVar(value=25)
    var_mensaje_resultado = tk.StringVar(value="Bienvenido. Modifica los controles y presiona el botón.")

    # 3. Título de cabecera (Header)
    frame_header = tk.Frame(ventana, bg="#2c3e50", padx=15, pady=15)
    frame_header.pack(fill=tk.X)

    lbl_titulo = tk.Label(
        frame_header,
        text="✨ Explorador de Widgets Básicos",
        font=("Segoe UI", 16, "bold"),
        fg="#ffffff",
        bg="#2c3e50"
    )
    lbl_titulo.pack()

    lbl_subtitulo = tk.Label(
        frame_header,
        text="Aprende cómo capturar datos con Labels, Entries, Checkbuttons y más",
        font=("Segoe UI", 9),
        fg="#bdc3c7",
        bg="#2c3e50"
    )
    lbl_subtitulo.pack(pady=(4, 0))

    # Contenedor principal con scroll/padding
    frame_cuerpo = tk.Frame(ventana, bg="#f4f6f9", padx=20, pady=15)
    frame_cuerpo.pack(fill=tk.BOTH, expand=True)

    # --- SECCIÓN 1: Entry y Label interactivo ---
    sec1 = tk.LabelFrame(frame_cuerpo, text=" 1. Entrada de Texto (Entry) ", font=("Segoe UI", 10, "bold"), bg="#ffffff", padx=10, pady=10)
    sec1.pack(fill=tk.X, pady=8)

    lbl_input = tk.Label(sec1, text="Ingresa tu nombre:", bg="#ffffff", font=("Segoe UI", 9))
    lbl_input.pack(anchor="w")

    entry_nombre = tk.Entry(sec1, textvariable=var_nombre, font=("Segoe UI", 10), relief=tk.SOLID, bd=1)
    entry_nombre.pack(fill=tk.X, pady=(2, 6))

    # --- SECCIÓN 2: Checkbutton (Casilla de verificación) y Spinbox ---
    sec2 = tk.LabelFrame(frame_cuerpo, text=" 2. Opciones y Números ", font=("Segoe UI", 10, "bold"), bg="#ffffff", padx=10, pady=10)
    sec2.pack(fill=tk.X, pady=8)

    chk_notif = tk.Checkbutton(
        sec2,
        text="Recibir notificaciones por correo",
        variable=var_notificaciones,
        bg="#ffffff",
        font=("Segoe UI", 9),
        activebackground="#ffffff"
    )
    chk_notif.pack(anchor="w")

    frame_spin = tk.Frame(sec2, bg="#ffffff")
    frame_spin.pack(anchor="w", pady=(6, 0))
    tk.Label(frame_spin, text="Edad:", bg="#ffffff", font=("Segoe UI", 9)).pack(side=tk.LEFT)
    spin_edad = tk.Spinbox(frame_spin, from_=1, to=120, textvariable=var_edad, width=5, font=("Segoe UI", 9))
    spin_edad.pack(side=tk.LEFT, padx=6)

    # --- SECCIÓN 3: Radiobutton (Selección exclusiva) ---
    sec3 = tk.LabelFrame(frame_cuerpo, text=" 3. Nivel de Experiencia (Radiobutton) ", font=("Segoe UI", 10, "bold"), bg="#ffffff", padx=10, pady=10)
    sec3.pack(fill=tk.X, pady=8)

    niveles = [("Principiante", "Principiante"), ("Intermedio", "Intermedio"), ("Avanzado", "Avanzado")]
    frame_radios = tk.Frame(sec3, bg="#ffffff")
    frame_radios.pack(anchor="w")

    for texto, valor in niveles:
        tk.Radiobutton(
            frame_radios,
            text=texto,
            value=valor,
            variable=var_nivel,
            bg="#ffffff",
            activebackground="#ffffff",
            font=("Segoe UI", 9)
        ).pack(side=tk.LEFT, padx=8)

    # --- SECCIÓN 4: Cuadro de texto multilínea (Text) ---
    sec4 = tk.LabelFrame(frame_cuerpo, text=" 4. Biografía o Comentarios (Text) ", font=("Segoe UI", 10, "bold"), bg="#ffffff", padx=10, pady=10)
    sec4.pack(fill=tk.BOTH, expand=True, pady=8)

    txt_comentarios = tk.Text(sec4, height=4, font=("Segoe UI", 9), relief=tk.SOLID, bd=1)
    txt_comentarios.insert(tk.END, "Escribe aquí tus comentarios u observaciones...")
    txt_comentarios.pack(fill=tk.BOTH, expand=True)

    # --- ACCIONES: Botones y resultado ---
    def procesar_datos():
        nombre = var_nombre.get().strip() or "Anónimo"
        notif = "Sí" if var_notificaciones.get() else "No"
        nivel = var_nivel.get()
        edad = var_edad.get()
        bio = txt_comentarios.get("1.0", tk.END).strip()

        resumen = f"Hola, {nombre}! (Edad: {edad}) | Nivel: {nivel} | Alertas: {notif}\nBio: {bio[:60]}..."
        var_mensaje_resultado.set(resumen)
        messagebox.showinfo("Datos Procesados", f"¡Formulario procesado con éxito para {nombre}!")

    def limpiar_campos():
        var_nombre.set("")
        var_notificaciones.set(False)
        var_nivel.set("Principiante")
        var_edad.set(18)
        txt_comentarios.delete("1.0", tk.END)
        var_mensaje_resultado.set("Campos reiniciados.")

    frame_botones = tk.Frame(frame_cuerpo, bg="#f4f6f9")
    frame_botones.pack(fill=tk.X, pady=6)

    btn_procesar = tk.Button(
        frame_botones,
        text="Procesar Formulario",
        command=procesar_datos,
        bg="#27ae60",
        fg="#ffffff",
        activebackground="#219150",
        activeforeground="#ffffff",
        font=("Segoe UI", 9, "bold"),
        relief=tk.FLAT,
        padx=12,
        pady=6,
        cursor="hand2"
    )
    btn_procesar.pack(side=tk.LEFT, padx=(0, 8))

    btn_limpiar = tk.Button(
        frame_botones,
        text="Limpiar",
        command=limpiar_campos,
        bg="#e74c3c",
        fg="#ffffff",
        activebackground="#c0392b",
        activeforeground="#ffffff",
        font=("Segoe UI", 9),
        relief=tk.FLAT,
        padx=12,
        pady=6,
        cursor="hand2"
    )
    btn_limpiar.pack(side=tk.LEFT)

    # Etiqueta de resultado
    lbl_resultado = tk.Label(
        frame_cuerpo,
        textvariable=var_mensaje_resultado,
        bg="#e8edf2",
        fg="#2c3e50",
        font=("Segoe UI", 9, "italic"),
        relief=tk.RIDGE,
        bd=1,
        padx=10,
        pady=8,
        wraplength=560,
        justify=tk.LEFT
    )
    lbl_resultado.pack(fill=tk.X, pady=(6, 0))

    return ventana


if __name__ == "__main__":
    app = crear_interfaz()
    app.mainloop()
