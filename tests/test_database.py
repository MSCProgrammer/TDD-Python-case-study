
import os
import pytest
from src.db.database import create_tables, add_minimum_data, get_all_operatori, get_all_categorie, get_all_articoli, get_all_turni, get_all_pagamenti

DB_PATH = os.getenv("CASH_FLOW_DB_NAME", "cash_flow.db")
 
@pytest.fixture(scope="module", autouse=True)
def setup_database():
    # Creazione del database e delle tabelle, oltre all'inserimento dei dati minimi
    create_tables()
    add_minimum_data()

def test_database_existence():
    # Verifica se il file del database esiste
    assert os.path.exists(DB_PATH), "Il database non esiste!"
    
def test_get_all_operatori():
    """
    Test per verificare che ci sia almeno un operatore nel database.
    """
    operatori = get_all_operatori()
    assert len(operatori) >= 1, "Non ci sono operatori nel database"

def test_get_all_categorie():
    """
    Test per verificare che ci sia almeno una categoria nel database.
    """
    categorie = get_all_categorie()
    assert len(categorie) >= 1, "Non ci sono categorie nel database"

def test_get_all_articoli():
    """
    Test per verificare che ci sia almeno un articolo nel database.
    """
    articoli= get_all_articoli()
    assert len(articoli) >= 1, "Non ci sono articoli nel database"

def test_get_all_turni():
    """
    Test per verificare che ci sia almeno un turno nel database.
    """
    turni = get_all_turni()
    assert len(turni) >= 1, "Non ci sono turni nel database"

def test_get_all_pagamenti():
    """
    Test per verificare che ci sia almeno una modalità di pagamento nel database.
    """
    pagamenti = get_all_pagamenti()
    assert len(pagamenti) >= 1, "Non ci sono modalità di pagamento nel database"


 