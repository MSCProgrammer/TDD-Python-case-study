import pytest
from unittest.mock import patch
from controller import report_controller

# Testa il recupero delle transazioni per un periodo specifico con dati validi
@patch("controller.report_controller.create_connection")
def test_get_transazioni_per_periodo_valid_data(mock_create_connection):
    """Testa che vengano restituite le transazioni corrette per un periodo specifico."""
    mock_conn = mock_create_connection.return_value
    mock_cursor = mock_conn.cursor.return_value
    mock_cursor.fetchall.return_value = [
        (1, "2024-11-01", 1, "Mattina", 1, "Operatore 1", 1, "Articolo 1", 5, 10.0, 0.0, 50.0, "Test", 1, "Contanti", 1, "Categoria 1")
    ]

    result = report_controller.get_transazioni_per_periodo("2024-11-01", "2024-11-02")
    assert len(result) == 1
    assert result[0][1] == "2024-11-01"

# Testa il caso in cui non ci siano transazioni nel periodo specificato
@patch("controller.report_controller.create_connection")
def test_get_transazioni_per_periodo_empty(mock_create_connection):
    """Testa che venga restituito un risultato vuoto se non ci sono dati nel periodo selezionato."""
    mock_conn = mock_create_connection.return_value
    mock_cursor = mock_conn.cursor.return_value
    mock_cursor.fetchall.return_value = []

    result = report_controller.get_transazioni_per_periodo("2024-11-01", "2024-11-02")
    assert result == []

# Testa la gestione di input non validi per le date
def test_get_transazioni_per_periodo_invalid_date():
    """Testa che venga sollevato un errore per date non valide."""
    with pytest.raises(ValueError):
        report_controller.get_transazioni_per_periodo("invalid-date", "2024-11-02")

# Testa la gestione di errori del database
@patch("controller.report_controller.create_connection", side_effect=Exception("Database error"))
def test_get_transazioni_per_periodo_db_error(mock_create_connection):
    """Testa che venga sollevato un errore se si verifica un problema nel database."""
    with pytest.raises(Exception, match="Database error"):
        report_controller.get_transazioni_per_periodo("2024-11-01", "2024-11-02")

# Testa la gestione di errori durante la generazione del PDF
@patch("controller.report_controller.canvas.Canvas", side_effect=Exception("PDF generation error"))
def test_generate_pdf_error(mock_canvas):
    """Testa che venga sollevato un errore se si verifica un problema durante la generazione del PDF."""
    with pytest.raises(Exception, match="PDF generation error"):
        report_controller.generate_pdf([], "test.pdf", "2024-11-01", "2024-11-02")
