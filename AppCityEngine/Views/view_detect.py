import tkinter as tk
from tkinter import filedialog, messagebox
import os
import shutil
from PIL import Image, ImageTk
from AppCityEngine.Component.generarRegla import GenerarCGA
from AppCityEngine.Component.objectdetection import ObjectDetectionModel
from AppCityEngine.Component.custom_components import TitleHeader, FileListBox, Footer, resourcePath
from AppCityEngine.Views.base_view import BaseView

class DetectView(BaseView):
    def __init__(self, master=None):
        super().__init__(master) # This loads generated files
        model_path = resourcePath("runs/detect/train/weights/best.pt")
        self.model = ObjectDetectionModel(model_path)
        self.create_widgets()

    def create_widgets(self):
        self.view_csv = tk.Frame(self, bg="blue")
        self.view_csv.pack(fill="both", expand=True)
        
        self.header = TitleHeader(self.view_csv)
        self.header.pack(fill="x")
        
        # Footer
        self.footer = Footer(self.view_csv, text_info="Vista para obtener reglas mediante detección de imágenes")
        self.footer.pack(side="bottom", fill="x")

        # Botones en el Footer
        self.load_image_button = self.footer.add_button(text="Upload Image", command=self.load_image, side="right", padx=30)
        self.delete_button = self.footer.add_button(text="Delete", command=self.delete_file, side="right", padx=10)
        self.download_button = self.footer.add_button(text="Download file", command=self.download_file, side="right", padx=10)
        self.back_button = self.footer.add_button(text="Return", command=self.show_main_view, side="left", padx=30)
        
        self.back_button.configure(highlightbackground="#CFB53B", highlightcolor="#CFB53B", highlightthickness=2)

        # File ListBox
        self.file_listbox_component = FileListBox(self.view_csv, self, width=50, height=15)
        # Rebind Double-Click to show image instead of download
        self.file_listbox_component.listbox.bind('<Double-1>', self.show_selected_image)
        
        self.file_listbox_component.place(relx=0.30, rely=0.82, anchor="s")
        self.file_listbox = self.file_listbox_component.listbox

        # Canvas
        self.image_canvas = tk.Canvas(self.view_csv, width=400, height=300, relief="sunken", borderwidth=5)
        self.image_canvas.pack(side="left", fill="both", padx=10, pady=10)
        self.image_canvas.place(relx=0.75, rely=0.82, anchor="s")

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
            # Fallback if list is empty or similar logic? Assumed valid for now based on prev code
            cantidadPiso = cantidad_por_piso[0] if cantidad_por_piso else 0 
            
            print(f"¿Se detectaron balcones o ventanas? {'Sí' if has_windows_or_balconies else 'No'}")
            print(f"Tipo predominante detectado: {predominant_type if predominant_type else 'Ninguno'}")
            print(f"Cantidad de pisos: {cantidad_pisos}")
            print(f"Cantidad de ventanas o balcones por piso: {cantidad_por_piso}")
            
            self.model.draw_boxes_and_count(file_path, detections, floors)
            
            try:
                reglaProcedural = GenerarCGA.GenerarProceduralDetect(typeObject, cantidadPiso, cantidad_pisos)
                # Use custom prefix to match original behavior if desired, or standard one.
                generated_file_path = self.get_next_filename(prefix="Prueba")
                os.makedirs(self.get_generated_files_dir(), exist_ok=True)
                
                with open(generated_file_path, "w") as file:
                    file.write(reglaProcedural)
                    print("El archivo regla procedural ha sido creado exitosamente")
                
                self.add_generated_file(generated_file_path) # Updates UI and file
            except Exception as e:    
                print(f"Error al crear el archivo CGA: {e}")
            
            # Save annotated image
            processed_image_path = file_path.replace('.jpg', '_annotated.jpg')
            if os.path.exists(processed_image_path):
                # Display processed image
                processed_img = Image.open(processed_image_path)
                processed_img = processed_img.resize((400, 300), Image.LANCZOS)
                self.loaded_image = ImageTk.PhotoImage(processed_img)
                self.image_canvas.create_image(0, 0, anchor="nw", image=self.loaded_image)
                
                self.add_generated_file(processed_image_path)

    def show_selected_image(self, event):
        selected_index = self.file_listbox.curselection()
        if selected_index:
            selected_file = self.file_listbox.get(selected_index)
            for filepath in self.generated_files:
                if os.path.basename(filepath) == selected_file:
                    # Load and display the image on the Canvas
                    try:
                        img = Image.open(filepath)
                        img = img.resize((400, 300), Image.LANCZOS)
                        self.loaded_image = ImageTk.PhotoImage(img)
                        self.image_canvas.create_image(0, 0, anchor="nw", image=self.loaded_image)
                    except Exception:
                        # Might be a .cga file, which is not an image
                        print(f"Cannot display {selected_file} as image")
                    break
