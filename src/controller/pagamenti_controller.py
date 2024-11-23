import sqlite3
import os

DATABASE_NAME = os.getenv("CASH_FLOW_DB_NAME", "cash_flow.db")

def create_connection():
    return sqlite3.connect(DATABASE_NAME)

def fetch_all_pagamenti():
    # Ottiene tutti i pagamenti dal database
    conn = create_connection()
    cursor = conn.cursor()
    cursor.execute(
        """
        SELECT id_pagamento, des_pagamento, CASE valore_zero WHEN 1 THEN 'SI' ELSE 'NO' END AS valore_zero FROM Pagamenti
        """
    )
    pagamenti = cursor.fetchall()
    conn.close()
    return pagamenti

def insert_pagamento(entries):
    # Inserisce un nuovo pagamento nel database
    conn = create_connection()
    cursor = conn.cursor()
    data = {field: entry.get() for field, entry in entries.items()}
    cursor.execute(
        "INSERT INTO Pagamenti (des_pagamento, valore_zero) VALUES (?, ?)",
        (data["des_pagamento"], 1 if data["valore_zero"] == "SI" else 0)
    )
    conn.commit()
    conn.close()

def modify_pagamento(entries):
    # Modifica un pagamento esistente
    conn = create_connection()
    cursor = conn.cursor()
    data = {field: entry.get() for field, entry in entries.items()}
    cursor.execute(
        "UPDATE Pagamenti SET des_pagamento=?, valore_zero=? WHERE id_pagamento=?",
        (data["des_pagamento"], 1 if data["valore_zero"] == "SI" else 0, data["id_pagamento"])
    )
    conn.commit()
    conn.close()

def delete_pagamento(entries):
    # Cancella un pagamento dal database
    conn = create_connection()
    cursor = conn.cursor()
    pagamento_id = entries["id_pagamento"].get()
    cursor.execute("DELETE FROM Pagamenti WHERE id_pagamento=?", (pagamento_id,))
    conn.commit()
    conn.close()