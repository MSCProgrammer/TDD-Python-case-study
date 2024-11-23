
import pytest
from src.controller import operatori_controller

# Fixture per simulare la connessione al database
@pytest.fixture(scope="function")
def mock_db_connection(mocker):
    mock_connect = mocker.patch('sqlite3.connect')
    mock_conn = mocker.MagicMock()
    mock_connect.return_value = mock_conn
    return mock_conn

def test_fetch_all_operatori(mock_db_connection):
    # Simulazione dei risultati della query per recuperare gli operatori
    mock_cursor = mock_db_connection.cursor.return_value
    mock_cursor.fetchall.return_value = [(1, "Mario", "Rossi"), (2, "Luigi", "Verdi")]

    # Chiamata alla funzione da testare
    result = operatori_controller.fetch_all_operatori()

    # Asserzione: verifica che i risultati siano quelli attesi
    assert result == [(1, "Mario", "Rossi"), (2, "Luigi", "Verdi")]

    # Verifica che la query SQL sia stata eseguita correttamente
    mock_db_connection.cursor.return_value.execute.assert_called_once_with(
        "SELECT id_operatore, nome, cognome FROM Operatori"
    )

def test_insert_operatore(mock_db_connection, mocker):
    # Simulazione dell'inserimento di un nuovo operatore
    entries = {
        "nome": mocker.Mock(get=lambda: "Carla"),
        "cognome": mocker.Mock(get=lambda: "Bianchi")
    }

    # Chiamata alla funzione di inserimento
    operatori_controller.insert_operatore(entries)

    # Verifica che la query SQL per l'inserimento sia corretta
    mock_db_connection.cursor.return_value.execute.assert_called_once_with(
        "INSERT INTO Operatori (nome, cognome) VALUES (?, ?)", ("Carla", "Bianchi")
    )
    # Verifica che il commit sia stato chiamato
    mock_db_connection.commit.assert_called_once()

def test_modify_operatore(mock_db_connection, mocker):
    # Simulazione dell'aggiornamento di un operatore esistente
    entries = {
        "id_operatore": mocker.Mock(get=lambda: "1"),
        "nome": mocker.Mock(get=lambda: "Luigi"),
        "cognome": mocker.Mock(get=lambda: "Verdi")
    }

    # Chiamata alla funzione di aggiornamento
    operatori_controller.modify_operatore(entries)

    # Verifica che la query SQL per l'aggiornamento sia corretta
    mock_db_connection.cursor.return_value.execute.assert_called_once_with(
        "UPDATE Operatori SET nome=?, cognome=? WHERE id_operatore=?",
        ("Luigi", "Verdi", "1")
    )
    # Verifica che il commit sia stato chiamato
    mock_db_connection.commit.assert_called_once()

def test_delete_operatore(mock_db_connection, mocker):
    # Simulazione della cancellazione di un operatore
    entries = {"id_operatore": mocker.Mock(get=lambda: "1")}

    # Chiamata alla funzione di cancellazione
    operatori_controller.delete_operatore(entries)

    # Verifica che la query SQL per la cancellazione sia corretta
    mock_db_connection.cursor.return_value.execute.assert_called_once_with(
        "DELETE FROM Operatori WHERE id_operatore=?", ("1",)
    )
    # Verifica che il commit sia stato chiamato
    mock_db_connection.commit.assert_called_once()
