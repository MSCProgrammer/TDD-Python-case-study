# Museo Cash Flow

Questo progetto è un **sistema di gestione del flusso di cassa** per una biglietteria di un museo e un bookshop. L'applicazione gestisce la vendita di biglietti e articoli del negozio, inclusi report e invio email. Il progetto è sviluppato in Python utilizzando la metodologia **Test-Driven Development (TDD)**.

## Funzionalità principali

- **Gestione articoli**: aggiunta, modifica e visualizzazione di articoli (inclusi biglietti e prodotti del bookshop).
- **Gestione operatori**: gestione degli addetti alle vendite.
- **Gestione turni**: registrazione delle vendite per turno (mattina/pomeriggio).
- **Gestione transazioni**: registrazione delle transazioni di vendita.
- **Report e invio email**: generazione di report PDF e CSV ed invio email.

## Struttura del progetto

/museum-cash-flow
│
├── /src
│   ├── /gui                   # Moduli per l'interfaccia grafica (Tkinter)
│   ├── /db                    # Gestione del database (SQLite)
│   ├── /controllers           # Logica dell'applicazione
│   ├── /img                   # Immagini usate nell'applicazione
│   └── main.py                # Avvio dell'applicazione
│
├── /tests                     # Test automatizzati con pytest
│
├── /reports                    # Directory per i report generati
│
├── /cash_flow.db               # File Database (SQLite)
│
├── requirements.txt            # Dipendenze del progetto
└── README.md                   # Documentazione del progetto
