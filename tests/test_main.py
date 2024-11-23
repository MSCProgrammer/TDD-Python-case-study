import pytest
from gui.start_home import StartHome

def test_gui_initialization(monkeypatch):
    """Testa l'inizializzazione della GUI senza avviare la finestra grafica."""
    # Simula il comportamento del metodo run per evitare che la GUI venga eseguita
    def mock_run(self):
        pass  # Metodo simulato per evitare side effects

    # Sostituisce il metodo run della classe StartHome con il mock
    monkeypatch.setattr(StartHome, "run", mock_run)
    
    # Istanzia la classe StartHome
    app = StartHome()
    
    # Verifica che l'oggetto app sia stato creato correttamente
    assert app is not None
    
    # Esegue il metodo run (simulato) senza errori
    app.run()
