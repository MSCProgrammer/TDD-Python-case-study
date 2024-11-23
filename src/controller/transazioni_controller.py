import sqlite3
import os
from datetime import datetime

# Legge il nome del database dalla variabile d'ambiente
DATABASE_NAME = os.getenv("CASH_FLOW_DB_NAME", "cash_flow.db")

def create_connection():
    """Crea e restituisce una connessione al database"""
    return sqlite3.connect(DATABASE_NAME)

def get_turno_options():
    """Recupera le opzioni dei turni dal database per popolare la dropdown"""
    conn = create_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT id_turno, des_turno FROM Turni")
    options = {row[1]: row[0] for row in cursor.fetchall()}
    conn.close()
    return options

def get_operatore_options():
    """Recupera le opzioni degli operatori dal database per popolare la dropdown"""
    conn = create_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT id_operatore, (nome  || ' ' || cognome) as operatore FROM Operatori")
    options = {row[1]: row[0] for row in cursor.fetchall()}
    conn.close()
    return options

def get_articolo_options():
    """Recupera le opzioni degli articoli dal database per popolare la dropdown"""
    conn = create_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT id_articolo, des_articolo FROM Articoli")
    options = {row[1]: row[0] for row in cursor.fetchall()}
    conn.close()
    return options

def get_categoria_options():
    """Recupera le opzioni delle categorie dal database per popolare la dropdown"""
    conn = create_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT id_categoria, des_categoria FROM Categorie")
    options = {row[1]: row[0] for row in cursor.fetchall()}
    conn.close()
    return options

def get_prezzo_unitario(id_articolo):
    """Recupera il prezzo unitario di un articolo dato il suo ID"""
    conn = create_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT cast(prezzo as decimal) FROM Articoli WHERE id_articolo = ?", (id_articolo,))
    prezzo = cursor.fetchone()[0]
    conn.close()
    return prezzo

def get_categoria_default(id_articolo):
    """Recupera il valore di default della categoria per un articolo dato il suo ID"""
    conn = create_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT id_categoria_default FROM Articoli WHERE id_articolo = ?", (id_articolo,))
    id_categoria_default = cursor.fetchone()[0]
    conn.close()
    return id_categoria_default

def get_pagamento_options():
    """Recupera le opzioni di pagamento dal database per popolare la dropdown"""
    conn = create_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT id_pagamento, des_pagamento FROM Pagamenti")
    options = {row[1]: row[0] for row in cursor.fetchall()}
    conn.close()
    return options

def insert_transazione(id_turno, id_operatore, id_articolo, quantita, valore_unitario, sconto, tot_transazione, des_transazione, id_pagamento, id_categoria):
    """Inserisce una nuova transazione nel database"""
    conn = create_connection()
    cursor = conn.cursor()
    
    cursor.execute(
        """INSERT INTO Transazioni (id_turno, id_operatore, id_articolo, quantita, valore_unitario, sconto, tot_transazione, des_transazione, data_ora, id_pagamento, id_categoria)
           VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)""",
        (
            id_turno,
            id_operatore,
            id_articolo,
            quantita,
            valore_unitario,
            sconto,
            tot_transazione,
            des_transazione,
            datetime.now().strftime("%Y-%m-%d"),
            id_pagamento,
            id_categoria
        )
    )
    conn.commit()
    conn.close()
    
def modify_transazione(id_transazione, id_turno, id_operatore, id_articolo, quantita, valore_unitario, sconto, tot_transazione, des_transazione, id_pagamento, id_categoria):
    """Modifica una transazione esistente nel database"""
    conn = create_connection()
    cursor = conn.cursor()
        
    cursor.execute(
        """UPDATE Transazioni SET id_turno=?, id_operatore=?, id_articolo=?, quantita=?, valore_unitario=?, sconto=?, tot_transazione=?, des_transazione=?, id_pagamento=?, data_ora=?, id_categoria=?
           WHERE id_transazione=?""",
        (
            id_turno,
            id_operatore,
            id_articolo,
            quantita,
            valore_unitario,
            sconto,
            tot_transazione,
            des_transazione,
            id_pagamento,
            datetime.now().strftime("%Y-%m-%d"),
            id_categoria,
            id_transazione
        )
    )

    conn.commit()
    conn.close()


    
def delete_transazione(entries):
    """Cancella una transazione dal database"""
    conn = create_connection()
    cursor = conn.cursor()
    transazione_id = entries["id_transazione"].get()
    cursor.execute("DELETE FROM Transazioni WHERE id_transazione=?", (transazione_id,))
    conn.commit()
    conn.close()

def get_totali_per_giorno(data):
    """Ottiene il totale quantità e il totale transazione per giorno, suddiviso per tipologia di pagamento"""
    conn = create_connection()
    cursor = conn.cursor()
    cursor.execute(
        """SELECT t.id_pagamento, p.des_pagamento, SUM(t.quantita) AS totale_quantita, SUM(t.tot_transazione) AS totale_transazione
           FROM Transazioni t
           JOIN Pagamenti p ON t.id_pagamento = p.id_pagamento
           WHERE t.data_ora = ?
           GROUP BY t.id_pagamento""",
        (data,)
    )
    totali = cursor.fetchall()
    conn.close()
    return totali

def get_transazioni_per_data(data):
    conn = create_connection()
    cursor = conn.cursor()
    cursor.execute("""SELECT t.id_transazione, t.data_ora, t.id_turno, tu.des_turno, t.id_operatore, (op.nome  || ' ' || op.cognome) as operatore, t.id_articolo, a.des_articolo, t.quantita, t.valore_unitario, t.sconto, t.tot_transazione, t.des_transazione, t.id_pagamento, p.des_pagamento, t.id_categoria, c.des_categoria FROM Transazioni as t LEFT JOIN turni as tu ON t.id_turno = tu.id_turno LEFT JOIN operatori as op ON t.id_operatore = op.id_operatore LEFT JOIN articoli as a ON t.id_articolo = a.id_articolo LEFT JOIN pagamenti as p ON t.id_pagamento = p.id_pagamento LEFT JOIN categorie as c ON t.id_categoria = c.id_categoria WHERE t.data_ora = DATE(?) ORDER BY t.data_ora, t.id_transazione""",
        (data,))
    transazioni = cursor.fetchall()
  
    return transazioni