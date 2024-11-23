import tkinter as tk
from tkinter import ttk, messagebox
from controller import operatori_controller

class OperatoriGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("Gestione Operatori")
        self.root.geometry("380x380")
        self.root.minsize(380, 380)
        self.root.resizable(False, False)

        self.create_widgets()
        self.load_operatori()  # Carica gli operatori all'avvio

    def create_widgets(self):
        fields = {
            "id_operatore": {"label": "ID", "editable": False},
            "nome": {"label": "Nome", "editable": True},
            "cognome": {"label": "Cognome", "editable": True}
        }

        self.entries = {}
        row_count = 0
        for field, config in fields.items():
            ttk.Label(self.root, text=config["label"]).grid(row=row_count, column=0, padx=5, pady=5, sticky="e")
            if config["editable"]:
                entry = ttk.Entry(self.root)
            else:
                entry = ttk.Entry(self.root, state="readonly")
            entry.grid(row=row_count, column=1, padx=5, pady=5)
            self.entries[field] = entry
            row_count += 1

        # Imposta l'ID come readonly
        self.entries["id_operatore"].config(state="readonly")
        
        # Pulsanti di azione principali
        self.new_button = ttk.Button(self.root, text="Nuovo", command=self.new_operatore)
        self.new_button.grid(row=row_count, column=0, pady=10)

        self.modify_button = ttk.Button(self.root, text="Modifica", command=self.modify_operatore)
        self.modify_button.grid(row=row_count, column=1, pady=10)

        self.delete_button = ttk.Button(self.root, text="Cancella", command=self.delete_operatore)
        self.delete_button.grid(row=row_count, column=2, pady=10)

        # Tabella degli operatori
        self.operatori_table = ttk.Treeview(self.root, columns=("ID", "Nome", "Cognome"), show="headings")
        self.operatori_table.heading("ID", text="ID")
        self.operatori_table.heading("Nome", text="Nome")
        self.operatori_table.heading("Cognome", text="Cognome")
        self.operatori_table.grid(row=row_count + 1, column=0, columnspan=5, padx=10, pady=10)

        # Imposta la larghezza delle colonne
        self.operatori_table.column("ID", width=50)
        self.operatori_table.column("Nome", width=150)
        self.operatori_table.column("Cognome", width=150)
                
        # Evento di selezione della riga per modificare i campi
        self.operatori_table.bind("<ButtonRelease-1>", self.select_record)

        # Pulsanti "Salva" e "Annulla" (nascosti inizialmente)
        self.save_button = ttk.Button(self.root, text="Salva", command=self.save_changes)
        self.cancel_button = ttk.Button(self.root, text="Annulla", command=self.cancel_action)
        self.save_button.grid(row=3, column=1, pady=10)
        self.cancel_button.grid(row=3, column=2, pady=10)
        self.save_button.grid_remove()
        self.cancel_button.grid_remove()

    def load_operatori(self):
        # Carica gli operatori esistenti nella tabella
        for row in self.operatori_table.get_children():
            self.operatori_table.delete(row)
        operatori = operatori_controller.fetch_all_operatori()
        for oper in operatori:
            self.operatori_table.insert("", "end", values=oper)

    def select_record(self, event):
        # Carica i dati del record selezionato nei campi di input
        selected_item = self.operatori_table.selection()
        if selected_item:
            values = self.operatori_table.item(selected_item)["values"]
            self.entries["id_operatore"].config(state="normal")
            self.entries["id_operatore"].delete(0, tk.END)
            self.entries["id_operatore"].insert(0, values[0])
            self.entries["id_operatore"].config(state="readonly")
            self.entries["nome"].delete(0, tk.END)
            self.entries["nome"].insert(0, values[1])
            self.entries["cognome"].delete(0, tk.END)
            self.entries["cognome"].insert(0, values[2])

    def new_operatore(self):
        # Prepara l'interfaccia per l'inserimento di un nuovo operatore con ID non modificabile
        self.clear_fields()
        self.entries["id_operatore"].config(state="readonly")
        self.entries["nome"].focus_set()
        self.toggle_save_cancel_buttons(visible=True)

    def modify_operatore(self):
        # Prepara l'interfaccia per la modifica dell'operatore selezionato
        if not self.operatori_table.selection():
            messagebox.showwarning("Attenzione", "Seleziona un operatore da modificare.")
            return
        self.entries["nome"].focus_set()
        self.toggle_save_cancel_buttons(visible=True)

    def delete_operatore(self):
        # Conferma la cancellazione e rimuove il record selezionato
        if not self.operatori_table.selection():
            messagebox.showwarning("Attenzione", "Seleziona un operatore da cancellare.")
            return
        if messagebox.askyesno("Conferma", "Sei sicuro di voler cancellare questo operatore?"):
            try:
                operatori_controller.delete_operatore(self.entries)
                messagebox.showinfo("Successo", "Operatore cancellato con successo!")
                self.load_operatori()
            except Exception as e:
                messagebox.showerror("Errore", f"Errore nella cancellazione dell'operatore: {e}")

    def save_changes(self):
        # Salva le modifiche apportate all'operatore
        try:
            if self.entries["id_operatore"].get():  # Se ID esiste, modifica
                operatori_controller.modify_operatore(self.entries)
                messagebox.showinfo("Successo", "Operatore modificato con successo!")
            else:  # Se ID è vuoto, inserisce nuovo operatore
                operatori_controller.insert_operatore(self.entries)
                messagebox.showinfo("Successo", "Operatore salvato con successo!")
            self.load_operatori()
            self.toggle_save_cancel_buttons(visible=False)
        except Exception as e:
            messagebox.showerror("Errore", f"Errore nel salvataggio: {e}")

    def cancel_action(self):
        # Annulla l'azione corrente e nasconde i pulsanti "Salva" e "Annulla"
        self.clear_fields()
        self.toggle_save_cancel_buttons(visible=False)
        self.entries["id_operatore"].config(state="readonly")

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
    app = OperatoriGUI(root)
    root.mainloop()