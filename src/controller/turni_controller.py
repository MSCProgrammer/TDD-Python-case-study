import sqlite3
import os

DATABASE_NAME = os.getenv("CASH_FLOW_DB_NAME", "cash_flow.db")

def create_connection():
    return sqlite3.connect(DATABASE_NAME)

def fetch_all_turni():
    # Ottiene tutti i turni dal database
    conn = create_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT id_turno, des_turno FROM Turni")
    turni = cursor.fetchall()
    conn.close()
    return turni

def insert_turno(entries):
    # Inserisce un nuovo turno nel database
    conn = create_connection()
    cursor = conn.cursor()
    data = {field: entry.get() for field, entry in entries.items()}
    cursor.execute(
        "INSERT INTO Turni (des_turno) VALUES (?)",
        (data["des_turno"],)
    )
    conn.commit()
    conn.close()

def modify_turno(entries):
    # Modifica un turno esistente
    conn = create_connection()
    cursor = conn.cursor()
    data = {field: entry.get() for field, entry in entries.items()}
    cursor.execute(
        "UPDATE Turni SET des_turno=? WHERE id_turno=?",
        (data["des_turno"], data["id_turno"])
    )
    conn.commit()
    conn.close()

def delete_turno(entries):
    # Cancella un turno dal database
    conn = create_connection()
    cursor = conn.cursor()
    turno_id = entries["id_turno"].get()
    cursor.execute("DELETE FROM Turni WHERE id_turno=?", (turno_id,))
    conn.commit()
    conn.close()