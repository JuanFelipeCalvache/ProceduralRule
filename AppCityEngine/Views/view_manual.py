import tkinter as tk
from tkinter import messagebox
import os
from AppCityEngine.Component.generarRegla import GenerarCGA
from AppCityEngine.Component.custom_components import TitleHeader, FileListBox, Footer, LabeledEntry
from AppCityEngine.Views.base_view import BaseView

class ManualView(BaseView):
    def __init__(self, master=None):
        super().__init__(master)
        self.create_widgets()

    def create_widgets(self):
        self.view_manual = tk.Frame(self, bg="blue")
        self.view_manual.pack(fill="both", expand=True)

        self.header = TitleHeader(self.view_manual)
        self.header.pack(fill="x")

        # Campos de entrada
        self.create_input_fields()

        # Lista de archivos generados
        self.create_file_listbox()

        # Botones de acciones
        self.create_buttons()

    def create_input_fields(self):
        # Grid System Constants
        self.col1_x = 0.20
        self.col2_x = 0.50
        self.col3_x = 0.80
        self.row1_y = 0.35
        self.row2_y = 0.50
        
        # 1. Tipo de edificio
        # For uniformity, we put the label above or beside? 
        # Since other inputs use LabeledEntry (Side-by-side), let's try to mimic that or just place them nicely.
        # We will place Label and OptionMenu manually but centered on Col 1
        
        # 1. Tipo de edificio
        self.labelBuilding = tk.Label(self.view_manual, text="Tipo de\nedificio", bg="blue", fg="white", font=("Arial", 16), justify="right")
        # Align Label and Dropdown
        # Move dropdown slightly right to start strictly after the label column space if needed, 
        # or keep centering around col1_x. 
        # Since text is now narrower but taller, it fits better in the left space.
        self.labelBuilding.place(relx=self.col1_x - 0.02, rely=self.row1_y, anchor="e") 
        
        self.building_type_var = tk.StringVar()
        self.building_type_var.set("Elija una opción")
        self.dropdownBuilding = tk.OptionMenu(self.view_manual, self.building_type_var, "residencial", "comercial", "industrial", command=self.update_fields_based_on_building_type)
        self.dropdownBuilding.config(width=15)
        self.dropdownBuilding.place(relx=self.col1_x + 0.02, rely=self.row1_y, anchor="w")

        # 2. Ancho (Col 2, Row 1)
        self.entryWidth = LabeledEntry(self.view_manual, "Ancho", entry_width=15)
        self.entryWidth.place(relx=self.col2_x, rely=self.row1_y, anchor="center")

        # 3. Altura (Col 3, Row 1)
        self.entryHeight = LabeledEntry(self.view_manual, "Altura", entry_width=15)
        self.entryHeight.place(relx=self.col3_x, rely=self.row1_y, anchor="center")

        # 4. Profundidad (Col 1, Row 2)
        # Note: LabeledEntry anchor="center" centers the whole (Label+Entry) block.
        self.entryDepth = LabeledEntry(self.view_manual, "Profundidad", entry_width=15)
        self.entryDepth.place(relx=self.col1_x, rely=self.row2_y, anchor="center")

        # 5. Ventanas/Techo (Conditional) (Col 2, Row 2)
        self.entryRoofType = LabeledEntry(self.view_manual, "Ventanas\npor piso", entry_width=15)
        # Position will be managed dynamically

        # 6. Pisos/Modulos (Conditional) (Col 3, Row 2)
        self.entryFloors = LabeledEntry(self.view_manual, "Pisos", entry_width=15)
        # Position will be managed dynamically
        
        # Trigger update
        self.update_fields_based_on_building_type(self.building_type_var.get())

    def update_fields_based_on_building_type(self, building_type):
        """Actualiza los campos dependiendo del tipo de edificio seleccionado."""
        
        # Hide dynamic fields
        self.entryRoofType.place_forget()
        self.entryFloors.place_forget()
        
        if building_type == "residencial" or building_type == "comercial":
            # Show Roof/Windows in Col 2
            self.entryRoofType.label.config(text="Ventanas\npor piso")
            self.entryRoofType.place(relx=self.col2_x, rely=self.row2_y, anchor="center")
            
            # Show Floors in Col 3
            self.entryFloors.label.config(text="Pisos")
            self.entryFloors.place(relx=self.col3_x, rely=self.row2_y, anchor="center")

        elif building_type == "industrial":
            # Industrial has NO Roof/Window input, only Modules (Floors)
            # We can put Modules in Col 2 or Col 3. 
            # Let's put it in Col 2 for balance since Col 3 is far right? 
            # Or Col 3 to keep "Floors/Modules" concept in same column.
            # Let's stick to Col 3 for semantic consistency (Height/Verticality).
            
            self.entryFloors.label.config(text="Módulos")
            self.entryFloors.place(relx=self.col2_x, rely=self.row2_y, anchor="center") 
            # Actually, user View had it shifting left. I'll put it in Col 2 so we have Input-Input-Empty behavior?
            # No, Col 2 is better center.

        self.master.update_idletasks()
        self.master.update()

    def create_file_listbox(self):
        # Pass self as handler (BaseView has necessary methods)
        self.file_listbox_component = FileListBox(self.view_manual, self, width=80, height=8) # Increased size slightly
        self.file_listbox_component.place(relx=0.5, rely=0.75, anchor="center")
        self.file_listbox = self.file_listbox_component.listbox
        self.update_file_listbox()

    def create_buttons(self):
        self.footer = Footer(self.view_manual, text_info="Vista para cargar datos manualmente")
        self.footer.pack(side="bottom", fill="x")

        self.submit_button = self.footer.add_button(text="Submit", command=self.submit_data, side="right", padx=30)
        self.delete_button = self.footer.add_button(text="Eliminar", command=self.delete_file, side="right", padx=10)
        self.back_button = self.footer.add_button(text="Volver", command=self.show_main_view, side="left", padx=30)

    def validate_fields(self):
        building_type = self.building_type_var.get()
        widthValue = self.entryWidth.get()
        heightValue = self.entryHeight.get()
        depthValue = self.entryDepth.get()
        floorsValue = self.entryFloors.get()
        roofValue = self.entryRoofType.get()

        if building_type == "Elija una opción":
            messagebox.showerror("Error", "Por favor, seleccione un tipo de edificio.")
            return False
        if not widthValue or not heightValue or not depthValue:
            messagebox.showerror("Error", "Por favor, complete todos los campos de ancho, altura y profundidad.")
            return False
        if building_type != "industrial" and (not floorsValue or not roofValue):
            messagebox.showerror("Error", "Por favor, complete los campos de pisos y tipo de techo.")
            return False
        return True

    def submit_data(self):
        if not self.validate_fields():
            return

        building_type = self.building_type_var.get()
        widthValue = self.entryWidth.get()
        heightValue = self.entryHeight.get()
        depthValue = self.entryDepth.get()
        floorsValue = self.entryFloors.get()
        roof_type = self.entryRoofType.get() if building_type != "industrial" else ""

        print(f"Información guardada: type: {building_type}, w: {widthValue}, h: {heightValue}, d: {depthValue}, r: {roof_type}, f: {floorsValue}")

        try:
            reglaProcedural = GenerarCGA.GenerarProceduralManual(building_type, widthValue, heightValue, depthValue, roof_type, floorsValue)
            generated_file_path = self.get_next_filename()
            os.makedirs(self.get_generated_files_dir(), exist_ok=True)

            with open(generated_file_path, "w") as file:
                file.write(reglaProcedural)
                print("El archivo regla procedural ha sido creado exitosamente")

            self.add_generated_file(generated_file_path)

        except Exception as e:
            print(f"Error al crear el archivo: {e}")
