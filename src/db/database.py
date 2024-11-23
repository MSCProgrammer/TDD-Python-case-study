import os
import sqlite3

DB_NAME = os.getenv("CASH_FLOW_DB_NAME", "cash_flow.db")

def connect_db():
    return sqlite3.connect(DB_NAME)

def create_tables():
    try:
        conn = connect_db()
        cursor = conn.cursor()

        # Tabella Turni
        cursor.execute('''
        CREATE TABLE IF NOT EXISTS turni (
            id_turno INTEGER PRIMARY KEY AUTOINCREMENT,
            des_turno TEXT NOT NULL
        )
        ''')

        # Tabella Operatori
        cursor.execute('''
        CREATE TABLE IF NOT EXISTS operatori (
            id_operatore INTEGER PRIMARY KEY AUTOINCREMENT,
            nome TEXT NOT NULL,
            cognome TEXT NOT NULL,
            data_inizio TEXT,
            data_fine TEXT
        )
        ''')

        # Tabella Categorie
        cursor.execute('''
        CREATE TABLE IF NOT EXISTS categorie (
            id_categoria INTEGER PRIMARY KEY AUTOINCREMENT,
            des_categoria TEXT NOT NULL
        )
        ''')

        # Tabella Articoli
        cursor.execute('''
        CREATE TABLE IF NOT EXISTS articoli (
            id_articolo INTEGER PRIMARY KEY AUTOINCREMENT,
            des_articolo TEXT NOT NULL,
            id_categoria_default INTEGER,
            prezzo REAL NOT NULL,
            disponibilita INTEGER DEFAULT 1,
            FOREIGN KEY (id_categoria_default) REFERENCES categorie (id_categoria)
        )
        ''')

        # Tabella Pagamenti
        cursor.execute('''
        CREATE TABLE IF NOT EXISTS pagamenti (
            id_pagamento INTEGER PRIMARY KEY AUTOINCREMENT,
            des_pagamento TEXT NOT NULL,
            valore_zero INTEGER DEFAULT 0
        )
        ''')

        # Tabella Transazioni
        cursor.execute('''
        CREATE TABLE IF NOT EXISTS transazioni (
            id_transazione INTEGER PRIMARY KEY AUTOINCREMENT,
            data_ora TEXT NOT NULL,
            id_turno INTEGER NOT NULL,
            id_operatore INTEGER NOT NULL,
            id_articolo INTEGER NOT NULL,
            id_categoria INTEGER NOT NULL,
            id_pagamento INTEGER NOT NULL,
            quantita INTEGER NOT NULL,
            valore_unitario REAL NOT NULL,
            sconto REAL DEFAULT 0,
            tot_transazione REAL NOT NULL,
            des_transazione TEXT,
            FOREIGN KEY (id_turno) REFERENCES turni (id_turno),
            FOREIGN KEY (id_operatore) REFERENCES operatori (id_operatore),
            FOREIGN KEY (id_articolo) REFERENCES articoli (id_articolo),
            FOREIGN KEY (id_categoria) REFERENCES categorie (id_categoria),
            FOREIGN KEY (id_pagamento) REFERENCES pagamenti (id_pagamento)
        )
        ''')

        conn.commit()
        conn.close()
        return True
    except Exception as e:
        print(f"Errore nella creazione delle tabelle: {e}")
        return False

# Funzioni per l'aggiunta di dati minimi se la tabella operatori è vuota
def add_operatore(nome, cognome, data_inizio, data_fine=None):
    conn = connect_db()
    cursor = conn.cursor()
    
    # Verifica se la tabella operatori è vuota 
    if len(get_all_operatori()) == 0:
        cursor.execute('''
        INSERT INTO operatori (nome, cognome, data_inizio, data_fine) 
        VALUES (?, ?, ?, ?)
        ''', (nome, cognome, data_inizio, data_fine))
        conn.commit()
        
    conn.close()

# Funzioni per l'aggiunta di dati minimi se la tabella turni è vuota
def add_turno(des_turno):
    conn = connect_db()
    cursor = conn.cursor()
    
    # Verifica se la tabella turni è vuota
    if len(get_all_turni()) == 0:
        cursor.execute('''
        INSERT INTO turni (des_turno)
        VALUES (?)
        ''', (des_turno,))
        conn.commit()
        
    conn.close()
# Funzioni per l'aggiunta di dati minimi se la categorie è vuota
def add_categoria(des_categoria):
    conn = connect_db()
    cursor = conn.cursor()
    
    # Verifica se la tabella categorie è vuota
    if len(get_all_categorie()) == 0:
        cursor.execute('''
        INSERT INTO categorie (des_categoria)
        VALUES (?)
        ''', (des_categoria,))
        conn.commit()
    
    conn.close()

