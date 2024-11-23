import pytest
from controller import transazioni_controller

# Fixture per simulare la connessione al database SQLite
@pytest.fixture(scope="function")
def mock_db_connection(mocker):
    # Mock della connessione SQLite
    mock_connect = mocker.patch("sqlite3.connect")
    mock_conn = mocker.MagicMock()  # Oggetto connessione simulata
    mock_connect.return_value = mock_conn  # Restituisce la connessione mock
    return mock_conn

# Testa l'inserimento di una nuova transazione (Create)
def test_insert_transazione(mock_db_connection, mocker):
    mock_cursor = mock_db_connection.cursor.return_value

    # Mock delle opzioni FK
    mocker.patch('controller.transazioni_controller.get_turno_options', return_value={"Turno Mattina": 1})
    mocker.patch('controller.transazioni_controller.get_operatore_options', return_value={"Operatore 1": 1})
    mocker.patch('controller.transazioni_controller.get_articolo_options', return_value={"Articolo A": 1})
    mocker.patch('controller.transazioni_controller.get_pagamento_options', return_value={"Contanti": 1})
    mocker.patch('controller.transazioni_controller.get_categoria_options', return_value={"Categoria 1": 1})

    # Chiamata al metodo sotto test
    transazioni_controller.insert_transazione(
        id_turno=1,
        id_operatore=1,
        id_articolo=1,
        quantita=10,
        valore_unitario=20.0,
        sconto=5.0,
        tot_transazione=150.0,
        des_transazione="Test transazione",
        id_pagamento=1,
        id_categoria=1
    )

    # Verifica che la query di inserimento sia stata eseguita correttamente
    mock_cursor.execute.assert_called_once_with(
        """INSERT INTO Transazioni (id_turno, id_operatore, id_articolo, quantita, valore_unitario, sconto, tot_transazione, des_transazione, data_ora, id_pagamento, id_categoria)
           VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)""",
        (1, 1, 1, 10, 20.0, 5.0, 150.0, "Test transazione", mocker.ANY, 1, 1)
    )
    mock_db_connection.commit.assert_called_once()

# Testa la modifica di una transazione esistente (Modify)
def test_modify_transazione(mock_db_connection, mocker):
    mock_cursor = mock_db_connection.cursor.return_value

    # Mock delle opzioni FK
    mocker.patch('controller.transazioni_controller.get_turno_options', return_value={"Turno Pomeriggio": 2})
    mocker.patch('controller.transazioni_controller.get_operatore_options', return_value={"Operatore 2": 2})
    mocker.patch('controller.transazioni_controller.get_articolo_options', return_value={"Articolo B": 2})
    mocker.patch('controller.transazioni_controller.get_pagamento_options', return_value={"Carta": 2})
    mocker.patch('controller.transazioni_controller.get_categoria_options', return_value={"Categoria 2": 2})

    # Chiamata al metodo sotto test
    transazioni_controller.modify_transazione(
        id_transazione=1,
        id_turno=2,
        id_operatore=2,
        id_articolo=2,
        quantita=5,
        valore_unitario=15.0,
        sconto=2.5,
        tot_transazione=70.0,
        des_transazione="Aggiornata",
        id_pagamento=2,
        id_categoria=2
    )

    # Verifica che la query di modifica sia stata eseguita correttamente
    mock_cursor.execute.assert_called_once_with(
        """UPDATE Transazioni SET id_turno=?, id_operatore=?, id_articolo=?, quantita=?, valore_unitario=?, sconto=?, tot_transazione=?, des_transazione=?, id_pagamento=?, data_ora=?, id_categoria=?
           WHERE id_transazione=?""",
        (2, 2, 2, 5, 15.0, 2.5, 70.0, "Aggiornata", 2, mocker.ANY, 2, 1)
    )
    mock_db_connection.commit.assert_called_once()

# Testa l'eliminazione di una transazione (Delete)
def test_delete_transazione(mock_db_connection, mocker):
    mock_cursor = mock_db_connection.cursor.return_value

    # Mock per simulare il comportamento dell'input GUI
    mock_entries = {"id_transazione": mocker.MagicMock()}
    mock_entries["id_transazione"].get.return_value = "1"  # ID della transazione da eliminare

    # Chiamata al metodo sotto test
    transazioni_controller.delete_transazione(mock_entries)

    # Verifica che la query di eliminazione sia stata eseguita correttamente
    mock_cursor.execute.assert_called_once_with(
        "DELETE FROM Transazioni WHERE id_transazione=?", ("1",)
    )
    mock_db_connection.commit.assert_called_once()


# Testa il recupero delle transazioni per data (Read)
def test_get_transazioni_per_data(mock_db_connection):
    mock_cursor = mock_db_connection.cursor.return_value
    mock_cursor.fetchall.return_value = [
        (1, "2024-11-20", "Mattina", "Turno Mattina", 1, "Operatore 1", 1, "Articolo A", 2, 10.0, 1.0, 19.0, "Test", 1, "Contanti", 1, "Categoria 1")
    ]

    # Chiamata al metodo sotto test
    result = transazioni_controller.get_transazioni_per_data("2024-11-20")

    # Verifica che i risultati siano quelli attesi
    expected_result = [
        (1, "2024-11-20", "Mattina", "Turno Mattina", 1, "Operatore 1", 1, "Articolo A", 2, 10.0, 1.0, 19.0, "Test", 1, "Contanti", 1, "Categoria 1")
    ]
    assert result == expected_result

    # Verifica che la query sia stata chiamata correttamente
    mock_cursor.execute.assert_called_once_with(
        """SELECT t.id_transazione, t.data_ora, t.id_turno, tu.des_turno, t.id_operatore, (op.nome  || ' ' || op.cognome) as operatore, t.id_articolo, a.des_articolo, t.quantita, t.valore_unitario, t.sconto, t.tot_transazione, t.des_transazione, t.id_pagamento, p.des_pagamento, t.id_categoria, c.des_categoria FROM Transazioni as t LEFT JOIN turni as tu ON t.id_turno = tu.id_turno LEFT JOIN operatori as op ON t.id_operatore = op.id_operatore LEFT JOIN articoli as a ON t.id_articolo = a.id_articolo LEFT JOIN pagamenti as p ON t.id_pagamento = p.id_pagamento LEFT JOIN categorie as c ON t.id_categoria = c.id_categoria WHERE t.data_ora = DATE(?) ORDER BY t.data_ora, t.id_transazione""",
        ("2024-11-20",)
    )
