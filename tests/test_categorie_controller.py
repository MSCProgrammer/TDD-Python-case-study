
import pytest
from src.controller import categorie_controller

# Fixture per simulare la connessione al database
@pytest.fixture(scope="function")
def mock_db_connection(mocker):
    # Mock della connessione SQLite
    mock_connect = mocker.patch('sqlite3.connect')
    mock_conn = mocker.MagicMock()  # Oggetto connessione simulata
    mock_connect.return_value = mock_conn  # Restituisce la connessione mock
    return mock_conn

def test_fetch_all_categories(mock_db_connection):
    # Simulazione dei risultati della query per recuperare le categorie
    mock_cursor = mock_db_connection.cursor.return_value
    mock_cursor.fetchall.return_value = [(1, "Categoria 1"), (2, "Categoria 2")]

    # Chiamata alla funzione da testare
    result = categorie_controller.fetch_all_categories()

    # Asserzione: verifica che i risultati siano quelli attesi
    assert result == [(1, "Categoria 1"), (2, "Categoria 2")]

    # Verifica che la query SQL sia stata eseguita correttamente
    mock_db_connection.cursor.return_value.execute.assert_called_once_with(
        "SELECT id_categoria, des_categoria FROM Categorie"
    )

def test_insert_categoria(mock_db_connection, mocker):
    # Simulazione dell'inserimento di una nuova categoria
    entries = {"des_categoria": mocker.Mock(get=lambda: "Categoria Test")}
    
    # Chiamata alla funzione di inserimento
    categorie_controller.insert_categoria(entries)
    
    # Verifica che la query SQL per l'inserimento sia corretta
    mock_db_connection.cursor.return_value.execute.assert_called_once_with(
        "INSERT INTO Categorie (des_categoria) VALUES (?)", ("Categoria Test",)
    )
    # Verifica che il commit sia stato chiamato
    mock_db_connection.commit.assert_called_once()

def test_modify_categoria(mock_db_connection, mocker):
    # Simulazione dell'aggiornamento di una categoria esistente
    entries = {
        "id_categoria": mocker.Mock(get=lambda: "1"),
        "des_categoria": mocker.Mock(get=lambda: "Categoria Modificata")
    }

    # Chiamata alla funzione di aggiornamento
    categorie_controller.modify_categoria(entries)

    # Verifica che la query SQL per l'aggiornamento sia corretta
    mock_db_connection.cursor.return_value.execute.assert_called_once_with(
        "UPDATE Categorie SET des_categoria=? WHERE id_categoria=?",
        ("Categoria Modificata", "1")
    )
    # Verifica che il commit sia stato chiamato
    mock_db_connection.commit.assert_called_once()

def test_delete_categoria(mock_db_connection, mocker):
    # Simulazione della cancellazione di una categoria
    entries = {"id_categoria": mocker.Mock(get=lambda: "1")}

    # Chiamata alla funzione di cancellazione
    categorie_controller.delete_categoria(entries)

    # Verifica che la query SQL per la cancellazione sia corretta
    mock_db_connection.cursor.return_value.execute.assert_called_once_with(
        "DELETE FROM Categorie WHERE id_categoria=?", ("1",)
    )
    # Verifica che il commit sia stato chiamato
    mock_db_connection.commit.assert_called_once()
