import os
import tkinter as tk
from tkinter import ttk
from gui.articoli_gui import ArticoliGUI
from gui.operatori_gui import OperatoriGUI
from gui.pagamenti_gui import PagamentiGUI
from gui.turni_gui import TurniGUI
from gui.categorie_gui import CategorieGUI
from gui.transazioni_gui import TransazioniGUI  # Importa la GUI per le transazioni
from gui.report_gui import ReportGUI
#from controller import app_controller
from datetime import datetime


# Legge il nome del file logo dalla variabile d'ambiente
CASH_FLOW_LOGO = os.getenv("CASH_FLOW_LOGO", "img/logo.png")

class StartHome:
    def __init__(self):
        # Inizializza la finestra principale dell'applicazione
        self.root = tk.Tk()
        self.root.title("Gestione Flusso di Cassa - Museo")
        self.root.geometry("600x500")
        self.root.resizable(False, False)

        # Configurazione del logo a sinistra
        self.add_logo()
        
        # Crea i widget principali
        self.create_main_widgets()     
                
        # Aggiorna data e ora continuamente
        self.update_datetime()
        
        # Centra la finestra principale
        self.center_window(self.root)  
        
    def add_logo(self):
        # Inserisce il logo sulla sinistra
        left_frame = tk.Frame(self.root)
        left_frame.pack(side="left", padx=10, pady=10)
        try:
            self.logo_img = tk.PhotoImage(file=CASH_FLOW_LOGO)  
            logo_label = ttk.Label(left_frame, image=self.logo_img)
            logo_label.pack()
        except Exception as e:
            print(f"Errore nel caricamento del logo: {e}")
        
    def update_datetime(self):
        # Aggiorna la data e l'ora
        self.datetime_label.config(text=f"Oggi: {datetime.now().strftime('%d-%m-%Y %H:%M:%S')}", foreground="green", font=("Helvetica", 16))
        # Chiama la funzione ogni secondo per aggiornare l'orario
        self.root.after(1000, self.update_datetime)
        
    def create_main_widgets(self):
        # Creazione di un titolo
        title_label = ttk.Label(self.root, text="Gestione Flusso di Cassa", font=("Helvetica", 16))
        title_label.pack(pady=10)

        # Etichetta per data e ora
        self.datetime_label = ttk.Label(self.root, font=("Helvetica", 12))
        self.datetime_label.pack(pady=15)

        # Pulsante evidenziato per "Nuova Transazione"
        new_transaction_button = ttk.Button(self.root, text="NUOVA TRANSAZIONE", command=self.open_transazioni, width=70)
        new_transaction_button.pack(pady=25)
        
        # Etichetta TEST
        self.test_label = ttk.Label(self.root, font=("Helvetica", 12), text="REPORT")
        self.test_label.pack(pady=15)

        # Pulsante per invio report giornaliero
        self.report_button = ttk.Button(self.root, text="Invia Report Giornaliero", command=self.open_report_window, width=50)
        self.report_button.pack(pady=20)

        # Etichetta anagrafiche di Base
        self.test_label = ttk.Label(self.root, font=("Helvetica", 12), text="ANAGRAFICHE DI BASE")
        self.test_label.pack(pady=15)
        
        # Frame per i pulsanti di gestione delle entità
        button_frame = tk.Frame(self.root,border=1,borderwidth=1)
        button_frame.pack(side="top")
        button_frame.pack(pady=20)

        # Pulsanti per aprire ciascuna finestra di gestione CRUD
        ttk.Button(button_frame, text="Gestione Categorie", command=self.open_categorie).grid(row=0, column=0, padx=10, pady=5)
        ttk.Button(button_frame, text="Gestione Articoli", command=self.open_articoli).grid(row=0, column=1, padx=10, pady=5)
        ttk.Button(button_frame, text="Gestione Pagamenti", command=self.open_pagamenti).grid(row=1, column=0, padx=10, pady=5)
        ttk.Button(button_frame, text="Gestione Operatori", command=self.open_operatori).grid(row=1, column=1, padx=10, pady=5)
        ttk.Button(button_frame, text="Gestione Turni", command=self.open_turni).grid(row=2, column=0, padx=10, pady=5)


    # Apertura delle GUI CRUD per ogni entità
    def open_articoli(self):
        articoli_window = tk.Toplevel(self.root)
        ArticoliGUI(articoli_window)

    def open_operatori(self):
        operatori_window = tk.Toplevel(self.root)
        OperatoriGUI(operatori_window)

    def open_pagamenti(self):
        pagamenti_window = tk.Toplevel(self.root)
        PagamentiGUI(pagamenti_window)

    def open_turni(self):
        turni_window = tk.Toplevel(self.root)
        TurniGUI(turni_window)

    def open_categorie(self):
        categorie_window = tk.Toplevel(self.root)
        CategorieGUI(categorie_window)

    def open_transazioni(self):
        # Apre la finestra di gestione transazioni
        transazioni_window = tk.Toplevel(self.root)
        TransazioniGUI(transazioni_window)

    def send_daily_report(self):
        app_controller.send_report()  # Chiama il controller per inviare il report

    def open_report_window(self):
        report_window = tk.Toplevel(self.root)
        ReportGUI(report_window)
        
    def run(self):
        # Avvia il loop principale dell'applicazione
        self.root.mainloop()


    def open_modal_window(self, window_class):
        # Funzione generica per aprire finestre modali
        modal_window = tk.Toplevel(self.root)
        modal_window.transient(self.root)  # Imposta la finestra come secondaria rispetto alla main window
        modal_window.grab_set()  # Impedisce l'interazione con la finestra principale
        modal_window.geometry("400x300")  # Dimensioni della finestra modale
        window_instance = window_class(modal_window)  # Inizializza l'istanza della finestra modale
        self.center_window(modal_window)  # Centra la finestra modale
        self.root.wait_window(modal_window)  # Aspetta che la finestra venga chiusa
        
    def center_window(self, window):
        window.update_idletasks()
        width = window.winfo_width()
        height = window.winfo_height()
        x = (window.winfo_screenwidth() // 2) - (width // 2)
        y = (window.winfo_screenheight() // 2) - (height // 2)
        window.geometry(f'{width}x{height}+{x}+{y}')
        
    def open_articoli(self):
        # Apre la gestione articoli come finestra modale
        self.open_modal_window(ArticoliGUI)

    def open_operatori(self):
        # Apre la gestione operatori come finestra modale
        self.open_modal_window(OperatoriGUI)

    def open_pagamenti(self):
        # Apre la gestione pagamenti come finestra modale
        self.open_modal_window(PagamentiGUI)

    def open_turni(self):
        # Apre la gestione turni come finestra modale
        self.open_modal_window(TurniGUI)

    def open_categorie(self):
        # Apre la gestione categorie come finestra modale
        self.open_modal_window(CategorieGUI)

    def open_transazioni(self):
        # Apre la gestione transazioni come finestra modale
        self.open_modal_window(TransazioniGUI)

    def open_report_window(self):
        self.open_modal_window(ReportGUI)
