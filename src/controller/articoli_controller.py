
import sqlite3
import os
import sys
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../src')))


# Nome del database per la connessione
DATABASE_NAME = os.getenv("CASH_FLOW_DB_NAME", "cash_flow.db")

def create_connection():
    # Crea una connessione al database
    return sqlite3.connect(DATABASE_NAME)

def get_category_options():
    # Ottiene tutte le categorie per la dropdown
    conn = create_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT des_categoria FROM Categorie")
    options = [row[0] for row in cursor.fetchall()]
    conn.close()
    return options

def fetch_all_articles():
    # Ottiene tutti gli articoli dal database
    conn = create_connection()
    cursor = conn.cursor()
    cursor.execute(
        """
        SELECT a.id_articolo, a.des_articolo, a.prezzo, 
               CASE a.disponibilita WHEN 1 THEN 'SI' ELSE 'NO' END AS disponibilita, 
               a.id_categoria_default, c.des_categoria
        FROM Articoli as a
        INNER JOIN Categorie as c 
        WHERE a.id_categoria_default = c.id_categoria
        """
    )
    articles = cursor.fetchall()
    conn.close()
    return articles

def insert_article(entries):
    # Inserisce un nuovo articolo nel database
    conn = create_connection()
    cursor = conn.cursor()
    data = {field: entry.get() for field, entry in entries.items()}
    
    # Recupera l'ID della categoria
    categoria_options = get_categoria_options()
    descrizione_categoria = data["id_categoria_default"]
    id_categoria_default = categoria_options.get(descrizione_categoria)
    
    if id_categoria_default is None:
        raise ValueError("Categoria non valida")
    
    cursor.execute(
        "INSERT INTO Articoli (des_articolo, prezzo, disponibilita, id_categoria_default) VALUES (?, ?, ?, ?)",
        (data["descrizione"], data["prezzo"], 1 if data["disponibilita"] == "SI" else 0, id_categoria_default)
    )
    conn.commit()
    conn.close()

def modify_article(entries):
    # Modifica un articolo esistente
    conn = create_connection()
    cursor = conn.cursor()
    data = {field: entry.get() for field, entry in entries.items()}
    
    # Recupera l'ID della categoria
    categoria_options = get_categoria_options()
    descrizione_categoria = data["id_categoria_default"]
    id_categoria_default = categoria_options.get(descrizione_categoria)
    
    if id_categoria_default is None:
        raise ValueError("Categoria non valida")
    
    cursor.execute(
        "UPDATE Articoli SET des_articolo=?, prezzo=?, disponibilita=?, id_categoria_default=? WHERE id_articolo=?",
        (data["descrizione"], data["prezzo"], 1 if data["disponibilita"] == "SI" else 0, id_categoria_default, data["id_articolo"])
    )
    conn.commit()
    conn.close()

def delete_article(entries):
    # Cancella un articolo dal database
    conn = create_connection()
    cursor = conn.cursor()
    article_id = entries["id_articolo"].get()
    cursor.execute("DELETE FROM Articoli WHERE id_articolo=?", (article_id,))
    conn.commit()
    conn.close()

def get_categoria_options():
    """Recupera le opzioni delle categorie dal database per popolare la dropdown"""
    conn = create_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT id_categoria, des_categoria FROM Categorie")
    options = {row[1]: row[0] for row in cursor.fetchall()}
    conn.close()
    return options

class ArticoliController:
    def __init__(self):
        pass
