import tkinter as tk
from tkinter import ttk, messagebox
from controller import articoli_controller

class ArticoliGUI:
    def __init__(self, root):
        # Inizializzazione della finestra di gestione articoli
        self.root = root
        self.root.title("Gestione Articoli")
        self.root.geometry("800x380")
        self.root.minsize(800, 390)
        self.root.resizable(False, False)

        self.create_widgets()
        self.load_articles()  # Carica gli articoli all'avvio

    def create_widgets(self):
        # Crea i campi di input per ID e descrizione articolo e inizializza pulsanti
        fields = {
            "id_articolo": {"label": "ID", "editable": False, "width": 10},
            "descrizione": {"label": "Descrizione", "editable": True, "width": 50},
            "prezzo": {"label": "Prezzo", "editable": True, "width": 10},
            "disponibilita": {"label": "Disponibilità", "editable": True, "type": "dropdown", "options": ["SI", "NO"], "width": 10},
            "id_categoria_default": {"label": "Categoria", "editable": True, "type": "dropdown", "options": articoli_controller.get_category_options(), "width": 20}
        }

        self.entries = {}

        # Prima riga: ID Articolo e Descrizione
        ttk.Label(self.root, text=fields["id_articolo"]["label"]).grid(row=0, column=0, padx=5, pady=5, sticky="e")
        self.entries["id_articolo"] = ttk.Entry(self.root, state="readonly", width=fields["id_articolo"]["width"])
        self.entries["id_articolo"].grid(row=0, column=1, padx=5, pady=5)

        ttk.Label(self.root, text=fields["descrizione"]["label"]).grid(row=0, column=2, padx=5, pady=5, sticky="e")
        self.entries["descrizione"] = ttk.Entry(self.root, width=fields["descrizione"]["width"])
        self.entries["descrizione"].grid(row=0, column=3, padx=5, pady=5)

        # Seconda riga: Prezzo, Disponibilità e Categoria
        ttk.Label(self.root, text=fields["prezzo"]["label"]).grid(row=1, column=0, padx=5, pady=5, sticky="e")
        self.entries["prezzo"] = ttk.Entry(self.root, width=fields["prezzo"]["width"], justify="right")
        self.entries["prezzo"].grid(row=1, column=1, padx=5, pady=5)

        ttk.Label(self.root, text=fields["disponibilita"]["label"]).grid(row=1, column=2, padx=5, pady=5, sticky="e")
        self.entries["disponibilita"] = ttk.Combobox(self.root, values=fields["disponibilita"]["options"], width=fields["disponibilita"]["width"])
        self.entries["disponibilita"].grid(row=1, column=3, padx=5, pady=5)

        ttk.Label(self.root, text=fields["id_categoria_default"]["label"]).grid(row=1, column=4, padx=5, pady=5, sticky="e")
        self.entries["id_categoria_default"] = ttk.Combobox(self.root, values=fields["id_categoria_default"]["options"], width=fields["id_categoria_default"]["width"])
        self.entries["id_categoria_default"].grid(row=1, column=5, padx=5, pady=5)

        # Pulsanti di azione principali
        self.new_button = ttk.Button(self.root, text="Nuovo", command=self.new_article)
        self.new_button.grid(row=2, column=0, padx=5, pady=10)

        self.modify_button = ttk.Button(self.root, text="Modifica", command=self.modify_article)
        self.modify_button.grid(row=2, column=1, padx=5, pady=10)

        self.delete_button = ttk.Button(self.root, text="Cancella", command=self.delete_article)
        self.delete_button.grid(row=2, column=2, padx=5, pady=10)

        # Tabella degli articoli
        self.article_table = ttk.Treeview(self.root, columns=("ID", "Descrizione", "Prezzo", "Disponibilità", "ID Categoria", "Categoria"), show="headings")
        self.article_table.heading("ID", text="ID")
        self.article_table.heading("Descrizione", text="Descrizione")
        self.article_table.heading("Prezzo", text="Prezzo")
        self.article_table.heading("Disponibilità", text="Disp.")
        self.article_table.heading("ID Categoria", text="Categoria")
        self.article_table.heading("Categoria", text="Categoria")
        self.article_table.grid(row=3, column=0, columnspan=6, pady=10)

        # Imposta la larghezza delle colonne
        self.article_table.column("ID", width=50)
        self.article_table.column("Descrizione", width=360)
        self.article_table.column("Prezzo", width=80)
        self.article_table.column("Disponibilità", width=40)
        self.article_table.column("ID Categoria", width=50)
        self.article_table.column("Categoria", width=200)

        # Nasconde la colonna ID Categoria
        self.article_table["displaycolumns"] = (0, 1, 2, 3, 5)
        
        # Evento di selezione della riga per modificare i campi
        self.article_table.bind("<ButtonRelease-1>", self.select_record)

        # Pulsanti "Salva" e "Annulla" (nascosti inizialmente)
        self.save_button = ttk.Button(self.root, text="Salva", command=self.save_changes)
        self.cancel_button = ttk.Button(self.root, text="Annulla", command=self.cancel_action)
        self.save_button.grid(row=2, column=2, pady=10)
        self.cancel_button.grid(row=2, column=3, pady=10)
        self.save_button.grid_remove()
        self.cancel_button.grid_remove()

    def load_articles(self):
        # Carica gli articoli esistenti nella tabella
        for row in self.article_table.get_children():
            self.article_table.delete(row)
        articles = articoli_controller.fetch_all_articles()
        for art in articles:
            self.article_table.insert("", "end", values=art)

    def select_record(self, event):
        # Carica i dati del record selezionato nei campi di input
        selected_item = self.article_table.selection()
        if selected_item:
            values = self.article_table.item(selected_item)["values"]
            self.entries["id_articolo"].config(state="normal")
            self.entries["id_articolo"].delete(0, tk.END)
            self.entries["id_articolo"].insert(0, values[0])
            self.entries["id_articolo"].config(state="readonly")
            self.entries["descrizione"].delete(0, tk.END)
            self.entries["descrizione"].insert(0, values[1])
            self.entries["prezzo"].delete(0, tk.END)
            self.entries["prezzo"].insert(0, values[2])
            self.entries["disponibilita"].set(values[3])
            self.entries["id_categoria_default"].set(values[5])

    def new_article(self):
        # Prepara l'interfaccia per l'inserimento di un nuovo articolo con ID non modificabile
        self.clear_fields()
        self.entries["id_articolo"].config(state="readonly")
        self.entries["descrizione"].focus_set()
        self.toggle_save_cancel_buttons(visible=True)

    def modify_article(self):
        # Prepara l'interfaccia per la modifica dell'articolo selezionato
        if not self.article_table.selection():
            messagebox.showwarning("Attenzione", "Seleziona un articolo da modificare.")
            return
        self.entries["descrizione"].focus_set()
        self.toggle_save_cancel_buttons(visible=True)

    def delete_article(self):
        # Conferma la cancellazione e rimuove il record selezionato
        if not self.article_table.selection():
            messagebox.showwarning("Attenzione", "Seleziona un articolo da cancellare.")
            return
        if messagebox.askyesno("Conferma", "Sei sicuro di voler cancellare questo articolo?"):
            try:
                articoli_controller.delete_article(self.entries)
                messagebox.showinfo("Successo", "Articolo cancellato con successo!")
                self.load_articles()
            except Exception as e:
                messagebox.showerror("Errore", f"Errore nella cancellazione dell'articolo: {e}")

    def save_changes(self):
        # Salva le modifiche apportate all'articolo
        try:
            if self.entries["id_articolo"].get():  # Se ID esiste, modifica
                articoli_controller.modify_article(self.entries)
                messagebox.showinfo("Successo", "Articolo modificato con successo!")
            else:  # Se ID è vuoto, inserisce nuovo articolo
                articoli_controller.insert_article(self.entries)
                messagebox.showinfo("Successo", "Articolo salvato con successo!")
            self.load_articles()
            self.toggle_save_cancel_buttons(visible=False)
        except Exception as e:
            messagebox.showerror("Errore", f"Errore nel salvataggio: {e}")

    def cancel_action(self):
        # Annulla l'azione corrente e nasconde i pulsanti "Salva" e "Annulla"
        self.clear_fields()
        self.toggle_save_cancel_buttons(visible=False)
        self.entries["id_articolo"].config(state="readonly")
        
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
    app = ArticoliGUI(root)
    root.mainloop()