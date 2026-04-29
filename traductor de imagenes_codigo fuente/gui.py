import tkinter as tk
from tkinter import filedialog, messagebox, simpledialog
from PIL import ImageTk, Image
import threading
import cv2
import numpy as np
import os
import re
from logic import reader, TranslatorLogic
from logic_bn import TextSeparator
from exporter import TextExporter

class TraductorApp:
    def __init__(self, root):
        self.root = root
        self.root.title("IA Translator Pro - Modular")
        self.root.geometry("1150x950")
        self.root.configure(bg="#121212")
        
        self.img_pil = None 
        self.historial = [] 
        self.texto_acumulado = [] # Lista para exportar luego
        self.img_display = None
        self.rect = None
        self.start_x = self.start_y = None
        
        self.filtro_bn = TextSeparator()
        self.setup_ui()

        self.memoria_traduccion = {}

    def setup_ui(self):
        self.frame_ctrl = tk.Frame(self.root, bg="#121212")
        self.frame_ctrl.pack(pady=10)
        btn_style = {"font": ("Arial", 10, "bold"), "padx": 15, "pady": 8, "relief": "flat", "fg": "white"}
        
        tk.Button(self.frame_ctrl, text="📂 CARGAR", command=self.load_image, bg="#3d5afe", **btn_style).grid(row=0, column=0, padx=5)
        self.btn_bn = tk.Button(self.frame_ctrl, text="FILTRO B/N: OFF", command=self.toggle_bn, bg="#424242", **btn_style)
        self.btn_bn.grid(row=0, column=1, padx=5)
        tk.Button(self.frame_ctrl, text="🤖 AUTO", command=self.start_auto_process, bg="#673ab7", **btn_style).grid(row=0, column=2, padx=5)
        tk.Button(self.frame_ctrl, text="↩️ DESHACER", command=self.deshacer, bg="#f44336", **btn_style).grid(row=0, column=3, padx=5)
        tk.Button(self.frame_ctrl, text="💾 GUARDAR", command=self.save_image, bg="#00c853", **btn_style).grid(row=0, column=4, padx=5)
        tk.Button(self.frame_ctrl, text="📄 EXPORTAR TXT", command=self.handle_export, bg="#ff9800", **btn_style).grid(row=0, column=5, padx=5)

        self.lbl_status = tk.Label(self.root, text="LISTO", font=("Consolas", 10), fg="#00e676", bg="#1e1e1e", width=110, pady=5)
        self.lbl_status.pack(pady=5)

        self.canvas = tk.Canvas(self.root, bg="#1a1a1a", cursor="cross")
        self.canvas.pack(pady=10, expand=True)
        self.canvas.bind("<ButtonPress-1>", self.on_button_press)
        self.canvas.bind("<B1-Motion>", self.on_move_press)
        self.canvas.bind("<ButtonRelease-1>", self.on_button_release)

    def guardar_estado(self):
        if self.img_pil:
            self.historial.append(self.img_pil.copy())
            
    def undo(self):
        """Recupera el último estado guardado en el historial."""
        if self.historial:
            # Sacamos la última imagen de la lista y la ponemos como la actual
            self.img_pil = self.historial.pop()
            
            if self.memoria_traduccion:
                ultima_clave = list(self.memoria_traduccion.keys())[-1]
                del self.memoria_traduccion[ultima_clave]
            
            self.update_canvas()
            self.log("Acción deshecha")
        else:
            self.log("No hay nada que deshacer")

    def toggle_bn(self):
        activo = self.filtro_bn.toggle()
        self.btn_bn.config(text=f"FILTRO B/N: {'ON' if activo else 'OFF'}", bg="#0277bd" if activo else "#424242")

    def handle_export(self):
        if not self.texto_acumulado:
            self.log("No hay traducciones acumuladas.")
            return
        TextExporter.export_and_open(self.texto_acumulado)

    def auto_run(self):
        self.log("Procesando...")
        img_cv = cv2.cvtColor(np.array(self.img_pil), cv2.COLOR_RGB2BGR)
        results = reader.readtext(img_cv, paragraph=True)
        
        for res in results:
            bbox, text_detected = res[0], res[1]
            
            # 1. Filtro B/N si está activo
            if self.filtro_bn.filtro_activo:
                roi_limpia = self.filtro_bn.aislar_texto(img_cv, bbox)
                res_pro = reader.readtext(roi_limpia)
                text_detected = " ".join([r[1] for r in res_pro]) if res_pro else text_detected

            # 2. Limpieza de puntos suspensivos (Afecta al original que se exportará)
            text_limpio = re.sub(r'_{2,}', '...', text_detected)
            text_limpio = re.sub(r'([a-zA-Z])_', r'\1...', text_limpio)
            
            try:
                # 3. Traducir
                trans = TranslatorLogic.translate_text(text_limpio)
                
                # 4. Mandar a dibujar y guardar en memoria
                box = (int(bbox[0][0]), int(bbox[0][1]), int(bbox[2][0]), int(bbox[2][1]))
                self.root.after(0, lambda o=text_limpio, t=trans, b=box: self.finalizar_dibujo_auto(o, t, b))
            except Exception as e:
                print(f"Error: {e}")

        self.root.after(0, self.update_canvas)
        self.root.after(0, lambda: self.log("Traducción automática finalizada"))

    def finalizar_dibujo_auto(self, original, traducido, box):
        """Dibuja y asegura que el cambio se guarde para la exportación."""
        # Guardamos el par exacto que se acaba de generar
        self.memoria_traduccion[original] = traducido
        
        # Dibujamos en la imagen
        TranslatorLogic.draw_text_on_image(self.img_pil, traducido, box)
        self.update_canvas()

    def process_manual(self, box):
        # Recorte de la imagen PIL
        crop = self.img_pil.crop(box)
        cv_crop = cv2.cvtColor(np.array(crop), cv2.COLOR_RGB2BGR)
        
        if self.filtro_bn.filtro_activo:
            cv_crop = self.filtro_bn.aislar_texto(cv_crop, [[0,0],[0,0],[cv_crop.shape[1], cv_crop.shape[0]]])

        # OCR: Leemos el texto
        res = reader.readtext(cv_crop)
        text_detected = " ".join([r[1] for r in res]) if res else ""
        
        # Limpieza de puntos suspensivos (...) y guiones (_)
        text_limpio = re.sub(r'_{2,}', '...', text_detected)
        text_limpio = re.sub(r'([a-zA-Z])_', r'\1...', text_limpio)
        
        # Traducción inicial
        try:
            trans_inicial = GoogleTranslator(source='auto', target='es').translate(text_limpio) if text_limpio else ""
        except:
            trans_inicial = ""

        # LLAMADA A LA VENTANA (Debe ser en el hilo principal con .after)
        self.root.after(0, lambda: self.abrir_editor_texto(text_limpio, trans_inicial, box))

    def update_canvas(self):
        if not self.img_pil: return
        img_rs = self.img_pil.copy()
        img_rs.thumbnail((950, 750))
        self.img_display = ImageTk.PhotoImage(img_rs)
        self.canvas.config(width=img_rs.width, height=img_rs.height)
        self.canvas.delete("all")
        self.canvas.create_image(0, 0, anchor=tk.NW, image=self.img_display)

    def log(self, mensaje): self.lbl_status.config(text=f">> {mensaje.upper()}")
    
    def load_image(self):
        path = filedialog.askopenfilename()
        if path:
            self.img_pil = Image.open(path).convert("RGB")
            # Reiniciar todo para la nueva imagen
            self.texto_acumulado = [] 
            self.memoria_traduccion = {}
            self.historial = []
            self.update_canvas()
    
    def save_image(self):
        if self.img_pil: 
            path = filedialog.asksaveasfilename(defaultextension=".png")
            if path: self.img_pil.save(path)

    def start_auto_process(self):
        if self.img_pil: self.guardar_estado(); threading.Thread(target=self.auto_run, daemon=True).start()

    def deshacer(self):
        if self.historial: self.img_pil = self.historial.pop(); self.update_canvas()

    def on_button_press(self, event):
        self.start_x, self.start_y = self.canvas.canvasx(event.x), self.canvas.canvasy(event.y)
        self.rect = self.canvas.create_rectangle(self.start_x, self.start_y, self.start_x, self.start_y, outline='#00ffff')

    def on_move_press(self, event):
        self.canvas.coords(self.rect, self.start_x, self.start_y, self.canvas.canvasx(event.x), self.canvas.canvasy(event.y))

    def on_button_release(self, event):
        if self.rect:
            # Obtener coordenadas del rectángulo dibujado en el canvas
            coords = self.canvas.coords(self.rect)
            if coords:
                x1, y1, x2, y2 = coords
                box = self.get_image_coordinates(x1, y1, x2, y2)
                # Lanzar el proceso en un hilo para que la ventana no se congele
                import threading
                threading.Thread(target=self.process_manual, args=(box,), daemon=True).start()
            
            self.canvas.delete(self.rect)
            self.rect = None

    def get_image_coordinates(self, x1, y1, x2, y2):
        """Convierte las coordenadas del Canvas a las coordenadas reales de la imagen."""
        # Obtenemos el tamaño del Canvas y de la imagen cargada
        canvas_width = self.canvas.winfo_width()
        canvas_height = self.canvas.winfo_height()
        img_width, img_height = self.img_pil.size

        # Calculamos la escala (asumiendo que la imagen se ajusta al canvas)
        scale_x = img_width / canvas_width
        scale_y = img_height / canvas_height

        # Ajustamos las coordenadas
        real_x1 = int(min(x1, x2) * scale_x)
        real_y1 = int(min(y1, y2) * scale_y)
        real_x2 = int(max(x1, x2) * scale_x)
        real_y2 = int(max(y1, y2) * scale_y)

        return (real_x1, real_y1, real_x2, real_y2)

    def finalizar_dibujo(self, texto, box):
        TranslatorLogic.draw_text_on_image(self.img_pil, texto, box)
        self.texto_acumulado.append(texto) # Guardamos la traducción manual
        self.update_canvas()
    
    def handle_export(self):
        """Genera el TXT con todo lo acumulado (Manual y Automático)."""
        if not self.memoria_traduccion:
            self.log("Nada que exportar.")
            return
            
        datos_finales = []
        for orig, trad in self.memoria_traduccion.items():
            datos_finales.append({
                'original': orig,
                'traducido': trad
            })
            
        # Llamar al exportador
        TextExporter.export_and_open(datos_finales)
        self.log("Exportación bilingüe completada.")

    def _run_export_logic(self):
        try:
            img_cv = cv2.cvtColor(np.array(self.img_pil), cv2.COLOR_RGB2BGR)
            results = reader.readtext(img_cv, paragraph=True)
            
            # Extraemos solo el texto de los resultados del OCR
            textos_detectados = [res[1] for res in results]
            
            # Llamamos al nuevo módulo
            self.root.after(0, lambda: TextExporter.export_to_txt(textos_detectados))
            self.root.after(0, lambda: self.log("Exportación finalizada"))
        except Exception as e:
            self.root.after(0, lambda: self.log(f"Error al exportar: {e}"))
    
    def handle_export(self):
        """Exporta el estado actual de la memoria (Original + Traducido)."""
        if not self.memoria_traduccion:
            self.log("No hay datos detectados para exportar.")
            return
            
        # Convertimos el diccionario en el formato que espera el exportador
        datos_a_exportar = []
        for orig, trad in self.memoria_traduccion.items():
            datos_a_exportar.append({
                'original': orig,
                'traducido': trad
            })
            
        TextExporter.export_and_open(datos_a_exportar)
        self.log("TXT actualizado con todos los cambios.")

    def _run_quick_export(self):
        img_cv = cv2.cvtColor(np.array(self.img_pil), cv2.COLOR_RGB2BGR)
        results = reader.readtext(img_cv, paragraph=True)
        textos = [res[1] for res in results]
        from exporter import TextExporter
        self.root.after(0, lambda: TextExporter.export_and_open(textos))
    
    def abrir_editor_texto(self, original, traducido, box):
        ventana = tk.Toplevel(self.root)
        ventana.title("Editar Texto")
        ventana.geometry("400x350")
        ventana.attributes("-topmost", True) # Asegura que salga por encima

        tk.Label(ventana, text="Texto detectado:").pack()
        txt_orig = tk.Text(ventana, height=4, width=40)
        txt_orig.insert("1.0", original)
        txt_orig.pack(pady=5)

        tk.Label(ventana, text="Traducción:").pack()
        txt_trad = tk.Text(ventana, height=4, width=40)
        txt_trad.insert("1.0", traducido)
        txt_trad.pack(pady=5)

        def guardar():
            final_orig = txt_orig.get("1.0", "end-1c").strip()
            final_trad = txt_trad.get("1.0", "end-1c").strip()
            
            # Guardamos una copia de la imagen ANTES de pintarla
            self.historial.append(self.img_pil.copy())
            # ---------------------------

            self.memoria_traduccion[final_orig] = final_trad
            
            # Dibujamos el texto
            TranslatorLogic.draw_text_on_image(self.img_pil, final_trad, box)
            
            self.update_canvas()
            ventana.destroy()

        tk.Button(ventana, text="Aceptar y Pegar", command=guardar).pack()