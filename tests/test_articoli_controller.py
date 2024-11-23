
import pytest
from src.controller import articoli_controller

# Fixture per simulare la connessione al database
@pytest.fixture(scope="function")
def mock_db_connection(mocker):
    mock_connect = mocker.patch('sqlite3.connect')
    mock_conn = mocker.MagicMock()
    mock_connect.return_value = mock_conn
    return mock_conn

def test_fetch_all_articles(mock_db_connection):
    # Simulazione dei risultati della query per recuperare gli articoli
    mock_cursor = mock_db_connection.cursor.return_value
    mock_cursor.fetchall.return_value = [
        (1, "Articolo 1", 10.0, "SI", 1, "Categoria 1"),
        (2, "Articolo 2", 20.0, "NO", 2, "Categoria 2")
    ]

    # Chiamata alla funzione da testare
    result = articoli_controller.fetch_all_articles()

    # Asserzione: verifica che i risultati siano quelli attesi
    assert result == [
        (1, "Articolo 1", 10.0, "SI", 1, "Categoria 1"),
        (2, "Articolo 2", 20.0, "NO", 2, "Categoria 2")
    ]

    # Verifica che la query SQL sia stata eseguita correttamente
    mock_db_connection.cursor.return_value.execute.assert_called_once()

def test_insert_article(mock_db_connection, mocker):
    # Mock delle opzioni delle categorie (FK simulate)
    mocker.patch('src.controller.articoli_controller.get_categoria_options', return_value={"Categoria 1": 1})

    # Simulazione dei dati dell'articolo
    entries = {
        "descrizione": mocker.Mock(get=lambda: "Articolo Test"),
        "prezzo": mocker.Mock(get=lambda: "15.0"),
        "disponibilita": mocker.Mock(get=lambda: "SI"),
        "id_categoria_default": mocker.Mock(get=lambda: "Categoria 1")
    }

    # Chiamata alla funzione di inserimento
    articoli_controller.insert_article(entries)

    # Verifica che la query SQL per l'inserimento sia corretta
    mock_db_connection.cursor.return_value.execute.assert_called_once_with(
        "INSERT INTO Articoli (des_articolo, prezzo, disponibilita, id_categoria_default) VALUES (?, ?, ?, ?)",
        ("Articolo Test", "15.0", 1, 1)
    )
    # Verifica che il commit sia stato chiamato
    mock_db_connection.commit.assert_called_once()

def test_modify_article(mock_db_connection, mocker):
    # Mock delle opzioni delle categorie (FK simulate)
    mocker.patch('src.controller.articoli_controller.get_categoria_options', return_value={"Categoria 1": 1})

    # Simulazione dei dati aggiornati dell'articolo
    entries = {
        "id_articolo": mocker.Mock(get=lambda: "1"),
        "descrizione": mocker.Mock(get=lambda: "Articolo Aggiornato"),
        "prezzo": mocker.Mock(get=lambda: "20.0"),
        "disponibilita": mocker.Mock(get=lambda: "NO"),
        "id_categoria_default": mocker.Mock(get=lambda: "Categoria 1")
    }

    # Chiamata alla funzione di aggiornamento
    articoli_controller.modify_article(entries)

    # Verifica che la query SQL per l'aggiornamento sia corretta
    mock_db_connection.cursor.return_value.execute.assert_called_once_with(
        "UPDATE Articoli SET des_articolo=?, prezzo=?, disponibilita=?, id_categoria_default=? WHERE id_articolo=?",
        ("Articolo Aggiornato", "20.0", 0, 1, "1")
    )
    # Verifica che il commit sia stato chiamato
    mock_db_connection.commit.assert_called_once()

def test_delete_article(mock_db_connection, mocker):
    # Simulazione dell'eliminazione di un articolo
    entries = {"id_articolo": mocker.Mock(get=lambda: "1")}

    # Chiamata alla funzione di cancellazione
    articoli_controller.delete_article(entries)

    # Verifica che la query SQL per la cancellazione sia corretta
    mock_db_connection.cursor.return_value.execute.assert_called_once_with(
        "DELETE FROM Articoli WHERE id_articolo=?", ("1",)
    )
    # Verifica che il commit sia stato chiamato
    mock_db_connection.commit.assert_called_once()
