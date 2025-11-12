import shutil
import os
from tkinter import filedialog, messagebox
import pandas as pd
from AppCityEngine.Component.generarRegla import GenerarCGA

class EventButtons:
    def __init__(self, view):
        self.view = view
        self.generated_files = self.load_generated_files()

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
                generated_files = []
                os.makedirs("generated_files", exist_ok=True)

                for index, row in data.iterrows():
                    # Llamar a la función GenerarProceduralCsv para cada fila
                    ReglaProcedural = GenerarCGA.GenerarProceduralCsv(row)

                    # Generar un nombre de archivo único para cada regla
                    generated_file_path = self.get_next_filename(index)

                    # Verificar si el archivo ya existe, si no lo creamos
                    if not os.path.exists(generated_file_path):
                        with open(generated_file_path, "w") as file:
                            file.write(ReglaProcedural)
                            print(f"El archivo regla procedural para la fila {index} ha sido creado exitosamente")

                        # Agregar el archivo generado a la lista si no existe
                        generated_files.append(os.path.abspath(generated_file_path))

                # Actualizar la lista de archivos generados
                self.generated_files.extend(generated_files)
                self.view.update_file_listbox()  # Correcto
                self.save_generated_files()

            except Exception as e:
                print(f"Error al cargar el archivo CSV: {e}")

    def download_file(self, event):
        selected_index = self.view.file_listbox.curselection()
        if selected_index:
            selected_file = self.view.file_listbox.get(selected_index)
            for filepath in self.generated_files:
                if os.path.basename(filepath) == selected_file:
                    save_path = filedialog.asksaveasfilename(
                        initialfile=selected_file,
                        title="Guardar archivo",
                        defaultextension=".cga"
                    )
                    if save_path:
                        if os.path.exists(filepath):
                            shutil.copyfile(filepath, save_path)
                            messagebox.showinfo("Descarga completada", f"El archivo se ha guardado en: {save_path}")
                        else:
                            messagebox.showerror("Error", f"El archivo no existe: {filepath}")

    def delete_file(self):
        selected_index = self.view.file_listbox.curselection()
        if selected_index:
            selected_file = self.view.file_listbox.get(selected_index)
            for filepath in self.generated_files:
                if os.path.basename(filepath) == selected_file:
                    if os.path.exists(filepath):
                        os.remove(filepath)
                    self.generated_files.remove(filepath)
                    self.view.update_file_listbox()  # Correcto
                    self.save_generated_files()
                    messagebox.showinfo("Eliminación completada", f"El archivo {selected_file} ha sido eliminado.")
                    break

    def save_generated_files(self):
        with open("generated_files_list.txt", "w") as file:
            for filepath in self.generated_files:
                file.write(filepath + "\n")

    def load_generated_files(self):
        try:
            self.generated_files = []  # Inicialización por si el archivo no existe
            if os.path.exists("generated_files_list.txt"):
                with open("generated_files_list.txt", "r") as file:
                    self.generated_files = [line.strip() for line in file.readlines()]
            self.clean_generated_files()
        except Exception as e:
            print(f"Error al cargar los archivos generados: {e}")
        return self.generated_files



    def update_file_listbox(self):
        if not hasattr(self.view, 'file_listbox'):
            print("Error: file_listbox no está definido en la vista.")
            return
        self.view.file_listbox.delete(0, "end")
        for filepath in self.generated_files:
            self.view.file_listbox.insert("end", os.path.basename(filepath))

    def clean_generated_files(self):
        if hasattr(self, 'generated_files') and self.generated_files:
            self.generated_files = [filepath for filepath in self.generated_files if os.path.exists(filepath)]
        
    def get_next_filename(self, index=None):
        if index is None:
            index = len(self.generated_files)  # Evita colisiones con los índices anteriores

        i = index
        while True:
            filename = f"regla_procedural_{i}.cga"
            full_path = os.path.join("generated_files", filename)
            if not os.path.exists(full_path):
                return full_path
            i += 1
