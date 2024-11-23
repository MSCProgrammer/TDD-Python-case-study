import tkinter as tk
from tkinter import ttk, messagebox
from controller import turni_controller

class TurniGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("Gestione Turni")
        self.root.geometry("320x350")
        self.root.minsize(320, 350)
        self.root.resizable(False, False)

        self.create_widgets()
        self.load_turni()  # Carica i turni all'avvio

    def create_widgets(self):
        fields = {
            "id_turno": {"label": "ID", "editable": False},
            "des_turno": {"label": "Descrizione", "editable": True}
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
        self.entries["id_turno"].config(state="readonly")
        
        # Pulsanti di azione principali
        self.new_button = ttk.Button(self.root, text="Nuovo", command=self.new_turno)
        self.new_button.grid(row=row_count, column=0, pady=10)

        self.modify_button = ttk.Button(self.root, text="Modifica", command=self.modify_turno)
        self.modify_button.grid(row=row_count, column=1, pady=10)

        self.delete_button = ttk.Button(self.root, text="Cancella", command=self.delete_turno)
        self.delete_button.grid(row=row_count, column=2, pady=10)

        # Tabella dei turni
        self.turni_table = ttk.Treeview(self.root, columns=("ID", "Descrizione"), show="headings")
        self.turni_table.heading("ID", text="ID")
        self.turni_table.heading("Descrizione", text="Descrizione")
        self.turni_table.grid(row=row_count + 1, column=0, columnspan=5, padx=10, pady=10)

        # Imposta la larghezza delle colonne
        self.turni_table.column("ID", width=70)
        self.turni_table.column("Descrizione", width=220)
        
        # Evento di selezione della riga per modificare i campi
        self.turni_table.bind("<ButtonRelease-1>", self.select_record)

        # Pulsanti "Salva" e "Annulla" (nascosti inizialmente)
        self.save_button = ttk.Button(self.root, text="Salva", command=self.save_changes)
        self.cancel_button = ttk.Button(self.root, text="Annulla", command=self.cancel_action)
        self.save_button.grid(row=2, column=1, pady=10)
        self.cancel_button.grid(row=2, column=2, pady=10)
        self.save_button.grid_remove()
        self.cancel_button.grid_remove()

    def load_turni(self):
        # Carica i turni esistenti nella tabella
        for row in self.turni_table.get_children():
            self.turni_table.delete(row)
        turni = turni_controller.fetch_all_turni()
        for turno in turni:
            self.turni_table.insert("", "end", values=turno)

    def select_record(self, event):
        # Carica i dati del record selezionato nei campi di input
        selected_item = self.turni_table.selection()
        if selected_item:
            values = self.turni_table.item(selected_item)["values"]
            self.entries["id_turno"].config(state="normal")
            self.entries["id_turno"].delete(0, tk.END)
            self.entries["id_turno"].insert(0, values[0])
            self.entries["id_turno"].config(state="readonly")
            self.entries["des_turno"].delete(0, tk.END)
            self.entries["des_turno"].insert(0, values[1])

    def new_turno(self):
        # Prepara l'interfaccia per l'inserimento di un nuovo turno con ID non modificabile
        self.clear_fields()
        self.entries["id_turno"].config(state="readonly")
        self.entries["des_turno"].focus_set()
        self.toggle_save_cancel_buttons(visible=True)

    def modify_turno(self):
        # Prepara l'interfaccia per la modifica del turno selezionato
        if not self.turni_table.selection():
            messagebox.showwarning("Attenzione", "Seleziona un turno da modificare.")
            return
        self.entries["des_turno"].focus_set()
        self.toggle_save_cancel_buttons(visible=True)

    def delete_turno(self):
        # Conferma la cancellazione e rimuove il record selezionato
        if not self.turni_table.selection():
            messagebox.showwarning("Attenzione", "Seleziona un turno da cancellare.")
            return
        if messagebox.askyesno("Conferma", "Sei sicuro di voler cancellare questo turno?"):
            try:
                turni_controller.delete_turno(self.entries)
                messagebox.showinfo("Successo", "Turno cancellato con successo!")
                self.load_turni()
            except Exception as e:
                messagebox.showerror("Errore", f"Errore nella cancellazione del turno: {e}")

    def save_changes(self):
        # Salva le modifiche apportate al turno
        try:
            if self.entries["id_turno"].get():  # Se ID esiste, modifica
                turni_controller.modify_turno(self.entries)
                messagebox.showinfo("Successo", "Turno modificato con successo!")
            else:  # Se ID è vuoto, inserisce nuovo turno
                turni_controller.insert_turno(self.entries)
                messagebox.showinfo("Successo", "Turno salvato con successo!")
            self.load_turni()
            self.toggle_save_cancel_buttons(visible=False)
        except Exception as e:
            messagebox.showerror("Errore", f"Errore nel salvataggio: {e}")

    def cancel_action(self):
        # Annulla l'azione corrente e nasconde i pulsanti "Salva" e "Annulla"
        self.clear_fields()
        self.toggle_save_cancel_buttons(visible=False)
        self.entries["id_turno"].config(state="readonly")
        
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
    app = TurniGUI(root)
    root.mainloop()