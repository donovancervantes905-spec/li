"""
08_proyecto_completo_gestor_tareas.py
-------------------------------------
Proyecto Integrador: Gestor de Tareas y Proyectos de Escritorio
Aplica todos los conceptos vistos en los módulos anteriores:
  - Arquitectura Orientada a Objetos modular y escalable
  - Combinación armónica de ttk.Treeview, ttk.Combobox, Frames y Entry
  - Persistencia de datos en disco (formato JSON)
  - Diálogos de confirmación, menús, barra de estado inferior
  - Filtros en tiempo real por búsqueda y categoría
  - Exportación e importación de archivos mediante filedialog
"""

import tkinter as tk
from tkinter import ttk, messagebox, filedialog
import json
import os
from datetime import datetime


ARCHIVO_POR_DEFECTO = "tareas_guardadas.json"


class GestorTareasApp(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("TaskMaster Pro - Gestor de Tareas en Tkinter")
        self.geometry("920x680")
        self.minsize(750, 500)
        self.config(bg="#f8fafc")

        # Modelo de datos interno (lista de diccionarios)
        self.tareas = []
        self.archivo_actual = ARCHIVO_POR_DEFECTO

        self.configurar_estilos()
        self.crear_menu()
        self.construir_ui()
        self.cargar_datos_desde_disco(silencioso=True)

    def configurar_estilos(self):
        self.style = ttk.Style(self)
        if "clam" in self.style.theme_names():
            self.style.theme_use("clam")

        self.style.configure("Treeview.Heading", font=("Segoe UI", 9, "bold"))
        self.style.configure("Treeview", rowheight=26, font=("Segoe UI", 9))
        self.style.map("Treeview", background=[("selected", "#2563eb")], foreground=[("selected", "#ffffff")])

    def crear_menu(self):
        barra_menu = tk.Menu(self)

        menu_archivo = tk.Menu(barra_menu, tearoff=0)
        menu_archivo.add_command(label="Guardar Tareas", accelerator="Ctrl+S", command=self.guardar_datos_en_disco)
        menu_archivo.add_command(label="Exportar a JSON...", command=self.exportar_json)
        menu_archivo.add_command(label="Importar desde JSON...", command=self.importar_json)
        menu_archivo.add_separator()
        menu_archivo.add_command(label="Salir", command=self.destroy)
        barra_menu.add_cascade(label="Archivo", menu=menu_archivo)

        menu_ayuda = tk.Menu(barra_menu, tearoff=0)
        menu_ayuda.add_command(label="Acerca de", command=lambda: messagebox.showinfo("TaskMaster Pro", "Proyecto integral desarrollado con Tkinter y ttk.\nDemostración de arquitectura de escritorio en Python."))
        barra_menu.add_cascade(label="Ayuda", menu=menu_ayuda)

        self.config(menu=barra_menu)
        self.bind("<Control-s>", lambda e: self.guardar_datos_en_disco())

    def construir_ui(self):
        # 1. Cabecera (Header)
        header = tk.Frame(self, bg="#1e293b", padx=20, pady=14)
        header.pack(fill=tk.X)

        tk.Label(header, text="📌 TaskMaster Pro", font=("Segoe UI", 16, "bold"), fg="#ffffff", bg="#1e293b").pack(side=tk.LEFT)
        tk.Label(header, text="Gestor de Tareas y Productividad", font=("Segoe UI", 10), fg="#94a3b8", bg="#1e293b").pack(side=tk.LEFT, padx=(10, 0), pady=(4, 0))

        # 2. Formulario de creación de tareas
        frame_form = tk.LabelFrame(self, text=" Nueva Tarea ", font=("Segoe UI", 9, "bold"), bg="#ffffff", padx=15, pady=10)
        frame_form.pack(fill=tk.X, padx=15, pady=10)

        # Fila 1: Título de tarea
        tk.Label(frame_form, text="Título / Descripción:", bg="#ffffff", font=("Segoe UI", 9)).grid(row=0, column=0, sticky="w", pady=4)
        self.entry_titulo = tk.Entry(frame_form, font=("Segoe UI", 9), relief=tk.SOLID, bd=1)
        self.entry_titulo.grid(row=0, column=1, columnspan=5, sticky="ew", pady=4, padx=(5, 0))
        self.entry_titulo.bind("<Return>", lambda e: self.agregar_tarea())

        # Fila 2: Categoría, Prioridad y Botón Agregar
        tk.Label(frame_form, text="Categoría:", bg="#ffffff", font=("Segoe UI", 9)).grid(row=1, column=0, sticky="w", pady=4)
        self.combo_categoria = ttk.Combobox(frame_form, values=["Trabajo", "Estudio", "Personal", "Finanzas", "Hogar"], state="readonly", width=14)
        self.combo_categoria.current(0)
        self.combo_categoria.grid(row=1, column=1, sticky="w", pady=4, padx=(5, 15))

        tk.Label(frame_form, text="Prioridad:", bg="#ffffff", font=("Segoe UI", 9)).grid(row=1, column=2, sticky="w", pady=4)
        self.combo_prioridad = ttk.Combobox(frame_form, values=["Alta 🔴", "Media 🟡", "Baja 🟢"], state="readonly", width=12)
        self.combo_prioridad.current(1)
        self.combo_prioridad.grid(row=1, column=3, sticky="w", pady=4, padx=(5, 15))

        btn_agregar = tk.Button(frame_form, text="➕ Agregar Tarea", command=self.agregar_tarea, bg="#2563eb", fg="white", font=("Segoe UI", 9, "bold"), relief=tk.FLAT, padx=12, pady=4, cursor="hand2")
        btn_agregar.grid(row=1, column=4, sticky="e", padx=(10, 0))

        frame_form.columnconfigure(1, weight=1)

        # 3. Barra de Búsqueda y Filtros
        frame_filtros = tk.Frame(self, bg="#f8fafc", padx=15)
        frame_filtros.pack(fill=tk.X, pady=(0, 6))

        tk.Label(frame_filtros, text="🔍 Buscar:", bg="#f8fafc", font=("Segoe UI", 9, "bold")).pack(side=tk.LEFT, padx=(0, 5))
        self.var_busqueda = tk.StringVar()
        self.var_busqueda.trace_add("write", lambda *args: self.actualizar_vista_tabla())
        entry_busqueda = tk.Entry(frame_filtros, textvariable=self.var_busqueda, width=22, relief=tk.SOLID, bd=1, font=("Segoe UI", 9))
        entry_busqueda.pack(side=tk.LEFT, padx=(0, 15))

        tk.Label(frame_filtros, text="Filtrar Categoría:", bg="#f8fafc", font=("Segoe UI", 9, "bold")).pack(side=tk.LEFT, padx=(0, 5))
        self.var_filtro_cat = tk.StringVar(value="Todas")
        self.combo_filtro_cat = ttk.Combobox(frame_filtros, values=["Todas", "Trabajo", "Estudio", "Personal", "Finanzas", "Hogar"], state="readonly", width=12, textvariable=self.var_filtro_cat)
        self.combo_filtro_cat.pack(side=tk.LEFT)
        self.combo_filtro_cat.bind("<<ComboboxSelected>>", lambda e: self.actualizar_vista_tabla())

        # Botones de Acción de la Tabla
        btn_eliminar = tk.Button(frame_filtros, text="🗑️ Eliminar", command=self.eliminar_tarea_seleccionada, bg="#ef4444", fg="white", font=("Segoe UI", 8, "bold"), relief=tk.FLAT, padx=8, pady=3, cursor="hand2")
        btn_eliminar.pack(side=tk.RIGHT, padx=4)

        btn_completar = tk.Button(frame_filtros, text="✔️ Alternar Estado", command=self.alternar_estado_tarea, bg="#10b981", fg="white", font=("Segoe UI", 8, "bold"), relief=tk.FLAT, padx=8, pady=3, cursor="hand2")
        btn_completar.pack(side=tk.RIGHT, padx=4)

        # 4. Tabla de Tareas (Treeview)
        frame_tabla = tk.Frame(self, bg="#ffffff", padx=15)
        frame_tabla.pack(fill=tk.BOTH, expand=True, padx=15, pady=(0, 10))

        cols = ("id", "estado", "titulo", "categoria", "prioridad", "fecha")
        self.tree = ttk.Treeview(frame_tabla, columns=cols, show="headings", selectmode="browse")

        self.tree.heading("id", text="#")
        self.tree.heading("estado", text="Estado")
        self.tree.heading("titulo", text="Título")
        self.tree.heading("categoria", text="Categoría")
        self.tree.heading("prioridad", text="Prioridad")
        self.tree.heading("fecha", text="Fecha de Creación")

        self.tree.column("id", width=40, anchor="center")
        self.tree.column("estado", width=100, anchor="center")
        self.tree.column("titulo", width=340, anchor="w")
        self.tree.column("categoria", width=110, anchor="center")
        self.tree.column("prioridad", width=100, anchor="center")
        self.tree.column("fecha", width=130, anchor="center")

        # Scroll vertical
        scroll = ttk.Scrollbar(frame_tabla, orient=tk.VERTICAL, command=self.tree.yview)
        self.tree.configure(yscrollcommand=scroll.set)

        self.tree.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        scroll.pack(side=tk.RIGHT, fill=tk.Y)

        # Configurar colores de fila según estado
        self.tree.tag_configure("completada", foreground="#94a3b8")
        self.tree.tag_configure("pendiente", foreground="#0f172a")

        # 5. Barra de estado inferior (Status bar)
        self.frame_status = tk.Frame(self, bg="#e2e8f0", padx=15, pady=4)
        self.frame_status.pack(fill=tk.X, side=tk.BOTTOM)

        self.lbl_status = tk.Label(self.frame_status, text="Listo.", bg="#e2e8f0", fg="#475569", font=("Segoe UI", 8))
        self.lbl_status.pack(side=tk.LEFT)

        self.lbl_stats = tk.Label(self.frame_status, text="Total: 0 | Pendientes: 0 | Completadas: 0", bg="#e2e8f0", fg="#475569", font=("Segoe UI", 8, "bold"))
        self.lbl_stats.pack(side=tk.RIGHT)

    def agregar_tarea(self):
        titulo = self.entry_titulo.get().strip()
        if not titulo:
            messagebox.showwarning("Campo Vacío", "Por favor ingresa un título para la tarea.")
            return

        nueva_tarea = {
            "id": len(self.tareas) + 1,
            "titulo": titulo,
            "categoria": self.combo_categoria.get(),
            "prioridad": self.combo_prioridad.get(),
            "completada": False,
            "fecha": datetime.now().strftime("%Y-%m-%d %H:%M")
        }

        self.tareas.append(nueva_tarea)
        self.entry_titulo.delete(0, tk.END)
        self.actualizar_vista_tabla()
        self.actualizar_barra_estado(f"Tarea '{titulo}' agregada con éxito.")

    def alternar_estado_tarea(self):
        seleccion = self.tree.selection()
        if not seleccion:
            messagebox.showinfo("Selección", "Selecciona una tarea de la lista para cambiar su estado.")
            return

        item = self.tree.item(seleccion[0])
        tarea_id = item["values"][0]

        for t in self.tareas:
            if t["id"] == tarea_id:
                t["completada"] = not t["completada"]
                estado_str = "Completada" if t["completada"] else "Pendiente"
                self.actualizar_barra_estado(f"Tarea #{tarea_id} marcada como {estado_str}.")
                break

        self.actualizar_vista_tabla()

    def eliminar_tarea_seleccionada(self):
        seleccion = self.tree.selection()
        if not seleccion:
            messagebox.showinfo("Selección", "Selecciona una tarea para eliminar.")
            return

        item = self.tree.item(seleccion[0])
        tarea_id = item["values"][0]
        titulo = item["values"][2]

        if messagebox.askyesno("Confirmar Eliminación", f"¿Estás seguro de eliminar la tarea:\n'{titulo}'?"):
            self.tareas = [t for t in self.tareas if t["id"] != tarea_id]
            self.actualizar_vista_tabla()
            self.actualizar_barra_estado(f"Tarea #{tarea_id} eliminada.")

    def actualizar_vista_tabla(self):
        # Limpiar filas existentes
        for item in self.tree.get_children():
            self.tree.delete(item)

        termino = self.var_busqueda.get().lower().strip()
        filtro_cat = self.var_filtro_cat.get()

        pendientes = 0
        completadas = 0

        for t in self.tareas:
            if t["completada"]:
                completadas += 1
            else:
                pendientes += 1

            # Filtrado por búsqueda
            if termino and termino not in t["titulo"].lower() and termino not in t["categoria"].lower():
                continue

            # Filtrado por categoría
            if filtro_cat != "Todas" and t["categoria"] != filtro_cat:
                continue

            estado_icono = "✅ Hecha" if t["completada"] else "⏳ Pendiente"
            tag = "completada" if t["completada"] else "pendiente"

            self.tree.insert(
                "",
                tk.END,
                values=(t["id"], estado_icono, t["titulo"], t["categoria"], t["prioridad"], t["fecha"]),
                tags=(tag,)
            )

        self.lbl_stats.config(text=f"Total: {len(self.tareas)} | Pendientes: {pendientes} | Completadas: {completadas}")

    def actualizar_barra_estado(self, mensaje):
        self.lbl_status.config(text=mensaje)

    def guardar_datos_en_disco(self):
        try:
            with open(self.archivo_actual, "w", encoding="utf-8") as f:
                json.dump(self.tareas, f, indent=2, ensure_ascii=False)
            self.actualizar_barra_estado(f"Datos guardados exitosamente en '{self.archivo_actual}'.")
            messagebox.showinfo("Guardado", "Tareas guardadas correctamente.")
        except Exception as e:
            messagebox.showerror("Error al guardar", f"No se pudo guardar: {e}")

    def cargar_datos_desde_disco(self, silencioso=False):
        if not os.path.exists(self.archivo_actual):
            # Cargar tareas iniciales de demostración si no existe archivo
            self.tareas = [
                {"id": 1, "titulo": "Diseñar interfaz con Tkinter", "categoria": "Trabajo", "prioridad": "Alta 🔴", "completada": True, "fecha": "2026-10-20 09:30"},
                {"id": 2, "titulo": "Aprender gestión de layouts (grid y pack)", "categoria": "Estudio", "prioridad": "Alta 🔴", "completada": True, "fecha": "2026-10-21 11:15"},
                {"id": 3, "titulo": "Implementar hilos para tareas asíncronas", "categoria": "Trabajo", "prioridad": "Media 🟡", "completada": False, "fecha": "2026-10-22 14:00"},
                {"id": 4, "titulo": "Comprar insumos de oficina", "categoria": "Hogar", "prioridad": "Baja 🟢", "completada": False, "fecha": "2026-10-22 16:45"},
            ]
            self.actualizar_vista_tabla()
            return

        try:
            with open(self.archivo_actual, "r", encoding="utf-8") as f:
                self.tareas = json.load(f)
            self.actualizar_vista_tabla()
            if not silencioso:
                messagebox.showinfo("Cargado", "Tareas cargadas correctamente.")
        except Exception as e:
            if not silencioso:
                messagebox.showerror("Error de Carga", f"No se pudo leer el archivo: {e}")

    def exportar_json(self):
        ruta = filedialog.asksaveasfilename(defaultextension=".json", filetypes=[("Archivos JSON", "*.json")])
        if ruta:
            try:
                with open(ruta, "w", encoding="utf-8") as f:
                    json.dump(self.tareas, f, indent=2, ensure_ascii=False)
                messagebox.showinfo("Exportación Exitosa", f"Archivo exportado a:\n{ruta}")
            except Exception as e:
                messagebox.showerror("Error", f"No se pudo exportar: {e}")

    def importar_json(self):
        ruta = filedialog.askopenfilename(filetypes=[("Archivos JSON", "*.json")])
        if ruta:
            try:
                with open(ruta, "r", encoding="utf-8") as f:
                    datos = json.load(f)
                if isinstance(datos, list):
                    self.tareas = datos
                    self.actualizar_vista_tabla()
                    messagebox.showinfo("Importación Exitosa", f"Se cargaron {len(datos)} tareas.")
                else:
                    messagebox.showerror("Formato Inválido", "El archivo JSON debe contener una lista de tareas.")
            except Exception as e:
                messagebox.showerror("Error", f"No se pudo importar: {e}")


if __name__ == "__main__":
    app = GestorTareasApp()
    app.mainloop()
