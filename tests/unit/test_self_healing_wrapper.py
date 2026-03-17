"""
Unit tests for self_healing_wrapper.py
"""
import pytest
import os
import sys
import tempfile
from pathlib import Path
from unittest.mock import Mock, patch, MagicMock

sys.path.insert(0, str(Path(__file__).parent.parent.parent / "SANDKASSE" / "07_Sandkasse_SelfHealing"))

try:
    from self_healing_wrapper import SelfHealingSystem, heal
except ImportError:
    pytest.skip("self_healing_wrapper module not available", allow_module_level=True)


@pytest.fixture
def temp_backup_dir():
    """Create a temporary directory for backups"""
    with tempfile.TemporaryDirectory() as tmpdir:
        yield tmpdir


@pytest.fixture
def healing_system(temp_backup_dir):
    """Create a SelfHealingSystem instance"""
    with patch('self_healing_wrapper.AIFixer') as MockAIFixer:
        mock_ai = Mock()
        mock_ai.kimi_available = False
        mock_ai.gemini_available = False
        MockAIFixer.return_value = mock_ai
        
        system = SelfHealingSystem(backup_dir=temp_backup_dir)
        yield system


class TestSelfHealingSystem:
    """Test suite for SelfHealingSystem class"""
    
    @pytest.mark.unit
    def test_initialization(self, temp_backup_dir):
        """Test system initialization"""
        with patch('self_healing_wrapper.AIFixer') as MockAIFixer:
            mock_ai = Mock()
            mock_ai.kimi_available = True
            mock_ai.gemini_available = False
            MockAIFixer.return_value = mock_ai
            
            system = SelfHealingSystem(backup_dir=temp_backup_dir)
            
            assert system.backup_dir == temp_backup_dir
            assert os.path.exists(temp_backup_dir)
            assert system.stats['total_runs'] == 0
    
    @pytest.mark.unit
    def test_successful_function_execution(self, healing_system):
        """Test that successful functions execute normally"""
        @healing_system.heal
        def success_func():
            return 42
        
        result = success_func()
        assert result == 42
        assert healing_system.stats['successful_runs'] == 1
    
    @pytest.mark.unit
    def test_healing_attempt(self, healing_system):
        """Test that healing is attempted on failure"""
        call_count = 0
        
        @healing_system.heal
        def failing_func():
            nonlocal call_count
            call_count += 1
            if call_count < 2:
                raise ValueError("Simulated error")
            return "fixed"
        
        # Mock the healing process
        with patch.object(healing_system, '_attempt_healing', return_value=True):
            result = failing_func()
            assert result == "fixed"
    
    @pytest.mark.unit
    def test_max_attempts_exceeded(self, healing_system):
        """Test that function fails after max attempts"""
        @healing_system.heal
        def always_fails():
            raise ValueError("Persistent error")
        
        with patch.object(healing_system, '_attempt_healing', return_value=False):
            with pytest.raises(ValueError, match="Persistent error"):
                always_fails()
        
        assert healing_system.stats['failed_fixes'] == 1
    
    @pytest.mark.unit
    def test_get_function_source(self, healing_system):
        """Test extracting function source code"""
        def test_function():
            """Docstring"""
            x = 1
            return x
        
        source = healing_system._get_function_source(test_function)
        assert 'def test_function()' in source
        assert 'x = 1' in source
    
    @pytest.mark.unit
    def test_create_backup(self, healing_system, temp_backup_dir):
        """Test backup creation"""
        # Create a dummy main.py
        main_py = Path("main.py")
        main_py.write_text("# test content")
        
        try:
            healing_system._create_backup("test_func")
            
            # Check backup was created
            backups = list(Path(temp_backup_dir).glob("*.bak"))
            assert len(backups) == 1
            assert "test_func" in backups[0].name
        finally:
            if main_py.exists():
                main_py.unlink()
    
    @pytest.mark.unit
    def test_get_stats(self, healing_system):
        """Test statistics retrieval"""
        # Simulate some activity
        healing_system.stats['total_runs'] = 10
        healing_system.stats['successful_runs'] = 8
        healing_system.stats['auto_fixed'] = 5
        healing_system.stats['failed_fixes'] = 2
        
        stats = healing_system.get_stats()
        
        assert stats['total_runs'] == 10
        assert stats['successful_runs'] == 8
        assert stats['auto_fixed'] == 5
        assert stats['failed_fixes'] == 2
        assert stats['healing_success_rate'] == 50.0  # 5/10 * 100
    
    @pytest.mark.unit
    def test_heal_decorator_factory(self):
        """Test the heal decorator factory"""
        # The global heal decorator should work
        @heal
        def decorated_func():
            return "success"
        
        # Should execute without error
        result = decorated_func()
        assert result == "success"


class TestHealingIntegration:
    """Integration-style tests for healing behavior"""
    
    @pytest.mark.unit
    def test_error_logging_during_heal(self, healing_system):
        """Test that errors are logged during healing attempts"""
        errors_logged = []
        
        original_handle_error = healing_system.error_handler.handle_error
        
        def mock_handle_error(error, code_context, function_name="unknown"):
            errors_logged.append({
                'type': type(error).__name__,
                'function': function_name
            })
            return original_handle_error(error, code_context, function_name)
        
        healing_system.error_handler.handle_error = mock_handle_error
        
        @healing_system.heal
        def error_func():
            raise ValueError("Test error")
        
        with pytest.raises(ValueError):
            error_func()
        
        assert len(errors_logged) > 0
        assert errors_logged[0]['type'] == 'ValueError'
