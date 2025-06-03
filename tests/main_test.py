import pytest
import streamlit as st
from unittest.mock import Mock, patch, MagicMock
import sys
import os

# Add the parent directory to the path to import the modules
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))


from util.llm_constants import OLLAMA_MODELS


class TestPromptWranglerApp:
    """Test suite for the Prompt Wrangler Streamlit application."""

    @pytest.fixture(autouse=True)
    def setup_streamlit_mock(self):
        """Set up Streamlit mocks for each test."""
        with (
            patch("streamlit.set_page_config") as mock_config,
            patch("streamlit.title") as mock_title,
            patch("streamlit.text_area") as mock_text_area,
            patch("streamlit.button") as mock_button,
            patch("streamlit.spinner") as mock_spinner,
            patch("streamlit.columns") as mock_columns,
            patch("streamlit.header") as mock_header,
            patch("streamlit.write") as mock_write,
            patch("streamlit.error") as mock_error,
        ):
            self.mock_config = mock_config
            self.mock_title = mock_title
            self.mock_text_area = mock_text_area
            self.mock_button = mock_button
            self.mock_spinner = mock_spinner
            self.mock_columns = mock_columns
            self.mock_header = mock_header
            self.mock_write = mock_write
            self.mock_error = mock_error

            # Set up column mocks
            col1_mock = Mock()
            col2_mock = Mock()
            self.mock_columns.return_value = [col1_mock, col2_mock]
            col1_mock.__enter__ = Mock(return_value=col1_mock)
            col1_mock.__exit__ = Mock(return_value=None)
            col2_mock.__enter__ = Mock(return_value=col2_mock)
            col2_mock.__exit__ = Mock(return_value=None)

            # Set up spinner mock
            spinner_mock = Mock()
            spinner_mock.__enter__ = Mock(return_value=spinner_mock)
            spinner_mock.__exit__ = Mock(return_value=None)
            self.mock_spinner.return_value = spinner_mock

            yield

    @patch("ui.user_session.create_chatModel")
    @patch("ui.user_session.init_session_state")
    @patch("ui.user_session.create_sidebar")
    @patch("ui.user_session.update_sidebar_stats")
    def test_successful_llm_call(
        self, mock_update_stats, mock_sidebar, mock_init, mock_create_model
    ):
        """Test successful LLM call and result display."""
        # Mock the provider and its response
        mock_provider = Mock()
        mock_result = "Test output"
        mock_metadata = {"tokens": 100, "time": 1.5}
        mock_provider.call_llm.return_value = (mock_result, mock_metadata)
        mock_create_model.return_value = mock_provider

        # Mock UI interactions
        self.mock_text_area.return_value = "test input"
        self.mock_button.return_value = True  # Button is clicked

        # Simulate running the app
        exec(open("main.py").read())

        # Verify LLM was called
        mock_provider.call_llm.assert_called_once_with("test input")

        # Verify results are displayed
        self.mock_write.assert_called_with(mock_result)

        # Verify stats are updated
        mock_update_stats.assert_called_once_with(mock_metadata)

    @patch("ui.user_session.create_chatModel")
    @patch("ui.user_session.init_session_state")
    @patch("ui.user_session.create_sidebar")
    @patch("ui.user_session.update_sidebar_stats")
    def test_llm_call_exception_handling(
        self, mock_update_stats, mock_sidebar, mock_init, mock_create_model
    ):
        """Test exception handling during LLM call processing."""
        # Mock the provider to raise an exception
        mock_provider = Mock()
        mock_provider.call_llm.return_value = ("result", {"tokens": 100})
        mock_create_model.return_value = mock_provider

        # Mock update_sidebar_stats to raise an exception
        mock_update_stats.side_effect = Exception("Test exception")

        # Mock UI interactions
        self.mock_text_area.return_value = "test input"
        self.mock_button.return_value = True

        # Simulate running the app
        exec(open("main.py").read())

        # Verify error is displayed
        self.mock_error.assert_called_once()
        error_call_args = self.mock_error.call_args[0][0]
        assert "An error occurred while displaying the results:" in error_call_args
        assert "Test exception" in error_call_args

    # Longer timeout for slow LLM calls
    @patch("ui.user_session.create_chatModel")
    @patch("ui.user_session.init_session_state")
    @patch("ui.user_session.create_sidebar")
    def test_slow_llm_response(self, mock_sidebar, mock_init, mock_create_model):
        """Test handling of slow LLM responses."""
        import time

        # Mock a slow provider
        mock_provider = Mock()

        def slow_call_llm(input_text):
            time.sleep(2)  # Simulate slow response
            return ("Slow response", {"tokens": 50, "time": 2.0})

        mock_provider.call_llm.side_effect = slow_call_llm
        mock_create_model.return_value = mock_provider

        # Mock UI interactions
        self.mock_text_area.return_value = "test input"
        self.mock_button.return_value = True

        start_time = time.time()

        # Simulate running the app
        exec(open("main.py").read())

        end_time = time.time()

        # Verify the call took some time but completed
        assert end_time - start_time >= 2.0

        # Verify spinner was used
        self.mock_spinner.assert_called_once_with("Processing...")

    def test_default_model_constant(self):
        """Test that the default model constant is properly set."""
        from util.llm_constants import OLLAMA_MODELS

        # Verify DEFAULT_MODEL is set correctly
        assert hasattr(OLLAMA_MODELS, "GEMMA3_12B")
        default_model = OLLAMA_MODELS.GEMMA3_12B.value
        assert default_model is not None

    @patch("ui.user_session.create_chatModel")
    @patch("ui.user_session.init_session_state")
    @patch("ui.user_session.create_sidebar")
    def test_button_not_clicked(self, mock_sidebar, mock_init, mock_create_model):
        """Test behavior when the Run button is not clicked."""
        mock_provider = Mock()
        mock_create_model.return_value = mock_provider

        # Mock UI interactions - button not clicked
        self.mock_text_area.return_value = "test input"
        self.mock_button.return_value = False

        # Simulate running the app
        exec(open("main.py").read())

        # Verify LLM was not called
        mock_provider.call_llm.assert_not_called()

        # Verify no results are displayed
        assert not any(
            "Output:" in str(call) for call in self.mock_header.call_args_list
        )

    @pytest.mark.timeout(35)
    @patch("ui.user_session.create_chatModel")
    @patch("ui.user_session.init_session_state")
    @patch("ui.user_session.create_sidebar")
    def test_empty_input_handling(self, mock_sidebar, mock_init, mock_create_model):
        """Test handling of empty input text."""
        mock_provider = Mock()
        mock_provider.call_llm.return_value = ("Empty response", {"tokens": 0})
        mock_create_model.return_value = mock_provider

        # Mock UI interactions with empty input
        self.mock_text_area.return_value = ""
        self.mock_button.return_value = True

        # Simulate running the app
        exec(open("main.py").read())

        # Verify LLM was called with empty string
        mock_provider.call_llm.assert_called_once_with("")

