
import sqlite3
import os

# Nome del database per la connessione
DATABASE_NAME = os.getenv("CASH_FLOW_DB_NAME", "cash_flow.db")

def create_connection():
    # Crea una connessione al database
    return sqlite3.connect(DATABASE_NAME)

def fetch_all_categories():
    # Ottiene tutte le categorie dal database
    conn = create_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT id_categoria, des_categoria FROM Categorie")
    categories = cursor.fetchall()
    conn.close()
    return categories

def insert_categoria(entries):
    # Inserisce una nuova categoria nel database
    conn = create_connection()
    cursor = conn.cursor()
    data = {field: entry.get() for field, entry in entries.items()}
    cursor.execute(
        "INSERT INTO Categorie (des_categoria) VALUES (?)",
        (data["des_categoria"],)
    )
    conn.commit()
    conn.close()

def modify_categoria(entries):
    # Modifica una categoria esistente
    conn = create_connection()
    cursor = conn.cursor()
    data = {field: entry.get() for field, entry in entries.items()}
    cursor.execute(
        "UPDATE Categorie SET des_categoria=? WHERE id_categoria=?",
        (data["des_categoria"], data["id_categoria"])
    )
    conn.commit()
    conn.close()

def delete_categoria(entries):
    # Cancella una categoria dal database
    conn = create_connection()
    cursor = conn.cursor()
    categoria_id = entries["id_categoria"].get()
    cursor.execute("DELETE FROM Categorie WHERE id_categoria=?", (categoria_id,))
    conn.commit()
    conn.close()
