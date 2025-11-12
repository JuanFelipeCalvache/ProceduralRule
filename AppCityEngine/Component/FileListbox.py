import tkinter as tk
from tkinter import filedialog, messagebox
import os


class FileListbox(tk.Frame):
    def __init__(self, master, generated_files, event_buttons, **kwargs):
        super().__init__(master, **kwargs)
        self.generated_files = generated_files
        self.event_buttons = event_buttons
        self.file_listbox = None
        self.create_widgets()

    def create_widgets(self):
        # Listbox para los archivos generados
        self.file_listbox = tk.Listbox(self, font=("Arial", 13), width=50, height=7, relief="sunken", borderwidth=5)
        self.file_listbox.pack()
        self.file_listbox.bind('<Double-1>', self.on_file_double_click)
        self.file_listbox.place(relx=0.50, rely=0.75, anchor="center")

        # Botón de eliminar
        self.delete_button = tk.Button(self, text="Eliminar", command=self.delete_file, font=("Arial", 10, "bold"), relief="raised", borderwidth=5)
        self.delete_button.pack(side="bottom", pady=10)
        self.delete_button.place(relx=0.5, rely=0.99, anchor="s")

        self.update_file_listbox()

    def on_file_double_click(self, event):
        selected_index = self.file_listbox.curselection()
        if selected_index:
            selected_file = self.file_listbox.get(selected_index)
            self.event_buttons.download_file(self.file_listbox, self.generated_files, selected_file)

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

    def update_file_listbox(self):
        self.file_listbox.delete(0, tk.END)
        for filepath in self.generated_files:
            self.file_listbox.insert(tk.END, os.path.basename(filepath))

    def save_generated_files(self):
        with open("generated_files_list.txt", "w") as file:
            for filepath in self.generated_files:
                file.write(filepath + "\n")
