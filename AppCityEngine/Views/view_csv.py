import tkinter as tk
from tkinter import ttk, filedialog, messagebox
import os
from AppCityEngine.Component.generarRegla import GenerarCGA
import shutil

# Asegúrate de importar EventButtons
from AppCityEngine.Component.eventButtons import EventButtons

import sys
import os


def resourcePath(relativePath):
    """ Get absolute path to resource, works for dev and for PyInstaller """
    try:
        # PyInstaller creates a temp folder and stores path in _MEIPASS
        basePath = sys._MEIPASS
    except Exception:
        basePath = os.path.abspath(".")

    return os.path.join(basePath, relativePath)
    
    
class CsvView(tk.Frame):
    def __init__(self, master=None):
        super().__init__(master)
        self.master = master
        self.event_buttons = EventButtons(self)  # Pasamos la instancia de la vista a EventButtons
        self.create_widgets()

    def create_widgets(self):
        self.view_csv = tk.Frame(self, bg="blue")
        self.view_csv.pack(fill="both", expand=True)
        
        self.label = tk.Label(self, text="Vista para cargar datos desde CSV")
        self.label.pack(side="top", pady=10)
        
        # Carga el logo
        logo2_path = resourcePath("images/ambosLogos.png")
        self.logo2 = tk.PhotoImage(file=logo2_path).subsample(4, 4)
        
        # Crear un frame
        frame_style = ttk.Style()
        frame_style.configure("RoundedFrame.TFrame", borderwidth=5, relief="raised", background="lightgrey", bordercolor="darkgreen")
        self.rounded_frame = ttk.Frame(self.view_csv, style="RoundedFrame.TFrame")
        self.rounded_frame.pack(side="top", fill="both", padx=10, pady=(20, 40))

        # Etiqueta con texto e imagen dentro del frame redondeado
        self.labelTittle = tk.Label(self.rounded_frame, text="PROCEDURAL RULE CREATOR", image=self.logo2,  compound=tk.LEFT, bg="snow", font=("Arial", 14, "bold"), relief="sunken", highlightbackground="#000080", highlightcolor="#000080", highlightthickness=2)
        self.labelTittle.image = self.logo2
        self.labelTittle.pack(fill="both", expand=True, padx=10, pady=10)
        
        # Botones
        self.back_button = tk.Button(self.view_csv, text="Return", command=self.show_main_view, font=("Arial", 10, "bold"), relief="raised", borderwidth=5, highlightbackground="#CFB53B", highlightcolor="#CFB53B", highlightthickness=2)
        self.back_button.pack(side="bottom", pady=10)
        self.back_button.place(relx=0.4, rely=0.9, anchor="s")
        
        self.delete_button = tk.Button(self.view_csv, text="Delete", command=self.event_buttons.delete_file, font=("Arial", 10, "bold"), relief="raised", borderwidth=5)
        self.delete_button.pack(side="bottom", pady=10)
        self.delete_button.place(relx=0.5, rely=0.9, anchor="s")
        
        self.load_csv_button = tk.Button(self.view_csv, text="Upload CSV", command=self.event_buttons.load_csv, font=("Arial", 10, "bold"), relief="raised", borderwidth=5)
        self.load_csv_button.pack(side="top", pady=10)
        self.load_csv_button.place(relx=0.6, rely=0.9, anchor="s")
        
        # Lista de archivos CGA
        self.file_listbox = tk.Listbox(self.view_csv, font=("Arial", 13), width=108, relief="sunken", borderwidth=5)
        self.file_listbox.pack(side="top", fill="both", padx=10, pady=10)
        self.file_listbox.bind('<Double-1>', self.event_buttons.download_file)

        self.update_file_listbox()

    def show_main_view(self):
        self.pack_forget()
        self.master.show_main_view()

    def update_file_listbox(self):
        self.event_buttons.update_file_listbox()
