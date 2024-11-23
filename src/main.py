import os
import json
from gui.start_home import StartHome  # Import corretto della classe StartHome

# Definisci la variabile d'ambiente per il nome del database
os.environ["CASH_FLOW_DB_NAME"] = "cash_flow.db"
  
# Definisci la variabile d'ambiente per il nome file logo
os.environ["CASH_FLOW_LOGO"] = "img/logo.png"

if __name__ == "__main__":
    app = StartHome()  # Creazione dell'istanza con il nome della classe corretto
    app.run()  # Avvio dell'applicazione
    