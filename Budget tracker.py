import tkinter as tk
from tkinter import ttk, messagebox
import pandas as pd

class BudgetTracker:
    def __init__(self, root):
        self.root = root
        self.root.title("Rastreador de presupuesto")

        # Crear DataFrame vacío
        self.df = pd.DataFrame(columns=["Descripción", "Cantidad", "Categoría"])

        # Crear widgets
        self.eliminar_button = ttk.Button(self.root, text="Eliminar", command=self.eliminar_gasto)
        self.eliminar_button.grid(row=3, column=2, padx=(20, 0), pady=(20, 10))

        self.editar_button = ttk.Button(self.root, text="Editar", command=self.editar_gasto)
        self.editar_button.grid(row=3, column=3, padx=(20, 0), pady=(20, 10))

        self.descripcion_entry = ttk.Entry(self.root, width=30)
        self.descripcion_entry.grid(row=0, column=0, padx=(20, 0), pady=(20, 10))

        self.cantidad_entry = ttk.Entry(self.root, width=30)
        self.cantidad_entry.grid(row=0, column=1, padx=(20, 0), pady=(20, 10))

        self.categoria_combobox = ttk.Combobox(self.root, width=30, values=["Alimentos", "Transporte", "Entretenimiento", "Otros"])
        self.categoria_combobox.set("Alimentos")
        self.categoria_combobox.grid(row=0, column=2, padx=(20, 0), pady=(20, 10))

        self.agregar_button = ttk.Button(self.root, text="Agregar", command=self.agregar_gasto)
        self.agregar_button.grid(row=0, column=3, padx=(20, 0), pady=(20, 10))

        self.treeview = ttk.Treeview(self.root, columns=("Descripción", "Cantidad", "Categoría"), show="headings")
        self.treeview.heading("Descripción", text="Descripción")
        self.treeview.heading("Cantidad", text="Cantidad")
        self.treeview.heading("Categoría", text="Categoría")
        self.treeview.column("Cantidad", anchor="e")
        self.treeview.column("Categoría", anchor="center")
        self.treeview.grid(row=1, column=0, columnspan=4, padx=20, pady=(0, 20))

        self.total_label = ttk.Label(self.root, text="Total: $0.00")
        self.total_label.grid(row=2, column=0, columnspan=2, sticky="w", padx=20)

    def agregar_gasto(self):
        descripcion = self.descripcion_entry.get().strip()
        cantidad = self.cantidad_entry.get().strip()
        categoria = self.categoria_combobox.get().strip()

        if not descripcion or not cantidad or not categoria:
            messagebox.showerror("Error", "Por favor, completa todos los campos")
            return

        try:
            cantidad = float(cantidad)
        except ValueError:
            messagebox.showerror("Error", "La cantidad debe ser un número")
            return

        self.df = self.df.append({"Descripción": descripcion, "Cantidad": cantidad, "Categoría": categoria}, ignore_index=True)
        self.treeview.insert("", tk.END, values=(descripcion, f"${cantidad:.2f}", categoria))

        total = self.df["Cantidad"].sum()
        self.total_label["text"] = f"Total: ${total:.2f}"

        self.descripcion_entry.delete(0, tk.END)
        self.cantidad_entry.delete(0, tk.END)

    def eliminar_gasto(self):
        selected_item = self.treeview.selection()
        if not selected_item:
            messagebox.showerror("Error", "Selecciona un gasto para eliminar")
            return

        index = self.treeview.index(selected_item[0])
        self.df = self.df.drop(index).reset_index(drop=True)
        self.treeview.delete(selected_item)

        total = self.df["Cantidad"].sum()
        self.total_label["text"] = f"Total: ${total:.2f}"

    def editar_gasto(self):
        selected_item = self.treeview.selection()
        if not selected_item:
            messagebox.showerror("Error", "Selecciona un gasto para editar")
            return

        index = self.treeview.index(selected_item[0])
        gasto = self.df.loc[index]

        self.descripcion_entry.delete(0, tk.END)
        self.descripcion_entry.insert(0, gasto["Descripción"])

        self.cantidad_entry.delete(0, tk.END)
        self.cantidad_entry.insert(0, gasto["Cantidad"])

        self.categoria_combobox.set(gasto["Categoría"])

        self.agregar_button["text"] = "Guardar cambios"
        self.agregar_button["command"] = lambda: self.guardar_cambios(index)

    def guardar_cambios(self, index):
        descripcion = self.descripcion_entry.get().strip()
        cantidad = self.cantidad_entry.get().strip()
        categoria = self.categoria_combobox.get().strip()

        if not descripcion or not cantidad or not categoria:
            messagebox.showerror("Error", "Por favor, completa todos los campos")
            return

        try:
            cantidad = float(cantidad)
        except ValueError:
            messagebox.showerror("Error", "La cantidad debe ser un número")
            return

        self.df.loc[index] = [descripcion, cantidad, categoria]
        self.treeview.item(self.treeview.selection(), values=(descripcion, f"${cantidad:.2f}", categoria))

        total = self.df["Cantidad"].sum()
        self.total_label["text"] = f"Total: ${total:.2f}"

        self.descripcion_entry.delete(0, tk.END)
        self.cantidad_entry.delete(0, tk.END)

        self.agregar_button["text"] = "Agregar"
        self.agregar_button["command"] = self.agregar_gasto


if __name__ == "__main__":
    root = tk.Tk()
    tracker = BudgetTracker(root)
    root.mainloop()
