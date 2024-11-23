import sqlite3
import os

DATABASE_NAME = os.getenv("CASH_FLOW_DB_NAME", "cash_flow.db")

def create_connection():
    return sqlite3.connect(DATABASE_NAME)

def fetch_all_operatori():
    # Ottiene tutti gli operatori dal database
    conn = create_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT id_operatore, nome, cognome FROM Operatori")
    operatori = cursor.fetchall()
    conn.close()
    return operatori

def insert_operatore(entries):
    # Inserisce un nuovo operatore nel database
    conn = create_connection()
    cursor = conn.cursor()
    data = {field: entry.get() for field, entry in entries.items()}
    cursor.execute(
        "INSERT INTO Operatori (nome, cognome) VALUES (?, ?)",
        (data["nome"], data["cognome"])
    )
    conn.commit()
    conn.close()

def modify_operatore(entries):
    # Modifica un operatore esistente
    conn = create_connection()
    cursor = conn.cursor()
    data = {field: entry.get() for field, entry in entries.items()}
    cursor.execute(
        "UPDATE Operatori SET nome=?, cognome=? WHERE id_operatore=?",
        (data["nome"], data["cognome"], data["id_operatore"])
    )
    conn.commit()
    conn.close()

def delete_operatore(entries):
    # Cancella un operatore dal database
    conn = create_connection()
    cursor = conn.cursor()
    operatore_id = entries["id_operatore"].get()
    cursor.execute("DELETE FROM Operatori WHERE id_operatore=?", (operatore_id,))
    conn.commit()
    conn.close()