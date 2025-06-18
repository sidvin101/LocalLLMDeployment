import pytest
from unittest.mock import patch, MagicMock
from LocalLLMDeployment.api_wrapper import APIWrapper
from app import app as flask_app
import json
import hashlib

# Set the flask application to testing mode
@pytest.fixture
def client():
    flask_app.config["TESTING"] = True
    with flask_app.test_client() as client:
        yield client

"""
Unit Test: _cache_key()
"""
def test_cache_key_consistency():
    api = APIWrapper()
    messages = [{"role": "user", "content": "Hello"}]
    key1 = api._cache_key(messages, 64, 0.7)
    key2 = api._cache_key(messages, 64, 0.7)
    assert key1 == key2
    assert isinstance(key1, str)
    assert len(key1) == 64  # SHA-256 hash length

"""
Unit Test: generate_chat() - success with mock
"""
@patch("LocalLLMDeployment.api_wrapper.requests.post")
def test_generate_chat_success(mock_post):
    mock_response = MagicMock()
    expected_result = {
        "choices": [
            {"message": {"content": "Mocked response"}}
        ]
    }
    mock_response.json.return_value = expected_result
    mock_response.raise_for_status.return_value = None
    mock_post.return_value = mock_response

    api = APIWrapper()
    messages = [{"role": "user", "content": "Test"}]
    result = api.generate_chat(messages)

    assert result == expected_result
    assert "Mocked response" in result["choices"][0]["message"]["content"]

"""
Unit Test: generate_chat() - simulate timeout
"""
@patch("LocalLLMDeployment.api_wrapper.requests.post", side_effect=Exception("Timeout"))
def test_generate_chat_timeout(mock_post):
    api = APIWrapper()
    result = api.generate_chat([{"role": "user", "content": "Slow?"}])
    assert result is None

"""
Integration Test: Flask POST route
"""
@patch("LocalLLMDeployment.api_wrapper.APIWrapper.generate_chat")
def test_flask_post(client, mock_generate_chat):
    mock_generate_chat.return_value = {
        "choices": [{"message": {"content": "Flask test passed"}}]
    }
    response = client.post("/", data={"user_input": "Hello"}, follow_redirects=True)
    assert response.status_code == 200
    assert b"Flask test passed" in response.data
