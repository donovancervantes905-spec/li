"""
07_hilos_y_asincronia_after.py
------------------------------
Demuestra cómo evitar que la interfaz gráfica (GUI) se congele:
  1. El error común: Ejecutar tareas pesadas (time.sleep, llamadas HTTP, cálculos)
     directamente en el hilo principal bloquea el bucle de eventos mainloop().
  2. Uso de root.after(ms, callback): Ejecución diferida o periódica sin bloquear.
  3. Uso de hilos concurrentes (threading.Thread): Ejecución en segundo plano.
  4. Comunicación segura entre hilos y la GUI mediante colas (queue.Queue).
"""

import tkinter as tk
from tkinter import ttk, messagebox
import threading
import queue
import time


class DemoAsincronia(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("07 - Hilos (Threading), Asincronía y after() en Tkinter")
        self.geometry("740x620")
        self.minsize(620, 500)
        self.config(bg="#f8fafc")

        # Cola thread-safe para comunicar el hilo de fondo con el hilo principal
        self.cola_mensajes = queue.Queue()

        self.contador_reloj = 0
        self.construir_ui()

        # Iniciar verificación periódica de la cola
        self.revisar_cola()

        # Iniciar reloj animado continuo para evidenciar si la UI se congela
        self.actualizar_reloj()

    def construir_ui(self):
        # Header
        frame_head = tk.Frame(self, bg="#0f172a", padx=15, pady=12)
        frame_head.pack(fill=tk.X)

        tk.Label(frame_head, text="🧵 Concurrencia y Prevención de Congelamiento", font=("Segoe UI", 14, "bold"), fg="#ffffff", bg="#0f172a").pack(anchor="w")
        tk.Label(frame_head, text="Aprende a ejecutar procesos largos en segundo plano sin congelar la ventana.", font=("Segoe UI", 9), fg="#94a3b8", bg="#0f172a").pack(anchor="w")

        # Monitor de Fluidez (Reloj activo que demuestra si la UI se congela)
        frame_monitor = tk.Frame(self, bg="#e2e8f0", padx=15, pady=10)
        frame_monitor.pack(fill=tk.X, padx=15, pady=(15, 10))

        tk.Label(frame_monitor, text="⏱️ Monitor de Fluidez de la GUI:", bg="#e2e8f0", font=("Segoe UI", 10, "bold"), fg="#1e293b").pack(side=tk.LEFT)
        self.lbl_reloj = tk.Label(frame_monitor, text="0.0s", bg="#ffffff", fg="#2563eb", font=("Consolas", 11, "bold"), padx=10, pady=4, relief=tk.SOLID, bd=1)
        self.lbl_reloj.pack(side=tk.LEFT, padx=10)

        tk.Label(frame_monitor, text="(Si este contador se detiene, la interfaz está congelada)", bg="#e2e8f0", fg="#64748b", font=("Segoe UI", 9, "italic")).pack(side=tk.LEFT)

        # Panel de Pruebas Comparativas
        frame_comparativa = tk.Frame(self, bg="#f8fafc", padx=15)
        frame_comparativa.pack(fill=tk.X)

        # Caso A: Modo bloqueante
        box_malo = tk.LabelFrame(frame_comparativa, text=" ❌ Caso Incorrecto: Tarea en Hilo Principal ", font=("Segoe UI", 9, "bold"), fg="#b91c1c", bg="#ffffff", padx=12, pady=12)
        box_malo.pack(fill=tk.X, pady=6)

        tk.Label(box_malo, text="Ejecuta un bucle con time.sleep(5) directamente en el mainloop.\nNotarás que la ventana deja de responder inmediatamente.", justify=tk.LEFT, bg="#ffffff", font=("Segoe UI", 9)).pack(anchor="w", pady=(0, 8))

        btn_bloquear = tk.Button(box_malo, text="Ejecutar Bloqueo (5 seg)", command=self.tarea_bloqueante, bg="#ef4444", fg="white", font=("Segoe UI", 9, "bold"), relief=tk.FLAT, padx=10, pady=6, cursor="hand2")
        btn_bloquear.pack(anchor="w")

        # Caso B: Modo no bloqueante con Hilo + Queue
        box_bueno = tk.LabelFrame(frame_comparativa, text=" ✅ Caso Correcto: Tarea con threading.Thread + Queue ", font=("Segoe UI", 9, "bold"), fg="#15803d", bg="#ffffff", padx=12, pady=12)
        box_bueno.pack(fill=tk.X, pady=6)

        tk.Label(box_bueno, text="Ejecuta la tarea en un hilo paralelo. El progreso se envía de forma segura\na la interfaz a través de una cola queue.Queue sin congelar nada.", justify=tk.LEFT, bg="#ffffff", font=("Segoe UI", 9)).pack(anchor="w", pady=(0, 8))

        frame_accion_buena = tk.Frame(box_bueno, bg="#ffffff")
        frame_accion_buena.pack(fill=tk.X)

        self.btn_hilo = tk.Button(frame_accion_buena, text="Iniciar Tarea en Hilo de Fondo", command=self.iniciar_tarea_segundo_plano, bg="#10b981", fg="white", font=("Segoe UI", 9, "bold"), relief=tk.FLAT, padx=10, pady=6, cursor="hand2")
        self.btn_hilo.pack(side=tk.LEFT)

        self.progreso = ttk.Progressbar(frame_accion_buena, orient="horizontal", mode="determinate", length=220)
        self.progreso.pack(side=tk.LEFT, padx=15)

        self.lbl_estado = tk.Label(frame_accion_buena, text="Listo.", bg="#ffffff", font=("Segoe UI", 9), fg="#475569")
        self.lbl_estado.pack(side=tk.LEFT)

        # Consola de salida
        tk.Label(self, text="Registro de Eventos:", bg="#f8fafc", font=("Segoe UI", 9, "bold"), fg="#334155").pack(anchor="w", padx=15, pady=(10, 2))
        self.txt_log = tk.Text(self, bg="#ffffff", font=("Consolas", 9), height=7, relief=tk.SOLID, bd=1)
        self.txt_log.pack(fill=tk.BOTH, expand=True, padx=15, pady=(0, 15))

    def log(self, texto):
        self.txt_log.insert(tk.END, f"{texto}\n")
        self.txt_log.see(tk.END)

    def actualizar_reloj(self):
        """Usa after() para actualizar un contador cada 100ms sin trabar la UI."""
        self.contador_reloj += 0.1
        self.lbl_reloj.config(text=f"{self.contador_reloj:.1f}s")
        self.after(100, self.actualizar_reloj)

    def tarea_bloqueante(self):
        """Ejemplo de lo que NO se debe hacer: congela la UI por 5 segundos."""
        self.log("⚠️ Iniciando tarea bloqueante (time.sleep)...")
        self.update_idletasks()  # Forzar refresco inmediato antes del bloqueo
        time.sleep(5)            # ¡Bloquea la UI por completo!
        self.log("❌ Tarea bloqueante terminada. La UI recuperó el control.")

    def iniciar_tarea_segundo_plano(self):
        """Inicia un hilo independiente (daemon) para realizar un proceso largo."""
        self.btn_hilo.config(state=tk.DISABLED)
        self.progreso["value"] = 0
        self.lbl_estado.config(text="Procesando en paralelo...")
        self.log("🚀 Hilo en segundo plano iniciado. La GUI continúa fluida e interactiva.")

        # Iniciar hilo de trabajo
        hilo = threading.Thread(target=self.proceso_largo_trabajador, daemon=True)
        hilo.start()

    def proceso_largo_trabajador(self):
        """Esta función se ejecuta en el HILO SECUNDARIO."""
        total_pasos = 10
        for paso in range(1, total_pasos + 1):
            time.sleep(0.5)  # Simula trabajo intensivo o descarga de red
            porcentaje = int((paso / total_pasos) * 100)
            # Enviar mensaje a la cola (¡No modificar widgets de Tkinter directamente aquí!)
            self.cola_mensajes.put(("PROGRESO", porcentaje, f"Paso {paso} de {total_pasos} completado."))

        self.cola_mensajes.put(("FINALIZADO", 100, "¡Trabajo completado exitosamente!"))

    def revisar_cola(self):
        """
        Revisa periódicamente la cola de mensajes en el hilo principal.
        Este es el patrón seguro de concurrencia en Tkinter.
        """
        try:
            while not self.cola_mensajes.empty():
                tipo, valor, mensaje = self.cola_mensajes.get_nowait()
                if tipo == "PROGRESO":
                    self.progreso["value"] = valor
                    self.lbl_estado.config(text=f"{valor}%")
                    self.log(f"Hilo -> {mensaje}")
                elif tipo == "FINALIZADO":
                    self.progreso["value"] = 100
                    self.lbl_estado.config(text="¡Completado!")
                    self.btn_hilo.config(state=tk.NORMAL)
                    self.log(f"Hilo -> {mensaje}")
                    messagebox.showinfo("Proceso Terminado", "La tarea en segundo plano finalizó exitosamente.")
        except queue.Empty:
            pass

        # Programar la siguiente revisión de la cola en 50 milisegundos
        self.after(50, self.revisar_cola)


if __name__ == "__main__":
    app = DemoAsincronia()
    app.mainloop()
