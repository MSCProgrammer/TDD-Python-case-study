
import pytest
from src.controller import pagamenti_controller

# Fixture per simulare la connessione al database
@pytest.fixture(scope="function")
def mock_db_connection(mocker):
    mock_connect = mocker.patch('sqlite3.connect')
    mock_conn = mocker.MagicMock()
    mock_connect.return_value = mock_conn
    return mock_conn

def test_fetch_all_pagamenti(mock_db_connection):
    # Simulazione dei risultati della query per recuperare i pagamenti
    mock_cursor = mock_db_connection.cursor.return_value
    mock_cursor.fetchall.return_value = [(1, "Contanti", 1), (2, "Carta", 0)]

    # Chiamata alla funzione da testare
    result = pagamenti_controller.fetch_all_pagamenti()

    # Asserzione: verifica che i risultati siano quelli attesi (uso di 1/0)
    assert result == [(1, "Contanti", 1), (2, "Carta", 0)]

    # Normalizzazione della query eseguita per il confronto
    actual_query = mock_db_connection.cursor.return_value.execute.call_args[0][0].replace("\n", "").replace("  ", " ").strip()
    expected_query = """SELECT id_pagamento, des_pagamento, CASE valore_zero WHEN 1 THEN 'SI' ELSE 'NO' END AS valore_zero FROM Pagamenti"""
    
    # Verifica che la query SQL normalizzata sia corretta
    assert actual_query == expected_query

def test_insert_pagamento(mock_db_connection, mocker):
    # Simulazione dell'inserimento di un nuovo pagamento
    entries = {
        "des_pagamento": mocker.Mock(get=lambda: "Bonifico"),
        "valore_zero": mocker.Mock(get=lambda: "NO")
    }

    # Chiamata alla funzione di inserimento
    pagamenti_controller.insert_pagamento(entries)

    # Verifica che la query SQL per l'inserimento sia corretta
    mock_db_connection.cursor.return_value.execute.assert_called_once_with(
        "INSERT INTO Pagamenti (des_pagamento, valore_zero) VALUES (?, ?)", ("Bonifico", 0)
    )
    # Verifica che il commit sia stato chiamato
    mock_db_connection.commit.assert_called_once()

def test_modify_pagamento(mock_db_connection, mocker):
    # Simulazione dell'aggiornamento di un pagamento esistente
    entries = {
        "id_pagamento": mocker.Mock(get=lambda: "1"),
        "des_pagamento": mocker.Mock(get=lambda: "Contanti"),
        "valore_zero": mocker.Mock(get=lambda: "SI")
    }

    # Chiamata alla funzione di aggiornamento
    pagamenti_controller.modify_pagamento(entries)

    # Verifica che la query SQL per l'aggiornamento sia corretta
    mock_db_connection.cursor.return_value.execute.assert_called_once_with(
        "UPDATE Pagamenti SET des_pagamento=?, valore_zero=? WHERE id_pagamento=?",
        ("Contanti", 1, "1")
    )
    # Verifica che il commit sia stato chiamato
    mock_db_connection.commit.assert_called_once()

def test_delete_pagamento(mock_db_connection, mocker):
    # Simulazione della cancellazione di un pagamento
    entries = {"id_pagamento": mocker.Mock(get=lambda: "1")}

    # Chiamata alla funzione di cancellazione
    pagamenti_controller.delete_pagamento(entries)

    # Verifica che la query SQL per la cancellazione sia corretta
    mock_db_connection.cursor.return_value.execute.assert_called_once_with(
        "DELETE FROM Pagamenti WHERE id_pagamento=?", ("1",)
    )
    # Verifica che il commit sia stato chiamato
    mock_db_connection.commit.assert_called_once()
