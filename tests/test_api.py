import pytest
from unittest.mock import Mock, patch
from api import (
    perform_openai_request,
)

@patch("api.openai.ChatCompletion.create")
def test_perform_openai_request(mock_openai_create):
    # Create a mock response from OpenAI
    mock_openai_response = Mock()

    # Create a mock choice and message content
    mock_choice = Mock()
    mock_message_content = Mock()

    # Configure the mock_message_content.content to return a string
    mock_message_content.content = "OpenAI Response"

    # Configure the mock_choice to return the mock_message_content
    mock_choice.message = mock_message_content

    # Configure the mock_openai_response to return the mock_choice
    mock_openai_response.choices = [mock_choice]

    # Configure the mock_openai_create to return the mock_openai_response
    mock_openai_create.return_value = mock_openai_response

    # Call the function under test
    result = perform_openai_request("test_prompt", "test_knowledge")

    # Check if the function returned the expected result
    assert isinstance(result, str)
    assert result == "OpenAI Response"
