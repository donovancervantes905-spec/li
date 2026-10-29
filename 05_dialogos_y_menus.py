"""
05_dialogos_y_menus.py
----------------------
Demuestra el sistema de menús y ventanas de diálogo de Tkinter:
  - Barra de menús principal (Menu Bar) con cascadas y atajos de teclado
  - Menú contextual emergente (clic derecho / popup)
  - Diálogos estándar del sistema:
      * messagebox (showinfo, showwarning, showerror, askyesno)
      * filedialog (abrir archivo, guardar archivo, seleccionar carpeta)
      * colorchooser (paleta de colores del sistema)
      * simpledialog (captura rápida de texto, enteros y decimales)
  - Diálogo modal personalizado usando Toplevel con grab_set()
"""

import tkinter as tk
from tkinter import ttk, messagebox, filedialog, colorchooser, simpledialog


class DemoMenusYDialogos(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("05 - Menús y Diálogos en Tkinter")
        self.geometry("700x560")
        self.minsize(550, 420)
        self.config(bg="#f8fafc")

        self.crear_barra_menus()
        self.crear_menu_contextual()
        self.construir_ui()

    def crear_barra_menus(self):
        barra_menu = tk.Menu(self)

        # Menú Archivo
        menu_archivo = tk.Menu(barra_menu, tearoff=0)
        menu_archivo.add_command(label="Nuevo Archivo", accelerator="Ctrl+N", command=lambda: self.registrar_accion("Nuevo Archivo"))
        menu_archivo.add_command(label="Abrir...", accelerator="Ctrl+O", command=self.dialogo_abrir_archivo)
        menu_archivo.add_command(label="Guardar Como...", accelerator="Ctrl+S", command=self.dialogo_guardar_archivo)
        menu_archivo.add_separator()
        menu_archivo.add_command(label="Salir", accelerator="Alt+F4", command=self.confirmar_salida)
        barra_menu.add_cascade(label="Archivo", menu=menu_archivo)

        # Menú Opciones
        menu_opciones = tk.Menu(barra_menu, tearoff=0)
        self.var_modo_oscuro = tk.BooleanVar(value=False)
        menu_opciones.add_checkbutton(label="Modo Oscuro (Simulado)", variable=self.var_modo_oscuro, command=self.toggle_modo)
        barra_menu.add_cascade(label="Opciones", menu=menu_opciones)

        # Menú Ayuda
        menu_ayuda = tk.Menu(barra_menu, tearoff=0)
        menu_ayuda.add_command(label="Acerca de Tkinter Showcase", command=lambda: messagebox.showinfo("Acerca de", "Tkinter Showcase v1.0\nEjemplo completo de menús y diálogos."))
        barra_menu.add_cascade(label="Ayuda", menu=menu_ayuda)

        self.config(menu=barra_menu)

        # Enlazar atajos de teclado de la ventana
        self.bind_all("<Control-n>", lambda e: self.registrar_accion("Nuevo Archivo (Atajo)"))
        self.bind_all("<Control-o>", lambda e: self.dialogo_abrir_archivo())
        self.bind_all("<Control-s>", lambda e: self.dialogo_guardar_archivo())

    def crear_menu_contextual(self):
        self.menu_popup = tk.Menu(self, tearoff=0)
        self.menu_popup.add_command(label="Copiar selección", command=lambda: self.registrar_accion("Acción: Copiar"))
        self.menu_popup.add_command(label="Pegar contenido", command=lambda: self.registrar_accion("Acción: Pegar"))
        self.menu_popup.add_separator()
        self.menu_popup.add_command(label="Limpiar registro", command=self.limpiar_log)

    def construir_ui(self):
        # Header
        frame_head = tk.Frame(self, bg="#0f172a", padx=15, pady=12)
        frame_head.pack(fill=tk.X)

        tk.Label(frame_head, text="🧭 Menús y Cuadros de Diálogo", font=("Segoe UI", 14, "bold"), fg="#ffffff", bg="#0f172a").pack(anchor="w")
        tk.Label(frame_head, text="Prueba los botones inferiores o haz clic derecho en el área de texto para ver el menú contextual.", font=("Segoe UI", 9), fg="#94a3b8", bg="#0f172a").pack(anchor="w")

        # Botonera de diálogos
        frame_grid_btn = tk.Frame(self, bg="#f8fafc", padx=15, pady=10)
        frame_grid_btn.pack(fill=tk.X)

        dialogos = [
            ("Mensaje Info", lambda: messagebox.showinfo("Información", "¡Operación completada con éxito!")),
            ("Mensaje Advertencia", lambda: messagebox.showwarning("Aviso", "El archivo contiene campos vacíos.")),
            ("Mensaje Error", lambda: messagebox.showerror("Error Crítico", "No se pudo conectar a la base de datos.")),
            ("Confirmación (Sí/No)", self.dialogo_confirmacion),
            ("Seleccionar Archivo", self.dialogo_abrir_archivo),
            ("Seleccionar Carpeta", self.dialogo_abrir_carpeta),
            ("Selector de Color", self.dialogo_color),
            ("Pedir Texto", self.dialogo_pedir_texto),
            ("Pedir Número Entero", self.dialogo_pedir_numero),
            ("Modal Personalizado", self.abrir_modal_personalizado),
        ]

        # Colocar botones en 5 columnas x 2 filas
        for idx, (titulo, comando) in enumerate(dialogos):
            r = idx // 5
            c = idx % 5
            btn = tk.Button(
                frame_grid_btn,
                text=titulo,
                command=comando,
                bg="#ffffff",
                fg="#1e293b",
                relief=tk.SOLID,
                bd=1,
                font=("Segoe UI", 8, "bold"),
                padx=6,
                pady=6,
                cursor="hand2"
            )
            btn.grid(row=r, column=c, padx=3, pady=3, sticky="ew")
            frame_grid_btn.columnconfigure(c, weight=1)

        # Área de registro de eventos (Log)
        lbl_log = tk.Label(self, text="Registro de Eventos y Respuestas de Diálogos (Clic derecho aquí para menú contextual):", bg="#f8fafc", font=("Segoe UI", 9, "bold"), fg="#475569")
        lbl_log.pack(anchor="w", padx=15, pady=(10, 4))

        self.txt_log = tk.Text(self, bg="#ffffff", font=("Consolas", 9), relief=tk.SOLID, bd=1, padx=8, pady=8)
        self.txt_log.pack(fill=tk.BOTH, expand=True, padx=15, pady=(0, 15))

        # Enlazar menú contextual al área de texto (clic derecho)
        self.txt_log.bind("<Button-3>", self.mostrar_menu_contextual)

    def mostrar_menu_contextual(self, event):
        try:
            self.menu_popup.tk_popup(event.x_root, event.y_root)
        finally:
            self.menu_popup.grab_release()

    def registrar_accion(self, texto):
        self.txt_log.insert(tk.END, f">> {texto}\n")
        self.txt_log.see(tk.END)

    def limpiar_log(self):
        self.txt_log.delete("1.0", tk.END)

    def dialogo_confirmacion(self):
        resp = messagebox.askyesno("Confirmación Requerida", "¿Deseas guardar los cambios pendientes antes de continuar?")
        self.registrar_accion(f"Resultado confirmación: {'SÍ (Aceptó)' if resp else 'NO (Canceló)'}")

    def dialogo_abrir_archivo(self):
        archivo = filedialog.askopenfilename(
            title="Seleccionar archivo",
            filetypes=[("Archivos de Texto", "*.txt"), ("Archivos Python", "*.py"), ("Todos los archivos", "*.*")]
        )
        if archivo:
            self.registrar_accion(f"Archivo abierto: {archivo}")

    def dialogo_guardar_archivo(self):
        archivo = filedialog.asksaveasfilename(
            title="Guardar archivo",
            defaultextension=".txt",
            filetypes=[("Archivos de Texto", "*.txt"), ("Todos los archivos", "*.*")]
        )
        if archivo:
            self.registrar_accion(f"Guardado en: {archivo}")

    def dialogo_abrir_carpeta(self):
        carpeta = filedialog.askdirectory(title="Seleccionar directorio de trabajo")
        if carpeta:
            self.registrar_accion(f"Carpeta seleccionada: {carpeta}")

    def dialogo_color(self):
        color = colorchooser.askcolor(title="Selecciona un color")[1]
        if color:
            self.registrar_accion(f"Color hexadecimal seleccionado: {color}")

    def dialogo_pedir_texto(self):
        nombre = simpledialog.askstring("Entrada de Texto", "¿Cuál es tu nombre de usuario?")
        if nombre:
            self.registrar_accion(f"Texto ingresado: '{nombre}'")

    def dialogo_pedir_numero(self):
        edad = simpledialog.askinteger("Entrada Numérica", "Ingresa tu edad (entre 0 y 120):", minvalue=0, maxvalue=120)
        if edad is not None:
            self.registrar_accion(f"Número ingresado: {edad}")

    def abrir_modal_personalizado(self):
        # Crear ventana secundaria modal
        modal = tk.Toplevel(self)
        modal.title("Diálogo Modal Personalizado")
        modal.geometry("380x220")
        modal.resizable(False, False)
        modal.transient(self)      # Asociada a la ventana padre
        modal.grab_set()           # Bloquea interacciones con la ventana principal mientras esté abierta

        # Centrar respecto a la ventana padre
        modal.config(bg="#ffffff", padx=20, pady=20)

        tk.Label(modal, text="⚙️ Configuración Rápida", font=("Segoe UI", 12, "bold"), bg="#ffffff").pack(anchor="w")
        tk.Label(modal, text="Este es un diálogo Toplevel modal con grab_set().\nNo permite hacer clic en la ventana principal.", bg="#ffffff", fg="#64748b", font=("Segoe UI", 9)).pack(anchor="w", pady=(4, 15))

        entry = tk.Entry(modal, relief=tk.SOLID, bd=1, font=("Segoe UI", 10))
        entry.insert(0, "Parámetro personalizado")
        entry.pack(fill=tk.X, pady=(0, 15))

        def cerrar():
            valor = entry.get()
            self.registrar_accion(f"Modal cerrado con valor: '{valor}'")
            modal.destroy()

        btn = tk.Button(modal, text="Guardar y Cerrar", command=cerrar, bg="#2563eb", fg="white", relief=tk.FLAT, font=("Segoe UI", 9, "bold"), pady=6)
        btn.pack(fill=tk.X)

    def toggle_modo(self):
        oscuro = self.var_modo_oscuro.get()
        bg_color = "#1e293b" if oscuro else "#ffffff"
        fg_color = "#f8fafc" if oscuro else "#000000"
        self.txt_log.config(bg=bg_color, fg=fg_color)
        self.registrar_accion(f"Modo oscuro {'activado' if oscuro else 'desactivado'}")

    def confirmar_salida(self):
        if messagebox.askokcancel("Salir", "¿Realmente deseas cerrar la aplicación?"):
            self.destroy()


if __name__ == "__main__":
    app = DemoMenusYDialogos()
    app.mainloop()
