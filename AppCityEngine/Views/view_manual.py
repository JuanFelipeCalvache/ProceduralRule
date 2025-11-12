import tkinter as tk
from tkinter import ttk, filedialog, messagebox
import os
from AppCityEngine.Component.generarRegla import GenerarCGA
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

class ManualView(tk.Frame):
    def __init__(self, master=None):
        super().__init__(master)
        self.master = master
        self.event_buttons = EventButtons(self)  # Pasamos la instancia de la vista a EventButtons
        self.generated_files = []
        self.create_widgets()

    def create_widgets(self):
        self.view_manual = tk.Frame(self, bg="blue")
        self.view_manual.pack(fill="both", expand=True)

        self.label = tk.Label(self, text="Vista para cargar datos manualmente", bg="blue", fg="white")
        self.label.pack(side="bottom", pady=10)
        

        # Carga el logo
        logo2_path = resourcePath("images/ambosLogos.png")
        self.logo2 = tk.PhotoImage(file=logo2_path).subsample(4, 4)

        # Crear un frame con estilo para el título
        frame_style = ttk.Style()
        frame_style.configure("RoundedFrame.TFrame", borderwidth=5, relief="raised", background="lightgrey", bordercolor="gold")
        self.rounded_frame = ttk.Frame(self.view_manual, style="RoundedFrame.TFrame", relief="raised")
        self.rounded_frame.pack(side="top", fill="both", padx=10, pady=(20, 40))

        # Título con logo
        self.labelTittle = tk.Label(self.rounded_frame, text="SISTEMA DE GENERACIÓN DE REGLAS AUTOMÁTICAS", image=self.logo2, compound=tk.LEFT, bg="snow", font=("Arial", 14, "bold"), relief="sunken", highlightbackground="#000080", highlightcolor="#000080", highlightthickness=2)
        self.labelTittle.image = self.logo2
        self.labelTittle.pack(fill="both", expand=True, padx=10, pady=10)

        # Campos de entrada y etiquetas
        self.create_input_fields()

        # Lista de archivos generados
        self.create_file_listbox()

        # Botones de acciones
        self.create_buttons()

    def create_input_fields(self):
        # Tipo de edificio
        self.labelTextBuilding = tk.Label(self.view_manual, text="Tipo de edificio", bg="blue", fg="white", font=("Arial", 16))
        self.labelTextBuilding.pack()
        self.labelTextBuilding.place(relx=0.08, rely=0.4, anchor="n")

        self.building_type_var = tk.StringVar()
        self.building_type_var.set("Elija una opción")
        self.dropdownBuilding = tk.OptionMenu(self.view_manual, self.building_type_var, "residencial", "comercial", "industrial", command=self.update_fields_based_on_building_type)
        self.dropdownBuilding.pack()
        self.dropdownBuilding.place(relx=0.22, rely=0.41, anchor="n")

        # Ancho
        self.labelWidth = tk.Label(self.view_manual, text="Ancho", bg="blue", fg="white", font=("Arial", 16))
        self.labelWidth.pack()
        self.labelWidth.place(relx=0.41, rely=0.4, anchor="n")

        self.frameTextWidth = tk.Entry(self.view_manual, width=20)
        self.frameTextWidth.pack()
        self.frameTextWidth.place(relx=0.57, rely=0.41, anchor="n")

        # Altura
        self.labelHeight = tk.Label(self.view_manual, text="Altura", bg="blue", fg="white", font=("Arial", 16))
        self.labelHeight.pack()
        self.labelHeight.place(relx=0.8, rely=0.4, anchor="n")

        self.frameTextHeight = tk.Entry(self.view_manual, width=20)
        self.frameTextHeight.pack()
        self.frameTextHeight.place(relx=0.9, rely=0.41, anchor="n")

        # Profundidad
        self.labelDepth = tk.Label(self.view_manual, text="Profundidad", bg="blue", fg="white", font=("Arial", 16))
        self.labelDepth.pack()
        self.labelDepth.place(relx=0.08, rely=0.5, anchor="n")

        self.frameTextDepth = tk.Entry(self.view_manual, width=20)
        self.frameTextDepth.pack()
        self.frameTextDepth.place(relx=0.22, rely=0.51, anchor="n")

        # Tipo de techo (solo para algunos tipos de edificios)
        self.labelRoof = tk.Label(self.view_manual, text="Ventanas\npor piso", bg="blue", fg="white", font=("Arial", 16))
        self.labelRoof.pack()
        self.labelRoof.place(relx=0.43, rely=0.5, anchor="n")

        self.frameTextRoofType = tk.Entry(self.view_manual, width=20)
        self.frameTextRoofType.pack()
        self.frameTextRoofType.place(relx=0.57, rely=0.51, anchor="n")

        # Número de pisos (solo para algunos tipos de edificios)
        self.labelFloors = tk.Label(self.view_manual, text="Pisos", bg="blue", fg="white", font=("Arial", 16))
        self.labelFloors.pack()
        self.labelFloors.place(relx=0.8, rely=0.5, anchor="n")

        self.frameTextLevelValue = tk.Entry(self.view_manual, width=20)
        self.frameTextLevelValue.pack()
        self.frameTextLevelValue.place(relx=0.9, rely=0.51, anchor="n")

        # Llamada a la función de actualización para ocultar/mostrar campos
        self.update_fields_based_on_building_type(self.building_type_var.get())

    def update_fields_based_on_building_type(self, building_type):
        """Actualiza los campos dependiendo del tipo de edificio seleccionado."""
        # Por defecto ocultamos todo
        self.labelRoof.place_forget()
        self.frameTextRoofType.place_forget()
        self.labelFloors.place_forget()
        self.frameTextLevelValue.place_forget()

        # Mostramos campos basados en el tipo de edificio
        if building_type == "residencial" or building_type == "comercial":
            # Si es residencial o comercial, mostramos campos de número de pisos y tipo de techo
            self.labelRoof.place(relx=0.43, rely=0.5, anchor="n")
            self.frameTextRoofType.place(relx=0.57, rely=0.51, anchor="n")
            self.labelFloors.config(text="Pisos")  # Aseguramos que vuelva a mostrar "Pisos"
            self.labelFloors.place(relx=0.8, rely=0.5, anchor="n")
            self.frameTextLevelValue.place(relx=0.9, rely=0.51, anchor="n")
        elif building_type == "industrial":
            # Si es industrial, mostrar diferentes campos
            self.labelFloors.config(text="Módulos")  # Cambiar "Pisos" a "Módulos"
            self.labelFloors.place(relx=0.4, rely=0.5, anchor="n")  # Ajustamos la posición a la izquierda
            self.frameTextLevelValue.place(relx=0.57, rely=0.51, anchor="n")  # Ajustamos la posición a la izquierda
            # No mostramos el campo de "Tipo de techo"
            self.labelRoof.place_forget()
            self.frameTextRoofType.place_forget()

        # Aseguramos que la interfaz se actualice correctamente después de modificar la visibilidad
        self.master.update_idletasks()  # Actualiza tareas de la interfaz
        self.master.update()  # Procesa los eventos pendientes

    def create_file_listbox(self):
        self.file_listbox = tk.Listbox(self.view_manual, font=("Arial", 13), width=50, height=7, relief="sunken", borderwidth=5)
        self.file_listbox.pack()
        self.file_listbox.bind('<Double-1>', self.event_buttons.download_file)
        self.file_listbox.place(relx=0.5, rely=0.75, anchor="center")
        self.update_file_listbox()

    def create_buttons(self):
        # Botón para regresar a la vista principal
        self.back_button = tk.Button(self.view_manual, text="Volver", command=self.show_main_view, font=("Arial", 10, "bold"), relief="raised", borderwidth=5, width=10)
        self.back_button.pack(side="bottom", pady=10)
        self.back_button.place(relx=0.4, rely=0.99, anchor="s")

        # Botón para eliminar archivo
        self.delete_button = tk.Button(self.view_manual, text="Eliminar", command=self.event_buttons.delete_file, font=("Arial", 10, "bold"), relief="raised", borderwidth=5)
        self.delete_button.pack(side="bottom", pady=10)
        self.delete_button.place(relx=0.5, rely=0.99, anchor="s")

        # Botón para enviar la información
        self.submit_button = tk.Button(self.view_manual, text="Submit", command=self.submit_data, font=("Arial", 10, "bold"), relief="raised", borderwidth=5, width=10)
        self.submit_button.pack(side="bottom", pady=10)
        self.submit_button.place(relx=0.6, rely=0.99, anchor="s")

    def update_file_listbox(self):
        self.event_buttons.update_file_listbox()

    def validate_fields(self):
        # Validación de campos
        building_type = self.building_type_var.get()
        widthValue = self.frameTextWidth.get()
        heightValue = self.frameTextHeight.get()
        depthValue = self.frameTextDepth.get()
        floorsValue = self.frameTextLevelValue.get()

        if building_type == "Elija una opción":
            messagebox.showerror("Error", "Por favor, seleccione un tipo de edificio.")
            return False
        if not widthValue or not heightValue or not depthValue:
            messagebox.showerror("Error", "Por favor, complete todos los campos de ancho, altura y profundidad.")
            return False
        if building_type != "industrial" and (not floorsValue or not self.frameTextRoofType.get()):
            messagebox.showerror("Error", "Por favor, complete los campos de pisos y tipo de techo.")
            return False
        return True

    def submit_data(self):
        # Validar antes de proceder
        if not self.validate_fields():
            return

        # Si todos los campos son válidos, se procede
        building_type = self.building_type_var.get()
        widthValue = self.frameTextWidth.get()
        heightValue = self.frameTextHeight.get()
        depthValue = self.frameTextDepth.get()
        floorsValue = self.frameTextLevelValue.get()
        roof_type = self.frameTextRoofType.get() if building_type != "industrial" else ""  # Si es industrial, no tomamos techo

        print(f"Información guardada: building_type: {building_type}, width: {widthValue}, height: {heightValue}, depth: {depthValue}, roof: {roof_type}, floors: {floorsValue}")

        try:
            # Llamada a la generación de la regla procedural
            reglaProcedural = GenerarCGA.GenerarProceduralManual(building_type, widthValue, heightValue, depthValue, roof_type, floorsValue)
            generated_file_path = self.event_buttons.get_next_filename()
            os.makedirs("generated_files", exist_ok=True)

            # Guardar la regla generada en un archivo
            with open(generated_file_path, "w") as file:
                file.write(reglaProcedural)
                print("El archivo regla procedural ha sido creado exitosamente")

            self.event_buttons.generated_files.append(os.path.abspath(generated_file_path))
            self.update_file_listbox()

            # Guardar lista de archivos generados
            self.event_buttons.save_generated_files()

        except Exception as e:
            print(f"Error al crear el archivo: {e}")

    def show_main_view(self):
        self.pack_forget()
        self.master.show_main_view()
