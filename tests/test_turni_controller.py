
import pytest
from src.controller import turni_controller

# Fixture per simulare la connessione al database
@pytest.fixture(scope="function")
def mock_db_connection(mocker):
    mock_connect = mocker.patch('sqlite3.connect')
    mock_conn = mocker.MagicMock()
    mock_connect.return_value = mock_conn
    return mock_conn

def test_fetch_all_turni(mock_db_connection):
    # Simulazione dei risultati della query per recuperare i turni
    mock_cursor = mock_db_connection.cursor.return_value
    mock_cursor.fetchall.return_value = [(1, "Mattina"), (2, "Pomeriggio")]

    # Chiamata alla funzione da testare
    result = turni_controller.fetch_all_turni()

    # Asserzione: verifica che i risultati siano quelli attesi
    assert result == [(1, "Mattina"), (2, "Pomeriggio")]

    # Verifica che la query SQL sia stata eseguita correttamente
    mock_db_connection.cursor.return_value.execute.assert_called_once_with(
        "SELECT id_turno, des_turno FROM Turni"
    )

def test_insert_turno(mock_db_connection, mocker):
    # Simulazione dell'inserimento di un nuovo turno
    entries = {"des_turno": mocker.Mock(get=lambda: "Notturno")}

    # Chiamata alla funzione di inserimento
    turni_controller.insert_turno(entries)

    # Verifica che la query SQL per l'inserimento sia corretta
    mock_db_connection.cursor.return_value.execute.assert_called_once_with(
        "INSERT INTO Turni (des_turno) VALUES (?)", ("Notturno",)
    )
    # Verifica che il commit sia stato chiamato
    mock_db_connection.commit.assert_called_once()

def test_modify_turno(mock_db_connection, mocker):
    # Simulazione dell'aggiornamento di un turno esistente
    entries = {
        "id_turno": mocker.Mock(get=lambda: "1"),
        "des_turno": mocker.Mock(get=lambda: "Sera")
    }

    # Chiamata alla funzione di aggiornamento
    turni_controller.modify_turno(entries)

    # Verifica che la query SQL per l'aggiornamento sia corretta
    mock_db_connection.cursor.return_value.execute.assert_called_once_with(
        "UPDATE Turni SET des_turno=? WHERE id_turno=?", ("Sera", "1")
    )
    # Verifica che il commit sia stato chiamato
    mock_db_connection.commit.assert_called_once()

def test_delete_turno(mock_db_connection, mocker):
    # Simulazione della cancellazione di un turno
    entries = {"id_turno": mocker.Mock(get=lambda: "1")}

    # Chiamata alla funzione di cancellazione
    turni_controller.delete_turno(entries)

    # Verifica che la query SQL per la cancellazione sia corretta
    mock_db_connection.cursor.return_value.execute.assert_called_once_with(
        "DELETE FROM Turni WHERE id_turno=?", ("1",)
    )
    # Verifica che il commit sia stato chiamato
    mock_db_connection.commit.assert_called_once()
