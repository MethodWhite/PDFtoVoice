import tkinter as tk
from tkinter import filedialog, messagebox
import PyPDF2
from gtts import gTTS

def seleccionar_archivo():
    file_path = filedialog.askopenfilename(filetypes=[("PDF Files", "*.pdf")])
    if file_path:
        generar_audio(file_path)

def generar_audio(pdf_file):
    try:
        with open(pdf_file, 'rb') as file:
            reader = PyPDF2.PdfReader(file)
            num_pages = len(reader.pages)
            text = ""

            for page_num in range(num_pages):
                page = reader.pages[page_num]
                text += page.extract_text()

        output_file = pdf_file.replace('.pdf', '.mp3')
        tts = gTTS(text, lang='es')
        tts.save(output_file)

        messagebox.showinfo("Éxito", f"Archivo MP3 generado con éxito:\n{output_file}")
    except Exception as e:
        messagebox.showerror("Error", f"Se produjo un error al generar el archivo MP3:\n{e}")

# Configuración de la ventana de Tkinter
root = tk.Tk()
root.title("Conversor de PDF a MP3")
root.geometry("400x150")

boton_seleccionar = tk.Button(root, text="Seleccionar PDF", command=seleccionar_archivo)
boton_seleccionar.pack(pady=20)

root.mainloop()
