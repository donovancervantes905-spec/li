"""
06_eventos_y_atajos_teclado.py
------------------------------
Explica y demuestra el sistema de eventos de Tkinter:
  - Enlace de eventos con widget.bind(secuencia, manejador)
  - Eventos de ratón:
      * Clic izquierdo (<Button-1>), Doble clic (<Double-Button-1>)
      * Movimiento con botón presionado (<B1-Motion>)
      * Cursor entra / sale de un área (<Enter>, <Leave>)
      * Rueda de desplazamiento (<MouseWheel>)
  - Eventos de teclado:
      * Teclas generales (<Key>), teclas especiales (<Return>, <Escape>)
      * Atajos combinados (<Control-Shift-A>)
  - Eventos de ventana:
      * Redimensionamiento de ventana (<Configure>)
      * Cierre de ventana (protocol("WM_DELETE_WINDOW"))
  - Telemetría en vivo del objeto Event (x, y, keysym, keycode, delta, widget)
"""

import tkinter as tk
from tkinter import messagebox


class DemoEventos(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("06 - Manejo de Eventos y Atajos de Teclado")
        self.geometry("780x640")
        self.minsize(620, 500)
        self.config(bg="#f1f5f9")

        self.construir_ui()
        self.configurar_eventos()

    def construir_ui(self):
        # Header
        frame_head = tk.Frame(self, bg="#1e293b", padx=15, pady=12)
        frame_head.pack(fill=tk.X)

        tk.Label(frame_head, text="⚡ Inspector de Eventos en Tiempo Real", font=("Segoe UI", 14, "bold"), fg="#ffffff", bg="#1e293b").pack(anchor="w")
        tk.Label(frame_head, text="Interactúa con la zona interactiva o presiona teclas para inspeccionar los eventos.", font=("Segoe UI", 9), fg="#94a3b8", bg="#1e293b").pack(anchor="w")

        # Contenedor superior interactivo
        frame_interactivo = tk.Frame(self, bg="#f1f5f9", padx=15, pady=12)
        frame_interactivo.pack(fill=tk.X)

        # Pad interactivo para el ratón
        self.pad_raton = tk.Label(
            frame_interactivo,
            text="🎯 Zona de Pruebas de Ratón\n\n• Clic normal / Doble clic\n• Arrastra el ratón\n• Pasa el cursor por aquí\n• Usa la rueda del ratón",
            bg="#e2e8f0",
            fg="#334155",
            font=("Segoe UI", 10, "bold"),
            relief=tk.RIDGE,
            bd=2,
            height=7,
            cursor="crosshair"
        )
        self.pad_raton.pack(fill=tk.X, pady=(0, 10))

        # Campo de entrada para pruebas de teclado
        frame_input = tk.Frame(frame_interactivo, bg="#f1f5f9")
        frame_input.pack(fill=tk.X)

        tk.Label(frame_input, text="Entrada de prueba de teclado:", bg="#f1f5f9", font=("Segoe UI", 9, "bold")).pack(side=tk.LEFT, padx=(0, 8))
        self.entry_teclado = tk.Entry(frame_input, font=("Consolas", 10), relief=tk.SOLID, bd=1)
        self.entry_teclado.pack(side=tk.LEFT, fill=tk.X, expand=True)
        self.entry_teclado.insert(0, "Presiona teclas aquí o usa Ctrl+Shift+A")

        # Telemetría del evento actual
        frame_telemetria = tk.LabelFrame(self, text=" Propiedades del Último Evento (Objeto tk.Event) ", font=("Segoe UI", 9, "bold"), bg="#ffffff", padx=12, pady=8)
        frame_telemetria.pack(fill=tk.X, padx=15, pady=6)

        self.var_tipo = tk.StringVar(value="-")
        self.var_coords = tk.StringVar(value="-")
        self.var_tecla = tk.StringVar(value="-")
        self.var_widget = tk.StringVar(value="-")

        grid_params = [
            ("Tipo de Evento:", self.var_tipo),
            ("Coordenadas (x, y):", self.var_coords),
            ("Tecla (keysym / code):", self.var_tecla),
            ("Widget Origen:", self.var_widget),
        ]

        for i, (label_t, var) in enumerate(grid_params):
            r = i // 2
            c = (i % 2) * 2
            tk.Label(frame_telemetria, text=label_t, font=("Segoe UI", 8, "bold"), bg="#ffffff", fg="#64748b").grid(row=r, column=c, sticky="w", padx=5, pady=2)
            tk.Label(frame_telemetria, textvariable=var, font=("Consolas", 9), bg="#ffffff", fg="#0f172a").grid(row=r, column=c+1, sticky="w", padx=5, pady=2)

        # Bitácora de eventos
        lbl_log = tk.Label(self, text="Historial de Eventos Capturados:", bg="#f1f5f9", font=("Segoe UI", 9, "bold"), fg="#334155")
        lbl_log.pack(anchor="w", padx=15, pady=(8, 2))

        self.txt_log = tk.Text(self, bg="#ffffff", font=("Consolas", 9), relief=tk.SOLID, bd=1, height=8)
        self.txt_log.pack(fill=tk.BOTH, expand=True, padx=15, pady=(0, 10))

    def configurar_eventos(self):
        # Eventos de ratón sobre el pad
        self.pad_raton.bind("<Button-1>", lambda e: self.procesar_evento("Clic Izquierdo (<Button-1>)", e))
        self.pad_raton.bind("<Double-Button-1>", lambda e: self.procesar_evento("Doble Clic (<Double-Button-1>)", e))
        self.pad_raton.bind("<B1-Motion>", lambda e: self.procesar_evento("Arrastre (<B1-Motion>)", e))
        self.pad_raton.bind("<Enter>", lambda e: self.al_entrar(e))
        self.pad_raton.bind("<Leave>", lambda e: self.al_salir(e))
        self.pad_raton.bind("<MouseWheel>", lambda e: self.al_rueda(e))

        # Eventos de teclado sobre el campo
        self.entry_teclado.bind("<KeyPress>", lambda e: self.procesar_evento(f"Tecla Presionada ({e.keysym})", e))
        self.entry_teclado.bind("<Return>", lambda e: self.procesar_evento("Enter (<Return>)", e))
        self.entry_teclado.bind("<Escape>", lambda e: self.entry_teclado.delete(0, tk.END))

        # Atajo global en la ventana: Ctrl+Shift+A
        self.bind("<Control-Shift-A>", lambda e: self.procesar_evento("Atajo Especial: Ctrl+Shift+A", e))

        # Evento de cambio de tamaño de la ventana
        self.bind("<Configure>", self.al_redimensionar)

        # Protocolo de cierre de ventana
        self.protocol("WM_DELETE_WINDOW", self.al_cerrar_ventana)

    def procesar_evento(self, descripcion, event):
        self.var_tipo.set(descripcion)
        self.var_coords.set(f"x={event.x}, y={event.y} (Pantalla: {getattr(event, 'x_root', '-')}, {getattr(event, 'y_root', '-')})")
        tecla_str = f"char='{event.char}' | sym='{event.keysym}' | code={event.keycode}" if event.keysym != "??" else "N/A (Ratón)"
        self.var_tecla.set(tecla_str)
        self.var_widget.set(str(event.widget))

        self.txt_log.insert(tk.END, f"[{descripcion}] en ({event.x}, {event.y})\n")
        self.txt_log.see(tk.END)

    def al_entrar(self, event):
        self.pad_raton.config(bg="#dbeafe", text="¡El cursor está DENTRO de la zona!")
        self.procesar_evento("Cursor Entró (<Enter>)", event)

    def al_salir(self, event):
        self.pad_raton.config(bg="#e2e8f0", text="🎯 Zona de Pruebas de Ratón\n\n• Clic normal / Doble clic\n• Arrastra el ratón\n• Pasa el cursor por aquí\n• Usa la rueda del ratón")
        self.procesar_evento("Cursor Salió (<Leave>)", event)

    def al_rueda(self, event):
        delta = event.delta
        self.procesar_evento(f"Rueda Ratón (<MouseWheel>) delta={delta}", event)

    def al_redimensionar(self, event):
        # Filtrar solo eventos de la ventana principal
        if event.widget == self:
            pass  # Podrías registrar: f"Ventana reconfigurada: {event.width}x{event.height}"

    def al_cerrar_ventana(self):
        # Demostración del protocolo WM_DELETE_WINDOW
        if messagebox.askyesno("Confirmación de salida", "¿Deseas cerrar el inspector de eventos?"):
            self.destroy()


if __name__ == "__main__":
    app = DemoEventos()
    app.mainloop()
