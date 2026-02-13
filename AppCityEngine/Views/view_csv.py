import tkinter as tk
from tkinter import filedialog, messagebox
import pandas as pd
import os
from AppCityEngine.Component.generarRegla import GenerarCGA
from AppCityEngine.Component.custom_components import TitleHeader, FileListBox, Footer
from AppCityEngine.Views.base_view import BaseView

class CsvView(BaseView):
    def __init__(self, master=None):
        super().__init__(master)
        self.create_widgets()

    def create_widgets(self):
        self.view_csv = tk.Frame(self, bg="blue")
        self.view_csv.pack(fill="both", expand=True)
        
        self.header = TitleHeader(self.view_csv)
        self.header.pack(fill="x")
        
        # Lista de archivos CGA
        self.file_listbox_component = FileListBox(self.view_csv, self, width=108)
        self.file_listbox_component.pack(side="top", fill="both", padx=10, pady=10)
        self.file_listbox = self.file_listbox_component.listbox 

        # Footer
        self.footer = Footer(self.view_csv, text_info="Vista para cargar datos desde CSV")
        self.footer.pack(side="bottom", fill="x")

        # Botones en el Footer
        self.load_csv_button = self.footer.add_button(text="Upload CSV", command=self.load_csv, side="right", padx=30)
        self.delete_button = self.footer.add_button(text="Delete", command=self.delete_file, side="right", padx=10)
        self.back_button = self.footer.add_button(text="Return", command=self.show_main_view, side="left", padx=30)
        
        self.back_button.configure(highlightbackground="#CFB53B", highlightcolor="#CFB53B", highlightthickness=2)

        self.update_file_listbox()

    def load_csv(self):
        file_path = filedialog.askopenfilename(
            filetypes=[("CSV files", "*.csv")],
            title="Seleccionar un archivo CSV"
        )
        if file_path:
            try:
                data = pd.read_csv(file_path, sep=',', decimal='.')
                print(data)

                # Iterar sobre cada fila del DataFrame y generar archivos CGA
                os.makedirs(self.get_generated_files_dir(), exist_ok=True)

                for index, row in data.iterrows():
                    # Llamar a la función GenerarProceduralCsv para cada fila
                    ReglaProcedural = GenerarCGA.GenerarProceduralCsv(row)

                    # Generar un nombre de archivo único para cada regla (usando prefix simple)
                    generated_file_path = self.get_next_filename(prefix="regla_procedural_csv")

                    # Verificar si el archivo ya existe (get_next_filename garantiza unique, pero por seguridad)
                    if not os.path.exists(generated_file_path):
                        with open(generated_file_path, "w") as file:
                            file.write(ReglaProcedural)
                            print(f"El archivo regla procedural para la fila {index} ha sido creado exitosamente")

                        self.generated_files.append(os.path.abspath(generated_file_path))
                
                # Update at end
                self.save_generated_files()
                self.update_file_listbox()

            except Exception as e:
                print(f"Error al cargar el archivo CSV: {e}")
                messagebox.showerror("Error", f"Error al cargar CSV: {e}")
