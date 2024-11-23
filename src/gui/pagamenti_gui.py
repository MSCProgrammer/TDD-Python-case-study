import tkinter as tk
from tkinter import ttk, messagebox
from controller import pagamenti_controller

class PagamentiGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("Gestione Pagamenti")
        self.root.geometry("380x400")
        self.root.minsize(380, 400)
        self.root.resizable(False, False)

        self.create_widgets()
        self.load_pagamenti()  # Carica i pagamenti all'avvio

    def create_widgets(self):
        fields = {
            "id_pagamento": {"label": "ID", "editable": False},
            "des_pagamento": {"label": "Descrizione Pagamento", "editable": True},
            "valore_zero": {"label": "Valore Zero", "editable": True, "type": "dropdown", "options": ["SI", "NO"]}
        }

        self.entries = {}
        row_count = 0
        for field, config in fields.items():
            ttk.Label(self.root, text=config["label"]).grid(row=row_count, column=0, padx=5, pady=5, sticky="e")
            if config["editable"]:
                if config.get("type") == "dropdown":
                    entry = ttk.Combobox(self.root, values=config["options"], state="readonly")
                else:
                    entry = ttk.Entry(self.root)
            else:
                entry = ttk.Entry(self.root, state="readonly")
            entry.grid(row=row_count, column=1, padx=5, pady=5)
            self.entries[field] = entry
            row_count += 1
            
        # Imposta l'ID come readonly
        self.entries["id_pagamento"].config(state="readonly")
        
        # Pulsanti di azione principali
        self.new_button = ttk.Button(self.root, text="Nuovo", command=self.new_pagamento)
        self.new_button.grid(row=row_count, column=0, pady=10)

        self.modify_button = ttk.Button(self.root, text="Modifica", command=self.modify_pagamento)
        self.modify_button.grid(row=row_count, column=1, pady=10)

        self.delete_button = ttk.Button(self.root, text="Cancella", command=self.delete_pagamento)
        self.delete_button.grid(row=row_count, column=2, pady=10)

        # Tabella dei pagamenti
        self.pagamenti_table = ttk.Treeview(self.root, columns=("ID", "Descrizione Pagamento", "Valore Zero"), show="headings")
        self.pagamenti_table.heading("ID", text="ID")
        self.pagamenti_table.heading("Descrizione Pagamento", text="Descrizione Pagamento")
        self.pagamenti_table.heading("Valore Zero", text="Valore Zero")
        self.pagamenti_table.grid(row=row_count + 1, column=0, columnspan=5, pady=10)

        # Imposta la larghezza delle colonne
        self.pagamenti_table.column("ID", width=50)
        self.pagamenti_table.column("Descrizione Pagamento", width=200)
        self.pagamenti_table.column("Valore Zero", width=100)
                
        # Evento di selezione della riga per modificare i campi
        self.pagamenti_table.bind("<ButtonRelease-1>", self.select_record)

        # Pulsanti "Salva" e "Annulla" (nascosti inizialmente)
        self.save_button = ttk.Button(self.root, text="Salva", command=self.save_changes)
        self.cancel_button = ttk.Button(self.root, text="Annulla", command=self.cancel_action)
        self.save_button.grid(row=3, column=1, pady=10)
        self.cancel_button.grid(row=3, column=2, pady=10)
        self.save_button.grid_remove()
        self.cancel_button.grid_remove()

    def load_pagamenti(self):
        # Carica i pagamenti esistenti nella tabella
        for row in self.pagamenti_table.get_children():
            self.pagamenti_table.delete(row)
        pagamenti = pagamenti_controller.fetch_all_pagamenti()
        for pag in pagamenti:
            self.pagamenti_table.insert("", "end", values=pag)

    def select_record(self, event):
        # Carica i dati del record selezionato nei campi di input
        selected_item = self.pagamenti_table.selection()
        if selected_item:
            values = self.pagamenti_table.item(selected_item)["values"]
            self.entries["id_pagamento"].config(state="normal")
            self.entries["id_pagamento"].delete(0, tk.END)
            self.entries["id_pagamento"].insert(0, values[0])
            self.entries["id_pagamento"].config(state="readonly")
            self.entries["des_pagamento"].delete(0, tk.END)
            self.entries["des_pagamento"].insert(0, values[1])
            self.entries["valore_zero"].set(values[2])

    def new_pagamento(self):
        # Prepara l'interfaccia per l'inserimento di un nuovo pagamento con ID non modificabile
        self.clear_fields()
        self.entries["id_pagamento"].config(state="readonly")
        self.entries["des_pagamento"].focus_set()
        self.toggle_save_cancel_buttons(visible=True)

    def modify_pagamento(self):
        # Prepara l'interfaccia per la modifica del pagamento selezionato
        if not self.pagamenti_table.selection():
            messagebox.showwarning("Attenzione", "Seleziona un pagamento da modificare.")
            return
        self.entries["des_pagamento"].focus_set()
        self.toggle_save_cancel_buttons(visible=True)

    def delete_pagamento(self):
        # Conferma la cancellazione e rimuove il record selezionato
        if not self.pagamenti_table.selection():
            messagebox.showwarning("Attenzione", "Seleziona un pagamento da cancellare.")
            return
        if messagebox.askyesno("Conferma", "Sei sicuro di voler cancellare questo pagamento?"):
            try:
                pagamenti_controller.delete_pagamento(self.entries)
                messagebox.showinfo("Successo", "Pagamento cancellato con successo!")
                self.load_pagamenti()
            except Exception as e:
                messagebox.showerror("Errore", f"Errore nella cancellazione del pagamento: {e}")

    def save_changes(self):
        # Salva le modifiche apportate al pagamento
        try:
            if self.entries["id_pagamento"].get():  # Se ID esiste, modifica
                pagamenti_controller.modify_pagamento(self.entries)
                messagebox.showinfo("Successo", "Pagamento modificato con successo!")
            else:  # Se ID è vuoto, inserisce nuovo pagamento
                pagamenti_controller.insert_pagamento(self.entries)
                messagebox.showinfo("Successo", "Pagamento salvato con successo!")
            self.load_pagamenti()
            self.toggle_save_cancel_buttons(visible=False)
        except Exception as e:
            messagebox.showerror("Errore", f"Errore nel salvataggio: {e}")

    def cancel_action(self):
        # Annulla l'azione corrente e nasconde i pulsanti "Salva" e "Annulla"
        self.clear_fields()
        self.toggle_save_cancel_buttons(visible=False)
        self.entries["id_pagamento"].config(state="readonly")
        
    def clear_fields(self):
        # Pulisce i campi di input
        for entry in self.entries.values():
            entry.config(state="normal")
            entry.delete(0, tk.END)

    def toggle_save_cancel_buttons(self, visible):
        # Mostra o nasconde i pulsanti "Salva" e "Annulla"
        if visible:
            self.save_button.grid()
            self.cancel_button.grid()
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
    app = PagamentiGUI(root)
    root.mainloop()