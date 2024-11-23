
import tkinter as tk
from tkinter import ttk, messagebox
from controller import categorie_controller

class CategorieGUI:
    def __init__(self, root):
        # Inizializzazione della finestra di gestione categorie
        self.root = root
        self.root.title("Gestione Categorie")
        self.root.geometry("380x370")
        self.root.minsize(380, 370)
        self.root.resizable(False, False)

        self.create_widgets()
        self.load_categories()  # Carica le categorie all'avvio

    def create_widgets(self):
        # Crea i campi di input per ID e descrizione categoria e inizializza pulsanti
        fields = {
            "id_categoria": {"label": "ID", "editable": False},
            "des_categoria": {"label": "Descrizione ", "editable": True}
        }

        self.entries = {}
        row_count = 0
        for field, config in fields.items():
            ttk.Label(self.root, text=config["label"]).grid(row=row_count, column=0, padx=10, pady=5, sticky="e")
            entry_state = "readonly" if not config["editable"] else "normal"
            entry = ttk.Entry(self.root, state=entry_state)
            entry.grid(row=row_count, column=1, padx=10, pady=5)
            self.entries[field] = entry
            row_count += 1

        # Pulsanti di azione principali senza icone
        self.new_button = ttk.Button(self.root, text="Nuovo", command=self.new_category)
        self.new_button.grid(row=row_count, column=0, pady=10)

        self.modify_button = ttk.Button(self.root, text="Modifica", command=self.modify_category)
        self.modify_button.grid(row=row_count, column=1, pady=10)

        self.delete_button = ttk.Button(self.root, text="Cancella", command=self.delete_category)
        self.delete_button.grid(row=row_count, column=2, pady=10)

        # Pulsanti "Salva" e "Annulla" (nascosti inizialmente) senza icone
        self.save_button = ttk.Button(self.root, text="Salva", command=self.save_changes)
        self.cancel_button = ttk.Button(self.root, text="Annulla", command=self.cancel_action)

        # Tabella delle categorie
        self.category_table = ttk.Treeview(self.root, columns=("ID", "Descrizione"), show="headings")
        self.category_table.heading("ID", text="ID")
        self.category_table.heading("Descrizione", text="Descrizione")
        self.category_table.grid(row=row_count + 1, column=0, columnspan=4, pady=10)

        # Imposta la larghezza delle colonne
        self.category_table.column("ID", width=50)
        self.category_table.column("Descrizione", width=300)
        
        # Evento di selezione della riga per modificare i campi
        self.category_table.bind("<ButtonRelease-1>", self.select_record)

    def load_categories(self):
        # Carica le categorie esistenti nella tabella
        for row in self.category_table.get_children():
            self.category_table.delete(row)
        categories = categorie_controller.fetch_all_categories()
        for cat in categories:
            self.category_table.insert("", "end", values=cat)

    def select_record(self, event):
        # Carica i dati del record selezionato nei campi di input
        selected_item = self.category_table.selection()
        if selected_item:
            values = self.category_table.item(selected_item)["values"]
            self.entries["id_categoria"].config(state="normal")
            self.entries["id_categoria"].delete(0, tk.END)
            self.entries["id_categoria"].insert(0, values[0])
            self.entries["id_categoria"].config(state="readonly")
            self.entries["des_categoria"].delete(0, tk.END)
            self.entries["des_categoria"].insert(0, values[1])

    def new_category(self):
        # Prepara l'interfaccia per l'inserimento di una nuova categoria con ID non modificabile
        self.clear_fields()
        self.entries["id_categoria"].config(state="readonly")
        self.entries["des_categoria"].focus_set()
        self.toggle_save_cancel_buttons(visible=True)

    def modify_category(self):
        # Prepara l'interfaccia per la modifica della categoria selezionata
        if not self.category_table.selection():
            messagebox.showwarning("Attenzione", "Seleziona una categoria da modificare.")
            return
        self.entries["des_categoria"].focus_set()
        self.toggle_save_cancel_buttons(visible=True)

    def delete_category(self):
        # Conferma la cancellazione e rimuove il record selezionato
        if not self.category_table.selection():
            messagebox.showwarning("Attenzione", "Seleziona una categoria da cancellare.")
            return
        if messagebox.askyesno("Conferma", "Sei sicuro di voler cancellare questa categoria?"):
            try:
                categorie_controller.delete_categoria(self.entries)
                messagebox.showinfo("Successo", "Categoria cancellata con successo!")
                self.load_categories()
            except Exception as e:
                messagebox.showerror("Errore", f"Errore nella cancellazione della categoria: {e}")

    def save_changes(self):
        # Salva le modifiche apportate alla categoria
        try:
            if self.entries["id_categoria"].get():  # Se ID esiste, modifica
                categorie_controller.modify_categoria(self.entries)
                messagebox.showinfo("Successo", "Categoria modificata con successo!")
            else:  # Se ID è vuoto, inserisce nuova categoria
                categorie_controller.insert_categoria(self.entries)
                messagebox.showinfo("Successo", "Categoria salvata con successo!")
            self.load_categories()
            self.toggle_save_cancel_buttons(visible=False)
        except Exception as e:
            messagebox.showerror("Errore", f"Errore nel salvataggio: {e}")

    def cancel_action(self):
        # Annulla l'azione corrente e nasconde i pulsanti "Salva" e "Annulla"
        self.clear_fields()
        self.toggle_save_cancel_buttons(visible=False)
        self.entries["id_categoria"].config(state="readonly")

    def clear_fields(self):
        # Pulisce i campi di input
        for entry in self.entries.values():
            entry.config(state="normal")
            entry.delete(0, tk.END)

    def toggle_save_cancel_buttons(self, visible):
        # Mostra o nasconde i pulsanti "Salva" e "Annulla"
        if visible:
            self.save_button.grid(row=2, column=1, pady=10)
            self.cancel_button.grid(row=2, column=2, pady=10)
            self.new_button.grid_remove()
            self.modify_button.grid_remove()
            self.delete_button.grid_remove()
        else:
            self.save_button.grid_remove()
            self.cancel_button.grid_remove()
            self.new_button.grid()
            self.modify_button.grid()
            self.delete_button.grid()

if __name__ == "__main__":
    root = tk.Tk()
    app = CategorieGUI(root)
    root.mainloop()
