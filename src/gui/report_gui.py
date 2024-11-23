import os
import tkinter as tk
from tkinter import ttk, messagebox
from controller import report_controller
from datetime import datetime

class ReportGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("Invia Report Giornaliero")
        self.root.geometry("1060x550")
        self.root.resizable(False, False)

        self.create_widgets()

    def create_widgets(self):
        oggi = datetime.now()
        giorno = oggi.day
        mese = oggi.month
        anno = oggi.year

        # Selezione della data iniziale
        ttk.Label(self.root, text="Data Iniziale:").grid(row=0, column=0, padx=5, pady=5, sticky="e")
        self.start_date = ttk.Combobox(self.root, values=[str(i) for i in range(1, 32)], width=5)
        self.start_date.set(str(giorno))
        self.start_date.grid(row=0, column=1, padx=5, pady=5)

        # Selezione del mese iniziale
        ttk.Label(self.root, text="Mese Iniziale:").grid(row=0, column=2, padx=5, pady=5, sticky="e")
        self.start_month = ttk.Combobox(self.root, values=[str(i) for i in range(1, 13)], width=5)
        self.start_month.set(str(mese))
        self.start_month.grid(row=0, column=3, padx=5, pady=5)

        # Selezione dell'anno iniziale
        anni = [str(anno) for anno in range(anno - 3, anno + 2)]
        ttk.Label(self.root, text="Anno Iniziale:").grid(row=0, column=4, padx=5, pady=5, sticky="e")
        self.start_year = ttk.Combobox(self.root, values=anni, width=7)
        self.start_year.set(str(anno))
        self.start_year.grid(row=0, column=5, padx=5, pady=5)

        # Selezione della data finale
        ttk.Label(self.root, text="Data Finale:").grid(row=1, column=0, padx=2, pady=5, sticky="e")
        self.end_date = ttk.Combobox(self.root, values=[str(i) for i in range(1, 32)], width=5)
        self.end_date.set(str(giorno))
        self.end_date.grid(row=1, column=1, padx=5, pady=5)

        # Selezione del mese finale
        ttk.Label(self.root, text="Mese Finale:").grid(row=1, column=2, padx=5, pady=5, sticky="e")
        self.end_month = ttk.Combobox(self.root, values=[str(i) for i in range(1, 13)], width=5)
        self.end_month.set(str(mese))
        self.end_month.grid(row=1, column=3, padx=5, pady=5)

        # Selezione dell'anno finale
        ttk.Label(self.root, text="Anno Finale:").grid(row=1, column=4, padx=5, pady=5, sticky="e")
        self.end_year = ttk.Combobox(self.root, values=anni, width=7)
        self.end_year.set(str(anno))
        self.end_year.grid(row=1, column=5, padx=5, pady=5)

        # Pulsante per cercare le transazioni
        self.search_button = ttk.Button(self.root, text="Cerca", command=self.search_transactions)
        self.search_button.grid(row=2, column=0, columnspan=3, pady=5)

        # Pulsante per resettare i campi
        self.reset_button = ttk.Button(self.root, text="Reset", command=self.reset_fields)
        self.reset_button.grid(row=2, column=3, columnspan=3, pady=5)

        # Tabella delle transazioni
        self.transazioni_table = ttk.Treeview(self.root, columns=("ID", "Data Ora", "ID Turno", "Des. Turno", "ID Operatore", "Operatore", "ID Articolo", "Articolo", "Qtà", "Val. Unitario", "Sconto", "Totale", "Des. Transazione", "ID Pagamento", "Pagamento", "ID Categoria", "Categoria"), show="headings")
        for col in self.transazioni_table["columns"]:
            self.transazioni_table.heading(col, text=col)
        self.transazioni_table.grid(row=3, column=0, columnspan=6, padx=10, pady=10)

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

        # Nascondo le colonne non necessarie
        self.transazioni_table["displaycolumns"] = (1, 3, 5, 7, 8, 9, 10 ,11, 12, 14, 16)

        # Label per mostrare le somme
        self.summary_label = ttk.Label(self.root, text="", font=("Helvetica", 12))
        self.summary_label.grid(row=4, column=1, columnspan=6, padx=10, pady=5)
        
        # Pulsante per generare il report PDF
        self.generate_pdf_button = ttk.Button(self.root, text="Genera Report PDF", command=self.export_to_pdf)
        self.generate_pdf_button.grid(row=4, column=0, columnspan=3, padx=10, pady=10)

        # Aggiungi il pulsante per l'export su Excel nella tua GUI
        self.export_excel_button = ttk.Button(self.root, text="Genera Report Excel", command=self.export_to_excel)
        self.export_excel_button.grid(row=4, column=5, padx=10, pady=10)

        # Pulsante per inviare il report via email
        self.send_email_button = ttk.Button(self.root, text="Invia Report via Email", command=self.send_email)
        self.send_email_button.grid(row=7, column=4, columnspan=3, pady=5)
        
        # Campo per il mittente dell'email
        ttk.Label(self.root, text="Mittente:").grid(row=6, column=0, padx=5, pady=5, sticky="e")
        self.sender_email = ttk.Entry(self.root, width=30)
        self.sender_email.grid(row=6, column=1, columnspan=3, padx=5, pady=5)
        
        # Imposta il destinatario di default
        self.sender_email.insert(0, "biglietteria@museo.com")

        # Campo per il destinatario dell'email
        ttk.Label(self.root, text="Destinatario:").grid(row=7, column=0, padx=5, pady=5, sticky="e")
        self.recipient_email = ttk.Entry(self.root, width=30)
        self.recipient_email.grid(row=7, column=1, columnspan=2, padx=5, pady=5)
        
         # Imposta il destinatario di default
        self.recipient_email.insert(0, "contabilita@museo.com")
      
        # Dropdown list per selezionare il servizio SMTP
        ttk.Label(self.root, text="Servizio SMTP:").grid(row=6, column=3, padx=10, pady=10, sticky="e")
        self.smtp_service = ttk.Combobox(self.root, values=["Gmail", "Yahoo", "Outlook"], width=20)
        self.smtp_service.grid(row=6, column=4, columnspan=2, padx=10, pady=10)
        self.smtp_service.set("Gmail")
        
        # Effettuo la ricerca delle transazioni all'avvio
        self.search_transactions()

    def search_transactions(self):
        start_date = f"{self.start_year.get()}-{self.start_month.get()}-{self.start_date.get()}"
        end_date = f"{self.end_year.get()}-{self.end_month.get()}-{self.end_date.get()}"
        try:
            transazioni = report_controller.get_transazioni_per_periodo(start_date, end_date)
            self.update_treeview(transazioni)
            self.update_summary(transazioni)
            self.send_email_button.focus_set()
        except Exception as e:
            messagebox.showerror("Errore", f"Errore nella ricerca delle transazioni: {e}")

    def reset_fields(self):
        self.start_date.set(str(datetime.now().day))
        self.start_month.set(str(datetime.now().month))
        self.start_year.set(str(datetime.now().year))
        self.end_date.set(str(datetime.now().day))
        self.end_month.set(str(datetime.now().month))
        self.end_year.set(str(datetime.now().year))
        self.sender_email.delete(0, tk.END)
        self.recipient_email.delete(0, tk.END)
        for row in self.transazioni_table.get_children():
            self.transazioni_table.delete(row)
        self.summary_label.config(text="")

    def export_to_pdf(self):
        start_date = f"{self.start_year.get()}-{self.start_month.get()}-{self.start_date.get()}"
        end_date = f"{self.end_year.get()}-{self.end_month.get()}-{self.end_date.get()}"
        nome_file = os.path.abspath(f"reports/report_transazioni_{start_date}_to_{end_date}.pdf")
        try:
            transazioni = report_controller.get_transazioni_per_periodo(start_date, end_date)
            if transazioni:
                report_controller.generate_pdf(transazioni, nome_file, start_date, end_date)
                self.update_treeview(transazioni)
                self.update_summary(transazioni)
                nome_file = os.path.abspath(nome_file)
                if messagebox.askyesno("Successo", f"Report PDF generato con successo! \n {nome_file} \n Vuoi aprirlo?"):
                    import webbrowser
                    webbrowser.open_new(nome_file)
            else:
                messagebox.showinfo("Nessuna transazione", "Nessuna transazione trovata per il periodo selezionato")
        except Exception as e:
            messagebox.showerror("Errore", f"Errore nella generazione del report PDF: {e}")

    def export_to_excel(self):
        start_date = f"{self.start_year.get()}-{self.start_month.get()}-{self.start_date.get()}"
        end_date = f"{self.end_year.get()}-{self.end_month.get()}-{self.end_date.get()}"
        nome_file = os.path.abspath(f"reports/report_transazioni_{start_date}_to_{end_date}.xlsx")
        try:
            transazioni = report_controller.get_transazioni_per_periodo(start_date, end_date)
            if transazioni:
                report_controller.generate_xlsx(transazioni, nome_file, start_date, end_date)
                self.update_treeview(transazioni)
                self.update_summary(transazioni)
                nome_file = os.path.abspath(nome_file)
                if messagebox.askyesno("Successo", f"Report Excel generato con successo! \n {nome_file} \n Vuoi aprirlo?"):
                    import webbrowser
                    webbrowser.open_new(nome_file)
            else:
                messagebox.showinfo("Nessuna transazione", "Nessuna transazione trovata per il periodo selezionato")
        except Exception as e:
            messagebox.showerror("Errore", f"Errore nella generazione del report EXSL: {e}")

        
    def send_email(self):
        start_date = f"{self.start_year.get()}-{self.start_month.get()}-{self.start_date.get()}"
        end_date = f"{self.end_year.get()}-{self.end_month.get()}-{self.end_date.get()}"
        sender = self.sender_email.get()
        recipient = self.recipient_email.get()
        try:
            transazioni = report_controller.get_transazioni_per_periodo(start_date, end_date)
            if transazioni:
                nome_file = f"reports/report_transazioni_{start_date}_to_{end_date}"
                report_controller.generate_pdf(transazioni, nome_file+".pdf", start_date, end_date)
                report_controller.generate_xlsx(transazioni, nome_file+".xlsx", start_date, end_date)
                report_controller.send_email(nome_file, sender, recipient, self.smtp_service.get())
                self.update_treeview(transazioni)
                self.update_summary(transazioni)
                messagebox.showinfo("Successo", "Report inviato via email con successo!")
            else:
                messagebox.showinfo("Nessuna transazione", "Nessuna transazione trovata per il periodo selezionato")
        except Exception as e:
            messagebox.showerror("Errore", f"Errore nell'invio del report via email: {e}")

    def update_treeview(self, transazioni):
        for row in self.transazioni_table.get_children():
            self.transazioni_table.delete(row)
        for trans in transazioni:
            self.transazioni_table.insert("", "end", values=trans)

    def update_summary(self, transazioni):
        summary = {}
        for trans in transazioni:
            id_pagamento = trans[13]
            des_pagamento = trans[14]
            quantita = trans[8]
            tot_transazione = trans[11]
            if id_pagamento not in summary:
                summary[id_pagamento] = {"des_pagamento": des_pagamento, "quantita": 0, "tot_transazione": 0}
            summary[id_pagamento]["quantita"] += quantita
            summary[id_pagamento]["tot_transazione"] += tot_transazione

        if transazioni:
            summary_text = f"Totali per tipo di pagamento:\n"
            for id_pagamento, data in summary.items():
                summary_text += f"{data['des_pagamento']}  Quantità: {data['quantita']} - "
                summary_text += f"Transato: {data['tot_transazione']}\n"
        else:
            summary_text = "Nessuna transazione trovata"
        self.summary_label.config(text=summary_text, foreground="green", font=("Helvetica", 16))
        
if __name__ == "__main__":
    root = tk.Tk()
    app = ReportGUI(root)
    root.mainloop()