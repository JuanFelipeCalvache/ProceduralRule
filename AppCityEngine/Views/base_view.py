import tkinter as tk
from tkinter import filedialog, messagebox
import os
import shutil
from AppCityEngine.Component.custom_components import resourcePath

class BaseView(tk.Frame):
    def __init__(self, master=None):
        super().__init__(master)
        self.master = master
        self.generated_files = []
        # Try to load existing files on init (optional, but good for consistency)
        self.load_generated_files()

    def show_main_view(self):
        self.pack_forget()
        self.master.show_main_view()

    def get_generated_files_list_path(self):
        return "generated_files_list.txt"

    def get_generated_files_dir(self):
        return "generated_files"

    def save_generated_files(self):
        """Save the list of generated file paths to a text file."""
        with open(self.get_generated_files_list_path(), "w") as file:
            for filepath in self.generated_files:
                file.write(filepath + "\n")

    def load_generated_files(self):
        """Load the list of generated file paths from a text file."""
        list_path = self.get_generated_files_list_path()
        if os.path.exists(list_path):
            try:
                with open(list_path, "r") as file:
                    self.generated_files = [line.strip() for line in file.readlines()]
            except Exception as e:
                print(f"Error loading generated files list: {e}")
                self.generated_files = []
        
        self.clean_generated_files()
        self.save_generated_files() # Sync back cleaned list

    def clean_generated_files(self):
        """Remove files from the list that no longer exist on disk."""
        self.generated_files = [filepath for filepath in self.generated_files if os.path.exists(filepath)]

    def update_file_listbox(self):
        """Update the ListBox component if it exists."""
        if hasattr(self, 'file_listbox') and self.file_listbox:
            self.file_listbox.delete(0, tk.END)
            for filepath in self.generated_files:
                self.file_listbox.insert(tk.END, os.path.basename(filepath))

    def refresh_files(self):
        """Reload files and update UI."""
        self.load_generated_files()
        self.update_file_listbox()

    def get_next_filename(self, prefix="regla_procedural", extension=".cga"):
        """Generate a unique filename to avoid overwrites."""
        i = 1
        while True:
            # Check for generic numbering or specific index based if needed
            # For simplicity, we just find the next available number for the prefix
            # DetectView used "Prueba{i}.cga", EventButtons used "regla_procedural_{i}.cga"
            # We can standardize or allow prefix override.
            if prefix == "Prueba": # backward compatibility logic if needed, or just standard
                 filename = f"{prefix}{i}{extension}"
            else:
                 filename = f"{prefix}_{i}{extension}"
            
            full_path = os.path.join(self.get_generated_files_dir(), filename)
            if not os.path.exists(full_path):
                return full_path
            i += 1

    def add_generated_file(self, full_path):
        """Add a new file to the list and update persistence/UI."""
        self.generated_files.append(os.path.abspath(full_path))
        self.save_generated_files()
        self.update_file_listbox()

    def delete_file(self):
        """Delete the selected file from the listbox and disk."""
        if not hasattr(self, 'file_listbox'): return

        selected_index = self.file_listbox.curselection()
        if selected_index:
            selected_file = self.file_listbox.get(selected_index)
            file_to_remove = None
            
            for filepath in self.generated_files:
                if os.path.basename(filepath) == selected_file:
                    file_to_remove = filepath
                    break
            
            if file_to_remove:
                if os.path.exists(file_to_remove):
                    try:
                        os.remove(file_to_remove)
                    except Exception as e:
                        print(f"Error deleting file: {e}")
                
                self.generated_files.remove(file_to_remove)
                self.update_file_listbox()
                self.save_generated_files()
                messagebox.showinfo("Eliminación completada", f"El archivo {selected_file} ha sido eliminado.")

    def download_file(self, event=None):
        """Download (copy) the selected file to a user-chosen location."""
        if not hasattr(self, 'file_listbox'): return

        selected_index = self.file_listbox.curselection()
        if selected_index:
            selected_file = self.file_listbox.get(selected_index)
            for filepath in self.generated_files:
                if os.path.basename(filepath) == selected_file:
                    
                    # Determine extension/type
                    _, ext = os.path.splitext(filepath)
                    ext = ext.lower()
                    
                    filetypes = [("All files", "*.*")]
                    if ext == '.cga':
                        filetypes.insert(0, ("CGA files", "*.cga"))
                    elif ext in ['.jpg', '.png', '.jpeg']:
                        filetypes.insert(0, ("Image files", "*.jpg;*.png;*.jpeg"))
                    
                    save_path = filedialog.asksaveasfilename(
                        initialfile=selected_file,
                        title="Guardar archivo",
                        defaultextension=ext,
                        filetypes=filetypes
                    )
                    
                    if save_path:
                        if os.path.exists(filepath):
                            try:
                                shutil.copyfile(filepath, save_path)
                                messagebox.showinfo("Descarga completada", f"El archivo se ha guardado en: {save_path}")
                            except Exception as e:
                                messagebox.showerror("Error", f"Error al guardar: {e}")
                        else:
                            messagebox.showerror("Error", f"El archivo no existe: {filepath}")
                    return # Stop after finding match
