import os
import sys
import pytest
from fastapi.testclient import TestClient
from unittest.mock import patch, Mock, AsyncMock
import tempfile
from fastapi import FastAPI
import pytest_asyncio
from anthropic import APIError, APIConnectionError, APITimeoutError

# Add the services directory to Python path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

# Import after path setup
from main import app

# Create test client
client = TestClient(app=app)

# Mock environment variables
os.environ["ANTHROPIC_API_KEY"] = "test_key"

# Mock Anthropic API errors
class MockAPIError(Exception):
    def __init__(self, message):
        self.message = message
        super().__init__(message)

class MockAPIConnectionError(Exception):
    def __init__(self, message):
        self.message = message
        super().__init__(message)

class MockAPITimeoutError(Exception):
    def __init__(self, message):
        self.message = message
        super().__init__(message)

def test_root():
    response = client.get("/")
    assert response.status_code == 200
    assert response.json() == {"message": "Stock Recommendation System API"}

def test_health_check():
    response = client.get("/health")
    assert response.status_code == 200
    assert response.json() == {"status": "healthy"}

@pytest.mark.asyncio
async def test_chat_endpoint():
    # Mock the Anthropic response
    mock_content = [Mock()]
    mock_content[0].text = "Test response"
    mock_message = AsyncMock()
    mock_message.content = mock_content
    mock_create = AsyncMock(return_value=mock_message)
    
    with patch('main.anthropic.messages.create', mock_create):
        response = client.post(
            "/chat",
            json={"message": "Test message"}
        )
        assert response.status_code == 200
        data = response.json()
        assert data["response"] == "Test response"
        assert data["status"] == "success"
        mock_create.assert_awaited_once()

@pytest.mark.asyncio
async def test_chat_endpoint_api_error():
    # Mock an API error response
    mock_create = AsyncMock(side_effect=MockAPIError("API Error"))
    
    with patch('main.anthropic.messages.create', mock_create), \
         patch('main.APIError', MockAPIError):
        response = client.post(
            "/chat",
            json={"message": "Test message"}
        )
        assert response.status_code == 500
        data = response.json()
        assert data["detail"]["detail"] == "AI service error: API Error"
        assert data["detail"]["error_type"] == "api_error"
        assert data["detail"]["status"] == "error"
        mock_create.assert_awaited_once()

@pytest.mark.asyncio
async def test_chat_endpoint_connection_error():
    # Mock a connection error
    mock_create = AsyncMock(side_effect=MockAPIConnectionError("Connection Error"))
    
    with patch('main.anthropic.messages.create', mock_create), \
         patch('main.APIConnectionError', MockAPIConnectionError):
        response = client.post(
            "/chat",
            json={"message": "Test message"}
        )
        assert response.status_code == 503
        data = response.json()
        assert data["detail"]["detail"] == "Unable to connect to AI service. Please try again later."
        assert data["detail"]["error_type"] == "connection_error"
        assert data["detail"]["status"] == "error"
        mock_create.assert_awaited_once()

@pytest.mark.asyncio
async def test_chat_endpoint_timeout_error():
    # Mock a timeout error
    mock_create = AsyncMock(side_effect=MockAPITimeoutError("Timeout Error"))
    
    with patch('main.anthropic.messages.create', mock_create), \
         patch('main.APITimeoutError', MockAPITimeoutError):
        response = client.post(
            "/chat",
            json={"message": "Test message"}
        )
        assert response.status_code == 504
        data = response.json()
        assert data["detail"]["detail"] == "Request timed out. Please try again."
        assert data["detail"]["error_type"] == "timeout_error"
        assert data["detail"]["status"] == "error"
        mock_create.assert_awaited_once()

def test_chat_endpoint_invalid_request():
    # Test with empty message
    response = client.post(
        "/chat",
        json={"message": ""}
    )
    assert response.status_code == 422
    assert "message cannot be empty" in str(response.json()["detail"])

    # Test with missing message field
    response = client.post(
        "/chat",
        json={}
    )
    assert response.status_code == 422

if __name__ == "__main__":
    pytest.main([__file__, "-v"])
