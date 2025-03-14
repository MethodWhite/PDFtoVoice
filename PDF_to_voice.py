import tkinter as tk
from tkinter import ttk, filedialog, messagebox
import PyPDF2
from gtts import gTTS
import threading
import re

class PDFtoMP3Converter:
    def __init__(self, root):
        self.root = root
        self.root.title("Conversor de PDF a MP3")
        self.root.geometry("500x200")
        
        # Variables
        self.language = tk.StringVar(value='es')
        self.progress = tk.DoubleVar()
        self.progress.set(0)
        
        # Interfaz gráfica
        self.create_widgets()
        
    def create_widgets(self):
        # Marco principal
        main_frame = ttk.Frame(self.root, padding="20")
        main_frame.pack(fill=tk.BOTH, expand=True)
        
        # Botón de selección
        self.btn_select = ttk.Button(
            main_frame,
            text="Seleccionar PDF",
            command=self.select_pdf
        )
        self.btn_select.grid(row=0, column=0, pady=10, sticky=tk.W)
        
        # Selector de idioma
        ttk.Label(main_frame, text="Idioma:").grid(row=1, column=0, sticky=tk.W)
        self.language_combo = ttk.Combobox(
            main_frame,
            textvariable=self.language,
            values=['es', 'en', 'fr', 'de', 'it'],
            state="readonly",
            width=7
        )
        self.language_combo.grid(row=1, column=0, pady=5, sticky=tk.E)
        
        # Barra de progreso
        self.progress_bar = ttk.Progressbar(
            main_frame,
            variable=self.progress,
            maximum=100,
            mode='determinate'
        )
        self.progress_bar.grid(row=2, column=0, pady=10, sticky=tk.EW)
        
        # Etiqueta de estado
        self.status_label = ttk.Label(main_frame, text="")
        self.status_label.grid(row=3, column=0, pady=5, sticky=tk.W)
        
        # Configurar grid
        main_frame.columnconfigure(0, weight=1)
        
    def select_pdf(self):
        file_path = filedialog.askopenfilename(
            filetypes=[("PDF Files", "*.pdf")]
        )
        if file_path:
            output_path = filedialog.asksaveasfilename(
                defaultextension=".mp3",
                initialfile=file_path.replace('.pdf', '.mp3'),
                filetypes=[("MP3 Files", "*.mp3")]
            )
            if output_path:
                self.start_conversion(file_path, output_path)
                
    def start_conversion(self, pdf_path, output_path):
        self.btn_select.config(state=tk.DISABLED)
        self.status_label.config(text="Procesando...")
        self.progress.set(0)
        
        # Iniciar hilo de conversión
        thread = threading.Thread(
            target=self.convert_pdf,
            args=(pdf_path, output_path),
            daemon=True
        )
        thread.start()
        self.monitor_thread(thread)
        
    def monitor_thread(self, thread):
        if thread.is_alive():
            self.root.after(100, lambda: self.monitor_thread(thread))
        else:
            self.btn_select.config(state=tk.NORMAL)
            
    def convert_pdf(self, pdf_path, output_path):
        try:
            # Extraer texto del PDF
            text = self.extract_text(pdf_path)
            if not text:
                raise ValueError("El PDF no contiene texto extraíble")
            
            # Limpiar texto
            text = self.clean_text(text)
            
            # Convertir texto a audio
            self.update_progress(30)
            tts = gTTS(text, lang=self.language.get())
            
            # Guardar archivo
            self.update_progress(70)
            tts.save(output_path)
            
            # Actualizar interfaz
            self.show_success(output_path)
            self.update_progress(100)
            
        except Exception as e:
            self.show_error(str(e))
            self.update_progress(0)
            
    def extract_text(self, pdf_path):
        text = ""
        with open(pdf_path, 'rb') as file:
            reader = PyPDF2.PdfReader(file)
            total_pages = len(reader.pages)
            
            for i, page in enumerate(reader.pages):
                text += page.extract_text()
                # Actualizar progreso basado en páginas procesadas
                self.progress.set((i + 1) / total_pages * 30)
                
        return text
        
    def clean_text(self, text):
        # Eliminar espacios múltiples y caracteres especiales
        text = re.sub(r'\s+', ' ', text).strip()
        return text
        
    def update_progress(self, value):
        self.root.after(0, lambda: self.progress.set(value))
        
    def show_success(self, output_path):
        self.root.after(0, lambda: messagebox.showinfo(
            "Éxito",
            f"Archivo MP3 generado con éxito:\n{output_path}"
        ))
        self.root.after(0, lambda: self.status_label.config(text="Conversión completada"))
        
    def show_error(self, message):
        self.root.after(0, lambda: messagebox.showerror(
            "Error",
            f"Se produjo un error:\n{message}"
        ))
        self.root.after(0, lambda: self.status_label.config(text="Error en la conversión"))

if __name__ == "__main__":
    root = tk.Tk()
    app = PDFtoMP3Converter(root)
    root.mainloop()
