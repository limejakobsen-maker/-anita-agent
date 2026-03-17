"""
Unit tests for error_handler.py
"""
import pytest
import json
import os
import tempfile
from datetime import datetime
from pathlib import Path

# Import the module under test
import sys
sys.path.insert(0, str(Path(__file__).parent.parent.parent / "SANDKASSE" / "07_Sandkasse_SelfHealing"))

try:
    from error_handler import ErrorHandler
except ImportError:
    pytest.skip("error_handler module not available", allow_module_level=True)


@pytest.fixture
def temp_log_dir():
    """Create a temporary directory for test logs"""
    with tempfile.TemporaryDirectory() as tmpdir:
        yield tmpdir


@pytest.fixture
def error_handler(temp_log_dir):
    """Create an ErrorHandler instance with temp directory"""
    return ErrorHandler(log_dir=temp_log_dir)


class TestErrorHandler:
    """Test suite for ErrorHandler class"""
    
    @pytest.mark.unit
    def test_initialization(self, temp_log_dir):
        """Test that ErrorHandler initializes correctly"""
        handler = ErrorHandler(log_dir=temp_log_dir)
        assert handler.log_dir == temp_log_dir
        assert os.path.exists(temp_log_dir)
        assert handler.error_patterns == {}
    
    @pytest.mark.unit
    def test_hash_error(self, error_handler):
        """Test error hashing functionality"""
        error = ValueError("test error")
        hash1 = error_handler._hash_error(error, "test_function")
        hash2 = error_handler._hash_error(error, "test_function")
        
        # Same error should produce same hash
        assert hash1 == hash2
        assert len(hash1) == 12  # MD5 truncated to 12 chars
    
    @pytest.mark.unit
    def test_handle_error_new(self, error_handler):
        """Test handling a new error"""
        try:
            raise ValueError("test error message")
        except Exception as e:
            error_info = error_handler.handle_error(e, "test_code", "test_function")
        
        assert error_info['type'] == 'ValueError'
        assert error_info['message'] == 'test error message'
        assert error_info['function'] == 'test_function'
        assert error_info['frequency'] == 1
        assert error_info['previously_seen'] == False
        assert 'error_hash' in error_info
    
    @pytest.mark.unit
    def test_handle_error_recurring(self, error_handler):
        """Test handling a recurring error increases frequency"""
        try:
            raise ValueError("recurring error")
        except Exception as e:
            error_handler.handle_error(e, "code1", "func1")
        
        # Same error again
        try:
            raise ValueError("recurring error")
        except Exception as e:
            error_info = error_handler.handle_error(e, "code1", "func1")
        
        assert error_info['frequency'] == 2
        assert error_info['previously_seen'] == True
    
    @pytest.mark.unit
    def test_get_common_errors(self, error_handler):
        """Test retrieving common errors"""
        # Create multiple errors with different frequencies
        for i in range(5):
            try:
                raise ValueError(f"error {i}")
            except Exception as e:
                for _ in range(i + 1):  # Error i occurs i+1 times
                    error_handler.handle_error(e, f"code{i}", f"func{i}")
        
        common = error_handler.get_common_errors(n=3)
        assert len(common) <= 3
        # Most frequent should be first
        if len(common) >= 2:
            assert common[0]['frequency'] >= common[1]['frequency']
    
    @pytest.mark.unit
    def test_learn_from_fix(self, error_handler):
        """Test learning from a fix"""
        # First create an error
        try:
            raise ValueError("fixable error")
        except Exception as e:
            error_info = error_handler.handle_error(e, "code", "func")
        
        # Learn from fix
        error_handler.learn_from_fix(
            error_info['error_hash'],
            "Added null check",
            success=True,
            new_code="if x is not None:"
        )
        
        # Verify fix was recorded
        history = error_handler.get_error_history(error_info['error_hash'])
        assert len(history) == 1
        assert history[0]['description'] == "Added null check"
        assert history[0]['success'] == True
    
    @pytest.mark.unit
    def test_analyze_error_trends(self, error_handler):
        """Test error trend analysis"""
        # Create some errors
        for _ in range(3):
            try:
                raise ValueError("error")
            except Exception as e:
                error_handler.handle_error(e, "code", "func")
        
        # Mark one as fixed
        try:
            raise ValueError("fixed error")
        except Exception as e:
            info = error_handler.handle_error(e, "code2", "func2")
            error_handler.learn_from_fix(info['error_hash'], "Fixed", success=True)
        
        trends = error_handler.analyze_error_trends()
        assert trends['total_unique_errors'] == 2
        assert trends['fixed_errors'] == 1
    
    @pytest.mark.unit
    def test_save_and_load_patterns(self, error_handler, temp_log_dir):
        """Test persisting error patterns"""
        # Create an error
        try:
            raise ValueError("persistent error")
        except Exception as e:
            error_handler.handle_error(e, "code", "func")
        
        # Create new handler (should load patterns)
        new_handler = ErrorHandler(log_dir=temp_log_dir)
        
        assert len(new_handler.error_patterns) == 1
    
    @pytest.mark.unit
    def test_log_file_creation(self, error_handler, temp_log_dir):
        """Test that log files are created"""
        try:
            raise ValueError("logged error")
        except Exception as e:
            error_handler.handle_error(e, "code", "func")
        
        error_log = Path(temp_log_dir) / "errors.log"
        assert error_log.exists()
        
        # Verify JSON content
        with open(error_log) as f:
            log_entry = json.loads(f.readline())
            assert log_entry['type'] == 'ValueError'
