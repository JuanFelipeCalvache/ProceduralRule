import tkinter as tk
from tkinter import ttk
import os
import sys

def resourcePath(relativePath):
    """ Get absolute path to resource, works for dev and for PyInstaller """
    try:
        # PyInstaller creates a temp folder and stores path in _MEIPASS
        basePath = sys._MEIPASS
    except Exception:
        basePath = os.path.abspath(".")

    return os.path.join(basePath, relativePath)

class TitleHeader(tk.Frame):
    def __init__(self, master, title="PROCEDURAL RULE CREATOR"):
        super().__init__(master, bg="blue")
        self.master = master
        self.title = title
        self.create_widgets()

    def create_widgets(self):
        # Carga los logos
        logo_usc_path = resourcePath("images/logoUSC.png")
        logo_cartagena_path = resourcePath("images/universidadCartagena.png")

        # Ajustar subsample
        # USC: 400x400 -> /4 = 100x100
        # Cartagena: 2000x800 -> /8 = 250x100
        self.logo_left = tk.PhotoImage(file=logo_usc_path).subsample(4, 4)
        self.logo_right = tk.PhotoImage(file=logo_cartagena_path).subsample(8, 8)
        
        # Crear un frame con esquinas redondeadas
        frame_style = ttk.Style()
        frame_style.configure("RoundedFrame.TFrame", borderwidth=5, relief="raised", background="lightgrey", bordercolor="darkgreen")
        self.rounded_frame = ttk.Frame(self, style="RoundedFrame.TFrame", borderwidth=2)
        self.rounded_frame.pack(side="top", fill="both", padx=10, pady=(20, 40))

        # Crear contenedor blanco unificado
        self.white_frame = tk.Frame(
            self.rounded_frame, 
            bg="snow", 
            relief="sunken", 
            borderwidth=2,
            highlightbackground="#000080", 
            highlightcolor="#000080", 
            highlightthickness=2
        )
        self.white_frame.pack(fill="both", expand=True, padx=10, pady=10)

        # Configurar grid para 3 columnas dentro del frame blanco
        # Usar uniform="sides" fuerza a que las columnas de los logos tengan el mismo ancho
        # (el del mas ancho), lo que asegura que el titulo quede geometricamente centrado.
        self.white_frame.columnconfigure(0, weight=0, uniform="sides")
        self.white_frame.columnconfigure(1, weight=1)
        self.white_frame.columnconfigure(2, weight=0, uniform="sides")

        # Logo Izquierda (USC)
        self.label_logo_left = tk.Label(
            self.white_frame, 
            image=self.logo_left, 
            bg="snow"
        )
        self.label_logo_left.image = self.logo_left
        self.label_logo_left.grid(row=0, column=0, padx=20, pady=10, sticky="w")

        # Etiqueta con texto (Titulo)
        self.labelTittle = tk.Label(
            self.white_frame, 
            text=self.title, 
            bg="snow", 
            font=("Arial", 14, "bold"),
            anchor="center", 
            justify="center",
        )
        self.labelTittle.grid(row=0, column=1, padx=10, pady=10, sticky="ew")

        # Logo Derecha (Cartagena)
        self.label_logo_right = tk.Label(
            self.white_frame, 
            image=self.logo_right, 
            bg="snow"
        )
        self.label_logo_right.image = self.logo_right
        self.label_logo_right.grid(row=0, column=2, padx=20, pady=10, sticky="e")

class CustomButton(tk.Button):
    def __init__(self, master, text, command, **kwargs):
        default_config = {
            "font": ("Arial", 10, "bold"),
            "relief": "raised",
            "borderwidth": 5,
            "width": 10
        }
        # Update default config with user provided kwargs
        default_config.update(kwargs)
        super().__init__(master, text=text, command=command, **default_config)

class FileListBox(tk.Frame):
    def __init__(self, master, handler, height=7, width=50):
        super().__init__(master, bg="blue")
        self.handler = handler
        
        # Scrollbar and Listbox
        self.scrollbar = tk.Scrollbar(self, orient="vertical")
        self.listbox = tk.Listbox(
            self, 
            font=("Arial", 13), 
            width=width, 
            height=height, 
            relief="sunken", 
            borderwidth=5,
            yscrollcommand=self.scrollbar.set
        )
        self.scrollbar.config(command=self.listbox.yview)
        
        self.scrollbar.pack(side="right", fill="y")
        self.listbox.pack(side="left", fill="both", expand=True)
        
        # Bind double click to handler's download_file method
        # Assumes handler has a download_file method
        if hasattr(self.handler, 'download_file'):
            self.listbox.bind('<Double-1>', self.handler.download_file)

    def update_list(self, files):
        self.listbox.delete(0, tk.END)
        for filepath in files:
            self.listbox.insert(tk.END, os.path.basename(filepath))

    def get_selected(self):
        return self.listbox.curselection()

    def get(self, index):
        return self.listbox.get(index)

    # Proxy methods for listbox access if needed directly
    def delete(self, first, last=None):
        self.listbox.delete(first, last)

    def insert(self, index, *elements):
        self.listbox.insert(index, *elements)
    
    @property
    def curselection(self):
        return self.listbox.curselection

class LabeledEntry(tk.Frame):
    def __init__(self, master, label_text, entry_width=20):
        super().__init__(master, bg="blue")
        self.label = tk.Label(self, text=label_text, bg="blue", fg="white", font=("Arial", 16))
        self.label.pack(side="left", padx=5)
        self.entry = tk.Entry(self, width=entry_width)
        self.entry.pack(side="left", padx=5)

    def get(self):
        return self.entry.get()

class Footer(tk.Frame):
    def __init__(self, master, bg="blue", text_info=""):
        # We start with white background for the text part possibility, 
        # but the main heavy lifting is the blue button bar.
        # Actually, let's create a main container with NO fixed height to allow stacking.
        super().__init__(master, bg="white") 
        # We don't force height anymore because we stack two things (buttons + text)
        
        # 1. Blue Button Bar (Top of Footer)
        self.button_frame = tk.Frame(self, bg=bg, height=80)
        self.button_frame.pack(side="top", fill="x")
        self.button_frame.pack_propagate(False) # Keep button area height fixed
        
        # Center container for buttons
        self.center_frame = tk.Frame(self.button_frame, bg=bg)
        self.center_frame.place(relx=0.5, rely=0.5, anchor="center", relheight=1.0)
        
        # 2. White Info Bar (Bottom of Footer)
        self.info_label = tk.Label(self, text=text_info, bg="white", fg="black", font=("Arial", 10), pady=10)
        self.info_label.pack(side="bottom", fill="x")

    def add_button(self, text, command, side="left", padx=10):
        # Buttons are packed inside the center_frame of the button_frame
        btn = CustomButton(self.center_frame, text=text, command=command)
        btn.pack(side=side, padx=padx, pady=int(80-30)/2) # Center vertically approx in the 80px bar
        return btn

