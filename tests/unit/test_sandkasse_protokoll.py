"""
Tester for sandkasse_protokoll.py
"""
import pytest
import sys
import tempfile
import json
from pathlib import Path
from unittest.mock import Mock, patch, MagicMock

sys.path.insert(0, str(Path(__file__).parent.parent.parent))

try:
    from sandkasse_protokoll import SandkasseProtokoll, Prosjekt, LocalOllamaClient
except ImportError:
    pytest.skip("sandkasse_protokoll modul ikke tilgjengelig", allow_module_level=True)


class TestLocalOllamaClient:
    """Test suite for LocalOllamaClient"""
    
    @pytest.mark.unit
    def test_initialization(self):
        """Test initialisering av klient"""
        client = LocalOllamaClient()
        assert client.base_url == "http://localhost:11434"
        assert client.timeout == 120
    
    @pytest.mark.unit
    def test_initialization_custom_url(self):
        """Test initialisering med custom URL"""
        client = LocalOllamaClient("http://custom:11434")
        assert client.base_url == "http://custom:11434"


class TestProsjekt:
    """Test suite for Prosjekt dataclass"""
    
    @pytest.mark.unit
    def test_prosjekt_creation(self):
        """Test opprettelse av Prosjekt"""
        prosjekt = Prosjekt(
            navn="TestProsjekt",
            beskrivelse="Test beskrivelse"
        )
        
        assert prosjekt.navn == "TestProsjekt"
        assert prosjekt.beskrivelse == "Test beskrivelse"
        assert prosjekt.sprak == "python"
        assert prosjekt.status == "initiert"
        assert prosjekt.fase == 0
    
    @pytest.mark.unit
    def test_to_dict(self):
        """Test konvertering til dictionary"""
        prosjekt = Prosjekt(
            navn="TestProsjekt",
            beskrivelse="Test beskrivelse",
            fase=3,
            test_dekning=85.5
        )
        
        data = prosjekt.to_dict()
        
        assert isinstance(data, dict)
        assert data["navn"] == "TestProsjekt"
        assert data["fase"] == 3
        assert data["test_dekning"] == 85.5


class TestSandkasseProtokoll:
    """Test suite for SandkasseProtokoll"""
    
    @pytest.fixture
    def temp_base_path(self, tmp_path):
        """Temporær base path"""
        return tmp_path
    
    @pytest.mark.unit
    def test_initialization(self, temp_base_path, monkeypatch):
        """Test initialisering av protokoll"""
        monkeypatch.setattr(
            'sandkasse_protokoll.CONFIG',
            {
                "base_path": temp_base_path / "produksjon",
                "archive_path": temp_base_path / "arkiv",
                "log_path": temp_base_path / "logs",
                "local_ollama_url": "http://localhost:11434",
                "local_models": {"coder": "test"},
                "max_iterations": 10,
                "safety_checks": True,
                "required_tests_pass": 90,
            }
        )
        
        import queue
        event_queue = queue.Queue()
        
        protocol = SandkasseProtokoll(event_queue=event_queue)
        
        assert protocol.config["base_path"] == temp_base_path / "produksjon"
        assert protocol.is_running == False
    
    @pytest.mark.unit  
    def test_get_status_empty(self):
        """Test get_status uten aktivt prosjekt"""
        import queue
        protocol = SandkasseProtokoll(event_queue=queue.Queue())
        
        status = protocol.get_status()
        
        assert status["siste_prosjekt"] is None
        assert status["fase"] == 0
        assert status["status"] == "idle"