# Funzioni per l'aggiunta di dati minimi se la articoli è vuota
def add_articolo(des_articolo, id_categoria_default, prezzo, disponibilita=True):
    conn = connect_db()
    cursor = conn.cursor()
    
    # Verifica se la tabella articoli è vuota
    if len(get_all_articoli()) == 0:
        cursor.execute('''
        INSERT INTO articoli (des_articolo, id_categoria_default, prezzo, disponibilita)
        VALUES (?, ?, ?, ?)
        ''', (des_articolo, id_categoria_default, prezzo, int(disponibilita)))
        conn.commit()
        
    conn.close()

# Funzioni per l'aggiunta di dati minimi se la pagamenti è vuota
def add_pagamento(des_pagamento, valore_zero=False):
    conn = connect_db()
    cursor = conn.cursor()

    # Verifica se la tabella pagamenti è vuota
    if len(get_all_pagamenti()) == 0:
        cursor.execute('''
        INSERT INTO pagamenti (des_pagamento, valore_zero)
        VALUES (?, ?)
        ''', (des_pagamento, int(valore_zero)))
        conn.commit()
    conn.close()

def add_minimum_data():
    add_operatore("Mario", "Rossi", "2028-01-31")
    add_categoria("ARTIGIANATO")
    add_articolo("Biglietto Intero", 1, 10.0, True)
    add_turno("MATTINA")
    add_pagamento("Contanti", valore_zero=False)

# Funzioni per verificare il numero di record nelle tabelle
def get_all_operatori():
    conn = connect_db()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM operatori")
    operators = cursor.fetchall()
    conn.close()
    return operators

def get_all_categorie():
    conn = connect_db()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM categorie")
    categories = cursor.fetchall()
    conn.close()
    return categories

def get_all_articoli():
    conn = connect_db()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM articoli")
    articles = cursor.fetchall()
    conn.close()
    return articles

def get_all_turni():
    conn = connect_db()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM turni")
    turns = cursor.fetchall()
    conn.close()
    return turns

def get_all_pagamenti():
    conn = connect_db()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM pagamenti")
    payments = cursor.fetchall()
    conn.close()
    return payments

# Creazione delle tabelle e dati minimi all'avvio
if __name__ == "__main__":
    if create_tables():
        print("Tabelle create con successo.")
        add_minimum_data()  # Aggiunta di dati minimi
    else:
        print("Errore nella creazione delle tabelle.")
# Funzioni CRUD per la tabella Articoli

def create_articolo(article_data):
    try:
        conn = connect_db()
        cursor = conn.cursor()
        cursor.execute(
            '''
            INSERT INTO articoli (des_articolo, prezzo, disponibilita, id_categoria)
            VALUES (?, ?, ?, ?)
            ''',
            (article_data['des_articolo'], article_data['prezzo'], article_data['disponibilita'], article_data['id_categoria'])
        )
        conn.commit()
        return True
    except Exception as e:
        print(f"Errore nella creazione dell'articolo: {e}")
        return False

def update_articolo(article_data):
    try:
        conn = connect_db()
        cursor = conn.cursor()
        cursor.execute(
            '''
            UPDATE articoli
            SET des_articolo = ?, prezzo = ?, disponibilita = ?, id_categoria = ?
            WHERE id_articolo = ?
            ''',
            (article_data['des_articolo'], article_data['prezzo'], article_data['disponibilita'], article_data['id_categoria'], article_data['id_articolo'])
        )
        conn.commit()
        return True
    except Exception as e:
        print(f"Errore nell'aggiornamento dell'articolo: {e}")
        return False

def delete_articolo(article_id):
    try:
        conn = connect_db()
        cursor = conn.cursor()
        cursor.execute(
            '''
            DELETE FROM articoli WHERE id_articolo = ?
            ''',
            (article_id,)
        )
        conn.commit()
        return True
    except Exception as e:
        print(f"Errore nella cancellazione dell'articolo: {e}")
        return False

def get_articolo(article_id):
    try:
        conn = connect_db()
        cursor = conn.cursor()
        cursor.execute(
            '''
            SELECT * FROM articoli WHERE id_articolo = ?
            ''',
            (article_id,)
        )
        result = cursor.fetchone()
        return {"id_articolo": result[0], "des_articolo": result[1], "prezzo": result[2], "disponibilita": result[3], "id_categoria": result[4]}
    except Exception as e:
        print(f"Errore nel recupero dell'articolo: {e}")
        return None
