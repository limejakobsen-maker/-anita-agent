"""
Tester for ai_fixer.py
"""
import pytest
import sys
from pathlib import Path
from unittest.mock import Mock, patch, MagicMock

sys.path.insert(0, str(Path(__file__).parent.parent.parent / "SANDKASSE" / "07_Sandkasse_SelfHealing"))

try:
    from ai_fixer import AIFixer
except ImportError:
    pytest.skip("ai_fixer modul ikke tilgjengelig", allow_module_level=True)


class TestAIFixer:
    """Test suite for AIFixer"""
    
    @pytest.mark.unit
    def test_initialization_without_ai(self):
        """Test at AIFixer kan initialiseres uten eksterne AI-tjenester"""
        with patch('ai_fixer.AIAgent') as MockAgent:
            # Simuler at AI ikke er tilgjengelig
            mock_instance = Mock()
            mock_instance.kimi.er_tilgjengelig.return_value = False
            mock_instance.gemini.er_tilgjengelig.return_value = False
            MockAgent.return_value = mock_instance
            
            fixer = AIFixer()
            assert fixer.kimi_available == False
            assert fixer.gemini_available == False
    
    @pytest.mark.unit
    def test_standard_fix_indexerror(self):
        """Test standard fiks for IndexError"""
        fixer = AIFixer()
        
        error_info = {
            'type': 'IndexError',
            'message': 'list index out of range',
            'function': 'test_func'
        }
        code = "data[0]"
        
        fix = fixer._get_standard_fix(error_info['type'], error_info['message'], code)
        
        assert fix is not None
        assert 'data[0]' in fix
        assert 'len(data)' in fix or 'if' in fix
    
    @pytest.mark.unit
    def test_standard_fix_keyerror(self):
        """Test standard fiks for KeyError"""
        fixer = AIFixer()
        
        error_info = {
            'type': 'KeyError',
            'message': "'missing_key'",
            'function': 'test_func'
        }
        code = "config['missing_key']"
        
        fix = fixer._get_standard_fix(error_info['type'], error_info['message'], code)
        
        assert fix is not None
        assert '.get(' in fix
    
    @pytest.mark.unit
    def test_standard_fix_zero_division(self):
        """Test standard fiks for ZeroDivisionError"""
        fixer = AIFixer()
        
        error_info = {
            'type': 'ZeroDivisionError',
            'message': 'division by zero',
            'function': 'test_func'
        }
        code = "result = a / b"
        
        fix = fixer._get_standard_fix(error_info['type'], error_info['message'], code)
        
        assert fix is not None
        assert 'if' in fix or 'try' in fix
    
    @pytest.mark.unit
    def test_generate_fix_with_standard(self):
        """Test generate_fix med standard fiks"""
        fixer = AIFixer()
        
        error_info = {
            'type': 'IndexError',
            'message': 'list index out of range',
            'function': 'test_func',
            'frequency': 1
        }
        code = "data[0]"
        
        fix = fixer.generate_fix(error_info, code)
        
        assert fix is not None
        assert isinstance(fix, str)
    
    @pytest.mark.unit
    def test_validate_syntax_valid(self):
        """Test validering av gyldig Python-kode"""
        fixer = AIFixer()
        
        valid_code = "def test():\n    return 42"
        assert fixer.validate_syntax(valid_code) == True
    
    @pytest.mark.unit
    def test_validate_syntax_invalid(self):
        """Test validering av ugyldig Python-kode"""
        fixer = AIFixer()
        
        invalid_code = "def test(:\n    return 42"
        assert fixer.validate_syntax(invalid_code) == False
    
    @pytest.mark.unit
    def test_clean_code_markdown(self):
        """Test fjerning av markdown fra kode"""
        fixer = AIFixer()
        
        code_with_markdown = "```python\ndef test():\n    pass\n```"
        cleaned = fixer._clean_code(code_with_markdown)
        
        assert "```" not in cleaned
        assert "python" not in cleaned
        assert "def test():" in cleaned
