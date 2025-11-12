import tkinter as tk
from tkinter import ttk, filedialog, messagebox
import pandas as pd
import os
import shutil
from PIL import Image, ImageTk
from AppCityEngine.Component.generarRegla import GenerarCGA
from AppCityEngine.Component.objectdetection import ObjectDetectionModel
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


class DetectView(tk.Frame):
    def __init__(self, master=None):
        super().__init__(master)
        self.master = master
        self.generated_files = []
        self.load_generated_files()
        model_path = resourcePath("runs/detect/train/weights/best.pt")
        self.model = ObjectDetectionModel(model_path)
        self.create_widgets()

    def create_widgets(self):
        self.view_csv = tk.Frame(self, bg="blue")
        self.view_csv.pack(fill="both", expand=True)
        
        self.label = tk.Label(self, text="View for capturing data by image")
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
        self.labelTittle = tk.Label(self.rounded_frame, text="PROCEDURAL RULE CREATOR", image=self.logo2, compound="left", bg="snow", font=("Arial", 14, "bold"), relief="sunken", highlightbackground="#000080", highlightcolor="#000080", highlightthickness=2,  anchor="w", justify="left", padx=30 )
        self.labelTittle.image = self.logo2
        self.labelTittle.pack(fill="both", expand=True, padx=10, pady=10)
        
        # Download file button
        self.download_button = tk.Button(self.view_csv, text="Download file", command=self.download_file, font=("Arial", 10, "bold"), relief="raised", borderwidth=5)
        self.download_button.pack(side="bottom", pady=10)
        self.download_button.place(relx=0.27, rely=0.99, anchor="s")

        # Turn back Button
        self.back_button = tk.Button(self.view_csv, text="Return", command=self.show_main_view, font=("Arial", 10, "bold"), relief="raised", borderwidth=5, highlightbackground="#CFB53B", highlightcolor="#CFB53B", highlightthickness=2)
        self.back_button.pack(side="bottom", pady=10)
        self.back_button.place(relx=0.4, rely=0.99, anchor="s")
        
        # Delete file button
        self.delete_button = tk.Button(self.view_csv, text="Delete", command=self.delete_file, font=("Arial", 10, "bold"), relief="raised", borderwidth=5)
        self.delete_button.pack(side="bottom", pady=10)
        self.delete_button.place(relx=0.5, rely=0.99, anchor="s")
        
        # Button to load an image
        self.load_image_button = tk.Button(self.view_csv, text="Upload Image", command=self.load_image, font=("Arial", 10, "bold"), relief="raised", borderwidth=5)
        self.load_image_button.pack(side="top", pady=10)
        self.load_image_button.place(relx=0.63, rely=0.99, anchor="s")

        # CGA'S File list
        self.file_listbox = tk.Listbox(self.view_csv, font=("Arial", 13), width= 50, height=15, relief="sunken", borderwidth=5)
        self.file_listbox.pack(side="left", fill="both", padx=10, pady=10)
        self.file_listbox.bind('<Double-1>', self.show_selected_image)  # Bind the event to the method
        self.file_listbox.place(relx=0.30, rely=0.90, anchor="s")

        # Create a Canvas to display the image
        self.image_canvas = tk.Canvas(self.view_csv, width= 400, height= 300, relief="sunken", borderwidth=5)
        self.image_canvas.pack(side="left", fill="both", padx=10, pady=10)
        self.image_canvas.place(relx=0.75, rely=0.90, anchor="s")

        self.update_file_listbox()

    def load_image(self):
        file_path = filedialog.askopenfilename(
            filetypes=[("Image files", "*.jpg;*.png;*.jpeg;*.bmp")],
            title="Seleccionar una imagen"
        )
        if file_path:
            img = Image.open(file_path)
            img = img.resize((400, 300), Image.LANCZOS)
            self.loaded_image = ImageTk.PhotoImage(img)
            self.image_canvas.create_image(0, 0, anchor="nw", image=self.loaded_image)

            # Process the image
            detections = self.model.detect_image(file_path)
            floors, has_windows_or_balconies, predominant_type, cantidad_por_piso = self.model.classify_floors_by_windows_and_balconies(detections)
        
            cantidad_pisos = len(floors)
            typeObject = predominant_type
            cantidadPiso = cantidad_por_piso[0]
            

            print(f"¿Se detectaron balcones o ventanas? {'Sí' if has_windows_or_balconies else 'No'}")
            print(f"Tipo predominante detectado: {predominant_type if predominant_type else 'Ninguno'}")
            print(f"Cantidad de pisos: {cantidad_pisos}")
            print(f"Cantidad de ventanas o balcones por piso: {cantidad_por_piso}")
            print(cantidad_por_piso[0])
            
            self.model.draw_boxes_and_count(file_path, detections, floors)

            
            
            try:
                reglaProcedural = GenerarCGA.GenerarProceduralDetect(typeObject, cantidadPiso, cantidad_pisos)
                generated_file_path = self.get_next_filename()
                os.makedirs("generated_files", exist_ok=True)
                with open(generated_file_path, "w") as file:
                    file.write(reglaProcedural)
                    print("El archivo regla procedural ha sido creado exitosamente")
                self.generated_files.append(os.path.abspath(generated_file_path))
                self.update_file_listbox()
                self.save_generated_files()
            except Exception as e:    
                print(f"Error al crear el archivo: {e}")
            
            # Guardar la imagen procesada y añadirla a la lista
            processed_image_path = file_path.replace('.jpg', '_annotated.jpg')
            if os.path.exists(processed_image_path):
                self.file_listbox.insert(tk.END, os.path.basename(processed_image_path))
                self.generated_files.append(processed_image_path)
                self.save_generated_files()
                self.update_file_listbox()

                # Mostrar la imagen procesada en el canvas
                processed_img = Image.open(processed_image_path)
                processed_img = processed_img.resize((400, 300), Image.LANCZOS)
                self.loaded_image = ImageTk.PhotoImage(processed_img)
                self.image_canvas.create_image(0, 0, anchor="nw", image=self.loaded_image)



    def show_selected_image(self, event):
        selected_index = self.file_listbox.curselection()
        if selected_index:
            selected_file = self.file_listbox.get(selected_index)
            for filepath in self.generated_files:
                if os.path.basename(filepath) == selected_file:
                    # Load and display the image on the Canvas
                    img = Image.open(filepath)
                    img = img.resize((400, 300), Image.LANCZOS)
                    self.loaded_image = ImageTk.PhotoImage(img)
                    self.image_canvas.create_image(0, 0, anchor="nw", image=self.loaded_image)
                    break

    def download_file(self):
        selected_index = self.file_listbox.curselection()
        if selected_index:
            selected_file = self.file_listbox.get(selected_index)
            for filepath in self.generated_files:
                if os.path.basename(filepath) == selected_file:
                    # Determinar la extensión del archivo
                    if filepath.endswith('.cga'):
                        defaultextension = '.cga'
                        filetypes = [("CGA files", "*.cga"), ("All files", "*.*")]
                    else:
                        defaultextension = '.jpg'
                        filetypes = [("JPEG files", "*.jpg"), ("PNG files", "*.png"), ("All files", "*.*")]
                    
                    save_path = filedialog.asksaveasfilename(
                        initialfile=selected_file,
                        title="Guardar archivo",
                        defaultextension=defaultextension,
                        filetypes=filetypes
                    )
                    if save_path:
                        if os.path.exists(filepath):
                            shutil.copyfile(filepath, save_path)
                            messagebox.showinfo("Descarga completada", f"El archivo se ha guardado en: {save_path}")
                        else:
                            messagebox.showerror("Error", f"El archivo no existe: {filepath}")


    def delete_file(self):
        selected_index = self.file_listbox.curselection()
        if selected_index:
            selected_file = self.file_listbox.get(selected_index)
            for filepath in self.generated_files:
                if os.path.basename(filepath) == selected_file:
                    if os.path.exists(filepath):
                        os.remove(filepath)
                    self.generated_files.remove(filepath)
                    self.update_file_listbox()
                    self.save_generated_files()
                    messagebox.showinfo("Eliminación completada", f"El archivo {selected_file} ha sido eliminado.")
                    break

    def show_main_view(self):
        self.pack_forget()
        self.master.show_main_view()

    def save_generated_files(self):
        with open("generated_files_list.txt", "w") as file:
            for filepath in self.generated_files:
                file.write(filepath + "\n")

    def load_generated_files(self):
        if os.path.exists("generated_files_list.txt"):
            with open("generated_files_list.txt", "r") as file:
                self.generated_files = [line.strip() for line in file.readlines()]
        self.clean_generated_files()
        self.save_generated_files()

    def update_file_listbox(self):
        self.file_listbox.delete(0, tk.END)
        for filepath in self.generated_files:
            self.file_listbox.insert(tk.END, os.path.basename(filepath))

    def get_next_filename(self):
        i = 1
        while True:
            filename = f"Prueba{i}.cga"
            full_path = os.path.join("generated_files", filename)
            if not os.path.exists(full_path):
                return full_path
            i += 1

    def clean_generated_files(self):
        self.generated_files = [filepath for filepath in self.generated_files if os.path.exists(filepath)]
