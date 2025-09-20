#!/usr/bin/env python3
"""
Tests for Prompt Chaining example.
"""

import pytest
import sys
import os
from unittest.mock import patch, MagicMock

# Add the project directory to the path
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from main import main


class TestPromptChaining:
    """Test cases for the Prompt Chaining example."""
    
    def test_main_function_exists(self):
        """Test that the main function exists and is callable."""
        assert callable(main)
    
    @patch('main.time.sleep')
    @patch('builtins.print')
    def test_main_execution(self, mock_print, mock_sleep):
        """Test that main function executes without errors."""
        # This should not raise any exceptions
        main()
        
        # Verify that print was called multiple times
        assert mock_print.call_count > 0
        
        # Verify that sleep was called (simulating processing time)
        assert mock_sleep.call_count > 0
    
    @patch('main.time.sleep')
    @patch('builtins.print')
    def test_main_output_structure(self, mock_print, mock_sleep):
        """Test that main function produces expected output structure."""
        main()
        
        # Get all print calls
        print_calls = [call[0][0] for call in mock_print.call_args_list]
        
        # Check for expected output elements
        assert any("Prompt Chaining Example" in call for call in print_calls)
        assert any("Prompt Chain Steps:" in call for call in print_calls)
        assert any("completed successfully" in call for call in print_calls)
    
    def test_main_imports(self):
        """Test that main function can be imported without errors."""
        # This test ensures the module can be imported
        import main
        assert hasattr(main, 'main')


if __name__ == "__main__":
    pytest.main([__file__])
