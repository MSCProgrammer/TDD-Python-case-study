import tkinter as tk
from tkinter import ttk, messagebox
from controller import transazioni_controller
from datetime import datetime

class TransazioniGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("Gestione Transazioni")
        self.root.geometry("1080x700")
        self.root.minsize(1080, 700)     
        self.root.resizable(False, False)
           
        self.create_widgets()
        self.load_transazioni()  # Carica le transazioni all'avvio

    def create_widgets(self):
        # Label per la data corrente
        self.current_date_label = ttk.Label(self.root, text=f"Oggi: {datetime.now().strftime('%d-%m-%Y')}", foreground="green", font=("Helvetica", 16))
        self.current_date_label.grid(row=0, column=0, columnspan=6, pady=10)

        fields = {
            "id_transazione": {"label": "ID", "editable": False, "width": 10},
            "data_ora": {"label": "Data Ora riga", "editable": False, "width": 20},
            "id_turno": {"label": "Turno", "editable": True, "type": "dropdown", "options": list(transazioni_controller.get_turno_options().keys()), "width": 20},
            "des_turno": {"label": "Des. Turno", "editable": False, "width": 30},
            "id_operatore": {"label": "Operatore", "editable": True, "type": "dropdown", "options": list(transazioni_controller.get_operatore_options().keys()), "width": 20},
            "nome": {"label": "Des. Operatore", "editable": False, "width": 30},
            "id_articolo": {"label": "Articolo", "editable": True, "type": "dropdown", "options": list(transazioni_controller.get_articolo_options().keys()), "width": 30},
            "des_articolo": {"label": "Des. Articolo", "editable": False, "width": 30},
            "quantita": {"label": "Quantità", "editable": True, "width": 10},
            "valore_unitario": {"label": "Valore Unitario", "editable": True, "width": 10},
            "sconto": {"label": "Sconto", "editable": True, "width": 10},
            "tot_transazione": {"label": "Totale Transazione", "editable": False, "width": 15},
            "des_transazione": {"label": "Des. Transazione", "editable": True, "width": 50},
            "id_pagamento": {"label": "Pagamento", "editable": True, "type": "dropdown", "options": list(transazioni_controller.get_pagamento_options().keys()), "width": 20},
            "des_pagamento": {"label": "Des. Pagamento", "editable": False, "width": 30},
            "id_categoria": {"label": "Categoria", "editable": True, "type": "dropdown", "options": list(transazioni_controller.get_categoria_options().keys()), "width": 20},
            "des_categoria": {"label": "Des. Categoria", "editable": False, "width": 30}
        }

        self.entries = {}
        row_count = 1

        # Prima riga: ID Transazione, Turno, Operatore
        ttk.Label(self.root, text=fields["id_transazione"]["label"]).grid(row=row_count, column=0, padx=5, pady=5, sticky="e")
        self.entries["id_transazione"] = ttk.Entry(self.root, state="readonly", width=fields["id_transazione"]["width"])
        self.entries["id_transazione"].grid(row=row_count, column=1, padx=5, pady=5)

        ttk.Label(self.root, text=fields["id_turno"]["label"]).grid(row=row_count, column=2, padx=5, pady=5, sticky="e")
        self.entries["id_turno"] = ttk.Combobox(self.root, values=fields["id_turno"]["options"], state="readonly", width=fields["id_turno"]["width"])
        self.entries["id_turno"].grid(row=row_count, column=3, padx=5, pady=5)

        ttk.Label(self.root, text=fields["id_operatore"]["label"]).grid(row=row_count, column=4, padx=5, pady=5, sticky="e")
        self.entries["id_operatore"] = ttk.Combobox(self.root, values=fields["id_operatore"]["options"], state="readonly", width=fields["id_operatore"]["width"])
        self.entries["id_operatore"].grid(row=row_count, column=5, padx=5, pady=5)

        row_count += 1

        # Seconda riga: Articolo, Valore Unitario
        ttk.Label(self.root, text=fields["id_articolo"]["label"]).grid(row=row_count, column=0, padx=5, pady=5, sticky="e")
        self.entries["id_articolo"] = ttk.Combobox(self.root, values=fields["id_articolo"]["options"], state="readonly", width=fields["id_articolo"]["width"])
        self.entries["id_articolo"].grid(row=row_count, column=1, padx=5, pady=5)
        self.entries["id_articolo"].bind("<<ComboboxSelected>>", self.update_prezzo_unitario_and_categoria_default)
     
        ttk.Label(self.root, text=fields["valore_unitario"]["label"]).grid(row=row_count, column=2, padx=5, pady=5, sticky="e")
        self.entries["valore_unitario"] = ttk.Entry(self.root, width=fields["valore_unitario"]["width"], justify="right")
        self.entries["valore_unitario"].grid(row=row_count, column=3, padx=5, pady=5)
        self.entries["valore_unitario"].bind("<KeyRelease>", self.update_totale_transazione)

        ttk.Label(self.root, text=fields["id_categoria"]["label"]).grid(row=row_count, column=4, padx=5, pady=5, sticky="e")
        self.entries["id_categoria"] = ttk.Combobox(self.root, values=fields["id_categoria"]["options"], state="readonly", width=fields["id_categoria"]["width"])
        self.entries["id_categoria"].grid(row=row_count, column=5, padx=5, pady=5)
        self.entries["id_categoria"].bind("<<ComboboxSelected>>", self.update_totale_transazione)

        row_count += 1

        # Terza riga: Quantità, Sconto, Totale Transazione
        ttk.Label(self.root, text=fields["quantita"]["label"]).grid(row=row_count, column=0, padx=5, pady=5, sticky="e")
        self.entries["quantita"] = ttk.Entry(self.root, width=fields["quantita"]["width"], justify="right")
        self.entries["quantita"].grid(row=row_count, column=1, padx=5, pady=5)
        self.entries["quantita"].insert(0, "1")  # Imposta il valore di default della quantità a uno
        self.entries["quantita"].bind("<KeyRelease>", self.update_totale_transazione)

        ttk.Label(self.root, text=fields["sconto"]["label"]).grid(row=row_count, column=2, padx=5, pady=5, sticky="e")
        self.entries["sconto"] = ttk.Entry(self.root, width=fields["sconto"]["width"], justify="right")
        self.entries["sconto"].grid(row=row_count, column=3, padx=5, pady=5)
        self.entries["sconto"].insert(0, "0")  # Imposta il valore di default dello sconto a zero
        self.entries["sconto"].bind("<KeyRelease>", self.update_totale_transazione)

        ttk.Label(self.root, text=fields["tot_transazione"]["label"]).grid(row=row_count, column=4, padx=5, pady=5, sticky="e")
        self.entries["tot_transazione"] = ttk.Entry(self.root, state="readonly", width=fields["tot_transazione"]["width"], justify="right")
        self.entries["tot_transazione"].grid(row=row_count, column=5, padx=5, pady=5)

        row_count += 1

        # Quarta riga: Tipo Pagamento, Descrizione Transazione
        ttk.Label(self.root, text=fields["id_pagamento"]["label"]).grid(row=row_count, column=0, padx=5, pady=5, sticky="e")
        self.entries["id_pagamento"] = ttk.Combobox(self.root, values=fields["id_pagamento"]["options"], state="readonly", width=fields["id_pagamento"]["width"])
        self.entries["id_pagamento"].grid(row=row_count, column=1, padx=5, pady=5)
        self.entries["id_pagamento"].bind("<<ComboboxSelected>>", self.update_totale_transazione)

        ttk.Label(self.root, text=fields["des_transazione"]["label"]).grid(row=row_count, column=2, padx=5, pady=5, sticky="e")
        self.entries["des_transazione"] = ttk.Entry(self.root, width=fields["des_transazione"]["width"])
        self.entries["des_transazione"].grid(row=row_count, column=3, columnspan=3, padx=5, pady=5)

        ttk.Label(self.root, text=fields["data_ora"]["label"]).grid(row=row_count + 1, column=3, padx=5, pady=5, sticky="e")
        self.entries["data_ora"] = ttk.Entry(self.root, state="readonly", width=fields["data_ora"]["width"])
        self.entries["data_ora"].grid(row=row_count + 1, column=4, columnspan=3, padx=5, pady=5)

        row_count += 1

        # Pulsanti di azione principali
        self.new_button = ttk.Button(self.root, text="Nuovo", command=self.new_transazione)
        self.new_button.grid(row=row_count, column=0, pady=10)

        self.modify_button = ttk.Button(self.root, text="Modifica", command=self.modify_transazione)
        self.modify_button.grid(row=row_count, column=1, pady=10)

        self.delete_button = ttk.Button(self.root, text="Cancella", command=self.delete_transazione)
        self.delete_button.grid(row=row_count, column=2, pady=10)

        # Tabella delle transazioni
        self.transazioni_table = ttk.Treeview(self.root, columns=("ID", "Data Ora", "ID Turno", "Des. Turno", "ID Operatore", "Operatore", "ID Articolo", "Articolo", "Qtà", "Val. Unitario", "Sconto", "Totale", "Des. Transazione", "ID Pagamento", "Pagamento", "ID Categoria", "Categoria"), show="headings")
        for col in self.transazioni_table["columns"]:
            self.transazioni_table.heading(col, text=col)
        self.transazioni_table.grid(row=row_count + 1, column=0, columnspan=6, padx=10,pady=10)

        # Imposta la larghezza delle colonne
        self.transazioni_table.column("ID", width=50)
        self.transazioni_table.column("Data Ora", width=85)
        self.transazioni_table.column("ID Turno", width=50)
        self.transazioni_table.column("Des. Turno", width=100)
        self.transazioni_table.column("ID Operatore", width=50)
        self.transazioni_table.column("Operatore", width=100)
        self.transazioni_table.column("ID Articolo", width=50)
        self.transazioni_table.column("Articolo", width=100)
        self.transazioni_table.column("Qtà", width=40)
        self.transazioni_table.column("Val. Unitario", width=70)
        self.transazioni_table.column("Sconto", width=70)
        self.transazioni_table.column("Totale", width=80)
        self.transazioni_table.column("Des. Transazione", width=200)
        self.transazioni_table.column("ID Pagamento", width=50)
        self.transazioni_table.column("Pagamento", width=100)
        self.transazioni_table.column("ID Categoria", width=50)
        self.transazioni_table.column("Categoria", width=100)

        # Nasconde lle colonne non necessarie
        self.transazioni_table["displaycolumns"] = (1, 3, 5, 7, 8, 9, 10 ,11, 12, 14, 16)
                                   
        # Evento di selezione della riga per modificare i campi
        self.transazioni_table.bind("<ButtonRelease-1>", self.select_record)

        # Pulsanti "Salva" e "Annulla" (nascosti inizialmente)
        self.save_button = ttk.Button(self.root, text="Salva", command=self.save_changes)
        self.cancel_button = ttk.Button(self.root, text="Annulla", command=self.cancel_action)
        self.save_button.grid(row=5, column=1, pady=10)
        self.cancel_button.grid(row=5, column=2, pady=10)
        self.save_button.grid_remove()
        self.cancel_button.grid_remove()

        # Tabella dei totali per giorno
        self.totali_table = ttk.Treeview(self.root, columns=("ID Pagamento", "Pagamento", "Quantità Totale", "Transazione Totale"), show="headings")
        self.totali_table.heading("ID Pagamento", text="ID Pagamento")        
        self.totali_table.heading("Pagamento", text="Pagamento")
        self.totali_table.heading("Quantità Totale", text="Quantità Totale")
        self.totali_table.heading("Transazione Totale", text="Transazione Totale")
        self.totali_table.grid(row=row_count +3 , column=0, columnspan=6, pady=10)
        self.totali_table.column("Pagamento", width=150)
        self.totali_table.column("Quantità Totale", width=100)
        self.totali_table.column("Transazione Totale", width=200)

        # Nasconde lle colonne non necessarie
        self.totali_table["displaycolumns"] = (1, 2, 3)
        
    def load_transazioni(self):
        # Carica le transazioni esistenti nella tabella
        for row in self.transazioni_table.get_children():
            self.transazioni_table.delete(row)
        transazioni = transazioni_controller.get_transazioni_per_data(datetime.now().strftime("%Y-%m-%d"))
        for trans in transazioni:
            self.transazioni_table.insert("", "end", values=trans)
        if transazioni: # Se ci sono transazioni, aggiorna i totali    
          self.update_totali()

    def select_record(self, event):
        # Carica i dati del record selezionato nei campi di input
        selected_item = self.transazioni_table.selection()
        if selected_item:
            values = self.transazioni_table.item(selected_item)["values"]
            self.entries["id_transazione"].config(state="normal")
            self.entries["id_transazione"].delete(0, tk.END)
            self.entries["id_transazione"].insert(0, values[0])
            self.entries["id_transazione"].config(state="readonly")
            self.entries["id_turno"].set(values[2])
            self.entries["id_operatore"].set(values[4])
            self.entries["quantita"].delete(0, tk.END)
            self.entries["quantita"].insert(0, values[8])
            self.entries["valore_unitario"].delete(0, tk.END)
            self.entries["valore_unitario"].insert(0, values[9])
            self.entries["sconto"].delete(0, tk.END)
            self.entries["sconto"].insert(0, values[10])
            self.entries["tot_transazione"].config(state="normal")
            self.entries["tot_transazione"].delete(0, tk.END)
            self.entries["tot_transazione"].insert(0, values[11])
            self.entries["tot_transazione"].config(state="readonly")
            self.entries["des_transazione"].delete(0, tk.END)
            self.entries["des_transazione"].insert(0, values[12])

            # Conversione della data   
            data_ora = datetime.strptime(values[1], "%Y-%m-%d")
            data_ora_formattata = data_ora.strftime("%d-%m-%Y")
            self.entries["data_ora"].config(state="normal")
            self.entries["data_ora"].delete(0, tk.END)
            self.entries["data_ora"].insert(0, data_ora_formattata)
            self.entries["data_ora"].config(state="readonly")
        
            articolo_options = transazioni_controller.get_articolo_options()
            id_articolo = values[6]
            descrizione_articolo = [k for k, v in articolo_options.items() if v == id_articolo]
            self.entries["id_articolo"].set(descrizione_articolo)
            
            turno_options = transazioni_controller.get_turno_options()
            id_turno = values[2]
            descrizione_turno = [k for k, v in turno_options.items() if v == id_turno][0]
            self.entries["id_turno"].set(descrizione_turno)
            
            pagamento_options = transazioni_controller.get_pagamento_options()
            id_pagamento = values[13]
            descrizione_pagamento = [k for k, v in pagamento_options.items() if v == id_pagamento][0]
            self.entries["id_pagamento"].set(descrizione_pagamento)
            
            categoria_options = transazioni_controller.get_categoria_options()
            id_categoria = values[15]
            descrizione_categoria = [k for k, v in categoria_options.items() if v == id_categoria][0]
            self.entries["id_categoria"].set(descrizione_categoria)
            
            operatore_options = transazioni_controller.get_operatore_options()
            id_operatore = values[4]
            descrizione_operatore = [k for k, v in operatore_options.items() if v == id_operatore][0]
            self.entries["id_operatore"].set(descrizione_operatore)
                        
    def new_transazione(self):
        # Prepara l'interfaccia per l'inserimento di una nuova transazione con ID non modificabile
        self.clear_fields()
        self.entries["id_transazione"].config(state="readonly")
        self.entries["tot_transazione"].config(state="readonly")
        self.entries["id_categoria"].config(state="readonly")
        self.entries["data_ora"].config(state="normal")
        self.entries["data_ora"].delete(0, tk.END)
        self.entries["data_ora"].insert(0, datetime.now().strftime("%d-%m-%Y"))
        self.entries["data_ora"].config(state="readonly")
        self.entries["id_turno"].focus_set()
        self.toggle_save_cancel_buttons(visible=True)

    def modify_transazione(self):
        # Prepara l'interfaccia per la modifica della transazione selezionata
        if not self.transazioni_table.selection():
            messagebox.showwarning("Attenzione", "Seleziona una transazione da modificare.")
            return
        self.entries["id_turno"].focus_set()
        self.toggle_save_cancel_buttons(visible=True)

    def delete_transazione(self):
        # Conferma la cancellazione e rimuove il record selezionato
        if not self.transazioni_table.selection():
            messagebox.showwarning("Attenzione", "Seleziona una transazione da cancellare.")
            return
        if messagebox.askyesno("Conferma", "Sei sicuro di voler cancellare questa transazione?"):
            try:
                transazioni_controller.delete_transazione(self.entries)
                messagebox.showinfo("Successo", "Transazione cancellata con successo!")
                self.load_transazioni()
            except Exception as e:
                messagebox.showerror("Errore", f"Errore nella cancellazione della transazione: {e}")

    def save_changes(self):
        # Salva le modifiche apportate alla transazione
        try:
            # Recupera i valori dai campi di input
            id_transazione = self.entries["id_transazione"].get()
            des_transazione = self.entries["des_transazione"].get()
            
            quantita = float(self.entries["quantita"].get())
            valore_unitario = float(self.entries["valore_unitario"].get())
            sconto = float(self.entries["sconto"].get())
            tot_transazione = quantita * (valore_unitario - sconto)
            self.entries["tot_transazione"].config(state="normal")
            self.entries["tot_transazione"].delete(0, tk.END)
            self.entries["tot_transazione"].insert(0, tot_transazione)
            self.entries["tot_transazione"].config(state="readonly")

            turno_options = transazioni_controller.get_turno_options()
            descrizione_turno = self.entries["id_turno"].get()
            id_turno = turno_options.get(descrizione_turno)
            
            if id_turno is None:
                raise ValueError("Turno non valido")

            operatore_options = transazioni_controller.get_operatore_options()
            descrizione_operatore = self.entries["id_operatore"].get()
            id_operatore = operatore_options.get(descrizione_operatore)
            
            if id_operatore is None:
                raise ValueError("Operatore non valido")
            
            articolo_options = transazioni_controller.get_articolo_options()
            descrizione_articolo = self.entries["id_articolo"].get()
            id_articolo = articolo_options.get(descrizione_articolo)
            
            if id_articolo is None:
                raise ValueError("Articolo non valido")

            pagamento_options = transazioni_controller.get_pagamento_options()
            descrizione_pagamento = self.entries["id_pagamento"].get()
            id_pagamento = pagamento_options.get(descrizione_pagamento)
            
            if id_pagamento is None:
                raise ValueError("Tipo di pagamento non valido")

            #self.entries["id_pagamento"].set(id_pagamento)

            categoria_options = transazioni_controller.get_categoria_options()
            descrizione_categoria = self.entries["id_categoria"].get()
            id_categoria = categoria_options.get(descrizione_categoria)
            
            if id_categoria is None:
                raise ValueError("Categoria non valida")

            if self.entries["id_transazione"].get():  # Se ID esiste, modifica
                transazioni_controller.modify_transazione(id_transazione, id_turno, id_operatore, id_articolo, quantita, valore_unitario, sconto, tot_transazione, des_transazione, id_pagamento, id_categoria)
                messagebox.showinfo("Successo", "Transazione modificata con successo!")
            else:  # Se ID è vuoto, inserisce nuova transazione
                transazioni_controller.insert_transazione(id_turno, id_operatore, id_articolo, quantita, valore_unitario, sconto, tot_transazione, des_transazione, id_pagamento, id_categoria)
                messagebox.showinfo("Successo", "Transazione salvata con successo!")
                self.transazioni_table.selection_set()
            self.load_transazioni()
            self.toggle_save_cancel_buttons(visible=False)
            
        except Exception as e:
            messagebox.showerror("Errore", f"Errore nel salvataggio: {e}")
    
    def cancel_action(self):
        # Annulla l'azione corrente e nasconde i pulsanti "Salva" e "Annulla"
        self.clear_fields()
        self.toggle_save_cancel_buttons(visible=False)

    def clear_fields(self):
        # Pulisce i campi di input
        for entry in self.entries.values():
            entry.config(state="normal")
            entry.delete(0, tk.END)
        
        # Imposta i campi read only
        self.entries["id_transazione"].config(state="readonly")
        self.entries["tot_transazione"].config(state="readonly")
        self.entries["id_categoria"].config(state="readonly")
        self.entries["data_ora"].config(state="readonly")

    
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

    def update_totali(self):
        # Aggiorna i totali per giorno
        data = datetime.now().strftime("%Y-%m-%d")
        totali = transazioni_controller.get_totali_per_giorno(data)
        for row in self.totali_table.get_children():
            self.totali_table.delete(row)
        for id_pagamento, des_pagamento, totale_quantita, totale_transazione in totali:
            self.totali_table.insert("", "end", values=(id_pagamento, des_pagamento, totale_quantita, totale_transazione))
        
    def update_prezzo_unitario_and_categoria_default(self, event):
        # Aggiorna il campo "Categoria" quando un articolo viene selezionato
        articolo = self.entries["id_articolo"].get()
        id_articolo = transazioni_controller.get_articolo_options()[articolo]
        id_categoria_default = transazioni_controller.get_categoria_default(id_articolo)
        categoria_options = transazioni_controller.get_categoria_options()
        descrizione_categoria = [k for k, v in categoria_options.items() if v == id_categoria_default][0]
        self.entries["id_categoria"].set(descrizione_categoria)
        
        # Aggiorna il campo "Prezzo Unitario" quando un articolo viene selezionato
        articolo = self.entries["id_articolo"].get()
        id_articolo = transazioni_controller.get_articolo_options()[articolo]
        prezzo_unitario = transazioni_controller.get_prezzo_unitario(id_articolo)
        self.entries["valore_unitario"].delete(0, tk.END)
        self.entries["valore_unitario"].insert(0, prezzo_unitario)
        self.update_totale_transazione()

    def update_totale_transazione(self, event=None):
        # Aggiorna il campo "Totale Transazione" quando la quantità o il prezzo unitario cambiano
        try:
            # Se la quantità o il prezzo unitario sono vuoti, non fare nulla
            if not self.entries["quantita"].get() or not self.entries["valore_unitario"].get():
                return
            quantita = float(self.entries["quantita"].get())
            valore_unitario = float(self.entries["valore_unitario"].get())
            # Se lo sconto è vuoto, imposta il valore a zero
            if not self.entries["sconto"].get():
                self.entries["sconto"].insert(0, "0")
            sconto = float(self.entries["sconto"].get())
            tot_transazione = quantita * (valore_unitario - sconto)
            self.entries["tot_transazione"].config(state="normal")
            self.entries["tot_transazione"].delete(0, tk.END)
            self.entries["tot_transazione"].insert(0, tot_transazione)
            self.entries["tot_transazione"].config(state="readonly")
        except ValueError:
            pass  # Ignora gli errori di conversione


if __name__ == "__main__":
    root = tk.Tk()
    app = TransazioniGUI(root)
    root.mainloop()