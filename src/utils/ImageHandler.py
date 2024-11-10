import tkinter as tk
from tkinter import filedialog

# Función para abrir un diálogo de selección de archivos
def open_file_dialog():
    # Crear una instancia de Tkinter pero no mostrar la ventana principal
    root = tk.Tk()
    root.withdraw()  # Esto oculta la ventana principal de tkinter

    # Abrir el diálogo para seleccionar un archivo
    file_path = filedialog.askopenfilename(
        title="Seleccionar imagen",
        filetypes=[("Image Files", "*.png;*.jpg;*.jpeg;*.bmp")]
    )

    root.destroy()  # Cerrar completamente la ventana de tkinter
    return file_path
